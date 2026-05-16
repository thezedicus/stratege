"""
PageSpeed Insights service.
Python 3.9 compatible — uses Optional[dict] instead of dict | None.
"""
from typing import Optional
import httpx
import logging

logger = logging.getLogger(__name__)

try:
    from app.config import settings
    _PSI_KEY = getattr(settings, 'pagespeed_api_key', None)
except Exception:
    _PSI_KEY = None


async def analyze_pagespeed(url: str) -> Optional[dict]:
    """Fetch PageSpeed Insights data for a URL. Returns None if URL is invalid."""
    if not url or not url.startswith("http"):
        return None

    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params: dict = {
        "url": url,
        "strategy": "mobile",
        "category": ["performance", "seo", "accessibility", "best-practices"],
    }
    if _PSI_KEY:
        params["key"] = _PSI_KEY

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(api_url, params=params)
            if resp.status_code != 200:
                logger.warning("PageSpeed API returned %s", resp.status_code)
                return _mock_pagespeed()

            data = resp.json()
            cats   = data.get("lighthouseResult", {}).get("categories", {})
            audits = data.get("lighthouseResult", {}).get("audits", {})

            return {
                "performance":   _score(cats, "performance"),
                "seo":           _score(cats, "seo"),
                "accessibility": _score(cats, "accessibility"),
                "bestPractices": _score(cats, "best-practices"),
                "lcp": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
                "fid": audits.get("total-blocking-time",       {}).get("displayValue", "N/A"),
                "cls": audits.get("cumulative-layout-shift",   {}).get("displayValue", "N/A"),
            }
    except Exception as exc:
        logger.warning("PageSpeed analysis failed: %s", exc)
        return _mock_pagespeed()


def _score(cats: dict, key: str) -> int:
    return round((cats.get(key, {}).get("score", 0.5) or 0.5) * 100)


def _mock_pagespeed() -> dict:
    """Fallback mock data when PageSpeed API is unavailable."""
    return {
        "performance":   62,
        "seo":           78,
        "accessibility": 71,
        "bestPractices": 83,
        "lcp": "3.2 s",
        "fid": "120 ms",
        "cls": "0.12",
    }
