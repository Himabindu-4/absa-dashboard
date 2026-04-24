from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    predictions = relationship(
        "Prediction",
        back_populates="category",
        cascade="all, delete"
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(Text, nullable=False)
    overall_sentiment = Column(String, nullable=False, default="NEU")
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="predictions")

    aspects = relationship(
        "AspectPrediction",
        back_populates="prediction",
        cascade="all, delete-orphan"
    )


class AspectPrediction(Base):
    __tablename__ = "aspect_predictions"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    confidence = Column(Float, default=0.0)

    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False)
    prediction = relationship("Prediction", back_populates="aspects")