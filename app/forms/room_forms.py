from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import BooleanField

class RoomCreateForm(FlaskForm):
    title = StringField("Название комнаты", validators=[DataRequired(), Length(min=2, max=120)])
    video_url = StringField("Ссылка на видео (mp4)", validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField("Создать")
    is_private = BooleanField("Приватная комната", default=True)

class RoomJoinForm(FlaskForm):
    code = StringField("Код комнаты", validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField("Войти")