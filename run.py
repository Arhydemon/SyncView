import os

from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "1").strip().lower() not in {"0", "false", "no", "off"}

    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
