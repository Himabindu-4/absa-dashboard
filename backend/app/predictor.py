from transformers import pipeline
from .ate_model import extract_aspects

# ✅ Load fast BERT sentiment model
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


# ✅ Convert model labels to your format
def map_sentiment(label):
    if label == "POSITIVE":
        return "positive"
    elif label == "NEGATIVE":
        return "negative"
    return "neutral"


# ✅ Main ABSA function
def predict_absa(text: str):
    # 🔥 Use BERT-based aspect extraction
    aspects = extract_aspects(text)

    results = []
    sentiments = []

    # Analyze each aspect
    for aspect in aspects:
        input_text = f"{text}. Aspect: {aspect}"

        output = sentiment_model(input_text)[0]

        sentiment = map_sentiment(output["label"])
        confidence = float(output["score"])

        results.append({
            "term": aspect,
            "sentiment": sentiment,
            "confidence": round(confidence, 3)
        })

        sentiments.append(sentiment)

    # ✅ Fallback if no aspects detected
    if not results:
        output = sentiment_model(text)[0]

        sentiment = map_sentiment(output["label"])

        return {
            "overall_sentiment": sentiment,
            "confidence": float(output["score"]),
            "aspects": []
        }

    # ✅ Majority sentiment
    overall = max(set(sentiments), key=sentiments.count)

    return {
        "overall_sentiment": overall,
        "confidence": round(
            sum([r["confidence"] for r in results]) / len(results), 3
        ),
        "aspects": results
    }