"""
train.py
========
Train Linear Regression and Random Forest on cleaned housing data.
Saves best model (Random Forest) and scaler as .pkl files.

Run order:
  1. python data_cleaning.py   (creates cleaned_data.csv)
  2. python train.py           (creates model.pkl + scaler.pkl)
  3. python app.py             (starts Flask server)

Usage:
    python train.py
"""

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection    import train_test_split
from sklearn.preprocessing      import StandardScaler, LabelEncoder
from sklearn.linear_model       import LinearRegression
from sklearn.ensemble           import RandomForestRegressor
from sklearn.metrics            import r2_score, mean_absolute_error

# ──────────────────────────────────────────────
# 1. Load cleaned data
# ──────────────────────────────────────────────
df = pd.read_csv("data/cleaned_data.csv")
print("=" * 50)
print("  House Price Prediction — Model Training")
print("=" * 50)
print(f"\n[1] Loaded data  → shape: {df.shape}")

# ──────────────────────────────────────────────
# 2. Encode categorical columns
#    furnishingstatus : furnished / semi-furnished / unfurnished
#    airconditioning  : yes / no
# ──────────────────────────────────────────────
le_furnishing = LabelEncoder()
le_ac         = LabelEncoder()

df["furnishingstatus"] = le_furnishing.fit_transform(df["furnishingstatus"])
df["airconditioning"]  = le_ac.fit_transform(df["airconditioning"])

# Save encoders so app.py can use the same mapping
os.makedirs("models", exist_ok=True)
joblib.dump(le_furnishing, "models/le_furnishing.pkl")
joblib.dump(le_ac,         "models/le_ac.pkl")
print(f"[2] Encoded categoricals")
print(f"    furnishingstatus → {dict(zip(le_furnishing.classes_, le_furnishing.transform(le_furnishing.classes_)))}")
print(f"    airconditioning  → {dict(zip(le_ac.classes_,         le_ac.transform(le_ac.classes_)))}")

# ──────────────────────────────────────────────
# 3. Split features and target
# ──────────────────────────────────────────────
X = df.drop("price", axis=1)
y = df["price"]

feature_names = list(X.columns)
print(f"\n[3] Features used: {feature_names}")
print(f"    Target: price")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n[4] Train/test split → train: {X_train.shape[0]} rows | test: {X_test.shape[0]} rows")

# ──────────────────────────────────────────────
# 4. Scale features
# ──────────────────────────────────────────────
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# ──────────────────────────────────────────────
# 5. Train Linear Regression
# ──────────────────────────────────────────────
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
lr_r2    = r2_score(y_test, lr_preds)
lr_mae   = mean_absolute_error(y_test, lr_preds)

print(f"\n[5] Linear Regression")
print(f"    R²  = {lr_r2:.4f}")
print(f"    MAE = ₹{lr_mae:,.0f}")

# ──────────────────────────────────────────────
# 6. Train Random Forest
# ──────────────────────────────────────────────
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
rf_r2    = r2_score(y_test, rf_preds)
rf_mae   = mean_absolute_error(y_test, rf_preds)

print(f"\n[6] Random Forest")
print(f"    R²  = {rf_r2:.4f}")
print(f"    MAE = ₹{rf_mae:,.0f}")

# ──────────────────────────────────────────────
# 7. Compare and pick winner
# ──────────────────────────────────────────────
print(f"\n{'─'*50}")
print(f"  Model Comparison")
print(f"{'─'*50}")
print(f"  {'Model':<22} {'R²':>8} {'MAE':>15}")
print(f"  {'─'*22} {'─'*8} {'─'*15}")
print(f"  {'Linear Regression':<22} {lr_r2:>8.4f} ₹{lr_mae:>13,.0f}")
print(f"  {'Random Forest':<22} {rf_r2:>8.4f} ₹{rf_mae:>13,.0f}")
print(f"{'─'*50}")

best_model = rf if rf_r2 >= lr_r2 else lr
best_name  = "Random Forest" if rf_r2 >= lr_r2 else "Linear Regression"
print(f"\n  ✅ Best model: {best_name} (R² = {max(rf_r2, lr_r2):.4f})")

# ──────────────────────────────────────────────
# 8. Save model + scaler + feature names
# ──────────────────────────────────────────────
joblib.dump(best_model,    "models/model.pkl")
joblib.dump(scaler,        "models/scaler.pkl")
joblib.dump(feature_names, "models/feature_names.pkl")

print(f"\n[7] Saved files:")
print(f"    models/model.pkl")
print(f"    models/scaler.pkl")
print(f"    models/le_furnishing.pkl")
print(f"    models/le_ac.pkl")
print(f"    models/feature_names.pkl")
print(f"\n{'='*50}")
print(f"  Done! Next step → python app.py")
print(f"{'='*50}\n")
