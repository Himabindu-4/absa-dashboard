from app.ate_model import extract_aspects
from app.asc_model import predict_sentiment

text = "The battery life is poor but camera quality is amazing"

aspects = extract_aspects(text)

results = []

for asp in aspects:
    sentiment = predict_sentiment(text, asp)
    results.append({
        "term": asp,
        "sentiment": sentiment["sentiment"],
        "confidence": sentiment["confidence"]
    })

print(results)