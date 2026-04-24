from . import models


def serialize_prediction(prediction: models.Prediction):
    return {
        "id": prediction.id,
        "review_text": prediction.review_text,
        "overall_sentiment": prediction.overall_sentiment,
        "confidence": prediction.confidence,
        "created_at": prediction.created_at,
        "category": prediction.category.name,
        "aspects": [
            {
                "term": a.term,
                "sentiment": a.sentiment,
                "confidence": a.confidence
            }
            for a in prediction.aspects
        ]
    }
