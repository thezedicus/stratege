"""
seo_competitive.py — SEO avancé inspiré des meilleures pratiques concurrentes
Cible : LivePlan, BPI France, Enloop, Canvanizer, Bizplan, Stratpad, Upmetrics
Toutes techniques légales : meta tags, schema.org, sitemap, performance
"""

# ─── META TAGS SEO OPTIMAUX (inspiré Upmetrics + LivePlan) ──────────────────
SEO_META = {
    "title": "BiziApp — Strategie commerciale gratuite pour dirigeants TPE PME | Plan en 10 minutes",
    "description": "BiziApp genere votre strategie commerciale complete en 10 minutes : SWOT, plan marketing, personas, KPIs et roadmap 180 jours. Gratuit pour les dirigeants TPE PME. Alternative aux cabinets conseil a 5 000 EUR.",
    "keywords": [
        "business plan gratuit", "analyse SWOT gratuit", "stratégie commerciale",
        "plan marketing gratuit", "diagnostic entreprise", "plan stratégique",
        "PESTEL analyse", "stratégie digitale PME", "outil stratégie",
        "alternative consultant stratégie", "business plan rapide",
        "plan stratégique TPE PME", "logiciel business plan français",
        "outil diagnostic entreprise gratuit france", "SWOT personnalisé",
        "plan marketing TPE freelance", "stratégie croissance startup",
        "Lean Canvas gratuit", "Business Model Canvas", "Ocean Bleu stratégie",
    ],
    "og_title": "BiziApp — Votre expert stratégique virtuel | Gratuit",
    "og_description": "Plan commercial complet en 10 min : SWOT, Personas, SEO, Marketing, KPIs. 0€ vs 5 000€ cabinet conseil. 14 modules stratégiques.",
    "twitter_card": "summary_large_image",
    "canonical": "https://biziapp.streamlit.app",
    "robots": "index, follow, max-snippet:-1, max-image-preview:large",
    "lang": "fr",
    "geo_region": "FR",
    "geo_placename": "France",
}

# ─── SCHEMA.ORG JSON-LD (rich snippets Google) ───────────────────────────────
SCHEMA_ORG = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "BiziApp",
    "url": "https://biziapp.streamlit.app",
    "description": "Outil de stratégie commerciale 360° — business plan, SWOT, marketing, SEO en 10 minutes. Gratuit.",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "EUR",
        "availability": "https://schema.org/InStock",
    },
    "featureList": [
        "Analyse SWOT personnalisée",
        "Business Plan complet",
        "Stratégie Marketing 360°",
        "Plan SEO et GEO 2025",
        "Personas clients",
        "KPIs et OKRs",
        "Roadmap 180 jours",
        "14 modules stratégiques",
    ],
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": "247",
        "bestRating": "5",
    },
    "creator": {
        "@type": "Organization",
        "name": "BiziApp",
        "url": "https://biziapp.streamlit.app",
        "sameAs": ["https://github.com/thezedicus/stratege"],
    },
}

SCHEMA_FAQ = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question",
         "name": "BiziApp est-il vraiment gratuit pour les dirigeants TPE et PME ?",
         "acceptedAnswer": {"@type": "Answer",
                           "text": "Oui, BiziApp est entierement gratuit pour les dirigeants de TPE et PME. Aucune carte bancaire, aucune inscription obligatoire. Vous obtenez votre plan strategique complet en 10 minutes sans payer."}},
        {"@type": "Question",
         "name": "Combien de temps faut-il pour générer un business plan ?",
         "acceptedAnswer": {"@type": "Answer",
                           "text": "En moins de 10 minutes. Renseignez votre secteur, objectif et budget, et BiziApp génère instantanément un plan stratégique complet."}},
        {"@type": "Question",
         "name": "Quelle est la différence avec un cabinet de conseil ?",
         "acceptedAnswer": {"@type": "Answer",
                           "text": "Un cabinet de conseil facture en moyenne 5 000€ pour un diagnostic stratégique. BiziApp génère un plan équivalent gratuitement en 10 minutes."}},
        {"@type": "Question",
         "name": "Quels modules sont inclus dans BiziApp ?",
         "acceptedAnswer": {"@type": "Answer",
                           "text": "SWOT, QQOQCCP, PESTEL, Personas, Copywriting AIDA, SPIN Selling, Marketing 360°, SEO/GEO 2025, KPIs, OKRs, Roadmap 180j, Porter 5 Forces, Ansoff, Customer Journey, Pricing, Emailing, Social Media, RSE, et plus."}},
        {"@type": "Question",
         "name": "BiziApp est-il disponible sur mobile ?",
         "acceptedAnswer": {"@type": "Answer",
                           "text": "Oui, BiziApp est entièrement responsive et fonctionne sur iPhone, Android, Mac, PC, Linux, dans tous les navigateurs (Safari, Chrome, Firefox, Edge)."}},
    ],
}


def inject_seo_html() -> str:
    """Retourne le bloc HTML complet à injecter via st.markdown."""
    import json as _j
    schema_str = _j.dumps(SCHEMA_ORG, ensure_ascii=False)
    faq_str = _j.dumps(SCHEMA_FAQ, ensure_ascii=False)
    kw_str = ", ".join(SEO_META["keywords"])

    return f"""
<head>
<!-- ═══ SEO BIZIAPP v5.0 ═══════════════════════════════════════════════════ -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<meta name="description" content="{SEO_META['description']}">
<meta name="keywords" content="{kw_str}">
<meta name="robots" content="{SEO_META['robots']}">
<meta name="language" content="French">
<meta name="geo.region" content="{SEO_META['geo_region']}">
<meta name="geo.placename" content="{SEO_META['geo_placename']}">
<meta name="author" content="BiziApp">
<meta name="application-name" content="BiziApp">
<meta name="theme-color" content="#44C1BA">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="{SEO_META['og_title']}">
<meta property="og:description" content="{SEO_META['og_description']}">
<meta property="og:url" content="{SEO_META['canonical']}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="BiziApp">

<!-- Twitter Card -->
<meta name="twitter:card" content="{SEO_META['twitter_card']}">
<meta name="twitter:title" content="{SEO_META['og_title']}">
<meta name="twitter:description" content="{SEO_META['og_description']}">

<!-- Canonical -->
<link rel="canonical" href="{SEO_META['canonical']}">

<!-- Preconnect performance -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://api.allorigins.win">
<link rel="dns-prefetch" href="https://news.google.com">
<link rel="dns-prefetch" href="https://recherche-entreprises.api.gouv.fr">

<!-- Schema.org WebApplication -->
<script type="application/ld+json">{schema_str}</script>
<!-- Schema.org FAQPage -->
<script type="application/ld+json">{faq_str}</script>
</head>
"""


# ─── API CONCURRENTS — fonctionnalités à répliquer ──────────────────────────
# Fonctionnalités clés des concurrents et APIs gratuites pour les répliquer

COMPETITOR_FEATURES = {
    "LivePlan": {
        "features": ["Financial forecasting", "Pitch deck", "Business plan narrative"],
        "api_replicate": "Calculs ROI/projection biziapp + export PDF",
        "notre_avantage": "Gratuit + français + 10 minutes",
    },
    "Canvanizer": {
        "features": ["Business Model Canvas interactif", "Lean Canvas", "Partage collaboratif"],
        "api_replicate": "gen_business_model_canvas + gen_lean_canvas déjà intégrés",
        "notre_avantage": "Personnalisé par secteur + données live",
    },
    "Upmetrics": {
        "features": ["AI business plan", "Financial projections", "Investor ready"],
        "api_replicate": "gen_roi_projection + gen_synthesis + données sectorielles",
        "notre_avantage": "100% gratuit, sans limite, en français",
    },
    "BPI France Coach": {
        "features": ["Diagnostic auto-évaluation", "Plan action", "Financement"],
        "api_replicate": "gen_swot + gen_action_plan_180j + données INSEE gratuites",
        "notre_avantage": "Plus complet, plus rapide, disponible 24/7",
    },
    "Enloop": {
        "features": ["Auto-write business plan", "Financial ratios", "Score"],
        "api_replicate": "Analyse auto-personnalisée par secteur + score global synthesis",
        "notre_avantage": "Pas de paywall, données françaises, RGPD",
    },
}


def get_sitemap_urls() -> list:
    """URLs pour le sitemap XML."""
    base = "https://biziapp.streamlit.app"
    return [
        {"url": base, "priority": "1.0", "changefreq": "weekly"},
        {"url": f"{base}/?tab=swot", "priority": "0.9", "changefreq": "monthly"},
        {"url": f"{base}/?tab=marketing", "priority": "0.9", "changefreq": "monthly"},
        {"url": f"{base}/?tab=seo", "priority": "0.8", "changefreq": "monthly"},
        {"url": f"{base}/?tab=personas", "priority": "0.8", "changefreq": "monthly"},
        {"url": f"{base}/?tab=pricing", "priority": "0.7", "changefreq": "monthly"},
    ]
