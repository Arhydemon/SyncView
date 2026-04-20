import secrets
from datetime import datetime
from app.extensions import db

def generate_room_code(length: int = 6) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))

class Room(db.Model):
    is_private = db.Column(db.Boolean, default=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), unique=True, nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @staticmethod
    def new_code() -> str:
        # гарантия уникальности кода
        while True:
            code = generate_room_code()
            if not Room.query.filter_by(code=code).first():
                return code