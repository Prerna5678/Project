from flask import Flask, render_template, request, redirect, url_for
from config import get_db_connection

app = Flask(__name__)

# ---------------- HOME ---------------- #

@app.route("/")
def index():
    return render_template("index.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO login(name, password) VALUES(%s, %s)",
            (name, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("index"))

    return render_template("login.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO reg(name, password) VALUES(%s, %s)",
            (name, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- ADD EXPENSE ---------------- #

@app.route("/add", methods=["POST"])
def add():

    date = request.form["date"]
    category = request.form["category"]
    description = request.form["description"]
    amount = request.form["amount"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tracking(date, category, description, amount)
        VALUES(%s, %s, %s, %s)
        """,
        (date, category, description, amount)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("report"))


# ---------------- REPORT ---------------- #

@app.route("/report")
def report():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tracking")
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("report.html", tracking=expenses)


# ---------------- VIEW ---------------- #

@app.route("/view")
def view():
    return redirect(url_for("view"))


# ---------------- EDIT ---------------- #

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        date = request.form["date"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]

        cursor.execute(
            """
            UPDATE tracking
            SET date=%s,
                category=%s,
                description=%s,
                amount=%s
            WHERE id=%s
            """,
            (date, category, description, amount, id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("report"))

    cursor.execute("SELECT * FROM tracking WHERE id=%s", (id,))
    expense = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit.html", expense=expense)


# ---------------- DELETE ---------------- #

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tracking WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("report"))


if __name__ == "__main__":
    app.run(debug=True)