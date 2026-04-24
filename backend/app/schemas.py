from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AspectOut(BaseModel):
    term: str
    sentiment: str
    confidence: float

    class Config:
        from_attributes = True


class AnalyseRequest(BaseModel):
    text: str
    category: str


class PredictionOut(BaseModel):
    id: int
    review_text: str
    overall_sentiment: str
    confidence: float
    created_at: datetime
    category: str
    aspects: List[AspectOut]

    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
