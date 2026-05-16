from sqlalchemy import Column, String, Float, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class Analysis(Base):
    __tablename__ = "analyses"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_type  = Column(String, nullable=False)
    budget         = Column(Float, nullable=False)
    monthly_budget = Column(Float, nullable=False)
    goal           = Column(String, nullable=False)
    maturity       = Column(String, nullable=False)
    website_url    = Column(String, nullable=True)
    result         = Column(JSON, nullable=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())


VALID_ACTIVITY_TYPES = {
    "ecommerce", "saas", "service", "website",
    "application", "content", "consulting", "other",
}
VALID_GOALS     = {"awareness", "sales", "leads", "traffic"}
VALID_MATURITIES = {"idea", "inprogress", "launched"}


class AnalysisInput(BaseModel):
    activityType:  str
    budget:        float
    monthlyBudget: float
    goal:          str
    maturity:      str
    websiteUrl:    Optional[str] = None

    @field_validator("activityType")
    @classmethod
    def validate_activity(cls, v: str) -> str:
        if v not in VALID_ACTIVITY_TYPES:
            return "other"
        return v

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        if v not in VALID_GOALS:
            return "awareness"
        return v

    @field_validator("maturity")
    @classmethod
    def validate_maturity(cls, v: str) -> str:
        if v not in VALID_MATURITIES:
            return "idea"
        return v

    @field_validator("budget", "monthlyBudget")
    @classmethod
    def validate_budget(cls, v: float) -> float:
        if v < 1:
            return 10.0
        if v > 100_000:
            return 100_000.0
        return v


class AnalysisResponse(BaseModel):
    id:          str
    input:       dict
    swot:        dict
    personas:    list
    sales:       dict
    marketing:   dict
    seo:         dict
    ads:         dict
    pagespeed:   Optional[dict] = None
    synthesis:   dict
    created_at:  Optional[str] = None

    class Config:
        from_attributes = True
