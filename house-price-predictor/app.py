"""
app.py  —  House Price Predictor (Production)
=============================================
Flask app with:
  - / (home + prediction form)
  - /predict (POST → result)
  - /history (last 10 predictions stored in session)
  - /about (model info page)

Run:
    python app.py
Open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, session, redirect, url_for
import joblib
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "house-price-predictor-2024"   # needed for session

# ── Load assets once at startup ────────────────────────────────────────────
MODEL_DIR     = "models"
model         = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
scaler        = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
le_furnishing = joblib.load(os.path.join(MODEL_DIR, "le_furnishing.pkl"))
le_ac         = joblib.load(os.path.join(MODEL_DIR, "le_ac.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

print("✅  Model loaded:", type(model).__name__)
print("✅  Features    :", feature_names)


# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        area             = float(request.form["area"])
        bedrooms         = int(request.form["bedrooms"])
        bathrooms        = int(request.form["bathrooms"])
        parking          = int(request.form["parking"])
        furnishingstatus = request.form["furnishingstatus"]
        airconditioning  = request.form["airconditioning"]

        f_enc = int(le_furnishing.transform([furnishingstatus])[0])
        a_enc = int(le_ac.transform([airconditioning])[0])

        import pandas as pd
        X = pd.DataFrame([[area, bedrooms, bathrooms, parking, f_enc, a_enc]],
                         columns=feature_names)
        X_scaled      = scaler.transform(X)
        predicted      = float(model.predict(X_scaled)[0])
        price_int      = int(round(predicted))
        price_fmt      = f"₹{price_int:,}"

        # Price range (±8%)
        low_fmt  = f"₹{int(price_int * 0.92):,}"
        high_fmt = f"₹{int(price_int * 1.08):,}"

        # Save to session history
        history = session.get("history", [])
        history.insert(0, {
            "time":             datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "price":            price_fmt,
            "area":             int(area),
            "bedrooms":         bedrooms,
            "bathrooms":        bathrooms,
            "parking":          parking,
            "furnishingstatus": furnishingstatus,
            "airconditioning":  airconditioning,
        })
        session["history"] = history[:10]   # keep last 10
        session.modified = True

        return render_template(
            "result.html",
            price=price_fmt,
            low=low_fmt,
            high=high_fmt,
            area=int(area),
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            parking=parking,
            furnishingstatus=furnishingstatus,
            airconditioning=airconditioning,
        )

    except Exception as e:
        return render_template("index.html", error=f"Prediction error: {e}")


@app.route("/history")
def history():
    records = session.get("history", [])
    return render_template("history.html", records=records)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/clear-history")
def clear_history():
    session.pop("history", None)
    return redirect(url_for("history"))


# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Open browser automatically
    import threading, webbrowser
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")
    threading.Timer(1.2, open_browser).start()
    app.run(debug=True, use_reloader=False)
