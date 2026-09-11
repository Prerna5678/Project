from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import get_db_connection
import csv, os, traceback

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "jyesta_secret_key_2025")











if __name__ == "__main__":
    app.run(debug=True)