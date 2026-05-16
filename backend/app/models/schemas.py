from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_type = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    monthly_budget = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    maturity = Column(String, nullable=False)
    website_url = Column(String, nullable=True)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic schemas
class AnalysisInput(BaseModel):
    activityType: str
    budget: float
    monthlyBudget: float
    goal: str
    maturity: str
    websiteUrl: Optional[str] = None


class AnalysisResponse(BaseModel):
    id: str
    input: dict
    swot: dict
    personas: list
    sales: dict
    marketing: dict
    seo: dict
    ads: dict
    pagespeed: Optional[dict] = None
    synthesis: dict
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
