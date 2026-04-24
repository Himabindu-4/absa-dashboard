from sqlalchemy.orm import Session
from sqlalchemy import func  # ✅ IMPORTANT
from . import models
from .crud import create_prediction, get_or_create_category
from .predictor import predict_absa


SAMPLE_DATA = {
    "phones": [
        "The battery life is amazing but the camera is bad.",
        "Excellent display and smooth performance.",
        "The sound is poor and battery drains fast."
    ],
    "laptops": [
        "Performance is excellent but the price is too high.",
        "The design looks premium and the screen is great.",
        "Battery life is disappointing and the keyboard feels cheap."
    ],
    "restaurants": [
        "The food was amazing but the service was slow.",
        "Loved the taste and quality, but price is high.",
        "The staff were rude and the meal was cold."
    ],
    "tablets": [
        "Nice display and good battery backup.",
        "Performance is slow but the design is beautiful."
    ]
}


def seed_database(db: Session):
    # ✅ FIX: ORM way instead of raw SQL
    existing_categories = db.query(func.count(models.Category.id)).scalar()

    if existing_categories and existing_categories > 0:
        return

    for category, reviews in SAMPLE_DATA.items():
        get_or_create_category(db, category)

        for review in reviews:
            result = predict_absa(review)
            create_prediction(db, category, review, result)