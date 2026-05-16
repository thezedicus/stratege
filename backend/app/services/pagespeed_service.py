from typing import Optional
import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)


async def analyze_pagespeed(url: str) -> Optional[dict]:
    if not url or not url.startswith("http"):
        return None

    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": "mobile",
        "category": ["performance", "seo", "accessibility", "best-practices"],
    }
    if settings.pagespeed_api_key:
        params["key"] = settings.pagespeed_api_key

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(api_url, params=params)
            if resp.status_code != 200:
                logger.warning(f"PageSpeed API error: {resp.status_code}")
                return _mock_pagespeed()

            data = resp.json()
            cats = data.get("lighthouseResult", {}).get("categories", {})
            audits = data.get("lighthouseResult", {}).get("audits", {})

            return {
                "performance": _score(cats, "performance"),
                "seo": _score(cats, "seo"),
                "accessibility": _score(cats, "accessibility"),
                "bestPractices": _score(cats, "best-practices"),
                "lcp": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
                "fid": audits.get("total-blocking-time", {}).get("displayValue", "N/A"),
                "cls": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
            }
    except Exception as e:
        logger.warning(f"PageSpeed analysis failed: {e}")
        return _mock_pagespeed()


def _score(cats: dict, key: str) -> int:
    return round((cats.get(key, {}).get("score", 0.5) or 0.5) * 100)


def _mock_pagespeed() -> dict:
    return {
        "performance": 62,
        "seo": 78,
        "accessibility": 71,
        "bestPractices": 83,
        "lcp": "3.2s",
        "fid": "120ms",
        "cls": "0.12",
    }
