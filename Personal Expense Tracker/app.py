from flask import Flask, render_template, request, redirect, url_for
from config import get_db_connection

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# insert new row (POST)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date        = request.form["date"]
        category    = request.form["category"]
        description = request.form["description"]
        amount      = request.form["amount"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tracking (date, category, description, amount) VALUES (%s,%s,%s,%s)",
            (date, category, description, amount)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("view"))

    return render_template("index.html")


# READ — list all rows
@app.route("/view")
def view():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tracking")
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view.html", tracking=expenses)


# UPDATE — show edit form pre-filled (GET) / save changes (POST)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        date        = request.form["date"]
        category    = request.form["category"]
        description = request.form["description"]
        amount      = request.form["amount"]

        cursor.execute(
            "UPDATE tracking SET date=%s, category=%s, description=%s, amount=%s WHERE id=%s",
            (date, category, description, amount, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("view"))

    cursor.execute("SELECT * FROM tracking WHERE id=%s", (id,))
    expense = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template("report.html", expense=expense)


# DELETE — remove a row
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tracking WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("view"))


if __name__ == "__main__":
    app.run(debug=True)
