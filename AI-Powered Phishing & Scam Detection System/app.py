
from flask import (
    Flask, flash, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from functools import wraps
from config import get_db_connection


app = Flask(__name__)

# Use an environment variable for this in production.
app.secret_key = "PhisGuard@AI"


# --------------------------------------------------
# Login required decorator
# --------------------------------------------------
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))

        return route_function(*args, **kwargs)

    return wrapper


# --------------------------------------------------
# Home page
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# History page - show only current user's records
# --------------------------------------------------
@app.route("/history")
@login_required
def history():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Change 'history' and its column names if needed
        cursor.execute(
            """
            SELECT *
            FROM history
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (session["user_id"],)
        )

        records = cursor.fetchall()

        return render_template("history.html", records=records)

    except Exception:
        app.logger.exception("Unable to load user history")
        flash("Unable to load history right now.", "error")
        return render_template("history.html", records=[])

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --------------------------------------------------
# Result page
# --------------------------------------------------
@app.route("/result")
@login_required
def result():
    return render_template("result.html")


# --------------------------------------------------
# Registration
# --------------------------------------------------

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("reg.html")

    name = request.form.get("name", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not password or not confirm_password:
        flash("Please fill in all fields.", "error")
        return render_template("reg.html")

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("reg.html")

    if len(password) < 8:
        flash("Password must be at least 8 characters.", "error")
        return render_template("reg.html")

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check whether this username already exists.
        cursor.execute(
            "SELECT user_id FROM users WHERE name = %s",
            (name,)
        )

        if cursor.fetchone() is not None:
            flash("This username already exists. Choose another.", "error")
            return render_template("reg.html")

        # Hash the password before inserting.
        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (name, password)
            VALUES (%s, %s)
            """,
            (name, hashed_password)
        )

        # Save the new user permanently.
        conn.commit()

        app.logger.info("New user registered: %s", name)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    except Exception as e:
        if conn:
            conn.rollback()

        # The actual reason appears in your Flask terminal.
        app.logger.exception("Registration database error")

        # Handle a database error without hiding the cause in the logs.
        error_text = str(e).lower()

        if "duplicate" in error_text or "unique constraint" in error_text:
            flash("This username already exists.", "error")
        else:
            flash(
                "Database error. Check the Flask terminal for details.",
                "error"
            )

        return render_template("reg.html")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# --------------------------------------------------
# Login
# --------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")

        if not name or not password:
            flash("Please enter your username and password.", "error")
            return render_template("login.html")

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Find the specific user's account
            cursor.execute(
                """
                SELECT user_id, name, password
                FROM users
                WHERE name = %s
                """,
                (name,)
            )

            user = cursor.fetchone()

        except Exception:
            app.logger.exception("Login database query failed")
            flash(
                "Unable to log in right now. Please try again.",
                "error"
            )
            return render_template("login.html")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        if user is None:
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        # Support dictionary rows and tuple rows
        if isinstance(user, dict):
            user_id = user["user_id"]
            user_name = user["name"]
            stored_password = user["password"]
        else:
            user_id, user_name, stored_password = user

        # Verify hashed password
        if check_password_hash(stored_password, password):
            # Clear old session data before login
            session.clear()

            session["user_id"] = user_id
            session["user_name"] = user_name

            flash(
                f"Welcome back, {user_name}!",
                "success"
            )
            return redirect(url_for("index"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


# --------------------------------------------------
# Logout
# --------------------------------------------------
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# --------------------------------------------------
# Run application
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
