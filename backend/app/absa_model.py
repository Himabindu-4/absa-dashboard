from transformers import pipeline

# simple sentiment model (temporary)
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_text(text: str):
    result = sentiment_pipeline(text)[0]

    sentiment = result["label"].lower()
    confidence = float(result["score"])

    # fake aspects split (temporary until ATE)
    words = text.split()[:3]

    aspects = []
    for w in words:
        aspects.append({
            "term": w,
            "sentiment": sentiment,
            "confidence": confidence
        })

    return aspects