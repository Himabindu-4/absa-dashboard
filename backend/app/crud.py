from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


# ✅ Create or get category
def get_or_create_category(db: Session, category_name: str):
    category = db.query(models.Category).filter(
        models.Category.name == category_name
    ).first()

    if not category:
        category = models.Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    return category


# ✅ Create prediction
def create_prediction(db: Session, category_name: str, text: str, result: dict):
    category = get_or_create_category(db, category_name)

    prediction = models.Prediction(
        review_text=text,
        overall_sentiment=result["overall_sentiment"],
        confidence=result["confidence"],
        category_id=category.id
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    for asp in result["aspects"]:
        aspect_obj = models.AspectPrediction(
            term=asp["term"],
            sentiment=asp["sentiment"],
            confidence=asp["confidence"],
            prediction_id=prediction.id
        )
        db.add(aspect_obj)

    db.commit()
    db.refresh(prediction)

    return prediction


# ✅ Get all categories
def get_categories(db: Session):
    return db.query(models.Category).order_by(models.Category.name.asc()).all()


# ✅ Recent predictions
def get_recent_predictions(db: Session, category_name: str = None, limit: int = 10):
    query = db.query(models.Prediction)

    if category_name:
        query = query.join(models.Category).filter(
            models.Category.name == category_name
        )

    return query.order_by(
        models.Prediction.created_at.desc()
    ).limit(limit).all()


# ✅ Sentiment distribution
def get_sentiment_distribution(db: Session, category_name: str = None):
    query = db.query(
        models.Prediction.overall_sentiment,
        func.count(models.Prediction.id)
    ).join(models.Category)

    if category_name:
        query = query.filter(models.Category.name == category_name)

    query = query.group_by(
        models.Prediction.overall_sentiment
    ).all()

    result = {"positive": 0, "negative": 0, "neutral": 0}

    for sentiment, count in query:
        result[sentiment] = count

    return result


# ✅ Aspect distribution
def get_aspect_distribution(db: Session, category_name: str = None):
    query = db.query(
        models.AspectPrediction.term,
        models.AspectPrediction.sentiment,
        func.count(models.AspectPrediction.id)
    ).join(models.Prediction).join(models.Category)

    if category_name:
        query = query.filter(models.Category.name == category_name)

    rows = query.group_by(
        models.AspectPrediction.term,
        models.AspectPrediction.sentiment
    ).all()

    aspect_map = {}

    for term, sentiment, count in rows:
        if term not in aspect_map:
            aspect_map[term] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }

        aspect_map[term][sentiment] = count

    return aspect_map


# ✅ 🔥 FIXED TREND DATA (POSTGRESQL COMPATIBLE)
def get_trend_data(db: Session, category_name: str = None):
    query = db.query(
        func.date(models.Prediction.created_at),  # ✅ FIX
        models.Prediction.overall_sentiment,
        func.count(models.Prediction.id)
    ).join(models.Category)

    if category_name:
        query = query.filter(models.Category.name == category_name)

    rows = query.group_by(
        func.date(models.Prediction.created_at),  # ✅ FIX
        models.Prediction.overall_sentiment
    ).all()

    trend_map = {}

    for dt, sentiment, count in rows:
        date_str = str(dt)

        if date_str not in trend_map:
            trend_map[date_str] = {
                "date": date_str,
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }

        trend_map[date_str][sentiment] = count

    return list(trend_map.values())