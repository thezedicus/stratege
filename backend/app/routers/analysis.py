from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalysisInput, AnalysisResponse
from app.services.swot_service import generate_swot
from app.services.persona_service import generate_personas
from app.services.sales_service import generate_sales
from app.services.marketing_service import generate_marketing
from app.services.seo_service import generate_seo
from app.services.ads_service import generate_ads
from app.services.synthesis_service import generate_synthesis
from app.services.pagespeed_service import analyze_pagespeed
import uuid
import logging
from typing import Optional

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory store (replace with DB in production)
_analyses: dict = {}


@router.post("/analysis", response_model=AnalysisResponse)
async def create_analysis(input_data: AnalysisInput):
    analysis_id = str(uuid.uuid4())
    logger.info(f"Creating analysis {analysis_id} for {input_data.activityType}")

    try:
        swot = generate_swot(input_data)
        personas = await generate_personas(input_data)
        sales = generate_sales(input_data, personas)
        marketing = generate_marketing(input_data)
        seo = generate_seo(input_data)
        ads = generate_ads(input_data)
        pagespeed = None
        if input_data.websiteUrl:
            pagespeed = await analyze_pagespeed(input_data.websiteUrl)
        synthesis = generate_synthesis(input_data, swot, personas, marketing, seo, ads)

        result = {
            "id": analysis_id,
            "input": input_data.model_dump(),
            "swot": swot,
            "personas": personas,
            "sales": sales,
            "marketing": marketing,
            "seo": seo,
            "ads": ads,
            "pagespeed": pagespeed,
            "synthesis": synthesis,
        }
        _analyses[analysis_id] = result
        return result

    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    if analysis_id not in _analyses:
        raise HTTPException(status_code=404, detail="Analyse introuvable")
    return _analyses[analysis_id]
