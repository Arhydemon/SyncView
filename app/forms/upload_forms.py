from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadVideoForm(FlaskForm):
    video = FileField("MP4 файл", validators=[
        FileRequired(),
        FileAllowed(["mp4"], "Только .mp4")
    ])
    submit = SubmitField("Загрузить")