from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from collections import Counter, defaultdict
import csv, io

from app.database import get_db
from app.models import Prediction, AspectPrediction, Category

# 🔥 ABSA PIPELINE
from app.absa_pipeline import analyze_text

router = APIRouter()

# -----------------------------
# ANALYZE TEXT
# -----------------------------
@router.post("/analyze")
def analyze(payload: dict, db: Session = Depends(get_db)):

    text = payload.get("text")
    category_name = payload.get("category", "phones")

    # Get or create category
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    # 🔥 ABSA PIPELINE
    aspects = analyze_text(text)

    # Save prediction
    overall_sentiment = aspects[0]["sentiment"] if aspects else "neutral"
    confidence = aspects[0]["confidence"] if aspects else 0.5

    pred = Prediction(
        review_text=text,
        overall_sentiment=overall_sentiment,
        confidence=confidence,
        category_id=category.id,
        created_at=datetime.utcnow()
    )

    db.add(pred)
    db.commit()
    db.refresh(pred)

    # Save aspects
    for a in aspects:
        db.add(AspectPrediction(
            term=a["term"],
            sentiment=a["sentiment"],
            confidence=a["confidence"],
            prediction_id=pred.id
        ))

    db.commit()

    return {"aspects": aspects}


# -----------------------------
# CSV UPLOAD
# -----------------------------
@router.post("/upload")
def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    all_aspects = []

    for row in reader:
        text = row.get("review", "")
        category_name = row.get("category", "phones")

        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()
            db.refresh(category)

        aspects = analyze_text(text)

        overall_sentiment = aspects[0]["sentiment"] if aspects else "neutral"
        confidence = aspects[0]["confidence"] if aspects else 0.5

        pred = Prediction(
            review_text=text,
            overall_sentiment=overall_sentiment,
            confidence=confidence,
            category_id=category.id,
            created_at=datetime.utcnow()
        )

        db.add(pred)
        db.commit()
        db.refresh(pred)

        for a in aspects:
            db.add(AspectPrediction(
                term=a["term"],
                sentiment=a["sentiment"],
                confidence=a["confidence"],
                prediction_id=pred.id
            ))

        db.commit()

        all_aspects.extend(aspects)

    return {"aspects": all_aspects}


# -----------------------------
# STATS (FOR CHARTS)
# -----------------------------
@router.get("/stats")
def get_stats(category: str = None, db: Session = Depends(get_db)):

    query = db.query(AspectPrediction).join(Prediction).join(Category)

    if category:
        query = query.filter(Category.name == category)

    rows = query.all()

    result = []
    for r in rows:
        val = 1 if r.sentiment == "positive" else -1 if r.sentiment == "negative" else 0

        result.append({
            "term": r.term,
            "sentiment": r.sentiment,
            "value": val
        })

    return result


# -----------------------------
# TREND
# -----------------------------
@router.get("/trend")
def get_trend(category: str = None, db: Session = Depends(get_db)):

    query = db.query(Prediction).join(Category)

    if category:
        query = query.filter(Category.name == category)

    rows = query.all()

    trend = defaultdict(int)

    for r in rows:
        day = str(r.created_at.date())
        trend[day] += 1

    return [{"date": k, "count": v} for k, v in trend.items()]


# -----------------------------
# TOP ASPECTS
# -----------------------------
@router.get("/top-aspects")
def top_aspects(category: str = None, db: Session = Depends(get_db)):

    query = db.query(AspectPrediction).join(Prediction).join(Category)

    if category:
        query = query.filter(Category.name == category)

    rows = query.all()

    counter = Counter([r.term for r in rows])

    return dict(counter.most_common(5))