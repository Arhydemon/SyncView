from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.forms.room_forms import RoomCreateForm, RoomJoinForm
from app.models import Room, Membership, Message

bp = Blueprint("rooms", __name__)


@bp.get("/rooms")
@login_required
def list_rooms():
    memberships = Membership.query.filter_by(user_id=current_user.id).all()
    room_ids = [m.room_id for m in memberships]

    rooms = (
        Room.query.filter(Room.id.in_(room_ids))
        .order_by(Room.created_at.desc())
        .all()
        if room_ids else []
    )

    return render_template("rooms/list.html", rooms=rooms)


@bp.get("/rooms/public")
@login_required
def public_rooms():
    rooms = (
        Room.query.filter_by(is_private=False)
        .order_by(Room.created_at.desc())
        .all()
    )
    return render_template("rooms/public.html", rooms=rooms)


@bp.route("/rooms/create", methods=["GET", "POST"])
@login_required
def create_room():
    form = RoomCreateForm()

    if form.validate_on_submit():
        room = Room(
            code=Room.new_code(),
            title=form.title.data,
            video_url=form.video_url.data,
            owner_id=current_user.id,
            is_private=form.is_private.data,
        )
        db.session.add(room)
        db.session.flush()

        membership = Membership(
            user_id=current_user.id,
            room_id=room.id,
            role="host",
        )
        db.session.add(membership)

        db.session.commit()
        flash(f"Комната создана. Код: {room.code}", "ok")
        return redirect(url_for("rooms.watch_room", code=room.code))

    return render_template("rooms/create.html", form=form)


@bp.route("/rooms/join", methods=["GET", "POST"])
@login_required
def join_room():
    form = RoomJoinForm()

    if form.validate_on_submit():
        code = form.code.data.strip().upper()
        room = Room.query.filter_by(code=code).first()

        if not room:
            flash("Комната не найдена (проверь код)", "error")
            return render_template("rooms/join.html", form=form)

        membership = Membership.query.filter_by(
            user_id=current_user.id,
            room_id=room.id,
        ).first()

        if not membership:
            db.session.add(
                Membership(
                    user_id=current_user.id,
                    room_id=room.id,
                    role="member",
                )
            )
            db.session.commit()

        return redirect(url_for("rooms.watch_room", code=room.code))

    return render_template("rooms/join.html", form=form)


@bp.get("/room/<code>")
@login_required
def watch_room(code: str):
    code = code.strip().upper()
    room = Room.query.filter_by(code=code).first_or_404()

    membership = Membership.query.filter_by(
        user_id=current_user.id,
        room_id=room.id,
    ).first()

    if not membership:
        if room.is_private:
            flash("У вас нет доступа к этой комнате. Войдите по коду.", "error")
            return redirect(url_for("rooms.join_room"))

        db.session.add(
            Membership(
                user_id=current_user.id,
                room_id=room.id,
                role="member",
            )
        )
        db.session.commit()

        membership = Membership.query.filter_by(
            user_id=current_user.id,
            room_id=room.id,
        ).first()

    return render_template(
        "rooms/watch.html",
        room=room,
        role=membership.role,
    )


@bp.post("/room/<code>/delete")
@login_required
def delete_room(code: str):
    code = code.strip().upper()
    room = Room.query.filter_by(code=code).first_or_404()

    if room.owner_id != current_user.id:
        flash("Только создатель может удалить комнату.", "error")
        return redirect(url_for("rooms.watch_room", code=room.code))

    Message.query.filter_by(room_id=room.id).delete()
    Membership.query.filter_by(room_id=room.id).delete()
    db.session.commit()

    db.session.delete(room)
    db.session.commit()

    flash("Комната удалена.", "ok")
    return redirect(url_for("rooms.list_rooms"))