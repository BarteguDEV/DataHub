"""Prosta aplikacja Flask z logowaniem - gotowa do deployu na Azure App Service."""

import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
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

    # Stwórz domyślnego admina, jeśli nie istnieje
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Utworzono domyślnego użytkownika: admin / admin123")


# ---------------------------------------------------------------------------
# Start (lokalny)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
