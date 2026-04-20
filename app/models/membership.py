from datetime import datetime
from app.extensions import db

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False, index=True)

    role = db.Column(db.String(16), default="member", nullable=False)  # host/member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "room_id", name="uq_user_room"),
    )