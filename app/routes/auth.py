from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.extensions import db
from app.models.user import User
from app.forms.auth_forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        exists = User.query.filter_by(user_name=form.user_name.data).first()
        if exists:
            flash("Такой логин уже занят", "error")
            return render_template("auth/register.html", form=form)

        user = User(user_name=form.user_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Регистрация успешна. Теперь войдите.", "ok")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Неверный логин или пароль", "error")
            return render_template("auth/login.html", form=form)

        login_user(user)
        return redirect(url_for("pages.index"))

    return render_template("auth/login.html", form=form)

@bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "ok")
    return redirect(url_for("pages.index"))