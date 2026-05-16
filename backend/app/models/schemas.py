"""
Pydantic v2 schemas — modèles de données de l'API Stratège.
Python 3.9 compatible.
"""
from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, field_validator


# ─── Input wizard ─────────────────────────────────────────────────────────────
class WizardInput(BaseModel):
    activityType: str
    budget: float
    monthlyBudget: float
    goal: str
    maturity: str
    websiteUrl: Optional[str] = ""

    @field_validator("activityType")
    @classmethod
    def validate_activity(cls, v: str) -> str:
        allowed = {"ecommerce","saas","service","website","application","content","consulting","other"}
        return v if v in allowed else "other"

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        allowed = {"awareness","sales","leads","traffic"}
        return v if v in allowed else "awareness"

    @field_validator("maturity")
    @classmethod
    def validate_maturity(cls, v: str) -> str:
        allowed = {"idea","inprogress","launched"}
        return v if v in allowed else "idea"

    @field_validator("budget", "monthlyBudget")
    @classmethod
    def validate_budget(cls, v: float) -> float:
        return max(0.0, min(float(v), 1_000_000.0))

    @field_validator("websiteUrl")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if v and not v.startswith("http"):
            v = "https://" + v
        return v


# ─── Response models ──────────────────────────────────────────────────────────
class AnalysisCreateResponse(BaseModel):
    id: str
    status: str = "ok"


class AnalysisResponse(BaseModel):
    id: str
    input: Dict[str, Any]
    swot: Optional[Dict[str, Any]] = None
    qqoqccp: Optional[Dict[str, Any]] = None
    pestel: Optional[Dict[str, Any]] = None
    microEnv: Optional[Dict[str, Any]] = None
    competitive: Optional[Dict[str, Any]] = None
    personas: Optional[List[Dict[str, Any]]] = None
    sales: Optional[Dict[str, Any]] = None
    copywriting: Optional[Dict[str, Any]] = None
    marketing: Optional[Dict[str, Any]] = None
    seo: Optional[Dict[str, Any]] = None
    geo2025: Optional[Dict[str, Any]] = None
    ads: Optional[Dict[str, Any]] = None
    synthesis: Optional[Dict[str, Any]] = None
    pagespeed: Optional[Dict[str, Any]] = None
