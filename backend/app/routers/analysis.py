"""
Analysis router — POST /api/analysis  ·  GET /api/analysis/{id}
Orchestre tous les services d'analyse et stocke en mémoire.
Python 3.9 compatible.
"""
from __future__ import annotations
import asyncio
import uuid
import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException

from app.models.schemas import WizardInput, AnalysisCreateResponse

from app.services.swot_service import generate_swot
from app.services.qqoqccp_service import generate_qqoqccp
from app.services.pestel_service import generate_pestel, generate_micro_env, generate_competitive
from app.services.copywriting_service import generate_copywriting
from app.services.geo_2025_service import generate_geo_2025
from app.services.pagespeed_service import analyze_pagespeed

# Optional services — graceful degradation
try:
    from app.services.persona_service import generate_personas
    _PERSONA_OK = True
except ImportError:
    _PERSONA_OK = False

try:
    from app.services.marketing_service import generate_marketing
    _MARKETING_OK = True
except ImportError:
    _MARKETING_OK = False

try:
    from app.services.seo_service import generate_seo
    _SEO_OK = True
except ImportError:
    _SEO_OK = False

try:
    from app.services.ads_service import generate_ads
    _ADS_OK = True
except ImportError:
    _ADS_OK = False

try:
    from app.services.sales_service import generate_sales
    _SALES_OK = True
except ImportError:
    _SALES_OK = False

try:
    from app.services.synthesis_service import generate_synthesis
    _SYNTHESIS_OK = True
except ImportError:
    _SYNTHESIS_OK = False

logger = logging.getLogger(__name__)

# Note: NO prefix here — main.py mounts this router under /api
router = APIRouter(tags=["analysis"])

# ── In-memory store (survives process restarts only — DB layer optional) ───────
_analyses: Dict[str, Dict[str, Any]] = {}


@router.post("/api/analysis", response_model=AnalysisCreateResponse)
async def create_analysis(data: WizardInput) -> AnalysisCreateResponse:
    """
    Génère une analyse complète 360° à partir des données du wizard.
    """
    analysis_id = str(uuid.uuid4())[:8]
    inp = data.dict()

    # ── Services synchrones ───────────────────────────────────────────────────
    swot        = generate_swot(data.activityType, data.goal, data.maturity)
    qqoqccp     = generate_qqoqccp(data.activityType, data.goal, data.maturity)
    pestel      = generate_pestel(data.activityType)
    micro_env   = generate_micro_env(data.activityType)
    competitive = generate_competitive(data.activityType)
    copywriting = generate_copywriting(data.activityType, data.goal)

    personas   = generate_personas(data.activityType, data.goal, data.maturity) if _PERSONA_OK else _default_personas()
    marketing  = generate_marketing(data.activityType, data.goal, data.monthlyBudget) if _MARKETING_OK else None
    seo_data   = generate_seo(data.activityType, data.goal) if _SEO_OK else None
    ads_data   = generate_ads(data.activityType, data.goal, data.monthlyBudget) if _ADS_OK else None
    sales_data = generate_sales(data.activityType, data.goal) if _SALES_OK else None

    # ── Service async (PageSpeed) ─────────────────────────────────────────────
    pagespeed = None
    geo2025   = generate_geo_2025(data.activityType, data.goal, data.websiteUrl or "")
    if data.websiteUrl:
        try:
            pagespeed = await asyncio.wait_for(analyze_pagespeed(data.websiteUrl), timeout=25.0)
        except Exception as exc:
            logger.warning("PageSpeed timeout/error: %s", exc)

    # ── Synthesis ─────────────────────────────────────────────────────────────
    synthesis = None
    if _SYNTHESIS_OK:
        try:
            synthesis = generate_synthesis(
                swot=swot,
                personas=personas,
                marketing=marketing,
                seo=seo_data,
                ads=ads_data,
                input_data=inp,
            )
        except Exception as exc:
            logger.warning("Synthesis generation failed: %s", exc)

    # ── Assemble & store ──────────────────────────────────────────────────────
    analysis: Dict[str, Any] = {
        "id":          analysis_id,
        "input":       inp,
        "swot":        swot,
        "qqoqccp":     qqoqccp,
        "pestel":      pestel,
        "microEnv":    micro_env,
        "competitive": competitive,
        "personas":    personas,
        "sales":       sales_data,
        "copywriting": copywriting,
        "marketing":   marketing,
        "seo":         seo_data,
        "geo2025":     geo2025,
        "ads":         ads_data,
        "synthesis":   synthesis,
        "pagespeed":   pagespeed,
    }
    _analyses[analysis_id] = analysis
    logger.info("Analysis %s created for %s/%s", analysis_id, data.activityType, data.goal)

    return AnalysisCreateResponse(id=analysis_id)


@router.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str) -> Dict[str, Any]:
    """Récupère une analyse par son ID."""
    # Sanitize: only alphanumeric + hyphens
    if not analysis_id.replace("-", "").isalnum() or len(analysis_id) > 40:
        raise HTTPException(status_code=400, detail="Invalid analysis ID")
    analysis = _analyses.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analyse {analysis_id} introuvable")
    return analysis


def _default_personas() -> list:
    """Personas par défaut si le service persona n'est pas disponible."""
    return [
        {
            "name": "Alex",
            "age": 32,
            "job": "Responsable marketing",
            "goals": ["Augmenter la notoriété de la marque", "Générer des leads qualifiés"],
            "painPoints": ["Manque de temps", "Budget limité", "Difficulté à mesurer le ROI"],
            "channels": ["LinkedIn", "Google", "Email"],
            "quote": "J'ai besoin de solutions qui montrent des résultats rapides et mesurables.",
        },
        {
            "name": "Sophie",
            "age": 28,
            "job": "Entrepreneur indépendant",
            "goals": ["Développer sa clientèle", "Automatiser les tâches répétitives"],
            "painPoints": ["Isolement", "Gestion administrative", "Trouver des clients réguliers"],
            "channels": ["Instagram", "Bouche-à-oreille", "Google My Business"],
            "quote": "Je cherche des outils simples qui font vraiment la différence.",
        },
    ]
