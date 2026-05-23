# ── SEO & Meta tags (injectés via st.markdown) ───────────────────────────────
_SEO_KEYWORDS = {
    "ecommerce": "stratégie ecommerce, plan marketing boutique en ligne, SWOT ecommerce, personas clients ecommerce, ROI publicité, SEO ecommerce France",
    "saas": "stratégie SaaS, plan marketing logiciel, SWOT SaaS, personas B2B, growth hacking SaaS, SEO SaaS France",
    "service": "stratégie prestataire de services, plan commercial freelance, SWOT services, personas clients B2B, acquisition clients TPE",
    "consulting": "stratégie cabinet conseil, plan marketing consultant, personal branding consultant, acquisition clients conseil",
    "content": "stratégie créateur de contenu, monétisation contenu, plan marketing créateur, SEO YouTube, newsletter stratégie",
    "other": "stratégie commerciale TPE PME, plan marketing gratuit, SWOT gratuit, diagnostic stratégique entreprise France",
}

_SEO_DEFAULTS = {
    "title": "BiziApp — Stratégie commerciale 360° en 10 minutes | Gratuit",
    "description": "BiziApp génère votre plan commercial complet : SWOT, personas, SEO, marketing, KPIs, roadmap 180j. Gratuit, sans inscription, résultat en 10 minutes. Conçu pour TPE, freelances et consultants français.",
    "keywords": "stratégie commerciale gratuite, plan marketing TPE, SWOT gratuit, diagnostic entreprise, plan commercial 10 minutes, personas clients, SEO gratuit, BiziApp",
    "og_image": "https://biziapp.streamlit.app/",
    "canonical": "https://biziapp.streamlit.app/",
    "twitter_card": "summary_large_image",
    "author": "BiziApp — Expert virtuel en stratégie commerciale",
    "lang": "fr",
    "robots": "index, follow",
    "schema_org": {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "BiziApp",
        "applicationCategory": "BusinessApplication",
        "description": "Outil de stratégie commerciale 360° pour TPE et freelances",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "url": "https://biziapp.streamlit.app/",
        "author": {"@type": "Organization", "name": "BiziApp"},
        "keywords": "stratégie commerciale, SWOT, marketing, SEO, plan commercial",
    }
}

def inject_seo_meta(activity: str = "other") -> str:
    """Génère les balises meta SEO optimisées pour le contenu affiché."""
    import json as _j
    kw = _SEO_KEYWORDS.get(activity, _SEO_DEFAULTS["keywords"])
    schema = _j.dumps(_SEO_DEFAULTS["schema_org"], ensure_ascii=False)
    return f"""
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
  <title>{_SEO_DEFAULTS["title"]}</title>
  <meta name="description" content="{_SEO_DEFAULTS["description"]}">
  <meta name="keywords" content="{kw}">
  <meta name="author" content="{_SEO_DEFAULTS["author"]}">
  <meta name="robots" content="{_SEO_DEFAULTS["robots"]}">
  <meta name="language" content="{_SEO_DEFAULTS["lang"]}">
  <link rel="canonical" href="{_SEO_DEFAULTS["canonical"]}">
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{_SEO_DEFAULTS["title"]}">
  <meta property="og:description" content="{_SEO_DEFAULTS["description"]}">
  <meta property="og:url" content="{_SEO_DEFAULTS["canonical"]}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:site_name" content="BiziApp">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="{_SEO_DEFAULTS["twitter_card"]}">
  <meta name="twitter:title" content="{_SEO_DEFAULTS["title"]}">
  <meta name="twitter:description" content="{_SEO_DEFAULTS["description"]}">
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">{schema}</script>
  <!-- Alternate hreflang -->
  <link rel="alternate" hreflang="fr" href="{_SEO_DEFAULTS["canonical"]}">
  <link rel="alternate" hreflang="x-default" href="{_SEO_DEFAULTS["canonical"]}">
</head>
"""
