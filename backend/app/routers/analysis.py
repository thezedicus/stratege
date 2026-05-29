"""
Analysis router — POST /api/analysis  ·  GET /api/analysis/{id}
Orchestre tous les services d'analyse et stocke en mémoire.
Python 3.9 compatible.
"""
from __future__ import annotations
import asyncio
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

from fastapi import APIRouter, HTTPException

from app.models.schemas import WizardInput, AnalysisCreateResponse

from app.services.swot_service import generate_swot
from app.services.qqoqccp_service import generate_qqoqccp
from app.services.pestel_service import generate_pestel, generate_micro_env, generate_competitive
from app.services.copywriting_service import generate_copywriting
from app.services.geo_2025_service import generate_geo_2025
from app.services.pagespeed_service import analyze_pagespeed

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

router = APIRouter(tags=["analysis"])

# In-memory store — survives process restarts only; DB layer is optional
_analyses: Dict[str, Dict[str, Any]] = {}

# Thread pool for CPU-bound sync services
_executor = ThreadPoolExecutor(max_workers=8)


@router.post("/api/analysis", response_model=AnalysisCreateResponse)
async def create_analysis(data: WizardInput) -> AnalysisCreateResponse:
    """Génère une analyse complète 360° à partir des données du wizard."""
    analysis_id = str(uuid.uuid4())[:8]
    inp = data.dict()
    loop = asyncio.get_event_loop()

    # ── Run all sync services in parallel via thread pool ────────────────────
    task_defs = {
        "swot":        (generate_swot, data.activityType, data.goal, data.maturity),
        "qqoqccp":     (generate_qqoqccp, data.activityType, data.goal, data.maturity),
        "pestel":      (generate_pestel, data.activityType),
        "micro_env":   (generate_micro_env, data.activityType),
        "competitive": (generate_competitive, data.activityType),
        "copywriting": (generate_copywriting, data.activityType, data.goal),
        "geo2025":     (generate_geo_2025, data.activityType, data.goal, data.websiteUrl or ""),
    }
    if _MARKETING_OK:
        task_defs["marketing"] = (generate_marketing, data.activityType, data.goal, data.monthlyBudget)
    if _SEO_OK:
        task_defs["seo"] = (generate_seo, data.activityType, data.goal)
    if _ADS_OK:
        task_defs["ads"] = (generate_ads, data.activityType, data.goal, data.monthlyBudget)
    if _SALES_OK:
        task_defs["sales"] = (generate_sales, data.activityType, data.goal)

    async def run(fn, *args):
        return await loop.run_in_executor(_executor, fn, *args)

    coros = {key: run(*defn) for key, defn in task_defs.items()}
    results: Dict[str, Any] = {}
    for key, coro in coros.items():
        try:
            results[key] = await coro
        except Exception as exc:
            logger.warning("Service %s failed: %s", key, exc)
            results[key] = None

    # ── Personas (async service) ─────────────────────────────────────────────
    personas = _default_personas()
    if _PERSONA_OK:
        try:
            personas = await asyncio.wait_for(
                generate_personas(data.activityType, data.goal, data.maturity),
                timeout=10.0,
            )
        except Exception as exc:
            logger.warning("Persona service failed: %s", exc)

    # ── PageSpeed (async, external HTTP) ────────────────────────────────────
    pagespeed = None
    if data.websiteUrl:
        try:
            pagespeed = await asyncio.wait_for(analyze_pagespeed(data.websiteUrl), timeout=25.0)
        except Exception as exc:
            logger.warning("PageSpeed timeout/error: %s", exc)

    # ── Synthesis ────────────────────────────────────────────────────────────
    synthesis = None
    if _SYNTHESIS_OK:
        try:
            synthesis = generate_synthesis(
                swot=results.get("swot") or {},
                personas=personas,
                marketing=results.get("marketing"),
                seo=results.get("seo"),
                ads=results.get("ads"),
                input_data=inp,
            )
        except Exception as exc:
            logger.warning("Synthesis generation failed: %s", exc)

    # ── Assemble & store ─────────────────────────────────────────────────────
    analysis: Dict[str, Any] = {
        "id":          analysis_id,
        "input":       inp,
        "swot":        results.get("swot"),
        "qqoqccp":     results.get("qqoqccp"),
        "pestel":      results.get("pestel"),
        "microEnv":    results.get("micro_env"),
        "competitive": results.get("competitive"),
        "personas":    personas,
        "sales":       results.get("sales"),
        "copywriting": results.get("copywriting"),
        "marketing":   results.get("marketing"),
        "seo":         results.get("seo"),
        "geo2025":     results.get("geo2025"),
        "ads":         results.get("ads"),
        "synthesis":   synthesis,
        "pagespeed":   pagespeed,
    }
    _analyses[analysis_id] = analysis
    logger.info("Analysis %s created for %s/%s", analysis_id, data.activityType, data.goal)

    return AnalysisCreateResponse(id=analysis_id)


@router.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str) -> Dict[str, Any]:
    """Récupère une analyse par son ID."""
    if not analysis_id.replace("-", "").isalnum() or len(analysis_id) > 40:
        raise HTTPException(status_code=400, detail="Invalid analysis ID")
    analysis = _analyses.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analyse {analysis_id} introuvable")
    return analysis


def _default_personas() -> list:
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
