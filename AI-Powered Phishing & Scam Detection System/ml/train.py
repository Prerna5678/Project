import pandas as pd
from features import get_features

df = pd.read_csv("data/PhishingData.csv")

print(df.head())
print(df.shape)
print(df.columns)

X = get_features(df)
y = df["Result"]