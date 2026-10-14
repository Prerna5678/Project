from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_db_connection


app = Flask(__name__)
app.secret_key = "PhisGuard@AI" 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        name             = request.form["name"].strip()
        email            = request.form.get("email", "").strip()
        password         = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            flash("❌ Passwords do not match!", "error")
            return render_template("reg.html")
        hashed = generate_password_hash(password)
        conn = get_db_connection(); cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (name, email, hashed))
            conn.commit()
            flash("✅ Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            err = str(e)
            if "Duplicate entry" in err and "users.name" in err:
                flash(f"❌ Username '{name}' is already taken. Please choose a different username.", "error")
            elif "Duplicate entry" in err and "users.email" in err:
                flash(f"❌ This email is already registered. Please use a different email.", "error")
            else:
                flash(f"❌ Error: {err}", "error")
        finally:
            cursor.close(); conn.close()
    return render_template("reg.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name     = request.form["name"]
        password = request.form["password"]
        conn = get_db_connection(); cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, password FROM users WHERE name=%s", (name,))
        user = cursor.fetchone()
        cursor.close(); conn.close()
        if user is None:
            flash("❌ User does not exist!", "error")
            return render_template("login.html")
        if check_password_hash(user["password"], password):
            session["user_id"]   = user["user_id"]
            session["user_name"] = user["name"]
            flash(f"✅ Welcome back, {user['name']}!", "success")
            return redirect(url_for("index"))
        flash("❌ Invalid Username or Password!", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
