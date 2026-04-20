from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    user_name = StringField("Логин", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Повтор пароля", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
    user_name = StringField("Логин", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")