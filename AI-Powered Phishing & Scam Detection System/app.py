
from flask import Flask, render_template
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


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reg')
def reg():
    return render_template('reg.html')

if __name__ == '__main__':
    app.run(debug=True)
