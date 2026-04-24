# classical_baseline.py

import re
import pandas as pd
import nltk
import spacy

from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# SETUP
# -----------------------------
nltk.download("vader_lexicon")

nlp = spacy.load("en_core_web_sm")

# -----------------------------
# LOAD EXCEL DATA (FIXED)
# -----------------------------
df1 = pd.read_excel("app/data/Restaurants_Train_v2.xlsx")
df2 = pd.read_excel("app/data/Laptop_Train_v2.xlsx")

df = pd.concat([df1, df2], ignore_index=True)

# normalize column names
df.columns = [c.lower().strip() for c in df.columns]

# keep only required columns
df = df[["sentence", "polarity"]].dropna()

# rename for consistency
df.rename(columns={"sentence": "review", "polarity": "sentiment"}, inplace=True)

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower()

# -----------------------------
# SPACY PREPROCESS
# -----------------------------
def preprocess(text):
    doc = nlp(text)
    tokens = [t.lemma_ for t in doc if not t.is_stop]
    return " ".join(tokens)

df["clean"] = df["review"].apply(clean_text)
df["processed"] = df["clean"].apply(preprocess)

# -----------------------------
# TF-IDF + LOGISTIC REGRESSION
# -----------------------------
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["processed"])

y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

preds = model.predict(X_test)

print("\n📊 TF-IDF + Logistic Regression")
print(classification_report(y_test, preds))
print("F1 Score:", round(f1_score(y_test, preds, average="weighted"), 4))

# -----------------------------
# VADER
# -----------------------------
sia = SentimentIntensityAnalyzer()

def vader_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "positive"
    elif score < -0.05:
        return "negative"
    return "neutral"

df["vader"] = df["clean"].apply(vader_sentiment)

print("\n📊 VADER Results")
print(classification_report(df["sentiment"], df["vader"]))