"""Flask application for PhishGuard.AI.

The URL analyzer below is a transparent heuristic demo, not a trained AI model.
For production, replace analyze_url() with a validated model/reputation service.
"""
import os
import re
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from config import get_db_connection

BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-only-change-this-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to view scan results or save a scan.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def analyze_url(value):
    """Return a cautious rule-based URL assessment, not an AI prediction."""
    raw = (value or "").strip()
    if not raw:
        raise ValueError("Please enter a URL.")
    if len(raw) > 500:
        raise ValueError("The URL must be 500 characters or fewer.")
    candidate = raw if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw) else "https://" + raw
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a valid web address, such as https://example.com.")
    host = parsed.hostname.lower().rstrip(".")
    flags = []
    if parsed.scheme != "https":
        flags.append("The URL does not use HTTPS.")
    if "@" in parsed.netloc:
        flags.append("The URL contains an @ sign in its authority section.")
    if host.startswith("xn--") or ".xn--" in host:
        flags.append("The hostname contains an internationalized/punycode label.")
    if len(host.split(".")) >= 5:
        flags.append("The hostname has many subdomains.")
    if len(host) > 45:
        flags.append("The hostname is unusually long.")
    if re.search(r"\d{5,}", host):
        flags.append("The hostname contains a long sequence of digits.")
    suspicious_words = ("login", "verify", "secure", "account", "update", "wallet", "password", "confirm")
    if any(word in (host + parsed.path).lower() for word in suspicious_words):
        flags.append("The URL contains a word often used in credential-lure links.")
    if len(parsed.path) > 90:
        flags.append("The URL path is unusually long.")

    score = min(95, len(flags) * 18)
    if score >= 54:
        label = "Phishing risk indicators detected"
    elif score >= 18:
        label = "Suspicious — use caution"
    else:
        label = "No obvious indicators found"
    return {"url": candidate, "label": label, "score": score, "flags": flags}


@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("history.html")


@app.route("/history")
@login_required
def history():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT id, url, is_phishing, confidence_score, created_at
                   FROM scan_results WHERE user_id = %s
                   ORDER BY created_at DESC LIMIT 200""",
                (session["user_id"],),
            )
            rows = cursor.fetchall()
    finally:
        conn.close()
    return render_template("scan_history.html", results=rows)


@app.route("/results", methods=["GET", "POST"])
@app.route("/result", methods=["GET", "POST"])
@login_required
def results():
    scan = None
    if request.method == "POST":
        try:
            scan = analyze_url(request.form.get("url", ""))
        except ValueError as exc:
            flash(str(exc), "danger")
            return render_template("result.html", scan=None, results=[])

        # Save scan to the signed-in user's history.
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO scan_results
                       (user_id, url, is_phishing, confidence_score)
                       VALUES (%s, %s, %s, %s)""",
                    (session["user_id"], scan["url"], scan["score"] >= 54, scan["score"]),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            app.logger.exception("Could not save scan result")
            flash("The URL was analyzed, but the result could not be saved. Check your database schema and connection.", "warning")
        finally:
            conn.close()

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT id, url, is_phishing, confidence_score, created_at
                   FROM scan_results WHERE user_id = %s
                   ORDER BY created_at DESC LIMIT 20""",
                (session["user_id"],),
            )
            rows = cursor.fetchall()
    finally:
        conn.close()
    return render_template("result.html", scan=scan, results=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        if not name or not password:
            flash("Enter your username and password.", "danger")
            return render_template("login.html")
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, name, password FROM users WHERE name = %s", (name,))
                user = cursor.fetchone()
        finally:
            conn.close()
        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            flash("Login successful.", "success")
            target = request.args.get("next", "")
            # Only allow local relative redirects.
            if target.startswith("/") and not target.startswith("//"):
                return redirect(target)
            return redirect(url_for("home"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not name or not password:
            flash("Username and password are required.", "danger")
        elif len(name) > 100:
            flash("Username must be 100 characters or fewer.", "danger")
        elif len(password) < 8:
            flash("Use a password with at least 8 characters.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        else:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (name, password) VALUES (%s, %s)",
                        (name, generate_password_hash(password)),
                    )
                conn.commit()
            except Exception as exc:
                conn.rollback()
                app.logger.warning("Registration failed: %s", exc)
                flash("Registration failed. The username may already exist, or the database is unavailable.", "danger")
            else:
                flash("Account created. Please log in.", "success")
                return redirect(url_for("login"))
            finally:
                conn.close()
        return render_template("reg.html")
    return render_template("reg.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.context_processor
def inject_user():
    return {"current_user": session.get("name")}


if __name__ == "__main__":
    print("Project folder:", BASE_DIR)
    print("Homepage template exists:", (BASE_DIR / "templates" / "index.html").is_file())
    app.run(debug=True)
