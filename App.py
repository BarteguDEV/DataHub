"""Prosta aplikacja Flask z logowaniem - gotowa do deployu na Azure App Service."""

import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

# ---------------------------------------------------------------------------
# App & DB
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())

# SQLite lokalnie; na Azure można podmienić przez zmienną środowiskową
DB_URL = os.getenv("DATABASE_URL") or "sqlite:///users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def login_required(f):
    """Decorator – wymaga zalogowania."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Musisz się zalogować, aby uzyskać dostęp.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
@login_required
def index():
    return render_template("index.html", username=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session.permanent = True
            flash(f"Witaj, {user.username}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Niepoprawna nazwa użytkownika lub hasło.", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not username or not password:
            flash("Uzupełnij wszystkie pola.", "danger")
            return render_template("register.html")

        if password != confirm:
            flash("Hasła nie są zgodne.", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Użytkownik o takiej nazwie już istnieje.", "danger")
            return render_template("register.html")

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Konto utworzone! Możesz się zalogować.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Zostałeś wylogowany.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# API — Vue.js frontend
# ---------------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Niepoprawna nazwa użytkownika lub hasło"}), 401

    session["user_id"] = user.id
    session["username"] = user.username
    session.permanent = True
    return jsonify({"ok": True, "user": {"id": user.id, "username": user.username}})


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Uzupełnij wszystkie pola"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Użytkownik już istnieje"}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"ok": True}), 201


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me")
def api_me():
    if "user_id" not in session:
        return jsonify({"error": "Nie zalogowany"}), 401
    return jsonify({"id": session["user_id"], "username": session["username"]})


# Obsługa Vue SPA — wszystkie ścieżki /vue/... serwują index.html
@app.route("/vue/")
@app.route("/vue/<path:path>")
def vue_app(path=""):
    vue_dir = os.path.join(app.root_path, "static", "vue")
    if path and os.path.exists(os.path.join(vue_dir, path)):
        return send_from_directory(vue_dir, path)
    index_path = os.path.join(vue_dir, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(vue_dir, "index.html")
    return "Vue app not built. Run: cd vue-app && npm run build", 404


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("login.html", error="Strona nie została znaleziona."), 404


# ---------------------------------------------------------------------------
# Inicjalizacja bazy — uruchamia się przy starcie (lokalnie i na Azure)
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()

    # Stwórz domyślnego admina — bezpieczne dla wielu workerów gunicorna
    try:
        admin = User(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Utworzono domyślnego użytkownika: admin / admin123")
    except IntegrityError:
        db.session.rollback()
        # Admin już istnieje (inny worker go wstawił) — to nie błąd


# ---------------------------------------------------------------------------
# Start (lokalny)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
