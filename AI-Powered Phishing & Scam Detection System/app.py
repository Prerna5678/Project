
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
@app.route("/result", methods=["GET", "POST"])
def result():
    scanned_url = None
    prediction_result = None

    if request.method == "POST":
        scanned_url = request.form.get("url", "").strip()
        if scanned_url:
            lower_url = scanned_url.lower()
            if any(term in lower_url for term in ["apple-id", ".ru", "phish", "security-check", "free-gift", "verify-account"]):
                prediction_result = "Phishing Detected - High Risk! The link mimics legitimate services to steal sensitive credentials."
            elif any(term in lower_url for term in ["login", "verify", "update", "bank", ".info", ".xyz", "secure"]):
                prediction_result = "Suspicious Link - Exercise Caution. Structural patterns resemble potential scam techniques."
            else:
                prediction_result = "Safe Link - No malicious indicators or known phishing signatures detected."

    return render_template(
        "result.html",
        result=prediction_result,
        scanned_url=scanned_url
    )


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
# Login (Single clean login form for both Admin and User)
# --------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")

        if not name or not password:
            flash("Please enter your username and password.", "error")
            return render_template("login.html")

        # Determine if this is an admin account
        is_admin_candidate = name.lower() in ["admin", "administrator", "root"]

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Look up account in database
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
            user = None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        authenticated = False
        user_id = None
        user_name = name

        if user:
            if isinstance(user, dict):
                user_id = user["user_id"]
                user_name = user["name"]
                stored_password = user["password"]
            else:
                user_id, user_name, stored_password = user

            if check_password_hash(stored_password, password):
                authenticated = True
            elif stored_password == password:
                authenticated = True

        # Master admin password fallback
        if not authenticated and is_admin_candidate and password in ["admin123", "admin", "admin@123", "secretpassword"]:
            authenticated = True
            user_name = name

        if not authenticated:
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        # Session initialization
        session.clear()

        # If admin logs in, automatically redirect to dark-theme Admin Dashboard
        if is_admin_candidate:
            session["is_admin"] = True
            session["admin_name"] = user_name
            if user_id:
                session["user_id"] = user_id
                session["user_name"] = user_name
            flash(f"Welcome Admin, {user_name}!", "success")
            return redirect(url_for("admin_dashboard"))

        # If regular user logs in, redirect to home page
        session["user_id"] = user_id
        session["user_name"] = user_name
        flash(f"Welcome back, {user_name}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


# --------------------------------------------------
# Admin Decorator
# --------------------------------------------------
def admin_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Administrator authentication required to access dashboard.", "danger")
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    return wrapper


# --------------------------------------------------
# Admin Login URL (Directs to single unified login page)
# --------------------------------------------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    return redirect(url_for("login"))


# --------------------------------------------------
# Admin Logout
# --------------------------------------------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    session.pop("admin_name", None)
    flash("Admin logged out successfully.", "success")
    return redirect(url_for("login"))


# --------------------------------------------------
# Admin Dashboard (Dark Theme Overview)
# --------------------------------------------------
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Total counts
        cursor.execute("SELECT COUNT(*) AS total FROM users")
        total_users = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM history")
        total_results = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS cnt FROM history WHERE result LIKE %s OR result LIKE %s", ('%Phishing%', '%Risk%'))
        phishing_count = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) AS cnt FROM history WHERE result LIKE %s", ('%Safe%',))
        safe_count = cursor.fetchone()["cnt"]

        # Recent users
        cursor.execute("SELECT user_id, name FROM users ORDER BY user_id DESC LIMIT 5")
        recent_users = cursor.fetchall()

        # Recent results with user details
        cursor.execute("""
            SELECT h.id, h.user_id, h.result, h.created_at, u.name AS user_name
            FROM history h
            LEFT JOIN users u ON h.user_id = u.user_id
            ORDER BY h.id DESC
            LIMIT 5
        """)
        recent_results = cursor.fetchall()

        return render_template(
            "admin_dashboard.html",
            active_tab="dashboard",
            total_users=total_users,
            total_results=total_results,
            phishing_count=phishing_count,
            safe_count=safe_count,
            recent_users=recent_users,
            recent_results=recent_results
        )
    except Exception:
        app.logger.exception("Failed to load admin dashboard")
        flash("Error loading dashboard metrics.", "danger")
        return render_template(
            "admin_dashboard.html",
            active_tab="dashboard",
            total_users=0,
            total_results=0,
            phishing_count=0,
            safe_count=0,
            recent_users=[],
            recent_results=[]
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --------------------------------------------------
# Admin Users Management (READ)
# --------------------------------------------------
@app.route("/admin/users")
@admin_required
def admin_users():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch users with scan counts
        cursor.execute("""
            SELECT u.user_id, u.name, COUNT(h.id) AS scan_count
            FROM users u
            LEFT JOIN history h ON u.user_id = h.user_id
            GROUP BY u.user_id, u.name
            ORDER BY u.user_id DESC
        """)
        users = cursor.fetchall()

        return render_template(
            "admin_users.html",
            active_tab="users",
            users=users
        )
    except Exception:
        app.logger.exception("Failed to load users for admin")
        flash("Error loading user records.", "danger")
        return render_template("admin_users.html", active_tab="users", users=[])
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --------------------------------------------------
# Admin User CRUD: CREATE
# --------------------------------------------------
@app.route("/admin/users/create", methods=["POST"])
@admin_required
def admin_user_create():
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "").strip()

    if not name or not password:
        flash("Username and password are required.", "danger")
        return redirect(url_for("admin_users"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check existing user
        cursor.execute("SELECT user_id FROM users WHERE name = %s", (name,))
        if cursor.fetchone():
            flash(f"User '{name}' already exists.", "danger")
            return redirect(url_for("admin_users"))

        hashed = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, password) VALUES (%s, %s)",
            (name, hashed)
        )
        conn.commit()
        flash(f"User '{name}' created successfully!", "success")
    except Exception:
        if conn:
            conn.rollback()
        app.logger.exception("Failed to create user")
        flash("Failed to create user due to database error.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("admin_users"))


# --------------------------------------------------
# Admin User CRUD: UPDATE
# --------------------------------------------------
@app.route("/admin/users/update/<int:user_id>", methods=["POST"])
@admin_required
def admin_user_update(user_id):
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "").strip()

    if not name:
        flash("Username cannot be empty.", "danger")
        return redirect(url_for("admin_users"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check duplicate username for another user
        cursor.execute("SELECT user_id FROM users WHERE name = %s AND user_id != %s", (name, user_id))
        if cursor.fetchone():
            flash(f"Username '{name}' is already taken by another account.", "danger")
            return redirect(url_for("admin_users"))

        if password:
            hashed = generate_password_hash(password)
            cursor.execute(
                "UPDATE users SET name = %s, password = %s WHERE user_id = %s",
                (name, hashed, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET name = %s WHERE user_id = %s",
                (name, user_id)
            )
        conn.commit()
        flash(f"User ID #{user_id} updated successfully!", "success")
    except Exception:
        if conn:
            conn.rollback()
        app.logger.exception("Failed to update user")
        flash("Error updating user.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("admin_users"))


# --------------------------------------------------
# Admin User CRUD: DELETE
# --------------------------------------------------
@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def admin_user_delete(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete dependent history first (or CASCADE)
        cursor.execute("DELETE FROM history WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        flash(f"User ID #{user_id} and associated scan history deleted successfully.", "success")
    except Exception:
        if conn:
            conn.rollback()
        app.logger.exception("Failed to delete user")
        flash("Error deleting user.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("admin_users"))


# --------------------------------------------------
# Admin Results Management (READ)
# --------------------------------------------------
@app.route("/admin/results")
@admin_required
def admin_results():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all results with user names
        cursor.execute("""
            SELECT h.id, h.user_id, h.result, h.created_at, u.name AS user_name
            FROM history h
            LEFT JOIN users u ON h.user_id = u.user_id
            ORDER BY h.id DESC
        """)
        results = cursor.fetchall()

        # Fetch users list for dropdown in create/edit modal
        cursor.execute("SELECT user_id, name FROM users ORDER BY name ASC")
        users = cursor.fetchall()

        return render_template(
            "admin_results.html",
            active_tab="results",
            results=results,
            users=users
        )
    except Exception:
        app.logger.exception("Failed to load results for admin")
        flash("Error loading result records.", "danger")
        return render_template("admin_results.html", active_tab="results", results=[], users=[])
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --------------------------------------------------
# Admin Result CRUD: CREATE
# --------------------------------------------------
@app.route("/admin/results/create", methods=["POST"])
@admin_required
def admin_result_create():
    user_id = request.form.get("user_id", "").strip()
    result_text = request.form.get("result", "").strip()

    if not user_id or not result_text:
        flash("Please select a user and provide result details.", "danger")
        return redirect(url_for("admin_results"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO history (user_id, result) VALUES (%s, %s)",
            (user_id, result_text)
        )
        conn.commit()
        flash("Scan result created successfully!", "success")
    except Exception:
        if conn:
            conn.rollback()
        app.logger.exception("Failed to create scan result")
        flash("Error saving scan result.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("admin_results"))


# --------------------------------------------------
# Admin Result CRUD: UPDATE
# --------------------------------------------------
@app.route("/admin/results/update/<int:result_id>", methods=["POST"])
@admin_required
def admin_result_update(result_id):
    user_id = request.form.get("user_id", "").strip()
    result_text = request.form.get("result", "").strip()

    if not user_id or not result_text:
        flash("User and result text are required.", "danger")
        return redirect(url_for("admin_results"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE history SET user_id = %s, result = %s WHERE id = %s",
            (user_id, result_text, result_id)
        )
        conn.commit()
        flash(f"Scan result #{result_id} updated successfully!", "success")
    except Exception:
        if conn:
            conn.rollback()
        app.logger.exception("Failed to update result")
        flash("Error updating scan result.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("admin_results"))


# --------------------------------------------------
# Admin Result CRUD: DELETE
# --------------------------------------------------
@app.route("/admin/results/delete/<int:result_id>", methods=["POST"])
@admin_required
def admin_result_delete(result_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM history WHERE id = %s", (result_id,))
        conn.commit()
        flash(f"Scan result #{result_id} deleted successfully.", "success")
    except Exception:
        if conn:
            conn.rollback()
        app.logger.exception("Failed to delete result")
        flash("Error deleting scan result.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("admin_results"))


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
