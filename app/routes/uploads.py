import secrets
from pathlib import Path
from flask import Blueprint, current_app, render_template, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.forms.upload_forms import UploadVideoForm

bp = Blueprint("uploads", __name__)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadVideoForm()

    if form.validate_on_submit():
        file = form.video.data

        original = secure_filename(file.filename or "video.mp4")
        if not original.lower().endswith(".mp4"):
            flash("Только .mp4", "error")
            return render_template("upload.html", form=form)

        uniq = secrets.token_hex(6)
        filename = f"{uniq}_{original}"

        upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
        if not upload_dir.exists():
            upload_dir.mkdir(parents=True)

        save_path = upload_dir / filename
        file.save(save_path)

        video_url = url_for("static", filename=f"uploads/{filename}")
        flash("Видео загружено! Скопируй ссылку и вставь в комнату.", "ok")
        return render_template("upload_done.html", video_url=video_url)

    return render_template("upload.html", form=form)
