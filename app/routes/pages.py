import json
from pathlib import Path
from flask import Blueprint, current_app, render_template

bp = Blueprint("pages", __name__)

@bp.get("/")
def index():
    return render_template("index.html")

@bp.get("/about")
def about():
    about_path = Path(current_app.root_path).parent / "data" / "about.json"
    data = {}
    if about_path.exists():
        data = json.loads(about_path.read_text(encoding="utf-8"))
    return render_template("about.html", about=data)