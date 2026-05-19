from flask import request
from flask_login import current_user
from flask_socketio import join_room, leave_room, emit
from app.extensions import socketio, db
from app.models import Room, Membership, Message

presence = {}

def _room_access_check(code: str):
    code = (code or "").strip().upper()
    if not code:
        return None, None

    room = Room.query.filter_by(code=code).first()
    if not room:
        return None, None

    membership = Membership.query.filter_by(user_id=current_user.id, room_id=room.id).first()
    if not membership:
        return None, None

    return room, membership

def _emit_online(code: str):
    users = list(presence.get(code, {}).values())
    emit("online_update", {"count": len(users), "users": users}, room=code)

def _save_system(room_id: int, user_id: int | None, user_name: str, text: str):
    m = Message(
        room_id=room_id,
        user_id=user_id,
        user_name=user_name,
        text=text,
        is_system=True,
    )
    db.session.add(m)
    db.session.commit()
    return m

def register_socket_handlers():
    @socketio.on("join_room")
    def on_join_room(data):
        if not current_user.is_authenticated:
            emit("error_msg", {"message": "not authenticated"})
            return

        code = (data or {}).get("room_code", "")
        room, membership = _room_access_check(code)
        if not room:
            emit("error_msg", {"message": "room not found / no access"})
            return

        code = room.code

        join_room(code)

        presence.setdefault(code, {})
        presence[code][request.sid] = current_user.user_name

        sys_text = f"{current_user.user_name} вошёл(ла) в комнату"
        _save_system(room.id, current_user.id, current_user.user_name, sys_text)

        history = (
            Message.query.filter_by(room_id=room.id)
            .order_by(Message.created_at.desc())
            .limit(50)
            .all()
        )[::-1]

        emit(
            "chat_history",
            {
                "items": [
                    {
                        "user": m.user_name,
                        "text": m.text,
                        "is_system": bool(m.is_system),
                        "ts": m.created_at.isoformat(timespec="seconds"),
                    }
                    for m in history
                ]
            },
        )

        emit(
            "chat_new",
            {"user": current_user.user_name, "text": sys_text, "is_system": True},
            room=code,
            include_self=False,
        )

        _emit_online(code)

    @socketio.on("leave_room")
    def on_leave_room(data):
        code = (data or {}).get("room_code", "").strip().upper()
        if not code:
            return
        leave_room(code)

        if code in presence and request.sid in presence[code]:
            presence[code].pop(request.sid, None)
            if not presence[code]:
                presence.pop(code, None)
            else:
                _emit_online(code)

    @socketio.on("disconnect")
    def on_disconnect():
        if not current_user.is_authenticated:
            return

        for code, users in list(presence.items()):
            if request.sid in users:
                user_name = users.pop(request.sid, None)

                room = Room.query.filter_by(code=code).first()
                if room and user_name:
                    sys_text = f"{user_name} вышел(ла) из комнаты"
                    _save_system(room.id, current_user.id, user_name, sys_text)
                    emit(
                        "chat_new",
                        {"user": user_name, "text": sys_text, "is_system": True},
                        room=code,
                    )

                if not users:
                    presence.pop(code, None)
                else:
                    _emit_online(code)
                break

    @socketio.on("chat_send")
    def on_chat_send(data):
        if not current_user.is_authenticated:
            return

        code = (data or {}).get("room_code", "")
        text = (data or {}).get("text", "").strip()
        if not text:
            return

        room, membership = _room_access_check(code)
        if not room:
            return

        m = Message(
            room_id=room.id,
            user_id=current_user.id,
            user_name=current_user.user_name,
            text=text,
            is_system=False,
        )
        db.session.add(m)
        db.session.commit()

        emit(
            "chat_new",
            {"user": m.user_name, "text": m.text, "is_system": False},
            room=room.code,
        )

    @socketio.on("video_event")
    def on_video_event(data):
        if not current_user.is_authenticated:
            return

        payload = data or {}
        code = (payload.get("room_code", "")).strip().upper()
        etype = payload.get("type", "")
        t = payload.get("t", None)
        paused = payload.get("paused", None)

        if not code or etype not in {"play", "pause", "seek", "sync"}:
            return

        room, membership = _room_access_check(code)
        if not room:
            return

        # правило в публичной комнате управляет только host
        if (room.is_private is False) and (membership.role != "host"):
            emit("error_msg", {"message": "Только создатель может управлять видео в публичной комнате"})
            return
        
        emit(
            "video_update",
            {
                "type": etype,
                "t": t,
                "paused": paused,
                "sender": current_user.user_name,
            },
            room=room.code,
            include_self=False,
        )
