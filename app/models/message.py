from datetime import datetime
from app.extensions import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)

    user_name = db.Column(db.String(64), nullable=False) # для удобства, без join
    text = db.Column(db.String(2000), nullable=False)

    is_system = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
