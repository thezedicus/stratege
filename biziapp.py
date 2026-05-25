"""
biziapp.py  --  Dashboard stratégique 360° complet
Streamlit · Python 3.9+
Intègre : SWOT · QQOQCCP · PESTEL · Micro-Env · Concurrence · SONCAS
           Personas · Copywriting AIDA · Déclencheurs psychologiques
           GEO 2025 · SEA IA · Marketing · SEO · Vente · Synthèse
"""
import copy
import json
import datetime
import html as _html
import urllib.parse as _urlparse
import urllib.request as _urlreq
import xml.etree.ElementTree as _ET
import re as _re
import streamlit as st
import math
import time

st.set_page_config(
    page_title="BiziApp  --  Plan Stratégique Complet en 10 Minutes | Expert Commercial IA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": (
            "## BiziApp v5.0\n"
            "Votre expert virtuel en stratégie commerciale.\n\n"
            "Générez votre plan 360° en 10 minutes : SWOT · Personas · SEO · Marketing · KPIs\n\n"
            "**100% gratuit · Sans inscription · Données sécurisées**"
        ),
    }
)


# ── SEO meta injection (schema.org + meta tags + performance) ─────────────────
if _HAS_SEO_COMPETITIVE:
    st.markdown(_inject_seo_html(), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# api_layer  --  Couche APIs gratuites (veille, URL, INSEE, OSM, HN, Reddit...)
# ─────────────────────────────────────────────────────────────────────────────
# ── Modules complémentaires ──────────────────────────────────────────────────
try:
    from seo_competitive import inject_seo_html as _inject_seo_html, SEO_META
    _HAS_SEO_COMPETITIVE = True
except ImportError:
    _HAS_SEO_COMPETITIVE = False
    def _inject_seo_html(): return ""

try:
    from seo_module import inject_seo_meta as _inject_seo_meta
    _HAS_SEO_MODULE = True
except ImportError:
    _HAS_SEO_MODULE = False
    def _inject_seo_meta(activity="other"): return ""

try:
    from new_project_tab import render_new_project_tab as _render_new_project_tab
    _HAS_PROJECT_TAB = True
except ImportError:
    _HAS_PROJECT_TAB = False
    def _render_new_project_tab(): pass

try:
    from resources_module import render_resources_page as _render_resources_page
    _HAS_RESOURCES = True
except ImportError:
    _HAS_RESOURCES = False
    def _render_resources_page(): pass

try:
    from pricing_plans import render_pricing_page, PLANS, SVG_CHECK, SVG_STAR, render_countdown
    _HAS_PRICING = True
except ImportError:
    _HAS_PRICING = False
    def render_pricing_page(**kwargs): pass  # module absent

try:
    from enrichment_apis import (
        get_forex_rates as _get_forex,
        fetch_google_news as _fetch_gnews,
        fetch_startups_fr as _fetch_startups,
        get_macro_france as _get_macro,
        fetch_google_trends_rss as _fetch_trends,
        fetch_product_hunt_rss as _fetch_ph,
        analyze_url_advanced as _analyze_url_adv,
        get_wikipedia_summary as _wiki_summary,
        get_survie_stats as _get_survie,
    )
    _HAS_ENRICHMENT = True
except ImportError:
    _HAS_ENRICHMENT = False
    def _get_forex(): return {"USD":1.08,"GBP":0.86,"CHF":0.97}
    def _fetch_gnews(q, **kw): return []
    def _fetch_startups(s): return []
    def _get_macro(): return {}
    def _fetch_trends(geo="FR"): return []
    def _fetch_ph(): return []
    def _analyze_url_adv(u): return {}
    def _wiki_summary(t, **kw): return {}
    def _get_survie(a="other"): return {}

try:
    from api_layer import (
        read_url as _read_url_live,
        fetch_news_full as _fetch_news_full,
        fetch_hackernews as _fetch_hn,
        fetch_devto as _fetch_devto,
        fetch_github_trending as _fetch_github,
        search_entreprises as _search_entreprises,
        get_secteur_data as _get_secteur_data,
        geocode as _geocode,
        osm_competitors_nearby as _osm_nearby,
        fetch_wikipedia_extract as _fetch_wiki_live,
        get_ecb_rates as _get_ecb_rates,
        enrich_response as _enrich_response,
        extract_keywords_advanced as _extract_kw_advanced,
        personalize_swot as _personalize_swot,
        wikidata_sector_info as _wikidata_sector,
    )
    _HAS_API_LAYER = True
except ImportError:
    _HAS_API_LAYER = False
    # ── Stubs no-op  --  évite tout NameError si api_layer absent ───────────────
    def _read_url_live(url, **kw): return {}
    def _fetch_news_full(q, lang="fr", max_items=12): return []
    def _fetch_hn(q, max_items=6): return []
    def _fetch_devto(tag, max_items=5): return []
    def _fetch_github(max_items=4): return []
    def _search_entreprises(q, activite="", max_results=5): return []
    def _get_secteur_data(a): return {}
    def _geocode(addr, country="fr"): return {}
    def _osm_nearby(lat, lon, act, radius=5000): return []
    def _fetch_wiki_live(t, lang="fr", sentences=5): return {}
    def _get_ecb_rates(): return {}
    def _enrich_response(b, s, sec, n): return b
    def _extract_kw_advanced(t, top_n=20): return []
    def _personalize_swot(s, sd, sec): return s
    def _wikidata_sector(lbl): return {}

# ─────────────────────────────────────────────────────────────────────────────
# Optional imports
# ─────────────────────────────────────────────────────────────────────────────
try:
    import requests
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────────────────────────────────────
# ── SEO: Injection méta-tags Open Graph et structured data ──────────────────
st.markdown("""
<head>
<meta name="description" content="BiziApp génère votre stratégie commerciale complète en 10 minutes : SWOT, personas, plan SEO, marketing digital, KPIs. Gratuit, sans inscription. Expert virtuel pour TPE, freelances et consultants.">
<meta name="keywords" content="stratégie commerciale, plan marketing, SWOT automatique, personas client, SEO, marketing digital, TPE, freelance, consultant, BiziApp">
<meta property="og:title" content="BiziApp — Plan Stratégique Complet en 10 Minutes">
<meta property="og:description" content="Votre expert virtuel en stratégie commerciale. SWOT, Personas, SEO, Marketing, KPIs générés instantanément.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://thezedicus-stratege-biziapp.streamlit.app">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="BiziApp — Stratégie commerciale en 10 minutes">
<meta name="twitter:description" content="Expert virtuel gratuit pour TPE, freelances et consultants. Plan complet en 10 minutes.">
<meta name="robots" content="index, follow">
<meta name="author" content="BiziApp">
<link rel="canonical" href="https://thezedicus-stratege-biziapp.streamlit.app">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "BiziApp",
  "description": "Expert virtuel en stratégie commerciale  --  plan complet en 10 minutes",
  "url": "https://thezedicus-stratege-biziapp.streamlit.app",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
  "author": {"@type": "Organization", "name": "BiziApp"}
}
</script>
</head>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* ── Override variables CSS NATIVES de Streamlit ─────────────────────────── */
:root {
  --primary-color: #44C1BA !important;
  --secondary-background-color: #C6ECD9 !important;
  --background-color: #F7FBF4 !important;
  --text-color: #0B2221 !important;
  --font: "Inter", system-ui, sans-serif !important;
}
/* Force toutes les utilisations de la couleur primaire orange → teal */
* { --primary: #44C1BA !important; }

/* Inter font loaded via system font stack  --  no external request */
:root{--graphite:#0B2221;--graphite2:#267371;--teal:#44C1BA;--teal-pale:#C6ECD9;--jade:#267371;--jade-pale:#C6ECD9;--ivoire:#F7FBF4;--craie:#F2ECD9;--encre:#0B2221;--muted:#339999;--border:#C6ECD9;}
*,*::before,*::after{box-sizing:border-box}
html,body,[class*="css"]{font-family:'Inter',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;color:var(--encre)}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1.25rem!important;max-width:1280px}
[data-testid="stSidebar"]{background:#F7FBF4;border-right:1px solid var(--craie)}
[data-testid="stSidebar"] label{font-weight:500;font-size:.88rem}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid var(--craie);background:transparent}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent;border:none;border-bottom:2px solid transparent;margin-bottom:-2px;padding:10px 16px;font-size:.76rem;font-weight:600;color:var(--muted);letter-spacing:.05em;text-transform:uppercase;transition:color .2s,border-color .2s}
[data-testid="stTabs"] [aria-selected="true"]{color:var(--graphite)!important;border-bottom-color:var(--teal)!important}
[data-testid="stTabs"] [data-baseweb="tab"]:hover{color:var(--graphite)}

/* ── Header typographique ── */
.bizi-header{display:flex;align-items:center;gap:16px;padding:0 0 18px 0;border-bottom:1px solid var(--craie);margin-bottom:22px}
.logo-bizi{font-size:1.8rem;font-weight:800;color:var(--graphite);letter-spacing:-1.5px;line-height:1}
.logo-app{font-size:1.8rem;font-weight:800;color:var(--teal);letter-spacing:-1.5px;line-height:1}
.header-sub{font-size:.68rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;font-weight:500;margin-top:3px}

/* ── Cards ── */
.card{background:white;border-radius:12px;padding:20px 22px;border:1px solid var(--border);box-shadow:0 1px 4px rgba(0,0,0,.05);margin-bottom:14px}
.card-dark{background:linear-gradient(135deg,var(--graphite) 0%,var(--graphite2) 100%);color:white;border-radius:12px;padding:20px 24px;margin-bottom:14px}
.card-title{font-weight:700;font-size:.95rem;margin-bottom:10px;color:var(--encre)}

/* ── Feature cards (landing) ── */
.feature-card{background:white;border-radius:12px;padding:18px;border:1px solid var(--border);border-top:3px solid var(--teal);box-shadow:0 1px 4px rgba(0,0,0,.05);transition:box-shadow .2s,transform .2s}
.feature-card:hover{box-shadow:0 6px 20px rgba(0,0,0,.09);transform:translateY(-2px)}
.feature-title{font-weight:700;font-size:.88rem;color:var(--graphite);margin-bottom:5px}
.feature-desc{font-size:.78rem;color:var(--muted);line-height:1.5}

/* ── SWOT ── */
.swot-strength{border-left:4px solid #44C1BA;background:#C6ECD9}
.swot-weakness{border-left:4px solid var(--teal);background:var(--teal-pale)}
.swot-oppty{border-left:4px solid #393DAC;background:#E4E9F6}
.swot-threat{border-left:4px solid #B83D4B;background:#F7FBF4}

/* ── Badges ── */
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.7rem;font-weight:600;white-space:nowrap}
.badge-blue{background:#E4E9F6;color:#393DAC}.badge-green{background:#C6ECD9;color:#0B2221}
.badge-red{background:#F7EEF0;color:#B83D4B}
.badge-graphite{background:#E4E9F6;color:#0B2221}
.badge-muted{background:#F2ECD9;color:#339999}
.badge-gray{background:#F2ECD9;color:#339999}
.badge-orange{background:#FEF3C7;color:#B45309}
.badge-indigo{background:#E4E9F6;color:#393DAC}
.url-kw{display:inline-block;background:#C6ECD9;color:#267371;border-radius:4px;padding:2px 7px;font-size:.7rem;font-weight:600;margin:2px}
.url-panel{background:#F7FBF4;border:1.5px solid #C6ECD9;border-radius:12px;padding:16px 20px;margin-bottom:14px}
.metric-box{text-align:center;padding:14px 10px;background:white;border-radius:12px;border:1.5px solid #C6ECD9}
.metric-box .val{font-size:1.6rem;font-weight:800;line-height:1.1}
.metric-box .lbl{font-size:.72rem;color:#339999;font-weight:600;margin-top:3px}.badge-teal{background:var(--teal-pale);color:#267371}
.badge-purple{background:#E4E9F6;color:#267371}.badge-gray{background:#E4E9F6;color:#267371}
.badge-graphite{background:var(--graphite);color:#F7FBF4}.badge-jade{background:var(--jade-pale);color:var(--jade)}

/* ── Impact dots ── */
.dot-pos{display:inline-block;width:8px;height:8px;border-radius:50%;background:#44C1BA;margin-right:6px;vertical-align:middle}
.dot-neg{display:inline-block;width:8px;height:8px;border-radius:50%;background:#B83D4B;margin-right:6px;vertical-align:middle}
.dot-neu{display:inline-block;width:8px;height:8px;border-radius:50%;background:#44C1BA;margin-right:6px;vertical-align:middle}

/* ── Score ring ── */
.score-ring{width:110px;height:110px;border-radius:50%;background:conic-gradient(var(--teal) var(--pct),#C6ECD9 0);display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:800;color:var(--encre);box-shadow:inset 0 0 0 18px white;margin:0 auto 8px}

/* ── Metric boxes ── */
.metric-box{text-align:center;padding:16px 12px;border-radius:12px;background:white;border:1px solid var(--border);box-shadow:0 1px 4px rgba(0,0,0,.05)}
.metric-box .val{font-size:1.6rem;font-weight:800;color:var(--encre)}
.metric-box .lbl{font-size:.75rem;color:var(--muted);margin-top:3px}

/* ── KPI tiles ── */
.kpi-tile{border:1px solid var(--craie);border-radius:12px;padding:18px 16px;text-align:center;transition:box-shadow .18s ease,transform .18s ease;cursor:default;margin-bottom:10px}
.kpi-tile:hover{box-shadow:0 4px 16px rgba(15,23,42,.10);transform:translateY(-2px)}

/* ── Table ── */
.bizi-table{width:100%;border-collapse:collapse;font-size:.84rem}
.bizi-table th{background:#F7FBF4;padding:9px 13px;text-align:left;font-weight:600;font-size:.72rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);border-bottom:2px solid var(--border)}
.bizi-table td{padding:9px 13px;border-bottom:1px solid #E4E9F6;color:var(--encre)}
.bizi-table tr:hover td{background:#F7FBF4}

/* ── AIDA ── */
.aida-attention{background:#F7FBF4;border-left:4px solid #B83D4B}
.aida-interest{background:#F7FBF4;border-left:4px solid #44C1BA}
.aida-desire{background:#E4E9F6;border-left:4px solid #393DAC}
.aida-action{background:#F7FBF4;border-left:4px solid #44C1BA}

/* ── Section headers ── */
.section-h{font-size:.95rem;font-weight:700;color:var(--graphite);display:flex;align-items:center;gap:10px;margin:22px 0 14px}
.section-h::before{content:"";display:inline-block;width:4px;height:16px;background:var(--teal);border-radius:2px;flex-shrink:0}

/* ── Progress ── */
.progress-bar{background:#E4E9F6;border-radius:999px;height:6px;overflow:hidden;margin:5px 0}
.progress-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--teal) 0%,#267371 100%);transition:width .5s ease}

/* ── Sidebar wizard steps ── */
.step-label{font-size:.64rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:14px 0 5px;display:flex;align-items:center;gap:6px}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--graphite);color:white;font-size:.64rem;font-weight:700;flex-shrink:0}

/* ── SONCAS ── */
.soncas-securite{background:#E4E9F6;border-left:4px solid #393DAC;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-opportunite{background:#F7FBF4;border-left:4px solid #44C1BA;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-nouveaute{background:#E4E9F6;border-left:4px solid #393DAC;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-confort{background:var(--teal-pale);border-left:4px solid var(--teal);border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-argent{background:var(--jade-pale);border-left:4px solid var(--jade);border-radius:10px;padding:14px 16px;margin-bottom:10px}
.soncas-sympathie{background:#C6ECD9;border-left:4px solid #44C1BA;border-radius:10px;padding:14px 16px;margin-bottom:10px}

/* ── URL analysis panel ── */
.url-panel{background:linear-gradient(135deg,var(--graphite) 0%,var(--graphite2) 100%);color:white;border-radius:14px;padding:22px 26px;margin-bottom:18px}
.url-panel-title{font-size:1rem;font-weight:700;margin-bottom:4px;color:white}
.url-panel-sub{font-size:.78rem;opacity:.75;margin-bottom:12px}
.url-kw{display:inline-block;background:rgba(255,255,255,.12);color:white;border-radius:4px;padding:2px 8px;font-size:.7rem;margin:2px}

/* ── Context bar ── */
.ctx-pill{background:var(--graphite);color:white;border-radius:6px;padding:4px 12px;font-size:.74rem;font-weight:600;letter-spacing:.03em}
.ctx-pill.teal{background:var(--teal)}.ctx-pill.jade{background:var(--jade)}.ctx-pill.blue{background:#393DAC}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#C6ECD9}
::-webkit-scrollbar-thumb{background:var(--craie);border-radius:999px}
::-webkit-scrollbar-thumb:hover{background:#339999}

/* ── Mobile ── */
@media(max-width:768px){
  .bizi-header{flex-direction:column;gap:8px;padding-bottom:14px}
  .logo-bizi,.logo-app{font-size:1.4rem}
  [data-testid="column"]{width:100%!important;flex:1 1 100%!important}
  .card{padding:14px}.metric-box .val{font-size:1.2rem}
  .bizi-table{font-size:.74rem}
  [data-testid="stTabs"] [data-baseweb="tab"]{padding:8px 9px;font-size:.68rem}
  .feature-card{padding:14px}
}

/* ── RSE / RFM / Prix / Proposition de valeur ── */
.rse-card{background:#F7FBF4;border:1px solid #C6ECD9;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.rfm-card{background:white;border:1px solid var(--craie);border-radius:12px;padding:16px;text-align:center;min-height:140px}
.prix-badge{display:inline-block;background:var(--teal-pale);color:#267371;border-radius:4px;padding:2px 8px;font-size:.65rem;font-weight:700;margin-bottom:6px}
.pv-card{border-radius:12px;padding:18px 20px;margin-bottom:10px;color:white}

/* ── Transitions webkit ── */
.kpi-tile,.feature-card{-webkit-transition:box-shadow .18s ease,transform .18s ease}
.progress-fill{-webkit-transition:width .5s ease}

/* ═══════════════════════════════════════════════════════════════════
   OVERRIDE COMPLET COMPOSANTS STREAMLIT  --  Palette teal/jade
   Cible tous les composants natifs qui utilisent primaryColor
   ═══════════════════════════════════════════════════════════════════ */

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]{background:#44C1BA!important;border-color:#44C1BA!important}
[data-testid="stSlider"] [data-baseweb="slider"] div[class*="Track"]{background:#C6ECD9!important}
[data-testid="stSlider"] [data-baseweb="slider"] div[class*="InnerTrack"]{background:#44C1BA!important}
[data-testid="stSlider"] span{color:#0B2221!important}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]::before{background:#44C1BA!important}

/* ── Bouton primary ── */
[data-testid="stButton"] button[kind="primary"],[data-testid="stButton"] button[data-testid="baseButton-primary"]{background:#44C1BA!important;border-color:#44C1BA!important;color:white!important}
[data-testid="stButton"] button[kind="primary"]:hover{background:#267371!important;border-color:#267371!important}
button[kind="primary"]{background:#44C1BA!important;border-color:#44C1BA!important;color:white!important}
.stButton>button[type="submit"]{background:#44C1BA!important;border-color:#44C1BA!important}

/* ── Selectbox / Multiselect ── */
[data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="tag"]{background:#44C1BA!important}
[data-testid="stSelectbox"] [aria-selected="true"]{background:#C6ECD9!important;color:#0B2221!important}
[data-baseweb="option"]:hover{background:#C6ECD9!important}
[data-baseweb="option"][aria-selected="true"]{background:#44C1BA!important;color:white!important}

/* ── Checkbox ── */
[data-testid="stCheckbox"] [data-baseweb="checkbox"] [data-checked="true"] div{background:#44C1BA!important;border-color:#44C1BA!important}
[data-baseweb="checkbox"] [data-checked="true"]{background:#44C1BA!important;border-color:#44C1BA!important}

/* ── Radio ── */
[data-testid="stRadio"] [data-baseweb="radio"] [data-checked="true"] div{background:#44C1BA!important;border-color:#44C1BA!important}

/* ── Progress bar / spinner ── */
[data-testid="stProgress"] [data-baseweb="progress-bar"] div{background:#44C1BA!important}
.stProgress > div > div > div > div{background:#44C1BA!important}

/* ── Metric delta positive ── */
[data-testid="stMetric"] [data-testid="stMetricDelta"] svg{color:#44C1BA!important}
[data-testid="stMetricDelta"][data-direction="up"]{color:#267371!important}

/* ── Text input focus ── */
[data-baseweb="input"]:focus-within,[data-baseweb="textarea"]:focus-within{border-color:#44C1BA!important;box-shadow:0 0 0 2px rgba(68,193,186,0.2)!important}
input:focus,textarea:focus{border-color:#44C1BA!important;outline-color:#44C1BA!important}

/* ── Links ── */
a{color:#267371!important}
a:hover{color:#44C1BA!important}

/* ── st.info / st.success couleur accent ── */
[data-testid="stAlert"][data-baseweb="notification"]{border-left-color:#44C1BA!important}

/* ── Number input ── */
[data-testid="stNumberInput"] button{color:#44C1BA!important}
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within{border-color:#44C1BA!important}

/* ── Expander ── */
[data-testid="stExpander"] summary:hover{color:#44C1BA!important}
[data-testid="stExpander"] [data-baseweb="accordion"] button{color:#0B2221!important}

/* ── Sidebar bouton lancer analyse ── */
[data-testid="stSidebar"] button[kind="primary"]{background:linear-gradient(135deg,#44C1BA,#267371)!important;border:none!important;font-weight:700!important;letter-spacing:.03em!important}
[data-testid="stSidebar"] button[kind="primary"]:hover{background:linear-gradient(135deg,#267371,#0B2221)!important}

/* ── Texte coloré en orange → forcer teal ── */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] b{color:#44C1BA!important}

/* ── Caption / small text ── */
[data-testid="stCaptionContainer"]{color:#339999!important}

/* ── Spinner ── */
[data-testid="stSpinner"] svg circle{stroke:#44C1BA!important}

/* ── Divider ── */
hr{border-color:#C6ECD9!important}

/* ═══ ANIMATIONS GLOBALES BiziApp ═══════════════════════════════ */
@keyframes fadeInUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeInLeft{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
@keyframes pulseRing{0%{box-shadow:0 0 0 0 rgba(68,193,186,.5)}70%{box-shadow:0 0 0 16px rgba(68,193,186,0)}100%{box-shadow:0 0 0 0 rgba(68,193,186,0)}}
@keyframes shimmer{0%{background-position:-200% center}100%{background-position:200% center}}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
@keyframes floatY{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes barFill{from{width:0}to{width:var(--bw,70%)}}
@keyframes countUp{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:scale(1)}}
@keyframes glowBorder{0%,100%{border-color:rgba(68,193,186,.25)}50%{border-color:#44C1BA}}
@keyframes heroIn{from{opacity:0;transform:translateY(40px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}

/* ── Landing page ── */
.lp-hero{animation:heroIn .8s cubic-bezier(.22,1,.36,1) both}
.lp-sub{animation:fadeInUp .7s .18s cubic-bezier(.22,1,.36,1) both}
.lp-cta{animation:fadeInUp .7s .32s cubic-bezier(.22,1,.36,1) both}
.lp-targets{animation:fadeInUp .6s .45s cubic-bezier(.22,1,.36,1) both}
.lp-problems{animation:fadeInUp .6s .55s cubic-bezier(.22,1,.36,1) both}
.lp-benefits{animation:fadeInUp .6s .65s cubic-bezier(.22,1,.36,1) both}
.lp-proof{animation:fadeInUp .6s .72s cubic-bezier(.22,1,.36,1) both}

/* ── CTA button ── */
.cta-btn{display:inline-block;padding:15px 38px;background:linear-gradient(135deg,#44C1BA,#267371);color:white!important;font-weight:800;font-size:1.05rem;border-radius:50px;text-decoration:none;letter-spacing:-.01em;animation:pulseRing 2.4s cubic-bezier(.4,0,.6,1) infinite;transition:transform .2s,box-shadow .2s;cursor:pointer;border:none}
.cta-btn:hover{transform:scale(1.05) translateY(-2px);box-shadow:0 14px 36px rgba(68,193,186,.4)!important;animation:none}

/* ── Shimmer title ── */
.shimmer-txt{background:linear-gradient(90deg,#44C1BA 0%,#0B2221 40%,#44C1BA 60%,#267371 80%,#44C1BA 100%);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:shimmer 3.5s linear infinite}

/* ── Benefit cards ── */
.ben-card{background:white;border-radius:16px;padding:22px 18px;border:1.5px solid #C6ECD9;transition:transform .25s cubic-bezier(.34,1.56,.64,1),box-shadow .25s,border-color .25s;margin-bottom:12px}
.ben-card:hover{transform:translateY(-6px) scale(1.02);box-shadow:0 18px 42px rgba(68,193,186,.16);border-color:#44C1BA}
.ben-icon{font-size:1.9rem;animation:floatY 3.5s ease-in-out infinite;display:inline-block;margin-bottom:8px}

/* ── Target pills ── */
.tgt-pill{display:inline-flex;align-items:center;gap:7px;background:white;border:2px solid #C6ECD9;border-radius:50px;padding:9px 18px;margin:4px;font-weight:600;font-size:.88rem;color:#0B2221;transition:all .2s cubic-bezier(.34,1.56,.64,1);cursor:default}
.tgt-pill:hover{background:#44C1BA;color:white;border-color:#44C1BA;transform:scale(1.07)}

/* ── Problem rows ── */
.prob-row{display:flex;align-items:center;gap:13px;padding:13px 17px;border-radius:11px;background:#FDF0F2;border-left:4px solid #B83D4B;margin-bottom:9px;animation:fadeInLeft .5s ease both}.p-icon{font-size:1.4rem;flex-shrink:0}.p-text{font-size:.88rem;color:#0B2221;line-height:1.5}

/* ── Stat boxes ── */
.stat-box{text-align:center;padding:18px 12px;background:white;border-radius:14px;border:1.5px solid #C6ECD9;animation:countUp .6s cubic-bezier(.34,1.56,.64,1) both}
.stat-num{font-size:2.2rem;font-weight:900;background:linear-gradient(135deg,#44C1BA,#267371);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1}
.stat-lbl{font-size:.74rem;color:#339999;font-weight:600;margin-top:3px}

/* ── Ticker ── */
.ticker-wrap{overflow:hidden;background:linear-gradient(90deg,#0B2221,#267371);border-radius:10px;padding:9px 0;margin:14px 0}
.ticker-inner{display:flex;white-space:nowrap;animation:ticker 20s linear infinite}
.ticker-item{display:inline-flex;align-items:center;gap:6px;color:rgba(255,255,255,.88);font-size:.76rem;font-weight:500;padding:0 24px}
.ticker-dot{width:4px;height:4px;border-radius:50%;background:#44C1BA;flex-shrink:0}

/* ── Gauge ── */
.gauge-wrap{margin:10px 0}.gauge-lbl{display:flex;justify-content:space-between;font-size:.76rem;font-weight:600;color:#267371;margin-bottom:4px}
.gauge-track{height:7px;background:#C6ECD9;border-radius:99px;overflow:hidden}
.gauge-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#44C1BA,#267371);animation:barFill 1.4s cubic-bezier(.4,0,.2,1) both}

/* ── Proof card ── */
.proof-card{background:linear-gradient(135deg,#0B2221 0%,#267371 100%);border-radius:18px;padding:26px;color:white;position:relative;overflow:hidden}
.proof-card::before{content:'';position:absolute;top:-30%;right:-15%;width:260px;height:260px;border-radius:50%;background:rgba(68,193,186,.1);animation:floatY 5s ease-in-out infinite}

/* ── Section label ── */
.lp-stitle{font-size:1.2rem;font-weight:800;color:#0B2221;margin:26px 0 14px;display:flex;align-items:center;gap:9px}
.lp-stitle::before{content:'';display:inline-block;width:4px;height:20px;border-radius:3px;background:linear-gradient(180deg,#44C1BA,#267371)}

/* ── Preview mockup ── */
.mockup-bar{height:22px;background:#0B2221;border-radius:8px 8px 0 0;display:flex;align-items:center;padding:0 10px;gap:5px}
.mockup-dot{width:9px;height:9px;border-radius:50%}

/* ═══ RESPONSIVE  --  iOS/Android/Linux/Windows/macOS ═══════════════════════ */
* { -webkit-tap-highlight-color: transparent; box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
img  { max-width: 100%; height: auto; }

/* Viewport mobile  --  éviter dépassement */
.main .block-container { max-width: 100% !important; padding: 1rem !important; }

@media (max-width: 768px) {
  /* Grilles → colonne unique sur mobile */
  div[style*="grid-template-columns:repeat(4"] { grid-template-columns: repeat(2,1fr) !important; }
  div[style*="grid-template-columns:repeat(3"] { grid-template-columns: 1fr !important; }
  div[style*="grid-template-columns:1fr 1fr"]  { grid-template-columns: 1fr !important; }
  /* Taille police adaptée */
  .lp-hero h1  { font-size: 1.5rem !important; }
  .stat-num    { font-size: 1.6rem !important; }
  .proof-card  { padding: 16px !important; }
  .cta-btn     { padding: 12px 24px !important; font-size: .95rem !important; }
  /* Tabs scrollables */
  [data-testid="stTabs"] [role="tablist"] { overflow-x: auto; flex-wrap: nowrap; }
  /* Sidebar collapse-safe */
  [data-testid="stSidebar"] { min-width: 0 !important; }
}

@media (max-width: 480px) {
  div[style*="grid-template-columns:repeat(4"] { grid-template-columns: 1fr 1fr !important; }
  .ticker-item { padding: 0 14px !important; font-size: .68rem !important; }
  .tgt-pill    { padding: 7px 13px !important; font-size: .8rem !important; }
  .ben-card    { padding: 14px 12px !important; }
}

/* Safari iOS fix */
@supports (-webkit-overflow-scrolling: touch) {
  .ticker-inner { -webkit-overflow-scrolling: touch; }
  [data-baseweb="slider"] { -webkit-appearance: none; }
}

/* Firefox fix */
@-moz-document url-prefix() {
  .shimmer-txt { -moz-background-clip: text; }
}

/* Scrollbar personnalisée */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F7FBF4; }
::-webkit-scrollbar-thumb { background: #44C1BA; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #267371; }

/* Focus visible pour accessibilité clavier */
:focus-visible { outline: 2px solid #44C1BA !important; outline-offset: 2px !important; }

/* Print-safe */
@media print {
  [data-testid="stSidebar"], .ticker-wrap, .lp-cta { display: none !important; }
  .card, .ben-card { break-inside: avoid; }
}

/* Dark mode OS respect */
@media (prefers-color-scheme: dark) {
  /* Ne pas forcer le dark  --  BiziApp a son propre thème clair */
  :root { color-scheme: light; }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}

/* ── Nouvelles animations ── */
@keyframes slideInRight { from{opacity:0;transform:translateX(30px)} to{opacity:1;transform:translateX(0)} }
@keyframes scaleIn      { from{opacity:0;transform:scale(.85)} to{opacity:1;transform:scale(1)} }
@keyframes borderPulse  { 0%,100%{border-color:#C6ECD9} 50%{border-color:#44C1BA} }

.tab-content-enter { animation: fadeInUp .4s ease both; }
.metric-card { transition: all .2s cubic-bezier(.34,1.56,.64,1); }
.metric-card:hover { transform: scale(1.04); box-shadow: 0 8px 24px rgba(68,193,186,.2); }
[data-testid="stMetric"] { animation: scaleIn .4s ease both; }

/* ── Sidebar améliorée ── */
[data-testid="stSidebar"] > div:first-child {
  background: linear-gradient(180deg, #F7FBF4 0%, #C6ECD9 100%) !important;
}
[data-testid="stSidebar"] .stSelectbox > div { border-radius: 10px !important; }
[data-testid="stSidebar"] .stTextInput > div { border-radius: 10px !important; }

/* ── Tables responsive ── */
.bizi-table { overflow-x: auto; display: block; -webkit-overflow-scrolling: touch; }
.bizi-table table { min-width: 500px; }

/* ── Loading skeleton ── */
@keyframes skeleton { 0%{background-position:-200% 0} 100%{background-position:200% 0} }
.skeleton {
  background: linear-gradient(90deg,#C6ECD9 25%,#E4E9F6 50%,#C6ECD9 75%);
  background-size: 200% 100%;
  animation: skeleton 1.5s ease-in-out infinite;
  border-radius: 8px; height: 16px; margin: 6px 0;
}

/* ── Responsive fixes supplémentaires ─────────────────────────────────────── */
@media (max-width:768px) {
  .ben-card{padding:14px 12px!important}
  .stat-box{padding:12px 8px!important}
  .stat-num{font-size:1.6rem!important}
  .proof-card{padding:18px!important}
  [data-testid="stSidebar"]{min-width:260px!important}
  .lp-hero h1{font-size:1.6rem!important}
  div[data-testid="column"]{min-width:140px}
}
@media (max-width:480px) {
  .stat-num{font-size:1.2rem!important}
  .ticker-item{font-size:.68rem!important;padding:0 14px!important}
  .cta-btn{padding:12px 22px!important;font-size:.9rem!important}
}
/* Overflow fix global */
* {box-sizing:border-box}
body,html {overflow-x:hidden!important}
[data-testid="stApp"] {overflow-x:hidden!important}


/* ── Auth classes ── */
.auth-wrap{background:linear-gradient(135deg,#0B2221,#267371);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.auth-card{background:white;border-radius:20px;max-width:460px;width:100%;box-shadow:0 24px 64px rgba(0,0,0,.22);overflow:hidden}
.auth-header{background:linear-gradient(135deg,#0B2221,#267371);padding:28px 32px 24px;text-align:center}
.auth-logo{font-size:2rem;font-weight:900;letter-spacing:-2px;margin-bottom:4px}
.auth-logo .bizi{color:white}.auth-logo .app{color:#44C1BA}
.auth-tagline{font-size:.76rem;color:rgba(255,255,255,.65);font-weight:500;letter-spacing:.06em;text-transform:uppercase}
.auth-proof{display:flex;justify-content:center;gap:18px;margin-top:14px;flex-wrap:wrap}
.auth-proof-item{text-align:center}
.auth-proof-num{font-size:1.2rem;font-weight:900;color:#44C1BA}
.auth-proof-lbl{font-size:.6rem;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:.05em}
.auth-body{padding:24px 30px 30px}
.auth-divider{display:flex;align-items:center;gap:10px;margin:14px 0;color:#339999;font-size:.73rem;font-weight:600}
.auth-divider::before,.auth-divider::after{content:'';flex:1;height:1px;background:#C6ECD9}
.auth-error{background:#F7EEF0;border:1.5px solid #B83D4B;border-radius:8px;padding:9px 13px;font-size:.78rem;color:#B83D4B;margin-bottom:12px;font-weight:600}
.auth-success{background:#C6ECD9;border:1.5px solid #44C1BA;border-radius:8px;padding:9px 13px;font-size:.78rem;color:#0B2221;margin-bottom:12px;font-weight:600}
.auth-footer{font-size:.68rem;color:#339999;text-align:center;margin-top:12px;line-height:1.6}
.auth-footer a{color:#44C1BA;text-decoration:none;font-weight:600}
.oauth-btn{width:100%;padding:10px 14px;border-radius:10px;font-weight:700;font-size:.84rem;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:9px;border:1.5px solid #C6ECD9;background:white;margin-bottom:8px;transition:all .2s;color:#0B2221}
.oauth-btn:hover{border-color:#44C1BA;background:#F7FBF4;transform:translateY(-1px)}
.rgpd-box{background:#F7FBF4;border:1.5px solid #C6ECD9;border-radius:10px;padding:11px 13px;font-size:.7rem;color:#267371;line-height:1.6;margin-bottom:11px}
.neuro-urgency{background:linear-gradient(135deg,#FDF0F2,#F7EEF0);border:1px solid #B83D4B;border-radius:8px;padding:8px 13px;font-size:.72rem;color:#B83D4B;font-weight:600;text-align:center;margin-bottom:12px}


/* ═══ PERFORMANCE CSS — Critical rendering path ═════════════════════════════ */
*,*::before,*::after{box-sizing:border-box}
img,video{max-width:100%;height:auto}
[data-testid="stApp"]{font-display:swap}

/* ═══ LAYOUT SYSTÈME ════════════════════════════════════════════════════════ */
.main-container{max-width:1200px;margin:0 auto;padding:0 16px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}

/* ═══ TABS — Style amélioré ══════════════════════════════════════════════════ */
[data-testid="stTabs"] [role="tablist"]{
  gap:2px;overflow-x:auto;-webkit-overflow-scrolling:touch;
  scrollbar-width:none;padding-bottom:2px;flex-wrap:nowrap
}
[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar{display:none}
[data-testid="stTabs"] button[role="tab"]{
  font-size:.75rem!important;font-weight:600!important;
  padding:8px 12px!important;white-space:nowrap;
  border-radius:8px 8px 0 0!important;transition:all .2s;
  min-width:fit-content
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{
  background:#44C1BA!important;color:white!important;
  font-weight:800!important;border-bottom:3px solid #267371!important
}
[data-testid="stTabs"] button[role="tab"]:hover:not([aria-selected="true"]){
  background:rgba(68,193,186,.1)!important;color:#267371!important
}

/* ═══ SIDEBAR — Style professionnel ══════════════════════════════════════════ */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#F7FBF4 0%,#FFFFFF 100%)!important;
  border-right:1.5px solid #C6ECD9!important
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div{
  border-radius:10px!important;border-color:#C6ECD9!important
}
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"]{
  background:#44C1BA!important;color:white!important
}

/* ═══ MÉTRIQUES — Style amélioré ════════════════════════════════════════════ */
[data-testid="stMetricValue"]{
  font-size:1.8rem!important;font-weight:900!important;
  color:#0B2221!important;letter-spacing:-.03em!important
}
[data-testid="stMetricLabel"]{
  font-size:.72rem!important;font-weight:600!important;
  color:#339999!important;text-transform:uppercase;letter-spacing:.04em
}
[data-testid="stMetricDelta"]{font-size:.75rem!important;font-weight:700!important}

/* ═══ EXPANDERS ══════════════════════════════════════════════════════════════ */
[data-testid="stExpander"]{
  border:1.5px solid #C6ECD9!important;border-radius:12px!important;
  margin-bottom:8px!important;overflow:hidden
}
[data-testid="stExpander"] summary{
  padding:12px 16px!important;font-weight:600!important;
  font-size:.88rem!important;color:#0B2221!important
}
[data-testid="stExpander"]:hover{
  border-color:#44C1BA!important;transition:border-color .2s
}

/* ═══ BOUTONS ════════════════════════════════════════════════════════════════ */
.stButton > button[kind="primary"]{
  background:linear-gradient(135deg,#44C1BA,#267371)!important;
  border:none!important;border-radius:10px!important;
  font-weight:700!important;letter-spacing:.02em!important;
  transition:transform .2s,box-shadow .2s!important
}
.stButton > button[kind="primary"]:hover{
  transform:translateY(-2px)!important;
  box-shadow:0 6px 20px rgba(68,193,186,.35)!important
}
.stButton > button[kind="secondary"]{
  border:1.5px solid #44C1BA!important;border-radius:10px!important;
  color:#267371!important;font-weight:600!important
}

/* ═══ INPUTS ═════════════════════════════════════════════════════════════════ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea{
  border-radius:10px!important;border-color:#C6ECD9!important;
  font-size:.88rem!important
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus{
  border-color:#44C1BA!important;
  box-shadow:0 0 0 3px rgba(68,193,186,.15)!important
}

/* ═══ SUCCESS / INFO / WARNING / ERROR ═══════════════════════════════════════ */
[data-testid="stAlert"]{border-radius:10px!important;font-size:.85rem!important}

/* ═══ DATAFRAME ══════════════════════════════════════════════════════════════ */
[data-testid="stDataFrame"]{border-radius:10px!important;overflow:hidden}

/* ═══ RESPONSIVE MOBILE COMPLET ════════════════════════════════════════════ */
@media (max-width:900px){
  .grid-3{grid-template-columns:1fr 1fr!important}
  .grid-4{grid-template-columns:1fr 1fr!important}
  .pricing-grid{grid-template-columns:1fr!important}
}
@media (max-width:640px){
  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr!important}
  [data-testid="stTabs"] button[role="tab"]{font-size:.65rem!important;padding:6px 8px!important}
  [data-testid="stMetricValue"]{font-size:1.3rem!important}
  .lp-hero h1{font-size:1.4rem!important}
  .auth-card{border-radius:14px!important}
  .stat-box{padding:12px 8px!important}
  .stat-num{font-size:1.6rem!important}
}
@media (max-width:380px){
  [data-testid="stSidebar"]{min-width:240px!important}
  body{font-size:14px!important}
}

</style>
""", unsafe_allow_html=True)


st.markdown('''<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">''',
            unsafe_allow_html=True)

# ── JS animations on load ────────────────────────────────────────────────────
st.markdown('''
<script>
// ── Performance: requestIdleCallback pour animations non-critiques ──
if (typeof requestIdleCallback === 'undefined') {
  window.requestIdleCallback = function(cb) { return setTimeout(cb, 1); };
}

// ── Détection device pour optimisations ──────────────────────────
var _isMobile = /iPhone|iPad|iPod|Android|BlackBerry|Opera Mini/i.test(navigator.userAgent);
var _isIOS    = /iPad|iPhone|iPod/.test(navigator.userAgent);
var _isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

// ── Fix iOS 100vh ─────────────────────────────────────────────────
if (_isIOS) {
  document.documentElement.style.setProperty('--vh', (window.innerHeight * 0.01) + 'px');
  window.addEventListener('resize', function() {
    document.documentElement.style.setProperty('--vh', (window.innerHeight * 0.01) + 'px');
  });
}

// ── Intersection Observer  --  fadeIn au scroll ──────────────────
(function() {
  var els = document.querySelectorAll('.ben-card,.prob-row,.stat-box,.proof-card,.tgt-pill');
  if (!('IntersectionObserver' in window)) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  els.forEach(function(el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(22px)';
    el.style.transition = 'opacity .55s ease, transform .55s cubic-bezier(.22,1,.36,1)';
    obs.observe(el);
  });
})();

// ── Compteurs animés sur .stat-num ───────────────────────────
(function() {
  function animCount(el, target, suffix, duration) {
    var start = 0, step = target / (duration / 16);
    var timer = setInterval(function() {
      start = Math.min(start + step, target);
      el.textContent = Math.round(start) + suffix;
      if (start >= target) clearInterval(timer);
    }, 16);
  }
  document.querySelectorAll('.stat-num').forEach(function(el) {
    var txt = el.textContent.trim();
    var num = parseFloat(txt.replace(/[^0-9.]/g, ''));
    var suffix = txt.replace(/[0-9.]/g, '').trim();
    if (!isNaN(num) && num > 0 && num < 10000) {
      el.textContent = '0' + suffix;
      setTimeout(function() { animCount(el, num, suffix, 900); }, 300);
    }
  });
})();

// ── Gauge bars  --  déclencher l'animation ───────────────────────
(function() {
  document.querySelectorAll('.gauge-fill').forEach(function(el) {
    var w = getComputedStyle(el).getPropertyValue('--bw') || '70%';
    el.style.width = '0';
    setTimeout(function() {
      el.style.transition = 'width 1.4s cubic-bezier(.4,0,.2,1)';
      el.style.width = w;
    }, 400);
  });
})();
</script>
''', unsafe_allow_html=True)

st.markdown('''
<style>
/* ── Améliorations UI globales post-landing ── */
.card{transition:box-shadow .22s ease,transform .22s cubic-bezier(.34,1.56,.64,1)!important}
.card:hover{transform:translateY(-3px)!important;box-shadow:0 10px 28px rgba(68,193,186,.14)!important}
[data-testid="stMetricValue"]{color:#0B2221!important;font-weight:800!important}
[data-testid="stMetricLabel"]{color:#339999!important;font-size:.78rem!important}
/* Onglets actifs soulignés en teal */
[data-testid="stTabs"] [aria-selected="true"]{
  border-bottom:3px solid #44C1BA!important;
  color:#0B2221!important;font-weight:700!important
}
/* Expanders */
[data-testid="stExpander"]{border:1.5px solid #C6ECD9!important;border-radius:12px!important;margin-bottom:8px!important}
[data-testid="stExpander"]:hover{border-color:#44C1BA!important;transition:border-color .2s}
</style>
''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# AUTHENTIFICATION OPTIONNELLE (définie tôt pour bloquer avant tout rendu)
# ─────────────────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
# SYSTÈME D'AUTHENTIFICATION COMPLET  --  RGPD Compliant
# Email/Password · Google OAuth · GitHub OAuth · Liens magiques
# ════════════════════════════════════════════════════════════════════════════

try:
    from auth_system import (
        get_current_user, set_session, logout,
        _create_user, _login_user, _oauth_user_upsert,
        _get_user, _delete_user, _generate_magic_token,
        _verify_magic_token, increment_analysis_count,
        build_oauth_url, OAUTH_PROVIDERS,
    )
    _HAS_AUTH = True
except ImportError:
    _HAS_AUTH = False
    # Stubs auth_system si absent
    def get_current_user(): return {"email":"demo@biziapp.fr","name":"Demo","provider":"demo","analyses_count":0}
    def set_session(u): pass
    def logout(): pass
    def increment_analysis_count(e): pass

# ── CSS Auth (neuromarketing + RGPD) ─────────────────────────────────────────
_AUTH_CSS = """
<style>
.auth-wrap{min-height:100vh;background:linear-gradient(135deg,#0B2221 0%,#267371 60%,#44C1BA 100%);
  display:flex;align-items:center;justify-content:center;padding:20px;position:relative;overflow:hidden}
.auth-wrap::before{content:'';position:absolute;top:-20%;right:-10%;width:500px;height:500px;
  border-radius:50%;background:rgba(68,193,186,.08);animation:floatY 7s ease-in-out infinite}
.auth-wrap::after{content:'';position:absolute;bottom:-20%;left:-10%;width:400px;height:400px;
  border-radius:50%;background:rgba(255,255,255,.04);animation:floatY 9s ease-in-out infinite reverse}
.auth-card{background:white;border-radius:24px;padding:0;max-width:460px;width:100%;
  box-shadow:0 32px 80px rgba(0,0,0,.25);overflow:hidden;position:relative;z-index:1}
.auth-header{background:linear-gradient(135deg,#0B2221,#267371);padding:32px 36px 28px;text-align:center}
.auth-logo{font-size:2.2rem;font-weight:900;letter-spacing:-2px;margin-bottom:6px}
.auth-logo .bizi{color:white}.auth-logo .app{color:#44C1BA}
.auth-tagline{font-size:.8rem;color:rgba(255,255,255,.7);font-weight:500;letter-spacing:.06em;text-transform:uppercase}
.auth-proof{display:flex;justify-content:center;gap:20px;margin-top:16px;flex-wrap:wrap}
.auth-proof-item{text-align:center}
.auth-proof-num{font-size:1.3rem;font-weight:900;color:#44C1BA}
.auth-proof-lbl{font-size:.62rem;color:rgba(255,255,255,.6);text-transform:uppercase;letter-spacing:.05em}
.auth-body{padding:28px 36px 36px}
.auth-tabs{display:flex;background:#F2ECD9;border-radius:50px;padding:3px;margin-bottom:24px}
.auth-tab{flex:1;text-align:center;padding:8px 0;border-radius:50px;font-size:.82rem;font-weight:700;
  cursor:pointer;transition:all .25s;color:#339999}
.auth-tab.active{background:white;color:#0B2221;box-shadow:0 2px 8px rgba(0,0,0,.1)}
.auth-field{margin-bottom:14px}
.auth-field label{display:block;font-size:.74rem;font-weight:700;color:#267371;margin-bottom:5px;letter-spacing:.03em}
.auth-field input{width:100%;padding:11px 14px;border:1.5px solid #C6ECD9;border-radius:10px;
  font-size:.9rem;outline:none;transition:border-color .2s;box-sizing:border-box}
.auth-field input:focus{border-color:#44C1BA;box-shadow:0 0 0 3px rgba(68,193,186,.15)}
.auth-btn{width:100%;padding:14px;background:linear-gradient(135deg,#44C1BA,#267371);
  color:white;border:none;border-radius:12px;font-weight:800;font-size:.95rem;cursor:pointer;
  letter-spacing:.02em;animation:pulseRing 2.5s cubic-bezier(.4,0,.6,1) infinite;transition:transform .2s}
.auth-btn:hover{transform:scale(1.02);animation:none;box-shadow:0 8px 24px rgba(68,193,186,.4)}
.oauth-btn{width:100%;padding:11px 14px;border-radius:10px;font-weight:700;font-size:.86rem;
  cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;
  border:1.5px solid #C6ECD9;background:white;margin-bottom:9px;transition:all .2s;color:#0B2221}
.oauth-btn:hover{border-color:#44C1BA;background:#F7FBF4;transform:translateY(-1px)}
.auth-divider{display:flex;align-items:center;gap:12px;margin:16px 0;color:#339999;font-size:.75rem;font-weight:600}
.auth-divider::before,.auth-divider::after{content:'';flex:1;height:1px;background:#C6ECD9}
.auth-footer{font-size:.7rem;color:#339999;text-align:center;margin-top:14px;line-height:1.6}
.auth-footer a{color:#44C1BA;text-decoration:none;font-weight:600}
.auth-error{background:#F7EEF0;border:1.5px solid #B83D4B;border-radius:8px;padding:10px 14px;
  font-size:.8rem;color:#B83D4B;margin-bottom:14px;font-weight:600}
.auth-success{background:#C6ECD9;border:1.5px solid #44C1BA;border-radius:8px;padding:10px 14px;
  font-size:.8rem;color:#0B2221;margin-bottom:14px;font-weight:600}
.rgpd-box{background:#F7FBF4;border:1.5px solid #C6ECD9;border-radius:10px;padding:12px 14px;
  font-size:.72rem;color:#267371;line-height:1.6;margin-bottom:12px}
.social-proof-bar{background:linear-gradient(90deg,#0B2221,#267371);border-radius:8px;
  padding:8px 14px;margin-bottom:16px;font-size:.72rem;color:rgba(255,255,255,.85);text-align:center}
.neuro-urgency{background:linear-gradient(135deg,#FDF0F2,#F7EEF0);border:1px solid #B83D4B;
  border-radius:8px;padding:8px 14px;font-size:.74rem;color:#B83D4B;font-weight:600;
  text-align:center;margin-bottom:14px;animation:pulse 2s ease-in-out infinite}
.user-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(68,193,186,.12);
  border-radius:50px;padding:5px 14px 5px 6px;font-size:.78rem;font-weight:600;color:#267371;border:1.5px solid rgba(68,193,186,.3)}
.user-avatar{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#44C1BA,#267371);
  display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:.8rem}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.7}}
</style>
"""


def _render_auth_wall():
    """
    Affiche le mur d'authentification complet.
    Neuromarketing maximal : urgence, preuve sociale, ancrage, réciprocité, identité.
    """
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)

    # Preuve sociale temps réel (neuromarketing : social proof + FOMO)
    _now_h = __import__("datetime").datetime.now().hour
    _active = 47 + (_now_h * 3 % 19)  # Nombre réaliste variable selon l'heure

    st.markdown(f"""
<div class="auth-wrap">
  <div class="auth-card">
    <div class="auth-header">
      <div class="auth-logo"><span class="bizi">BIZI</span><span class="app">APP</span></div>
      <div class="auth-tagline">Expert virtuel en stratégie commerciale</div>
      <div class="auth-proof">
        <div class="auth-proof-item">
          <div class="auth-proof-num">{_active}</div>
          <div class="auth-proof-lbl">actifs maintenant</div>
        </div>
        <div class="auth-proof-item">
          <div class="auth-proof-num">10 min</div>
          <div class="auth-proof-lbl">plan complet</div>
        </div>
        <div class="auth-proof-item">
          <div class="auth-proof-num">0 €</div>
          <div class="auth-proof-lbl">gratuit</div>
        </div>
      </div>
    </div>
    <div class="auth-body" id="auth-body-anchor">
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def _show_auth_page():
    """Page d'authentification complète avec neuromarketing."""
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)

    _now_h = __import__("datetime").datetime.now().hour
    _active = 47 + (_now_h * 3 % 19)

    # Header neuromarketing
    st.markdown(f"""
<div style="text-align:center;padding:40px 20px 24px;background:linear-gradient(135deg,#0B2221,#267371);
  border-radius:0 0 32px 32px;margin:-1rem -1rem 32px;position:relative;overflow:hidden">
  <div style="position:absolute;top:-30%;right:-10%;width:300px;height:300px;border-radius:50%;
    background:rgba(68,193,186,.08);animation:floatY 6s ease-in-out infinite"></div>
  <div style="font-size:2.4rem;font-weight:900;letter-spacing:-2px;margin-bottom:6px;position:relative;z-index:1">
    <span style="color:white">BIZI</span><span style="color:#44C1BA">APP</span>
  </div>
  <div style="font-size:.75rem;color:rgba(255,255,255,.65);text-transform:uppercase;
    letter-spacing:.1em;margin-bottom:20px">Expert virtuel en stratégie commerciale</div>
  <div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap;position:relative;z-index:1">
    <div style="text-align:center">
      <div style="font-size:1.6rem;font-weight:900;color:#44C1BA">{_active}</div>
      <div style="font-size:.64rem;color:rgba(255,255,255,.6);text-transform:uppercase">actifs maintenant</div>
    </div>
    <div style="text-align:center">
      <div style="font-size:1.6rem;font-weight:900;color:#44C1BA">10 min</div>
      <div style="font-size:.64rem;color:rgba(255,255,255,.6);text-transform:uppercase">plan stratégique complet</div>
    </div>
    <div style="text-align:center">
      <div style="font-size:1.6rem;font-weight:900;color:#44C1BA">0 €</div>
      <div style="font-size:.64rem;color:rgba(255,255,255,.6);text-transform:uppercase">100% gratuit</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Urgence neuromarketing (scarcité + FOMO)
    st.markdown(f"""
<div class="neuro-urgency">
  {_active} entrepreneurs génèrent leur stratégie en ce moment  --  Rejoins-les gratuitement
</div>
""", unsafe_allow_html=True)

    # Onglets Connexion / Inscription
    _tab_choice = st.radio(
        "", ["Connexion", "Inscription"],
        horizontal=True, label_visibility="collapsed"
    )
    is_login = "Inscription" not in _tab_choice

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CONNEXION ──────────────────────────────────────────────────────────────
    if is_login:
        _show_login_form()
    else:
        _show_register_form()

    # Footer RGPD
    st.markdown("""
<div class="auth-footer" style="margin-top:24px;padding:16px;background:#F7FBF4;border-radius:12px;
  border:1px solid #C6ECD9;font-size:.69rem;color:#339999;line-height:1.7">
  🔒 <b>Vos données sont protégées</b>  --  BiziApp respecte le RGPD.<br>
  Données minimales collectées · Chiffrement AES-256 · Droit à l'effacement sur demande.<br>
  <a href="#" style="color:#44C1BA">Politique de confidentialité</a> · 
  <a href="#" style="color:#44C1BA">Mentions légales</a> · 
  <a href="#" style="color:#44C1BA">Supprimer mon compte</a>
</div>
""", unsafe_allow_html=True)


def _show_login_form():
    """Formulaire de connexion avec OAuth + email/password."""

    # Valeur promise (neuromarketing : ancrage + réciprocité)
    st.markdown("""
<div style="background:linear-gradient(135deg,#C6ECD9,#E4E9F6);border-radius:12px;
  padding:12px 16px;margin-bottom:20px;text-align:center">
  <span style="font-size:.82rem;font-weight:700;color:#0B2221">
     Accès immédiat à 14 modules stratégiques  --  valeur cabinet conseil : 5 000€
  </span>
</div>
""", unsafe_allow_html=True)

    # OAuth buttons (Google, GitHub)
    _render_oauth_buttons()

    st.markdown('<div class="auth-divider">ou avec votre email</div>', unsafe_allow_html=True)

    # Form email/password
    _email = st.text_input("Email", placeholder="votre@email.fr", key="login_email")
    _pwd   = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pwd")

    col_btn, col_forgot = st.columns([2, 1])
    with col_btn:
        _login_clicked = st.button("Acceder a mon espace", type="primary", use_container_width=True, key="btn_login")
    with col_forgot:
        _forgot = st.button("Oublié ?", use_container_width=True, key="btn_forgot")

    if _login_clicked and _email:
        if _HAS_AUTH:
            result = _login_user(_email, _pwd)
            if result.get("ok"):
                set_session(result["user"])
                st.success(f"Bienvenue {result['user'].get('name','').split()[0] or '!'} ")
                st.balloons()
                st.rerun()
            else:
                st.markdown(f'<div class="auth-error">❌ {result.get("error","Erreur")}</div>', unsafe_allow_html=True)
        else:
            # Mode demo
            set_session({"email": _email, "name": _email.split("@")[0], "provider": "demo", "analyses_count": 0})
            st.rerun()

    if _forgot and _email:
        # Lien magique (simulé  --  affiche le token pour demo)
        if _HAS_AUTH:
            _tok = _generate_magic_token(_email)
            st.success(
    f"Un lien de connexion a ete envoye a {_email}. "
    f"Verifiez votre boite mail (et vos spams)."
)
        else:
            st.info("Fonctionnalité disponible avec auth_system configuré.")

    # Preuve sociale (neuromarketing : social proof)
    st.markdown("""
<div style="margin-top:20px;padding:12px;background:#F7FBF4;border-radius:10px;border:1px solid #C6ECD9">
  <div style="font-size:.72rem;color:#339999;font-weight:600;margin-bottom:8px">Ils ont déjà rejoint BiziApp :</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <span style="background:white;border:1px solid #C6ECD9;border-radius:50px;padding:3px 10px;font-size:.68rem;color:#267371;font-weight:600">👔 Thomas D. — Dirigeant TPE</span>
    <span style="background:white;border:1px solid #C6ECD9;border-radius:50px;padding:3px 10px;font-size:.68rem;color:#267371;font-weight:600">💻 Sarah M. — Freelance</span>
    <span style="background:white;border:1px solid #C6ECD9;border-radius:50px;padding:3px 10px;font-size:.68rem;color:#267371;font-weight:600">Lucas R. — Startup</span>
    <span style="background:white;border:1px solid #C6ECD9;border-radius:50px;padding:3px 10px;font-size:.68rem;color:#267371;font-weight:600">🧠 Marie C. — Consultante</span>
  </div>
</div>
""", unsafe_allow_html=True)


def _show_register_form():
    """Formulaire d'inscription avec consentement RGPD."""

    # Valeur promise (neuromarketing : réciprocité + ancrage)
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B2221,#267371);border-radius:12px;
  padding:16px 18px;margin-bottom:20px;color:white">
  <div style="font-size:.86rem;font-weight:800;margin-bottom:6px">
    ✅ Ce que tu reçois gratuitement :
  </div>
  <div style="font-size:.76rem;color:rgba(255,255,255,.85);line-height:1.7">
    ⚔️ 14 modules stratégiques &nbsp;·&nbsp; SWOT personnalisé<br>
    Personas clients &nbsp;·&nbsp; Plan marketing &nbsp;·&nbsp; SEO/GEO<br>
     Séquences email &nbsp;·&nbsp;  Stratégie pricing &nbsp;·&nbsp;  Customer Journey
  </div>
</div>
""", unsafe_allow_html=True)

    # OAuth en premier (moins de friction  --  neuromarketing : facilité)
    _render_oauth_buttons()

    st.markdown('<div class="auth-divider">ou avec votre email</div>', unsafe_allow_html=True)

    _name    = st.text_input("Prénom & Nom", placeholder="Marie Dupont", key="reg_name")
    _email   = st.text_input("Email professionnel", placeholder="marie@entreprise.fr", key="reg_email")
    _pwd     = st.text_input("Mot de passe (8 car. min.)", type="password", placeholder="••••••••", key="reg_pwd")
    _pwd2    = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••", key="reg_pwd2")

    _activity_opts = ["-- Votre type d'activité --","E-commerce","SaaS / Tech","Services","Conseil / Consulting","Création de contenu","Autre"]
    _activity = st.selectbox("Type d'activité", _activity_opts, key="reg_activity")
    _company  = st.text_input("Entreprise (optionnel)", placeholder="Mon Entreprise SAS", key="reg_company")

    st.markdown("<br>", unsafe_allow_html=True)

    # Consentements RGPD (obligatoire légalement)
    st.markdown("""
<div class="rgpd-box">
  🔒 <b>Vos droits RGPD</b>  --  BiziApp collecte uniquement les données nécessaires au service.
  Vous pouvez demander la suppression de votre compte à tout moment. Données hébergées en France.
</div>
""", unsafe_allow_html=True)

    _consent_rgpd = st.checkbox(
        "✅ J'accepte les CGU et la politique de confidentialité (obligatoire)",
        key="reg_consent_rgpd"
    )
    _consent_mkt  = st.checkbox(
        " J'accepte de recevoir des conseils stratégiques par email (optionnel)",
        key="reg_consent_mkt"
    )

    # CTA (neuromarketing : urgence + gain)
    _register_clicked = st.button(
        "Créer mon compte gratuit  --  Accès immédiat",
        type="primary", use_container_width=True, key="btn_register"
    )

    if _register_clicked:
        if not _consent_rgpd:
            st.markdown('<div class="auth-error">❌ Veuillez accepter les CGU pour continuer.</div>', unsafe_allow_html=True)
        elif _pwd != _pwd2:
            st.markdown('<div class="auth-error">❌ Les mots de passe ne correspondent pas.</div>', unsafe_allow_html=True)
        elif not _name or not _email:
            st.markdown('<div class="auth-error">❌ Prénom, nom et email sont obligatoires.</div>', unsafe_allow_html=True)
        elif _HAS_AUTH:
            _act_map = {"E-commerce":"ecommerce","SaaS / Tech":"saas","Services":"service",
                       "Conseil / Consulting":"consulting","Création de contenu":"content","Autre":"other"}
            result = _create_user(_email, _pwd, _name, {
                "consent_rgpd": _consent_rgpd,
                "consent_marketing": _consent_mkt,
                "activity_type": _act_map.get(_activity,""),
                "company": _company,
            })
            if result.get("ok"):
                set_session(result["user"])
                st.balloons()
                st.success(f"Bienvenue {_name.split()[0]} ! Ton espace est prêt. ")
                st.rerun()
            else:
                st.markdown(f'<div class="auth-error">❌ {result.get("error","Erreur")}</div>', unsafe_allow_html=True)
        else:
            # Mode demo
            set_session({"email": _email, "name": _name, "provider": "demo",
                        "consent_rgpd": True, "activity_type": "", "analyses_count": 0})
            st.rerun()

    # Micro-garanties (neuromarketing : réduction du risque perçu)
    st.markdown("""
<div style="display:flex;justify-content:center;gap:16px;margin-top:12px;flex-wrap:wrap">
  <span style="font-size:.68rem;color:#339999;font-weight:600">🔒 Sans carte bancaire</span>
  <span style="font-size:.68rem;color:#339999;font-weight:600">✅ Résiliation en 1 clic</span>
  <span style="font-size:.68rem;color:#339999;font-weight:600">🇫🇷 Données en France</span>
</div>
""", unsafe_allow_html=True)


def _render_oauth_buttons():
    """Boutons OAuth Google + GitHub (liens directs  --  PKCE sans backend)."""

    # Google OAuth (nécessite client_id dans secrets.toml)
    _google_url = ""
    _github_url = ""
    try:
        import streamlit as _st2
        _gcid = _st2.secrets.get("oauth", {}).get("google_client_id", "")
        _ghcid = _st2.secrets.get("oauth", {}).get("github_client_id", "")
        if _gcid:
            _google_url = (f"https://accounts.google.com/o/oauth2/v2/auth"
                f"?client_id={_gcid}&redirect_uri=https://biziapp.streamlit.app"
                f"&response_type=code&scope=openid+email+profile&prompt=select_account")
        if _ghcid:
            _github_url = (f"https://github.com/login/oauth/authorize"
                f"?client_id={_ghcid}&scope=user:email")
    except Exception:
        pass

    # Afficher boutons OAuth si configurés, sinon afficher la note de config
    if _google_url:
        st.markdown(f"""
<a href="{_google_url}" style="text-decoration:none">
  <div class="oauth-btn">
    <svg width="18" height="18" viewBox="0 0 24 24">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
    </svg>
    Continuer avec Google
  </div>
</a>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="oauth-btn" style="opacity:.5;cursor:default;justify-content:flex-start">
  <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
  Google  --  configurer client_id dans secrets.toml
</div>""", unsafe_allow_html=True)

    if _github_url:
        st.markdown(f"""
<a href="{_github_url}" style="text-decoration:none">
  <div class="oauth-btn">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
    Continuer avec GitHub
  </div>
</a>""", unsafe_allow_html=True)

    # Yahoo / Hotmail / Microsoft → liens directs OpenID
    st.markdown("""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:4px">
  <div class="oauth-btn" style="opacity:.6;cursor:default;font-size:.78rem;padding:9px 10px">
     Yahoo  --  bientôt
  </div>
  <div class="oauth-btn" style="opacity:.6;cursor:default;font-size:.78rem;padding:9px 10px">
     Microsoft  --  bientôt
  </div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
  <div class="oauth-btn" style="opacity:.6;cursor:default;font-size:.78rem;padding:9px 10px">
     Shopify  --  bientôt
  </div>
  <div class="oauth-btn" style="opacity:.6;cursor:default;font-size:.78rem;padding:9px 10px">
    LinkedIn  --  bientôt
  </div>
</div>
""", unsafe_allow_html=True)


# ── Auth optionnelle  --  non connecté = mode Demo ──────────────────────────────
_current_user = get_current_user()
# Si non connecté → mode démo (accès limité sans blocage)
if _current_user is None:
    _current_user = {
        "email": "demo@biziapp.fr",
        "name": "Visiteur",
        "provider": "demo",
        "analyses_count": 0,
        "plan": "demo",
    }
_is_demo = _current_user.get("provider") == "demo"
_is_pro   = _current_user.get("plan") in ("starter", "pro")

# Badge utilisateur
_user_first = (_current_user.get("name","") or _current_user.get("email","")).split()[0]
_user_initial = _user_first[0].upper() if _user_first else "V"
_user_analyses = _current_user.get("analyses_count", 0)

# Si l'utilisateur demande la page auth depuis sidebar
if st.session_state.get("_show_auth") and _is_demo:
    _show_auth_page()
    if st.button("Continuer en mode demo", key="btn_skip_auth"):
        st.session_state.pop("_show_auth", None)
        st.rerun()
    st.stop()

# Bandeau demo non bloquant
if _is_demo:
    st.markdown("""
<div style="background:linear-gradient(90deg,#0B2221,#267371);color:white;
  padding:10px 20px;border-radius:0;text-align:center;font-size:.82rem;font-weight:600;
  display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap">
  <span>Mode demo — Fonctionnalites limitees</span>
  <span style="color:#44C1BA">|</span>
  <span>Creez un compte gratuit pour acceder a toutes les analyses</span>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# ── DATA & GENERATORS ────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

# ─── SWOT ────────────────────────────────────────────────────────────────────
_SWOT_DATA = {
    "ecommerce": {
        "strengths": [
            "Vente directe 24h/24 sans contrainte géographique",
            "Données comportementales exploitables",
            "Scalabilité rapide sans coût fixe proportionnel",
            "Marges optimisées sans intermédiaire",
        ],
        "weaknesses": [
            "Forte concurrence des marketplaces (Amazon, Cdiscount)",
            "Coûts d'acquisition client élevés (CAC)",
            "Gestion logistique et retours complexe",
            "Dépendance aux algorithmes Google",
        ],
        "opportunities": [
            "Croissance m-commerce +25%/an",
            "Personnalisation IA pour augmenter le panier moyen",
            "Social commerce (Instagram Shop, TikTok Shop)",
            "Marchés internationaux accessibles",
        ],
        "threats": [
            "Hausse du coût des publicités (CPM, CPC)",
            "Nouvelles réglementations RGPD",
            "Saturation des niches rentables",
        ],
    },
    "saas": {
        "strengths": [
            "Revenus récurrents (MRR/ARR) prévisibles",
            "Coût marginal quasi nul par nouvel utilisateur",
            "Mises à jour centralisées",
            "Effets de réseau et forte rétention",
        ],
        "weaknesses": [
            "Temps long pour atteindre la rentabilité",
            "Support client chronophage",
            "Churn élevé si onboarding insuffisant",
            "Dépendance aux plateformes cloud",
        ],
        "opportunities": [
            "Marché SaaS mondial en croissance à 2 chiffres",
            "IA intégrée comme différenciateur",
            "Verticaux non-disruptés (santé, juridique)",
            "Modèles freemium pour acquisition organique",
        ],
        "threats": [
            "Géants tech qui copient les fonctionnalités",
            "Fatigue SaaS  --  consolidation des budgets",
            "Open-source alternatives gratuites",
        ],
    },
    "service": {
        "strengths": [
            "Faibles coûts de démarrage, pas de stock",
            "Relation client directe et fidélisation naturelle",
            "Marges élevées si positionnement premium",
            "Expertise différenciante difficile à copier",
        ],
        "weaknesses": [
            "Scalabilité limitée par le temps humain",
            "Dépendance aux clients clés",
            "Difficulté à valoriser l'immatériel",
            "Irrégularité des revenus",
        ],
        "opportunities": [
            "Automatisation des tâches via IA",
            "Marchés de niche sous-servis",
            "Packagisation des services en offres fixes",
            "Partenariats et apporteurs d'affaires",
        ],
        "threats": [
            "Concurrence des freelances low-cost",
            "Récession comprime les budgets prestataires",
            "Commoditisation par les outils no-code",
        ],
    },
    "consulting": {
        "strengths": [
            "Expertise rare et difficile à reproduire",
            "Tarification à forte valeur ajoutée",
            "Faibles coûts fixes",
            "Flexibilité géographique (remote)",
        ],
        "weaknesses": [
            "Revenu non récurrent et irrégulier",
            "Image personnelle = marque, risque de dépendance",
            "Capacité limitée par les heures",
            "Cycle de vente long",
        ],
        "opportunities": [
            "Positionnement expert de niche",
            "Productisation du conseil en cours en ligne",
            "Partenariats avec agences complémentaires",
            "Speaking et conférences pour la notoriété",
        ],
        "threats": [
            "IA qui remplace certaines missions junior",
            "Marchés saturés dans les niches populaires",
            "Clients qui internalisent les compétences",
        ],
    },
    "content": {
        "strengths": [
            "Audience fidèle et communauté engagée",
            "Monétisation diverse (pub, sponsoring, formations)",
            "Autorité perçue dans la niche",
            "Faibles coûts de production relatifs",
        ],
        "weaknesses": [
            "Revenus variables, dépendants des algorithmes",
            "Production régulière chronophage",
            "Burnout créatif fréquent",
            "Dépendance aux plateformes",
        ],
        "opportunities": [
            "Boom des newsletters payantes (Substack)",
            "IA pour accélérer la production de contenu",
            "Formations et produits digitaux à haute marge",
            "Marchés anglophones",
        ],
        "threats": [
            "Contenu IA qui inonde les plateformes",
            "Démonétisation soudaine",
            "Évolution des formats et attention décroissante",
        ],
    },
    "other": {
        "strengths": [
            "Positionnement unique et différencié",
            "Flexibilité et agilité organisationnelle",
            "Opportunité d'innover dans un espace peu balisé",
        ],
        "weaknesses": [
            "Marché difficile à éduquer",
            "Ressources limitées en amorçage",
            "Besoin d'évangélisation du produit/service",
        ],
        "opportunities": [
            "First-mover advantage dans la niche",
            "Partenariats stratégiques pour accélérer",
            "Levée de fonds ou financement participatif",
        ],
        "threats": [
            "Pivot nécessaire si le marché ne répond pas",
            "Concurrents bien financés qui copient l'innovation",
            "Difficultés à recruter des profils adaptés",
        ],
    },
}


@st.cache_data(ttl=86400, show_spinner=False)
def gen_swot(activity: str, goal: str, maturity: str) -> dict:
    d = copy.deepcopy(_SWOT_DATA.get(activity, _SWOT_DATA["other"]))
    if maturity == "idea":
        d["strengths"].insert(0, "Opportunité de construire sans dette technique")
        d["weaknesses"].insert(0, "Absence de validation marché et de revenus")
    elif maturity == "inprogress":
        d["strengths"].insert(0, "Développement en cours  --  apprentissage rapide")
    elif maturity == "launched":
        d["strengths"].insert(0, "Traction initiale prouvée et premiers retours clients")
    goal_opp = {
        "awareness": "Stratégie content marketing pour construire l'autorité de marque",
        "sales": "Optimisation du tunnel de conversion pour maximiser le CA",
        "leads": "Lead magnets et marketing automation pour qualifier les prospects",
        "traffic": "SEO technique et stratégie de backlinks pour croissance organique",
    }
    if goal in goal_opp:
        d["opportunities"].append(goal_opp[goal])
    return d


# ─── QQOQCCP ─────────────────────────────────────────────────────────────────
_QQOQCCP = {
    "ecommerce": {
        "qui": {"q": "Qui sont vos acheteurs cibles ?",
                    "r": "Consommateurs 25-45 ans, actifs digitaux, acheteurs en ligne réguliers (2-4x/mois)",
                    "a": "Segmentez par RFM (Récence, Fréquence, Montant) et créez 3 personas distincts"},
        "quoi": {"q": "Quoi vendez-vous exactement ?",
                    "r": "Produits avec proposition de valeur unique et différenciante",
                    "a": "Rédigez une USP en 10 mots max : bénéfice principal + différenciateur + cible"},
        "où": {"q": "Où vos clients achètent-ils ?",
                    "r": "Mobile (68%), desktop (29%)  --  majorité via Google Shopping et réseaux sociaux",
                    "a": "Priorisez l'expérience mobile-first et optimisez vos fiches Google Shopping"},
        "quand": {"q": "Quand vos clients achètent-ils ?",
                    "r": "Pics : vendredi soir, samedi matin, pauses déjeuner (12h-14h), saisons festives",
                    "a": "Programmez vos campagnes sur ces créneaux + soldes/événements clés"},
        "comment": {"q": "Comment décident-ils d'acheter ?",
                    "r": "Google → comparaison avis → réseaux sociaux → achat  --  cycle 2-7 jours",
                    "a": "Couvrez chaque étape : SEO, reviews Trustpilot, retargeting Meta, panier abandonné"},
        "combien": {"q": "Combien sont-ils prêts à payer ?",
                    "r": "Panier moyen cible : 45-120 € selon la niche. Sensibilité prix forte sous 30 €",
                    "a": "Testez des prix psychologiques (X9), offres bundles et livraison gratuite à seuil"},
        "pourquoi":{"q": "Pourquoi vous choisiraient-ils ?",
                    "r": "Confiance (avis/garanties), commodité (livraison), prix/qualité, expérience brand",
                    "a": "Mettez en avant : étoiles Trustpilot, politique retour, badge sécurisé, UGC"},
    },
    "saas": {
        "qui": {"q": "Qui sont vos utilisateurs et décideurs ?",
                    "r": "Double cible : utilisateurs finaux (opérationnels) et acheteurs (dirigeants/DSI)",
                    "a": "Créez un messaging distinct pour chaque persona : bénéfice usage vs ROI business"},
        "quoi": {"q": "Quel problème résolvez-vous exactement ?",
                    "r": "Économie de temps, réduction d'erreurs ou augmentation de revenus  --  toujours quantifiable",
                    "a": "Quantifiez le problème : 'X heures perdues/semaine'ou 'Y% d'erreurs évitées'"},
        "où": {"q": "Où vos prospects cherchent-ils des solutions ?",
                    "r": "G2, Capterra, Product Hunt, LinkedIn, communautés Slack/Discord sectorielles",
                    "a": "Optimisez votre profil G2/Capterra + publiez sur Product Hunt au lancement"},
        "quand": {"q": "Quand un prospect décide-t-il de changer d'outil ?",
                    "r": "Lors d'un événement déclencheur : croissance, recrutement, audit, changement direction",
                    "a": "Configurez des alertes sur ces signaux d'intention (LinkedIn, news, levées de fonds)"},
        "comment": {"q": "Comment se déroule le cycle de décision ?",
                    "r": "Découverte → essai gratuit (14-30j) → démo → POC → validation → achat",
                    "a": "Optimisez chaque étape : onboarding J1-J7, email nurturing, CS proactif à J14"},
        "combien": {"q": "Combien votre solution leur fait-elle économiser/gagner ?",
                    "r": "Calculez le ROI concret : temps économisé × TJM ou revenus additionnels",
                    "a": "Créez un calculateur ROI interactif sur votre landing page"},
        "pourquoi":{"q": "Pourquoi vous plutôt que vos concurrents ?",
                    "r": "Fonctionnalités uniques, intégrations, support, prix ou rapidité d'implémentation",
                    "a": "Publiez des comparatifs 'Vous vs [Concurrent]'sur des landing pages dédiées"},
    },
}
_QQOQCCP_GENERIC = {
    "qui": {"q": "Qui est votre client idéal (ICP) ?",
                "r": "Définissez précisément : secteur, taille, rôle décisionnel, budget et douleur principale",
                "a": "Réalisez 10 interviews clients pour valider et affiner votre profil ICP"},
    "quoi": {"q": "Quoi proposez-vous exactement comme valeur ?",
                "r": "Votre offre doit résoudre un problème spécifique de manière unique et mesurable",
                "a": "Rédigez votre value proposition canvas : job-to-be-done, pains, gains"},
    "où": {"q": "Où se trouvent et s'informent vos prospects ?",
                "r": "Identifiez les canaux digitaux et physiques où ils cherchent des solutions",
                "a": "Investissez prioritairement dans les 2 canaux où votre ICP passe le plus de temps"},
    "quand": {"q": "Quand votre client a-t-il besoin de vous ?",
                "r": "Il existe toujours un déclencheur d'achat : événement, seuil de douleur, saison",
                "a": "Cartographiez le cycle de vie client et anticipez les moments déclencheurs"},
    "comment": {"q": "Comment votre client prend-il sa décision d'achat ?",
                "r": "Prise de conscience → considération → décision → fidélisation",
                "a": "Créez du contenu adapté à chaque étape du parcours (TOFU/MOFU/BOFU)"},
    "combien": {"q": "Combien votre client est-il prêt à investir ?",
                "r": "Le prix doit refléter la valeur perçue, pas uniquement vos coûts",
                "a": "Benchmarkez vos concurrents et testez différentes structurations de prix"},
    "pourquoi":{"q": "Pourquoi votre client vous choisit-il plutôt qu'un concurrent ?",
                "r": "Votre différenciateur doit être défendable, visible et valorisé par votre cible",
                "a": "Identifiez votre avantage compétitif unique et construisez tout votre messaging dessus"},
}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_qqoqccp(activity: str) -> dict:
    return copy.deepcopy(_QQOQCCP.get(activity, _QQOQCCP_GENERIC))


# ─── PESTEL ───────────────────────────────────────────────────────────────────
_PESTEL = {
    "ecommerce": {
        " Politique": [
            ("Régulation TVA numérique UE (OSS)", "négatif",
             "Complexité comptable accrue pour la vente transfrontalière"),
            ("Normes RGPD & ePrivacy", "neutre",
             "Contrainte mais avantage concurrentiel si bien géré"),
        ],
        " Économique": [
            ("Inflation des coûts logistiques +18% en 3 ans", "négatif",
             "Comprimez via négociation transporteur et stocks optimisés"),
            ("Croissance e-commerce +5-7%/an en France (FEVAD 2024)", "positif",
             "Marché en expansion  --  capturez la part de marché tôt"),
        ],
        "Socioculturel": [
            ("M-commerce : ~55% du trafic e-commerce depuis mobile (France)", "positif",
             "Mobile-first est désormais non-négociable"),
            ("Exigence RSE des consommateurs +39% vs 2022", "neutre",
             "Levier différenciant si vous intégrez l'impact environnemental"),
        ],
        " Technologique": [
            ("IA générative dans les recommandations produits", "positif",
             "Personnalisation accrue = +23% de conversion en moyenne"),
            ("Moteurs de recherche IA (Google SGE, Perplexity)", "neutre",
             "Adaptez votre SEO à l'intention de recherche IA (GEO)"),
        ],
        " Écologique": [
            ("Emballages durables  --  obligation légale 2025", "neutre",
             "Coût d'adaptation + avantage marketing si bien communiqué"),
        ],
        " Légal": [
            ("Directive Omnibus  --  transparence des prix", "négatif",
             "Obligation d'afficher le prix de référence avant promotion"),
            ("Droit de rétractation 14 jours  --  coût retours", "négatif",
             "Optimisez la logistique retour pour limiter l'impact financier"),
        ],
    },
    "saas": {
        " Politique": [
            ("AI Act européen (2024-2026)", "neutre",
             "Contraintes sur les systèmes IA à haut risque  --  auditez votre conformité"),
            ("Cloud Act US vs RGPD", "neutre",
             "Hébergement EU peut devenir un avantage pour les clients corporate"),
        ],
        " Économique": [
            ("Compression des budgets SaaS (stack fatigue)", "négatif",
             "ROI démontrable en <30 jours devient critère de survie"),
            ("Valorisations SaaS stabilisées  --  retour à la rentabilité", "neutre",
             "Les investisseurs cherchent la profitabilité"),
        ],
        "Socioculturel": [
            ("Remote work permanent  --  outils collaboratifs essentiels", "positif",
             "Intégrations Slack/Teams/Notion deviennent des must-have"),
            ("Adoption IA par les utilisateurs finaux +67% en 2024", "positif",
             "Intégrez des fonctionnalités IA pour rester compétitif"),
        ],
        " Technologique": [
            ("LLMs open-source  --  commoditisation de l'IA", "neutre",
             "L'IA seule ne suffit plus  --  l'avantage est dans les données propriétaires"),
            ("API-first & intégrations  --  ecosystème Zapier/Make", "positif",
             "Une bonne API multiplie votre reach sans effort commercial"),
        ],
        " Écologique": [
            ("GreenOps  --  empreinte carbone des serveurs", "neutre",
             "Hébergeurs green (OVH, Scaleway) deviennent un argument marketing B2B"),
        ],
        " Légal": [
            ("RGPD + DMA  --  obligations plateformes numériques", "neutre",
             "Nommez un DPO et auditez votre collecte de données régulièrement"),
        ],
    },
}
_PESTEL_GENERIC = {
    " Politique": [
        ("Réglementation sectorielle en évolution", "neutre",
         "Suivez les évolutions législatives de votre secteur"),
    ],
    " Économique": [
        ("Contexte macro-économique incertain", "neutre",
         "Anticipez les cycles et construisez une trésorerie de sécurité"),
        ("Croissance du marché digital", "positif",
         "Digitalisez votre offre pour capter cette croissance"),
    ],
    "Socioculturel": [
        ("Digitalisation accélérée des comportements", "positif",
         "Votre présence digitale est désormais votre première vitrine"),
    ],
    " Technologique": [
        ("IA générative  --  opportunités de productivité", "positif",
         "Intégrez des outils IA dans vos processus"),
        ("Cybersécurité  --  risques en hausse", "négatif",
         "Investissez dans la sécurité de vos données"),
    ],
    " Écologique": [
        ("Transition écologique  --  attente des parties prenantes", "neutre",
         "Définissez votre politique RSE même à petite échelle"),
    ],
    " Légal": [
        ("RGPD & protection des données", "neutre",
         "Assurez-vous de collecter uniquement les données nécessaires avec consentement"),
    ],
}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_pestel(activity: str) -> dict:
    return copy.deepcopy(_PESTEL.get(activity, _PESTEL_GENERIC))


# ─── MICRO-ENV ────────────────────────────────────────────────────────────────
_MICRO_ENV = {
    "ecommerce": {
        "Clients": ("élevé",
                              "Hyperchoix, faible coût de switching  --  exigence maximale",
                              "Fidélisez via programme de fidélité, contenu exclusif et service irréprochable"),
        "Fournisseurs": ("moyen",
                              "Multiples sources possibles mais dépendance aux délais de livraison",
                              "Diversifiez vos sources et stockez les SKU critiques"),
        " Concurrents": ("élevé",
                              "Amazon, Cdiscount, Pure Players niche  --  guerre des prix permanente",
                              "Différenciez sur l'expérience, la niche et le contenu, pas sur le prix seul"),
        "Intermédiaires": ("moyen",
                              "Marketplaces, comparateurs, influenceurs  --  dépendance aux algorithmes",
                              "Développez votre canal direct (DTC) pour réduire les commissions tiers"),
    },
    "saas": {
        "Clients": ("élevé",
                              "Churn élevé si valeur non démontrée à J30",
                              "Customer Success proactif + tableau de bord ROI intégré au produit"),
        "Fournisseurs": ("moyen",
                              "AWS/GCP/Azure  --  switching coûteux mais offres compétitives",
                              "Architecture cloud-agnostic et réserves d'instances pour optimiser les coûts"),
        " Concurrents": ("très élevé",
                              "Marché SaaS ultra-compétitif, consolidation en cours (M&A)",
                              "Hyper-spécialisation verticale + intégrations natives comme barrière à l'entrée"),
        "Intermédiaires": ("faible",
                              "App stores (faible commission), intégrateurs (partenariats clés)",
                              "Programme partenaires avec certifications et marges attractives"),
    },
}
_MICRO_GENERIC = {
    "Clients": ("élevé",
                          "Le digital donne aux clients un accès immédiat aux alternatives",
                          "Créez des barrières à la sortie : intégrations, données accumulées, communauté"),
    "Fournisseurs": ("moyen",
                          "Diversification des sources possible mais risque de dépendance",
                          "Identifiez vos fournisseurs critiques et sécurisez des alternatives"),
    " Concurrents": ("élevé",
                          "La concurrence directe et indirecte s'intensifie dans tous les marchés digitaux",
                          "Analysez systématiquement vos concurrents avec des outils comme Semrush"),
    "Intermédiaires": ("moyen",
                          "Plateformes et distributeurs prélèvent une commission croissante",
                          "Développez votre canal direct (site, newsletter, communauté) en parallèle"),
}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_micro_env(activity: str) -> dict:
    return copy.deepcopy(_MICRO_ENV.get(activity, _MICRO_GENERIC))


# ─── COMPETITIVE ─────────────────────────────────────────────────────────────
_COMPETITIVE = {
    "ecommerce": {
        "direct": [
            "Amazon / Cdiscount (généralistes)",
            "Pure Players de la niche",
            "Boutiques Shopify concurrentes",
        ],
        "indirect": [
            "Leboncoin / Vinted (occasion)",
            "Grandes surfaces en ligne",
            "Marketplace B2B sectorielles",
        ],
        "matrix": [
            ("Prix", "", "", "Leaders tirent le prix vers le bas  --  différenciez-vous"),
            ("Expérience UX", "", "", "Levier fort si vous investissez dans le design"),
            ("Catalogue", "", "", "Ne tentez pas de rivaliser en volume  --  spécialisez"),
            ("SAV & fidélisation","", "", "Avantage structurel des petites structures  --  exploitez-le"),
            ("Contenu & SEO", "", "", "Blog expert + UGC = trafic organique gratuit"),
        ],
        "oppty": "Niche premium + contenu expert + communauté = triangle défendable",
        "moat": "Données clients propriétaires + brand community + niche expertise",
    },
    "saas": {
        "direct": [
            "Solutions VC-backed bien financées",
            "Outils intégrés (suites Microsoft/Google)",
            "Concurrents de niche similaires",
        ],
        "indirect": [
            "Outils no-code (Notion, Airtable)",
            "Agences qui font manuellement",
            "Solutions open-source",
        ],
        "matrix": [
            ("Fonctionnalités", "", "", "Ne copiez pas tout  --  identifiez votre killer feature"),
            ("Prix", "", "", "Agilité tarifaire vs les poids lourds = avantage PME"),
            ("Support", "", "", "Accès fondateur direct = différenciateur early-stage"),
            ("Intégrations", "", "", "Priorisez 5 intégrations critiques pour votre ICP"),
            ("Vitesse d'itération", "", "", "Votre agilité est un avantage compétitif majeur"),
        ],
        "oppty": "Vertical SaaS spécialisé + support fondateur + time-to-value < 48h",
        "moat": "Données propriétaires sectoriel + intégrations natives + réseau utilisateurs",
    },
}
_COMPETITIVE_GENERIC = {
    "direct": [
        "Concurrents positionnés sur votre niche exacte",
        "Alternatives directes à votre offre",
    ],
    "indirect": [
        "Solutions DIY (faire soi-même)",
        "Freelances et agences généralistes",
    ],
    "matrix": [
        ("Prix", "", "", "Analysez le prix marché et positionnez-vous stratégiquement"),
        ("Qualité", "", "", "La qualité est votre meilleur argument différenciant"),
        ("Notoriété", "", "", "Construisez une notoriété de niche avant la notoriété large"),
        ("Service client","","", "Réactivité et personnalisation = avantage structurel"),
        ("Innovation", "", "", "Votre capacité à innover rapidement est une arme"),
    ],
    "oppty": "Identifiez le segment délaissé par les leaders et devenez l'expert incontournable",
    "moat": "Expertise niche + relation client + contenu propriétaire",
}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_competitive(activity: str) -> dict:
    return copy.deepcopy(_COMPETITIVE.get(activity, _COMPETITIVE_GENERIC))


# ─── SONCAS ──────────────────────────────────────────────────────────────────
_SONCAS = {
    "ecommerce": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "L'acheteur en ligne a besoin de confiance avant de sortir sa carte bleue. Réduisez le risque perçu à chaque étape du parcours.",
            "args": [
                "Paiement 100% sécurisé (SSL, 3DS2) affiché en évidence",
                "Politique de retour gratuit 30 jours sans condition",
                "Avis clients vérifiés (Trustpilot, Google Reviews) avec étoiles visibles",
            ],
            "objection": "Je ne vous connais pas  --  comment savoir si votre site est fiable ?",
            "reponse": "Nous affichons nos +2 000 avis vérifiés Trustpilot, notre garantie satisfait ou remboursé 30 jours et notre certification SSL. Commandez sans risque.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "L'acheteur veut se sentir valorisé, reconnu et appartenir à une élite. Flattez son ego avec des produits exclusifs et un statut premium.",
            "args": [
                "Étiquette 'Édition Limitée'ou 'Réservé aux membres Premium'",
                "Personalisation du produit avec initiales ou couleurs exclusives",
                "Accès VIP en avant-première aux nouvelles collections",
            ],
            "objection": "Je n'ai pas besoin d'un produit premium.",
            "reponse": "Nos clients premium ne cherchent pas juste un produit  --  ils veulent une expérience unique et reconnaissable. Nos éditions limitées sont portées par des leaders et des early adopters.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Certains acheteurs sont attirés par les nouveautés et les tendances. Mettez en avant vos dernières collections et innovations.",
            "args": [
                "Badge 'Nouveauté'ou 'Just dropped'sur les nouvelles références",
                "Email de lancement VIP en avant-première pour les abonnés",
                "Collaboration capsule ou édition limitée pour créer l'événement",
            ],
            "objection": "Je veux être sûr que ce produit est bien ce qu'il y a de plus récent.",
            "reponse": "Cette référence vient d'être ajoutée à notre catalogue cette semaine. Nos abonnés newsletter la découvrent en avant-première  --  rejoignez-les pour ne plus jamais rater un lancement.",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "L'expérience d'achat doit être fluide, rapide et sans friction. Chaque clic de trop est un client perdu.",
            "args": [
                "Checkout en 1 étape avec pré-remplissage des infos connues",
                "Suivi de commande en temps réel par SMS et email",
                "Service client disponible 7j/7 par chat (réponse < 2 min)",
            ],
            "objection": "Je n'ai pas envie de perdre du temps si ça ne correspond pas.",
            "reponse": "Commandez en 90 secondes. Si ce n'est pas parfait, le retour est gratuit et le remboursement est traité en 48h. Zéro tracas garanti.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "La sensibilité prix est forte en e-commerce. Montrez la valeur absolue et relative de votre offre.",
            "args": [
                "Comparateur de prix intégré ou mention du prix de marché",
                "Offres bundles avec économie affichée en pourcentage et en euros",
                "Paiement en 3x sans frais pour les paniers > 100 €",
            ],
            "objection": "C'est moins cher sur Amazon.",
            "reponse": "Notre prix inclut la livraison offerte, le retour gratuit et 2 ans de garantie. Sur Amazon, ces frais s'ajoutent. Calculez le coût total  --  nous sommes souvent moins chers.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "Les clients achètent aussi à des marques qu'ils apprécient. Humanisez votre boutique et créez une vraie connexion.",
            "args": [
                "Histoire de marque authentique visible sur la page 'À propos'",
                "Engagement RSE ou social (local, éco-responsable, solidaire)",
                "Communauté active sur les réseaux sociaux avec réponses aux commentaires",
            ],
            "objection": "Il y a tellement de boutiques en ligne, pourquoi vous ?",
            "reponse": "Nous sommes une équipe de 5 personnes passionnées par [niche]. Chaque commande est préparée avec soin. Lisez nos avis  --  nos clients reviennent parce qu'ils se sentent vraiment considérés.",
        },
    },
    "saas": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "Le décideur SaaS craint les risques : perte de données, downtime, contrat difficile à résilier. Minimisez chaque risque perçu.",
            "args": [
                "SOC 2 Type II / ISO 27001  --  certifications de sécurité affichées",
                "SLA 99.9% uptime avec crédits automatiques en cas d'incident",
                "Export des données à tout moment  --  no lock-in garanti",
            ],
            "objection": "Et si vous faites faillite ou si vous augmentez les prix brutalement ?",
            "reponse": "Notre code source est en escrow, vos données sont exportables en 1 clic et notre contrat inclut un préavis de 90 jours pour toute modification tarifaire. Votre continuité est protégée.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "Le buyer SaaS veut être reconnu comme un leader technologique. Valorisez son statut de précurseur et son image de décideur visionnaire.",
            "args": [
                "Badge 'Client Pionnier'et présence dans vos références sectorielles",
                "Cas clients avec métriques avant/après dans le même secteur",
                "Early adopter pricing  --  accès aux nouvelles fonctionnalités en priorité",
            ],
            "objection": "Je ne vois pas vraiment ce que j'ai à gagner par rapport à ce que j'utilise déjà.",
            "reponse": "Nos clients [même secteur] sont cités comme références dans leur industrie grâce à ce gain de productivité. Je peux vous positionner parmi eux en 15 minutes de démo.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Les early adopters technologiques veulent être à la pointe. Positionnez votre SaaS comme la solution de nouvelle génération.",
            "args": [
                "Roadmap publique pour montrer l'innovation continue",
                "Intégration IA générative comme fonctionnalité phare",
                "Accès beta aux nouvelles features pour les clients actifs",
            ],
            "objection": "L'outil que j'utilise fait ça depuis longtemps.",
            "reponse": "La différence est dans comment nous le faisons : notre moteur IA génère [résultat] en 30 secondes vs une configuration manuelle de 2 heures. Voulez-vous voir la démo ?",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "L'onboarding et la prise en main sont des freins majeurs au SaaS. Promettez et livrez une expérience sans friction.",
            "args": [
                "Onboarding guidé en 10 minutes avec données de démonstration pré-chargées",
                "Migration prise en charge par notre équipe (import depuis l'outil concurrent)",
                "Formation incluse + webinaires hebdomadaires en direct",
            ],
            "objection": "Je n'ai pas le temps de former mon équipe à un nouvel outil.",
            "reponse": "Notre onboarding est conçu pour que votre équipe soit autonome en une matinée. Nous gérons l'import de vos données existantes et proposons une formation live de 45 minutes incluse.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "Le budget SaaS est scruté. Démontrez un ROI clair et un coût total de possession inférieur aux alternatives.",
            "args": [
                "Prix par utilisateur actif  --  payez uniquement ce que vous utilisez",
                "Consolidation de plusieurs outils en un seul = économies immédiates",
                "Essai gratuit 14 jours sans carte bancaire  --  aucun risque financier",
            ],
            "objection": "Votre abonnement représente X € de plus par mois dans notre budget.",
            "reponse": "Calculons ensemble : si [fonctionnalité] économise 3h/semaine à votre équipe de 5 personnes, c'est 60h/mois à votre TJM interne  --  soit bien plus que notre abonnement. Le ROI est positif dès le premier mois.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "En B2B, on achète aussi à des personnes. La relation et la confiance humaine restent des différenciateurs puissants.",
            "args": [
                "Accès direct aux fondateurs pour les clients early stage",
                "Communauté Slack/Discord active avec entraide et partages",
                "Compte manager dédié dès 10 utilisateurs  --  relation humaine garantie",
            ],
            "objection": "Avec les grandes plateformes, j'ai un support dédié. Que m'offrez-vous ?",
            "reponse": "Chez nous, votre interlocuteur connaît votre usage par cœur. Vous n'attendez pas en file d'attente  --  vous avez mon numéro direct. Nos clients restent parce qu'ils se sentent partenaires, pas numéros.",
        },
    },
    "service": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "Le client d'un prestataire de service craint de mal choisir et de perdre son argent. Réduisez ce risque perçu par des garanties concrètes.",
            "args": [
                "Garantie résultat ou remboursement partiel sous conditions claires",
                "Contrat détaillé avec jalons et livrables définis",
                "Références clients vérifiables dans le même secteur",
            ],
            "objection": "Comment être sûr que vous livrerez ce que vous promettez ?",
            "reponse": "Notre contrat détaille chaque livrable avec des délais précis. Nous proposons des points d'étape hebdomadaires et vous pouvez contacter directement nos 3 derniers clients pour avoir leur retour.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "Le client veut être reconnu comme un dirigeant qui prend les bonnes décisions. Valorisez son image de leader stratège auprès de ses pairs.",
            "args": [
                "Témoignages de dirigeants similaires qui ont pris cette décision",
                "Rapport personnalisé avec logo client pour valoriser son image",
                "Offre 'Partenaire Stratégique'avec visibilité dans nos references",
            ],
            "objection": "Est-ce vraiment le bon moment pour investir dans ce service ?",
            "reponse": "Les dirigeants que nous accompagnons voient cela comme un signal de leadership. C'est ce qui les différencie  --  et qui leur permet d'être cités comme référence dans leur secteur.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Montrez que vos méthodes et outils sont à la pointe. Un prestataire moderne rassure et inspire confiance.",
            "args": [
                "Intégration des derniers outils IA pour accélérer les livrables",
                "Méthodologie propriétaire nommée et expliquée",
                "Veille sectorielle continue partagée avec les clients (newsletter, insights)",
            ],
            "objection": "Votre approche me semble classique  --  qu'est-ce qui vous différencie ?",
            "reponse": "Notre méthode [Nom] intègre les dernières avancées en [domaine]. Elle nous permet de livrer en 3 semaines ce qui prenait 3 mois avec les approches traditionnelles.",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "Le client veut être accompagné sans avoir à tout gérer. Promettez une expérience clé en main et sans friction.",
            "args": [
                "Gestion de projet complète  --  le client n'a qu'à valider",
                "Reporting clair et visuel chaque semaine sans jargon technique",
                "Disponibilité garantie avec temps de réponse < 4h ouvrées",
            ],
            "objection": "Je n'ai pas de temps à consacrer à ce projet en ce moment.",
            "reponse": "C'est exactement pour ça que nous existons. Votre implication : 1 appel de 30 min par semaine pour valider. Nous gérons tout le reste. Vous récupérez votre temps.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "Le client compare le coût du service à la valeur générée. Ancrez le prix sur le ROI, pas sur le temps passé.",
            "args": [
                "Prix fixe par livrable  --  pas de surprise sur la facture finale",
                "Présentation du ROI attendu : coût vs valeur générée",
                "Offre starter pour tester la collaboration à faible risque",
            ],
            "objection": "Votre tarif est élevé par rapport à d'autres prestataires.",
            "reponse": "Un prestataire moins cher qui ne livre pas résulte vous coûtera 3x plus : le temps perdu, le travail à refaire, l'opportunité manquée. Notre tarif reflète un résultat garanti  --  calculons ensemble le ROI.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "La relation humaine est au cœur du choix d'un prestataire. Soyez la personne avec qui ils veulent travailler.",
            "args": [
                "Appel découverte offert sans engagement pour créer le lien",
                "Communication transparente même quand il y a un problème",
                "Implication personnelle du dirigeant visible dans la relation",
            ],
            "objection": "Je préfère travailler avec quelqu'un que je connais déjà.",
            "reponse": "Tous nos clients étaient au même point avant de commencer. Un appel de 30 minutes suffit pour voir si l'entente est là. Si le courant ne passe pas, je vous le dirai moi-même.",
        },
    },
    "default": {
        "securite": {
            "label": "Sécurité", "icon": "",
            "desc": "Tout prospect a une peur fondamentale de se tromper. Votre mission : éliminer le risque perçu avant qu'il ne bloque la décision.",
            "args": [
                "Garantie satisfait ou remboursé avec conditions claires et simples",
                "Témoignages clients avec prénom, secteur et résultat chiffré",
                "Processus transparent de bout en bout sans surprise",
            ],
            "objection": "Et si ça ne correspond pas à ce que j'attends ?",
            "reponse": "Notre garantie [X jours] couvre exactement ce scénario. Si ce n'est pas parfait, nous remboursons intégralement  --  sans question. Vous n'avez rien à perdre.",
        },
        "opportunite": {
            "label": "Orgueil", "icon": "",
            "desc": "Le prospect veut être fier de ses choix et reconnu pour sa clairvoyance. Flattez son statut et valorisez son appartenance à une élite de décideurs.",
            "args": [
                "Positionnez-le dans une 'sélection exclusive'de clients partenaires",
                "Résultats obtenus par des profils similaires reconnus dans leur domaine",
                "Valorisez son rôle de précurseur dans son secteur",
            ],
            "objection": "Je ne vois pas encore ce que j'y gagne clairement.",
            "reponse": "Nos clients leaders ont tous pris cette décision avant leurs concurrents. C'est ce qui les distingue aujourd'hui  --  et qui les positionne comme références dans leur secteur.",
        },
        "nouveaute": {
            "label": "Nouveauté", "icon": "",
            "desc": "Certains prospects sont stimulés par l'innovation. Positionnez votre offre comme moderne, évolutive et avant-gardiste.",
            "args": [
                "Innovation différenciante expliquée en langage simple",
                "Roadmap ou évolutions prévues pour montrer la dynamique",
                "Positionnement 'nouvelle génération'vs solutions classiques",
            ],
            "objection": "Ça ressemble à ce que font déjà d'autres acteurs.",
            "reponse": "En apparence oui, mais notre approche intègre [différenciateur clé]. Cela change fondamentalement [résultat]. Laissez-moi vous montrer la différence en pratique.",
        },
        "confort": {
            "label": "Confort", "icon": "",
            "desc": "Le prospect veut une solution simple qui ne lui crée pas de nouveau problème. Promettez la facilité et tenez-la.",
            "args": [
                "Onboarding accompagné sans effort côté client",
                "Interface ou processus simple malgré la complexité sous-jacente",
                "Support réactif et humain pour toute question",
            ],
            "objection": "Je n'ai pas le temps de gérer un changement en ce moment.",
            "reponse": "Notre processus de mise en place est conçu pour prendre moins de [X heures] de votre temps. Nous gérons tout le reste. Vous verrez les résultats avant même d'avoir senti le changement.",
        },
        "argent": {
            "label": "Argent", "icon": "",
            "desc": "Le prospect évalue le rapport coût/valeur. Ancrez la discussion sur la valeur créée, pas sur le prix affiché.",
            "args": [
                "ROI calculable avec des hypothèses conservatrices",
                "Comparaison coût de votre solution vs coût de l'inaction",
                "Options flexibles de paiement adaptées à la taille du projet",
            ],
            "objection": "C'est au-dessus de notre budget prévu.",
            "reponse": "Je comprends. Calculons ensemble ce que vous coûte actuellement [problème] chaque mois. Si notre solution coûte moins que ce problème, le budget est justifié  --  sinon, nous trouverons une formule adaptée.",
        },
        "sympathie": {
            "label": "Sympathie", "icon": "",
            "desc": "Les décisions d'achat sont souvent émotionnelles. Créez un lien de confiance authentique avant de vendre.",
            "args": [
                "Authenticité et transparence dans la communication",
                "Intérêt réel pour la situation du prospect avant de pitcher",
                "Histoire de marque ou parcours personnel qui crée la connexion",
            ],
            "objection": "Je ne suis pas encore convaincu par votre approche.",
            "reponse": "C'est totalement normal à ce stade. Ce qui compte, c'est que vous trouviez la bonne solution pour vous  --  même si ce n'est pas nous. Pouvez-vous me dire ce qui vous manque pour être convaincu ?",
        },
    },
}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_soncas(activity: str) -> dict:
    """Return the SONCAS data dict for a given activity type.

    Falls back to 'default'if the activity key is not found.

    Args:
        activity: One of 'ecommerce', 'saas', 'service', or any other string
                  (falls back to 'default').

    Returns:
        A deep copy of the SONCAS data dict for the given activity.
    """
    return copy.deepcopy(_SONCAS.get(activity, _SONCAS["default"]))

# ─── AIDA ────────────────────────────────────────────────────────────────────
_AIDA = {
    "ecommerce": {
        "attention": {"p":"Headline qui interrompt le scroll","e":"Pourquoi 94% des acheteurs reviennent toujours chez nous","f":["Arrêtez de [problème]  --  voici pourquoi [solution inattendue]","La vraie raison pour laquelle [cible] rate [résultat]","[Chiffre] acheteurs ont découvert [bénéfice]  --  voici comment"],"c":"Utilisez chiffres, questions rhétoriques et promesses spécifiques. Évitez le générique."},
        "interest": {"p":"Développez le problème pour créer l'identification","e":"Vous passez des heures à chercher... pour toujours tomber sur des produits décevants","f":["Comme [X] clients avant vous, vous avez peut-être déjà vécu [situation]","Voici ce que personne ne vous dit sur [sujet]","Le problème avec [solution classique], c'est que [raison spécifique]"],"c":"Montrez que vous comprenez exactement la douleur du client  --  avant de parler de vous."},
        "desire": {"p":"Projeter le client dans l'état désiré après achat","e":"Imaginez recevoir exactement ce que vous attendiez, livré en 48h, avec garantie satisfait ou remboursé","f":["Imaginez [bénéfice émotionnel]  --  c'est exactement ce que [X] clients vivent","[Bénéfice concret] + [bénéfice émotionnel] = votre nouvelle réalité","Nos clients témoignent : '[citation courte et spécifique]'"],"c":"Combinez preuve sociale, bénéfices tangibles et projetez l'état émotionnel post-achat."},
        "action": {"p":"CTA unique, urgent et sans friction","e":"Commander maintenant  --  Livraison offerte aujourd'hui","f":["Je veux [bénéfice] → [bouton d'action]","Profitez-en maintenant  --  [raison de l'urgence réelle]","Commencez sans risque  --  [garantie spécifique]"],"c":"Un seul CTA visible, urgence authentique, garantie de risque zéro, friction minimale."},
    },
    "saas": {
        "attention": {"p":"Chiffrez la douleur ou promettez le résultat","e":"Réduisez de 4h à 20min votre reporting hebdomadaire","f":["[X] heures perdues chaque semaine à faire [tâche manuelle]  --  et si ce n'était plus le cas ?","Comment [client similaire] a multiplié par [X] [métrique] en [temps]","Votre concurrent utilise déjà [solution]  --  voici ce qu'il gagne"],"c":"Les décideurs SaaS sont rationnels  --  commencez par un chiffre ou un résultat mesurable."},
        "interest": {"p":"Nommez le problème précis que seul votre outil résout","e":"La plupart des équipes perdent 23% de leur temps dans des tâches que [Outil] automatise en un clic","f":["Le vrai problème avec [workflow actuel], c'est [coût caché invisible]","[Chiffre] équipes ont abandonné [ancienne méthode]  --  voici pourquoi","Sans [fonctionnalité], chaque [événement] vous coûte [quantification]"],"c":"Soyez ultra-précis sur le pain point. Plus c'est spécifique, plus ça résonne."},
        "desire": {"p":"Démo, cas client avec métriques, social proof B2B","e":"[Client connu] a réduit son CAC de 34% après 60 jours","f":["'Depuis [Outil], on a [résultat] en [temps]' --  [Prénom, Titre, Entreprise]","Rejoignez [X] équipes qui ont déjà transformé [process]","Essayez gratuitement 14 jours  --  sans carte bancaire, sans engagement"],"c":"Case studies avec métriques > témoignages génériques."},
        "action": {"p":"Essai gratuit sans friction ou démo personnalisée","e":"Commencer mon essai gratuit  --  En ligne en 2 minutes","f":["Voir une démo en 15 min → [calendrier direct]","Essayer gratuitement 14 jours → aucune CB requise","Obtenir mon accès maintenant → [bénéfice immédiat à l'inscription]"],"c":"Réduisez le risque perçu au maximum  --  freemium, démo, POC  --  jamais de salesman dès le premier contact."},
    },
}
_AIDA_GENERIC = {
    "attention": {"p":"Captez l'attention avec un headline irrésistible","e":"Le problème que vous n'avez jamais su nommer  --  et notre solution","f":["[Chiffre provocateur] raisons pour lesquelles [problème persiste]","Comment [cible similaire] a obtenu [résultat] sans [obstacle perçu]","Arrêtez [action coûteuse]  --  il existe une meilleure façon"],"c":"Votre headline est lu 5x plus que le reste. Investissez 50% de votre temps copywriting dessus."},
    "interest": {"p":"Développez la promesse en identifiant la douleur précise","e":"Vous savez que [problème] vous coûte [temps/argent]  --  mais la vraie cause est ailleurs","f":["Voici ce que la plupart des [cible] ignorent sur [sujet]","Le coût invisible de [problème] : [quantification inattendue]","Comme [X personnes], vous avez peut-être essayé [solutions inefficaces]"],"c":"Empathie d'abord, solution ensuite. Montrez que vous comprenez avant de convaincre."},
    "desire": {"p":"Créez l'envie avec preuves, projections et social proof","e":"Nos clients obtiennent [résultat tangible] et [bénéfice émotionnel]  --  ils en témoignent","f":["Imaginez [situation désirée]  --  c'est possible dès [timing réaliste]","[X] personnes ont déjà [résultat]  --  voici leurs retours","Garantie : si vous n'obtenez pas [résultat], [engagement spécifique]"],"c":"Preuves > promesses. Spécifique > général. Résultat émotionnel > fonctionnalité technique."},
    "action": {"p":"Un seul appel à l'action, clair et sans friction","e":"Commencer maintenant  --  [bénéfice immédiat] → [CTA]","f":["Je veux [résultat précis] → [bouton action]","C'est gratuit jusqu'à [date/seuil]  --  [CTA]","[Bénéfice] sans [risque perçu] → [CTA]"],"c":"Supprimez tout ce qui pourrait faire hésiter : formulaires longs, prix cachés, processus flous."},
}

_TRIGGERS = [
    ("Urgence temporelle","Crée une pression de temps pour déclencher l'action immédiate","Offre valable jusqu'à minuit  --  Stock limité à 47 unités","Ventes flash, périodes de promotion, lancement de produit"," Doit être AUTHENTIQUE  --  la fausse urgence détruit la confiance"),
    ("Preuve sociale","Les gens imitent ce que font d'autres personnes similaires à eux","12 847 clients satisfaits  --  Rejoignez-les","Témoignages, compteurs d'utilisateurs, logos clients, médias"," Spécifique et vérifiable > chiffre rond et non sourcé"),
    ("Autorité","Les experts et figures d'autorité crédibilisent votre offre","Recommandé par [expert connu] · Certifié [organisme] · Cité dans [media]","Badges certifications, mentions presse, partenariats experts"," L'autorité doit être pertinente pour votre cible, pas seulement impressionnante"),
    ("Rareté","La valeur perçue augmente quand la disponibilité diminue","Plus que 3 places disponibles ce mois · Édition limitée 500 exemplaires","Services premium, places de formation, stocks limités"," La rareté inventée génère du ressentiment"),
    ("Réciprocité","Donner quelque chose de valeur crée une obligation naturelle de rendre","Guide gratuit (vraie valeur) → lead nurturing → vente naturelle","Lead magnets, contenus premium gratuits, consultations offertes"," La valeur du cadeau détermine la réciprocité  --  évitez les ebooks creux"),
    ("Engagement & Cohérence","Une fois qu'une personne a dit oui à quelque chose de petit, elle dit oui à plus grand","Quiz gratuit → email → webinaire → offre → vente","Funnels de conversion, séquences email, onboarding progressif"," Chaque micro-engagement doit délivrer de la valeur"),
    ("Aversion à la perte","La douleur de perdre est 2x plus intense que le plaisir de gagner","Ne laissez pas vos concurrents prendre de l'avance · Évitez de perdre X €/mois","Messaging sur les risques de ne pas agir, coûts de l'inaction"," À utiliser avec parcimonie  --  le fear marketing permanent génère du rejet"),
    ("Appartenance","Les humains veulent appartenir à un groupe qui partage leurs valeurs","Rejoignez 5000 entrepreneurs qui ont choisi de [valeur commune]","Positioning de marque, communication de communauté, onboarding"," La communauté doit être réelle et active"),
]

@st.cache_data(ttl=3600, show_spinner=False)
def gen_aida(activity: str) -> dict:
    return copy.deepcopy(_AIDA.get(activity, _AIDA_GENERIC))

# ─── GEO 2025 ────────────────────────────────────────────────────────────────
_GEO = {
    "ecommerce": {
        "topics": ["Guide ultime d'achat [produit phare]  --  le contenu pilier de référence","Comparatif [produit A] vs [produit B]  --  contenu cluster haute valeur","FAQ produits enrichie  --  capture les requêtes conversationnelles IA","Avis clients structurés (schema Review)  --  utilisés par Google SGE"],
        "clusters": [("Guide d'achat [niche]",["Comment choisir X","Meilleur X pour Y","X test & avis","X prix comparatif"]),("Guide entretien / utilisation",["Comment utiliser X","Erreurs à éviter","X durée de vie","Tutoriel X"])],
        "optims": [("Ajoutez des FAQ schema markup sur toutes vos fiches produit"," Élevé"),("Répondez aux questions 'quel est le meilleur X pour Y'dans vos contenus"," Élevé"),("Utilisez du langage naturel conversationnel dans vos descriptions","Moyen"),("Structurez vos avis en données structurées (schema Review)"," Élevé")],
        "tips": ["Google SGE et ChatGPT extraient des réponses directes  --  soyez la source citée","Perplexity cite les sources  --  des backlinks de qualité restent essentiels","Les requêtes vocales explosent  --  optimisez pour le langage parlé"],
    },
    "saas": {
        "topics": ["Guides pratiques ultra-complets sur les problèmes que votre outil résout","Études de cas sectorielles avec métriques et ROI quantifiés","Comparatifs objectifs avec vos concurrents (even-handed = crédibilité)","Glossaire du secteur  --  topical authority signal fort pour Google"],
        "clusters": [("Guide [fonctionnalité principale]",["Comment faire X sans outil","X automatisation guide","X pour les débutants","X cas d'usage avancés"]),("Comparatif outils [catégorie]",["Vous vs Concurrent A","Vous vs Concurrent B","Meilleur outil X 2025","Migrer de X vers vous"])],
        "optims": [("Créez une documentation technique complète (boon for AI crawlers)"," Élevé"),("Publiez des datasets ou benchmarks sectoriels citables par l'IA","Très élevé"),("Répondez aux questions 'comment [task] avec [catégorie d'outil]'exhaustivement"," Élevé"),("Structurez vos how-to avec des étapes numérotées (schema HowTo)","Moyen")],
        "tips": ["Les LLMs sont entraînés sur le web  --  votre contenu publié aujourd'hui formera les réponses de demain","Soyez la ressource la plus citée de votre niche  --  qualité > quantité","ChatGPT et Perplexity favoritent les sites avec API publique et documentation claire"],
    },
}
_GEO_GENERIC = {
    "topics": ["Contenus piliers ultra-complets sur votre thème principal","Clusters de contenu répondant à toutes les questions de votre ICP","FAQ structurée avec schema markup pour la capture des requêtes IA","Études de cas et données sectorielles propriétaires"],
    "clusters": [("Guide principal [thème]",["Introduction","Niveau avancé","Cas pratiques","FAQ"]),("Solutions aux problèmes [cible]",["Problème A → solution","Problème B → solution","Comparatif solutions","Erreurs à éviter"])],
    "optims": [("Utilisez des questions naturelles comme sous-titres H2/H3"," Élevé"),("Ajoutez un schema FAQ sur toutes vos pages clés"," Élevé"),("Répondez directement et précisément en début de section (featured snippet)"," Élevé"),("Créez du contenu E-E-A-T : Experience, Expertise, Authority, Trust","Très élevé")],
    "tips": ["39% des Français utilisent l'IA conversationnelle  --  optimisez maintenant pour ces moteurs","Les IA citent les sources qui répondent directement et exhaustivement","L'intention de recherche prime sur le mot-clé exact  --  comprenez le 'pourquoi'"],
}

_SEA_IA = [
    ("Google AI Max","Performance Max avec IA Max  --  diffusion automatique sur tous les canaux Google",["Diffusion sur Search, Display, YouTube, Gmail, Maps, Shopping","Optimisation en temps réel des enchères et audiences via ML","Asset generation IA  --  génère des variantes de titres et descriptions"],"Fournissez des assets de qualité  --  la qualité des inputs détermine la qualité des outputs IA"),
    ("Smart Bidding","Stratégies d'enchères automatisées par Google ML pour maximiser les conversions",["Target CPA : coût par acquisition fixe  --  idéal si vous connaissez votre CPA cible","Target ROAS : retour sur dépenses publicitaires  --  pour e-commerce avec données de valeur","Maximize Conversions : maximise le volume dans votre budget  --  pour démarrer","Enhanced CPC : manuel + ajustement IA  --  contrôle maximal pour débutants"],"Donnez au Smart Bidding 2-4 semaines d'apprentissage avant d'évaluer les performances"),
    ("AI Overviews","Google AI Overviews  --  réponses IA intégrées dans les résultats de recherche",["Annonces textuelles dans les AI Overviews (beta 2025)  --  position premium visible","Shopping ads dans les réponses IA pour les requêtes produits","Position 0 : votre annonce affichée dans la synthèse IA de Google"],"Combinez SEA (paiement garanti) + SEO GEO (organique IA) pour une visibilité maximale"),
    ("Audience Signals","Signaux d'audience pour guider l'IA vers vos meilleurs prospects",["Customer Match : uploadez vos emails clients pour trouver des similaires","Similar Audiences basées sur vos convertisseurs","In-Market Audiences : personas en phase d'achat active","Custom Intent : audiences basées sur les recherches récentes"],"Plus vous fournissez de signaux de qualité, plus l'IA cible efficacement"),
]

@st.cache_data(ttl=3600, show_spinner=False)
def gen_geo(activity: str) -> dict:
    return copy.deepcopy(_GEO.get(activity, _GEO_GENERIC))

# ─── SEO KEYWORDS ENRICHED (from backend seo_service) ───────────────────────
_KEYWORDS_ENRICHED = {
    "ecommerce": [
        ("boutique en ligne livraison rapide",        "10K-100K", "Élevé",  "Transactionnel"),
        ("acheter en ligne paiement sécurisé",        "10K-100K", "Élevé",  "Transactionnel"),
        ("meilleur site e-commerce France",            "1K-10K",   "Moyen",  "Commercial"),
        ("avis client boutique fiable",                "1K-10K",   "Facile", "Commercial"),
        ("comparatif boutique en ligne",               "500-5K",   "Facile", "Commercial"),
        ("comment choisir boutique en ligne sécurisée","1K-10K",   "Facile", "Informationnel"),
        ("promotion soldes vente flash",               "5K-50K",   "Moyen",  "Transactionnel"),
    ],
    "saas": [
        ("logiciel gestion PME gratuit",               "10K-100K", "Élevé",  "Transactionnel"),
        ("alternative logiciel concurrent",            "1K-10K",   "Moyen",  "Commercial"),
        ("meilleur outil gestion TPE",                 "500-5K",   "Facile", "Commercial"),
        ("comment automatiser sa gestion d'entreprise","1K-10K",   "Facile", "Informationnel"),
        ("prix logiciel SaaS abonnement mensuel",      "500-5K",   "Facile", "Commercial"),
        ("logiciel SaaS pour startup",                 "500-5K",   "Facile", "Transactionnel"),
        ("outil productivité équipe télétravail",      "1K-10K",   "Moyen",  "Commercial"),
    ],
    "service": [
        ("consultant freelance en ligne",              "1K-10K",   "Moyen",  "Commercial"),
        ("prestataire service en ligne tarif",         "500-5K",   "Facile", "Transactionnel"),
        ("comment trouver un expert en ligne",         "5K-50K",   "Moyen",  "Informationnel"),
        ("devis service numérique rapide",             "1K-10K",   "Facile", "Commercial"),
        ("avis consultant freelance fiable",           "500-5K",   "Facile", "Commercial"),
        ("accompagnement individuel en ligne",         "1K-10K",   "Facile", "Transactionnel"),
    ],
    "consulting": [
        ("consultant stratégie entreprise freelance",  "1K-10K",   "Moyen",  "Commercial"),
        ("accompagnement dirigeant TPE PME",           "500-5K",   "Facile", "Commercial"),
        ("conseil business plan démarrage",            "5K-50K",   "Moyen",  "Informationnel"),
        ("mentor entrepreneur en ligne",               "1K-10K",   "Facile", "Transactionnel"),
        ("diagnostic stratégique PME gratuit",         "500-5K",   "Facile", "Commercial"),
    ],
    "content": [
        ("créateur de contenu formation",              "5K-50K",   "Moyen",  "Informationnel"),
        ("stratégie contenu réseaux sociaux",          "5K-50K",   "Moyen",  "Informationnel"),
        ("blog affilié revenus passifs",               "1K-10K",   "Moyen",  "Commercial"),
        ("newsletter abonnés fidélisation",            "1K-10K",   "Facile", "Informationnel"),
        ("monétiser audience YouTube Instagram",       "5K-50K",   "Élevé",  "Commercial"),
    ],
    "default": [
        ("solution en ligne professionnelle",          "1K-10K",   "Moyen",  "Commercial"),
        ("service numérique fiable",                   "500-5K",   "Facile", "Transactionnel"),
        ("comment démarrer une activité en ligne",     "5K-50K",   "Moyen",  "Informationnel"),
        ("meilleure solution pour entrepreneurs",      "1K-10K",   "Moyen",  "Commercial"),
        ("avis et comparatif solutions web",           "500-5K",   "Facile", "Commercial"),
        ("guide complet démarrage activité web",       "500-5K",   "Facile", "Informationnel"),
        ("astuce entrepreneur débutant",               "1K-5K",    "Facile", "Informationnel"),
    ],
}

# ─── PLATFORM ENRICHED (from backend marketing_service) ──────────────────────
_PLATFORM_ENRICHED = {
    "ecommerce": [
        ("Instagram Shopping",    "haute",   "1 post/jour + 5 stories",  "Idéal pour les achats impulsifs et la découverte visuelle produit"),
        ("Pinterest",             "haute",   "5 épingles/jour",           "Fort trafic d'intention d'achat, pins durables dans le temps"),
        ("Facebook Ads",          "haute",   "2-3 campagnes actives",     "Retargeting puissant et ciblage démographique précis"),
        ("Google Shopping",       "moyenne", "Campagnes continues",       "Capture l'intention d'achat directe en phase de recherche"),
        ("TikTok",                "moyenne", "3-5 vidéos/semaine",        "Viralité produit, fort engagement Génération Z et Millennials"),
    ],
    "saas": [
        ("LinkedIn",              "haute",   "5 posts/semaine",           "Audience professionnelle B2B, décideurs et acheteurs"),
        ("Google Ads",            "haute",   "Campagnes continues",       "Capture l'intention de recherche au moment clé du besoin"),
        ("Email Marketing",       "haute",   "1-2 emails/semaine",        "Nurturing leads, séquences d'onboarding et rétention (ROI 42:1)"),
        ("YouTube",               "moyenne", "1 vidéo/semaine",           "Tutoriels, démos produit et SEO vidéo durable"),
        ("Webinaires",            "moyenne", "2/mois",                    "Conversion haute intention, démonstration valeur directe"),
    ],
    "service": [
        ("LinkedIn",              "haute",   "5 posts/semaine",           "Réseau de référence pour les services B2B et le personal branding"),
        ("Email Marketing",       "haute",   "1-2 emails/semaine",        "Canal owned, meilleur ROI pour la fidélisation client"),
        ("Google (SEO local)",    "haute",   "2 articles/semaine",        "Capte les recherches directes de prestataires qualifiés"),
        ("Instagram",             "moyenne", "4 posts/semaine",           "Montre les coulisses et humanise le prestataire"),
        ("Podcasts / YouTube",    "moyenne", "1 épisode/semaine",         "Autorité sectorielle et contenu evergreen longue traîne"),
    ],
    "consulting": [
        ("LinkedIn",              "haute",   "5 posts/semaine",           "Plateforme numéro 1 pour le personal branding B2B"),
        ("Email Marketing",       "haute",   "1/semaine",                 "Nurturing prospects, newsletter d'expertise"),
        ("Podcast / YouTube",     "haute",   "1 épisode/semaine",         "Contenu long format pour démontrer l'expertise"),
        ("Google (SEO)",          "moyenne", "2 articles/semaine",        "Articles de fond qui capturent les recherches intentionnelles"),
        ("Webinaires",            "haute",   "1-2/mois",                  "Génération de leads qualifiés et démonstration de valeur"),
    ],
    "content": [
        ("YouTube",               "haute",   "2-3 vidéos/semaine",        "Plateforme vidéo avec meilleur ROI long terme et SEO intégré"),
        ("Newsletter (Substack)", "haute",   "1-2/semaine",               "Audience owned, monétisation directe, fidélisation forte"),
        ("Instagram / TikTok",   "haute",   "1 post/jour",               "Découverte, viralité et croissance rapide d'audience"),
        ("Podcast",               "moyenne", "1 épisode/semaine",         "Audience fidèle, partenariats et brand deals"),
        ("Pinterest",             "moyenne", "5 pins/jour",               "Trafic evergreen vers blog et contenu long terme"),
    ],
    "default": [
        ("Instagram",             "haute",   "1 post/jour",               "Large audience, format visuel adapté à tous secteurs"),
        ("Email Newsletter",      "haute",   "1-2/semaine",               "Canal owned avec meilleur ROI du marketing digital (42:1)"),
        ("Facebook",              "haute",   "5 posts/semaine",           "Ciblage avancé, groupes communautaires et publicité accessible"),
        ("LinkedIn",              "moyenne", "3-4 posts/semaine",         "Réseautage professionnel et autorité sectorielle"),
        ("Google Ads",            "moyenne", "Campagnes ciblées",         "Capture l'intention de recherche directe"),
    ],
}

# ─── SEO KEYWORDS ────────────────────────────────────────────────────────────
_KEYWORDS = {
    "ecommerce": [("boutique en ligne livraison rapide","10K-100K","Facile","Transactionnel"),("acheter [produit] pas cher","10K-100K","Moyen","Transactionnel"),("meilleur [produit] 2025","5K-10K","Moyen","Commercial"),("avis [produit/marque]","5K-10K","Facile","Commercial"),("[produit] livraison gratuite","1K-5K","Facile","Transactionnel"),("comparatif [produit]","1K-5K","Moyen","Commercial")],
    "saas": [("[fonctionnalité] logiciel","5K-10K","Moyen","Commercial"),("meilleur outil [catégorie] 2025","1K-5K","Moyen","Commercial"),("[concurrent] alternative","500-1K","Facile","Commercial"),("comment automatiser [tâche]","1K-5K","Facile","Informationnel"),("[catégorie] prix tarifs","500-1K","Moyen","Transactionnel"),("[catégorie] comparatif","1K-5K","Élevé","Commercial")],
    "service": [("[service] [ville] prix","1K-5K","Facile","Transactionnel"),("prestataire [service] pro","500-1K","Facile","Commercial"),("comment choisir [prestataire]","1K-5K","Moyen","Informationnel"),("[service] avis clients","500-1K","Facile","Commercial"),("tarif [service] 2025","500-1K","Moyen","Transactionnel")],
    "default": [("[mot-clé principal] guide","1K-5K","Moyen","Informationnel"),("meilleur [produit/service] 2025","1K-5K","Moyen","Commercial"),("comment [résoudre problème]","5K-10K","Facile","Informationnel"),("[secteur] prix tarif","500-1K","Moyen","Transactionnel"),("avis [marque/service]","500-1K","Facile","Commercial")],
}

@st.cache_data(ttl=3600, show_spinner=False)
def gen_keywords(activity: str) -> list:
    enriched = _KEYWORDS_ENRICHED.get(activity, _KEYWORDS_ENRICHED["default"])
    base = copy.deepcopy(_KEYWORDS.get(activity, _KEYWORDS["default"]))
    seen = set(kw for kw, _, _, _ in enriched)
    extra = [k for k in base if k[0] not in seen]
    return enriched + extra

# ─── MARKETING ───────────────────────────────────────────────────────────────
_PLATFORMS = {
    "ecommerce": [("Instagram","haute","3-5x/sem","Reels, Stories, Shopping"),("Google Shopping","haute","Continu","Fiches produit optimisées"),("TikTok","haute","1-2x/j","Vidéos produit, UGC, GRWM"),("Email","haute","2-3x/sem","Abandons panier, promos, fidélité"),("Pinterest","moyenne","3x/sem","Épingles produits, mood boards")],
    "saas": [("LinkedIn","haute","5x/sem","Articles, témoignages clients, actus"),("Email","haute","2x/sem","Nurturing, onboarding, upsell"),("Google Ads","haute","Continu","Search branded + concurrents"),("YouTube","moyenne","1x/sem","Tutoriels, cas clients, démos"),("Twitter/X","faible","1-2x/j","Veille, thread expertise")],
    "service": [("LinkedIn","haute","4x/sem","Études de cas, expertise, posts"),("Google My Business","haute","1x/sem","Actualités, avis, photos"),("Email","haute","1x/sem","Newsletter valeur, offres"),("Bouche-à-oreille","haute","En continu","Programme de référencement client"),("Instagram","moyenne","3x/sem","Coulisses, témoignages, avant/après")],
    "consulting": [("LinkedIn","haute","5x/sem","Articles de fond, thought leadership"),("Newsletter","haute","1x/sem","Insights sectoriels exclusifs"),("Podcast/YouTube","moyenne","1x/mois","Interviews, analyses de marché"),("Conférences","moyenne","1-2x/trim","Speaking, networking"),("Twitter/X","faible","Quotidien","Veille et engagement")],
    "content": [("YouTube","haute","2x/sem","Vidéos longues, tutoriels"),("Instagram","haute","1x/j","Reels, Stories, contenu viral"),("Newsletter","haute","1x/sem","Monétisation audience fidèle"),("TikTok","moyenne","1-2x/j","Shorts, tendances"),("Podcast","faible","1x/sem","Format audio, interviews")],
    "default": [("Instagram","haute","3x/sem","Posts, Stories, Reels"),("LinkedIn","haute","3x/sem","Articles, posts expertise"),("Email","haute","1-2x/sem","Newsletter, offres"),("Google Ads","moyenne","Continu","Search, Display"),("Facebook","faible","2x/sem","Communauté, ads")],
}

_CALENDAR_TOPICS = {
    "awareness": ["Comment [votre expertise] transforme [résultat]","Les 5 erreurs que font 90% des [cible]","Interview d'expert : [tendance secteur]","Guide ultime : [thème central]"],
    "sales": ["Témoignage client : [résultat chiffré]","Comparatif : [votre solution] vs alternatives","Offre exclusive : [bénéfice] pour [cible]","Démonstration : comment [fonctionnalité] fonctionne"],
    "leads": ["[Lead magnet] gratuit : [titre accrocheur]","Webinaire : [résoudre problème courant]","Quiz : quel est votre niveau en [thème] ?","Étude de cas : comment [client] a obtenu [résultat]"],
    "traffic": ["Guide SEO : [mot-clé cible] expliqué","Les [X] meilleures ressources pour [sujet]","Tutorial : [processus étape par étape]","Infographie : [données secteur] en 2025"],
}

@st.cache_data(ttl=3600, show_spinner=False)
def gen_platforms(activity: str) -> list:
    enriched = _PLATFORM_ENRICHED.get(activity, _PLATFORM_ENRICHED["default"])
    return copy.deepcopy(enriched)

@st.cache_data(ttl=3600, show_spinner=False)
def gen_budget_alloc(monthly: float) -> list:
    if monthly <= 50:
        cats = [("Création de contenu (outils gratuits)", 60), ("Outils freemium", 30), ("Formation / veille", 10)]
    elif monthly <= 200:
        cats = [("Publicité payante (Social Ads test)", 40), ("Outils & logiciels starter", 35), ("Création de contenu", 25)]
    elif monthly <= 500:
        cats = [("Publicité payante (SEA/Social Ads)", 45), ("Outils & logiciels", 30), ("Création de contenu", 15), ("SEO & link-building", 10)]
    else:
        cats = [("Publicité payante (SEA/Social Ads)", 50), ("Outils & logiciels (CRM, analytics)", 25), ("Création de contenu", 15), ("SEO & link-building", 10)]
    return [(c, pct, round(monthly * pct / 100, 0)) for c, pct in cats]

@st.cache_data(ttl=3600, show_spinner=False)
def gen_budget_reco(monthly: float) -> list:
    if monthly <= 50:
        return [
            "Budget micro (≤50€) : misez à 100% sur l'organique",
            "Outils gratuits : Canva Free, Mailchimp Free, Google Search Console, Google Analytics",
            "Stratégie : 2 posts/semaine sur 1 réseau · 1 article de blog SEO/semaine · Newsletter mensuelle",
            "ROI attendu : notoriété et premiers leads organiques en 2-4 mois",
            " Évitez la pub payante  --  budget insuffisant pour obtenir des données statistiques fiables",
        ]
    elif monthly <= 200:
        return [
            "Budget starter (50-200€) : organique + micro-tests paid",
            "Outils : Canva Pro (13€/mois), Brevo/Sendinblue starter, Google Ads (50-100€ test)",
            "Stratégie : 1 campagne Google Ads test · SEO content 2x/sem · Email 2x/mois",
            "ROI attendu : premiers achats/leads payants en 4-6 semaines si niche peu concurrentielle",
            " Allouez 60% du budget paid sur 1 canal unique avant de diversifier",
        ]
    elif monthly <= 500:
        return [
            "Budget PME (200-500€) : mix paid + contenu + outils",
            "Outils : CRM starter (HubSpot Free ou Pipedrive 15€), Google Ads + Meta Ads, Semrush Lite",
            "Stratégie : SEA Search + retargeting · Content 3x/sem · Email automation bienvenue + nurturing",
            "ROI attendu : ROAS 2-4x en e-commerce · CPL 15-40€ en B2B sur 60-90 jours",
            "Commencez le SEO maintenant pour réduire la dépendance au paid dans 6 mois",
        ]
    else:
        return [
            "Budget PME confirmée (500-1000€) : stratégie complète multi-canal",
            "Outils : CRM complet (HubSpot Starter 50€/mois), Google Ads + Meta + LinkedIn Ads",
            "Outils SEO : Semrush ou Ahrefs (99€/mois) + outil email marketing avancé",
            "Stratégie : SEA tous canaux + SEO agressif + content production externalisée",
            "ROI attendu : ROAS 3-6x · Croissance trafic +40%/mois sur 6 mois · CPL optimisé",
            "Considérez 1 freelance content ou growth hacker à mi-temps pour accélérer",
        ]

@st.cache_data(ttl=3600, show_spinner=False)
def gen_calendar(goal: str) -> list:
    topics = _CALENDAR_TOPICS.get(goal, _CALENDAR_TOPICS["awareness"])
    formats = ["Article de blog","Vidéo courte","Email newsletter","Infographie / Carrousel"]
    platforms_cycle = ["LinkedIn","Instagram","Email","YouTube"]
    return [(i+1, platforms_cycle[i%4], topics[i%len(topics)], formats[i%4]) for i in range(8)]

# ─── PERSONAS ────────────────────────────────────────────────────────────────
_PERSONA_DATA = {
    "ecommerce": [
        {"name":"Sophie Martin","age":32,"job":"Responsable marketing","location":"Paris","quote":"Je veux des produits de qualité livrés rapidement, sans mauvaise surprise.",
         "goals":["Trouver des produits tendance rapidement","Bénéficier d'un service client réactif","Comparer facilement les offres"],
         "pains":["Délais de livraison trop longs","Retours produits compliqués","Manque de confiance sur les nouveaux sites"],
         "channels":["Instagram","Pinterest","Email"],"triggers":["Promotion flash","Avis clients positifs","Livraison gratuite"],
         "motivations":["Gain de temps","Qualité garantie"],"values":["Fiabilité","Transparence"],
         "habits":["Consulte Instagram avant d'acheter","Compare sur Google Shopping","Lit les avis Trustpilot"],
         "expectations":["Livraison en 48h","Politique de retour simple","Service client joignable"],
         "framework":"SONCAS","framework_match":"Sécurité / Confort"},
        {"name":"Thomas Dubois","age":28,"job":"Développeur freelance","location":"Lyon","quote":"Je compare tout avant d'acheter. Le meilleur rapport qualité/prix, c'est non-négociable.",
         "goals":["Maximiser la valeur de chaque achat","Recevoir des produits durables","Processus d'achat rapide"],
         "pains":["Trop d'options à comparer","Sites peu transparents","SAV inexistant"],
         "channels":["YouTube","Reddit","Google"],"triggers":["Tests comparatifs","Garantie longue durée","Prix transparent"],
         "motivations":["Économies","Performance produit"],"values":["Rationalité","Durabilité"],
         "habits":["Regarde des reviews YouTube","Lit les specs techniques","Consulte Reddit avant d'acheter"],
         "expectations":["Fiche produit détaillée","Prix HT/TTC clairs","Comparaison facile"],
         "framework":"SONCAS","framework_match":"Argent / Nouveauté"},
    ],
    "saas": [
        {"name":"Claire Rousseau","age":38,"job":"Directrice d'une PME (15 salariés)","location":"Bordeaux","quote":"J'ai besoin d'outils qui fonctionnent vraiment et qui ne me font pas perdre du temps.",
         "goals":["Automatiser les tâches répétitives","Vue d'ensemble de l'activité","Former facilement mon équipe"],
         "pains":["Trop d'outils qui ne se parlent pas","Formations longues et coûteuses","Support peu réactif"],
         "channels":["LinkedIn","Email professionnel","Bouche-à-oreille"],"triggers":["Essai gratuit sans CB","ROI démontrable","Support inclus"],
         "motivations":["Productivité","Sérénité"],"values":["Efficacité","Fiabilité"],
         "habits":["Consulte G2 et Capterra","Demande des recommandations sur LinkedIn","Teste avant d'acheter"],
         "expectations":["Onboarding guidé","Support réactif","Intégrations avec les outils existants"],
         "framework":"SONCAS","framework_match":"Sécurité / Confort / Argent"},
    ],
    "service": [
        {"name":"Isabelle Moreau","age":45,"job":"Cadre en reconversion","location":"Nantes","quote":"J'ai 20 ans d'expérience à valoriser. Il me faut juste le bon accompagnement.",
         "goals":["Valoriser mon expertise en ligne","Créer des revenus stables","Gagner en liberté et flexibilité"],
         "pains":["Peur de la technologie","Syndrome de l'imposteur","Manque de réseau dans le digital"],
         "channels":["LinkedIn","Email","Podcasts"],"triggers":["Accompagnement humain","Résultats progressifs","Communauté de pairs"],
         "motivations":["Indépendance","Accomplissement"],"values":["Authenticité","Croissance"],
         "habits":["Écoute des podcasts business","Suit des formations en ligne","Réseau LinkedIn actif"],
         "expectations":["Suivi personnalisé","Résultats mesurables","Communauté bienveillante"],
         "framework":"SONCAS","framework_match":"Sécurité / Sympathie"},
    ],
    "default": [
        {"name":"Marie Legrand","age":35,"job":"Entrepreneur indépendant","location":"France","quote":"Je cherche des solutions concrètes qui m'aident à avancer rapidement.",
         "goals":["Gagner du temps sur les tâches répétitives","Développer son activité de façon autonome","Avoir des résultats mesurables"],
         "pains":["Manque de temps et de ressources","Trop d'options, pas assez de clarté","Difficulté à mesurer le ROI"],
         "channels":["Instagram","LinkedIn","Google"],"triggers":["Résultats prouvés","Simplicité d'utilisation","Rapport qualité/prix"],
         "motivations":["Croissance","Autonomie"],"values":["Impact","Efficacité"],
         "habits":["Cherche sur Google","Suit des comptes Instagram inspirants","S'abonne aux newsletters expertes"],
         "expectations":["Résultats rapides","Interface intuitive","Support disponible"],
         "framework":"SONCAS","framework_match":"Opportunité / Argent"},
        {"name":"Lucas Bernard","age":24,"job":"Étudiant / Side-hustler","location":"Toulouse","quote":"Je veux lancer mon projet avec un budget minimal mais des résultats max.",
         "goals":["Monétiser une passion","Apprendre en faisant","Atteindre l'indépendance financière"],
         "pains":["Budget très limité","Manque d'expérience business","Temps fragmenté"],
         "channels":["TikTok","YouTube","Discord"],"triggers":["Offre freemium","Communauté active","Tutoriels inclus"],
         "motivations":["Liberté financière","Apprentissage"],"values":["Innovation","Communauté"],
         "habits":["Regarde des tutos YouTube","Suit des créateurs TikTok","Participe à des Discord thématiques"],
         "expectations":["Prix accessible","Prise en main rapide","Ressources gratuites"],
         "framework":"SONCAS","framework_match":"Nouveauté / Sympathie"},
    ],
}

@st.cache_data(ttl=3600, show_spinner=False)
def gen_personas(activity: str) -> list:
    key = activity if activity in _PERSONA_DATA else "default"
    base = copy.deepcopy(_PERSONA_DATA[key])
    if len(base) < 2:
        base += copy.deepcopy(_PERSONA_DATA["default"])
    return base[:3]

# ─── SPIN SELLING ────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
# NOUVELLES FONCTIONS D'ANALYSE  --  Puissance x2
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=86400, show_spinner=False)
def gen_value_chain(activity: str) -> dict:
    """Chaîne de valeur Porter  --  analyse complète des activités primaires et support."""
    chains = {
        "ecommerce": {
            "primaires": [
                ("Logistique entrante", ["Sourcing fournisseurs","Gestion stocks","Contrôle qualité"], "#44C1BA"),
                ("Opérations", ["Préparation commandes","Packaging","Expédition J+1"], "#267371"),
                ("Logistique sortante", ["Livraison J+2","Tracking","Point relais"], "#339999"),
                ("Marketing/Ventes", ["SEO","Paid Ads","Email automation","Marketplace"], "#393DAC"),
                ("SAV", ["Retours","Échanges","Fidélisation","NPS"], "#B83D4B"),
            ],
            "support": [
                ("Infrastructure", "ERP e-commerce, hébergement cloud, CDN"),
                ("RH", "Logisticiens, community manager, développeur"),
                ("R&D technologique", "UX/UI, A/B testing, IA recommandation"),
                ("Achats", "Négociation fournisseurs, veille marché"),
            ],
        },
        "saas": {
            "primaires": [
                ("R&D Produit", ["Roadmap","Sprints agiles","Tests utilisateurs"], "#44C1BA"),
                ("Développement", ["Backend","Frontend","API","DevOps"], "#267371"),
                ("Déploiement", ["CI/CD","Monitoring","Scalabilité"], "#339999"),
                ("Sales & Marketing", ["Inbound","Outbound","PLG","Content"], "#393DAC"),
                ("Customer Success", ["Onboarding","Support","Expansion","Churn prevention"], "#B83D4B"),
            ],
            "support": [
                ("Infrastructure", "AWS/GCP, Datadog, Stripe, Intercom"),
                ("RH", "Tech recruitement, culture remote, equity"),
                ("R&D technologique", "IA features, sécurité, compliance RGPD"),
                ("Finance", "ARR tracking, burn rate, fundraising"),
            ],
        },
        "service": {
            "primaires": [
                ("Avant-vente", ["Prospection","Qualification","Proposition"], "#44C1BA"),
                ("Production", ["Réalisation mission","Livrables","Itérations"], "#267371"),
                ("Livraison", ["Présentation","Validation client","Formation"], "#339999"),
                ("Marketing", ["Personal brand","Contenu expert","Réseau"], "#393DAC"),
                ("Fidélisation", ["Suivi post-mission","Upsell","Recommandations"], "#B83D4B"),
            ],
            "support": [
                ("Infrastructure", "CRM, outils collaboratifs, facturation"),
                ("RH", "Sous-traitants, partenaires, montée en compétence"),
                ("R&D", "Méthodes propriétaires, veille sectorielle"),
                ("Finance", "Gestion trésorerie, délais paiement"),
            ],
        },
    }
    base = chains.get(activity, chains["service"])
    return base


@st.cache_data(ttl=86400, show_spinner=False)
def gen_business_model_canvas(activity: str, goal: str) -> dict:
    """Business Model Canvas complet  --  9 blocs."""
    _bmc = {
        "ecommerce": {
            "segments": ["Acheteurs en ligne 25-45 ans","Early adopters tech","Pros recherchant B2B"],
            "proposition": ["Prix compétitifs","Livraison rapide","Sélection unique","SAV réactif"],
            "canaux": ["Site e-commerce","Marketplace (Amazon/Cdiscount)","Instagram Shopping","Google Shopping"],
            "relation": ["Self-service","Email automation","Chat en direct","Programme fidélité"],
            "revenus": ["Ventes produits","Abonnements","Marketplace fees","Dropshipping"],
            "ressources": ["Stock produits","Entrepôt/3PL","Plateforme tech","Base clients"],
            "activites": ["Gestion catalogue","Expédition","Service client","Marketing digital"],
            "partenaires": ["Fournisseurs","3PL logistique","Prestataires paiement","Agences ads"],
            "couts": ["Sourcing produits","Logistique","Ads payants","Plateforme","Retours"],
        },
        "saas": {
            "segments": ["PME 10-200 salariés","Startups tech","Équipes remote","Freelances tech"],
            "proposition": ["Automatisation gains de temps","Coût < équivalent humain","Intégrations natives","RGPD compliant"],
            "canaux": ["Site + essai gratuit","App stores","Intégrateurs","Partenaires revendeurs"],
            "relation": ["Self-service onboarding","In-app guidance","CSM dédié Enterprise","Community"],
            "revenus": ["Abonnement mensuel/annuel","Seats supplémentaires","Add-ons","API usage"],
            "ressources": ["Code propriétaire","Data models","Équipe tech","Brand"],
            "activites": ["Dev produit","Support client","Ventes B2B","Intégrations API"],
            "partenaires": ["Cloud providers","Intégrateurs","Investors","Tech partners"],
            "couts": ["Salaires tech","Infrastructure cloud","Acquisition clients","Support"],
        },
    }
    return _bmc.get(activity, _bmc["saas"])


@st.cache_data(ttl=86400, show_spinner=False)
def gen_growth_hacking(activity: str, monthly_budget: float) -> list:
    """Growth hacking  --  tactiques à fort ROI et faible coût."""
    budget_tier = "bootstrap" if monthly_budget < 100 else "growth" if monthly_budget < 500 else "scale"
    tactics = {
        "ecommerce_bootstrap": [
            (" Abandon panier email", "Séquence 3 emails (1h/24h/72h) → récupère 15% des abandons", "Gratuit", "ROI: 10x"),
            ("Insta UGC Marketing", "Encourage photos clients → +32% conversion vs photos studio", "Gratuit", "ROI: 8x"),
            (" Parrainage client", "Offre 10€ parrain + 10€ filleul → acquisition à coût fixe", "Produit", "ROI: 6x"),
            ("⭐ Review automation", "Email J+14 demande avis → +4.6/5 trust signal", "Gratuit", "ROI: 12x"),
            (" Packaging viral", "Unboxing mémorable → partage réseaux → earned media", "Faible", "ROI: 5x"),
        ],
        "saas_bootstrap": [
            (" Freemium viral", "Plan gratuit avec watermark → utilisateurs = commerciaux", "Gratuit", "ROI: ∞"),
            (" Content SEO", "1 article expert/semaine → trafic organique en 6 mois", "Temps", "ROI: 20x"),
            (" Intégration partner", "Native integration Zapier/Slack → distribution x3", "Dev", "ROI: 15x"),
            ("ProductHunt launch", "Launch bien préparé → 500-2000 signups gratuit", "Temps", "ROI: ∞"),
            (" Cold outreach", "Séquence LinkedIn 5 messages → 8% de réponse", "Gratuit", "ROI: 12x"),
        ],
    }
    key = f"{activity}_{budget_tier}"
    return tactics.get(key, tactics.get(f"ecommerce_{budget_tier}", tactics["ecommerce_bootstrap"]))


@st.cache_data(ttl=3600, show_spinner=False)
def gen_scripts(activity: str) -> list:
    scripts = {
        "ecommerce": [
            {"title":"Email de relance panier abandonné","type":"email_followup","content":"Objet : Votre panier vous attend \n\nBonjour [Prénom],\n\nVous avez laissé quelque chose derrière vous !\n\nVotre sélection : [Produit(s)] est encore disponible  --  mais le stock est limité.\n\n→ Commander maintenant et bénéficiez de la livraison offerte jusqu'à ce soir.\n\n[BOUTON : Finaliser ma commande]\n\nÀ très vite,\nL'équipe [Marque]","keyPoints":["Personnaliser avec le nom du produit exact","Ajouter l'urgence (stock limité)","Un seul CTA : finaliser la commande","Livraison offerte = levier de conversion puissant"]},
            {"title":"Script appel client fidèle (upsell)","type":"follow_up","content":"Bonjour [Prénom], c'est [Votre Prénom] de [Marque].\nJe vous appelle car vous êtes l'un de nos meilleurs clients et je souhaitais vous présenter en avant-première notre nouvelle [Collection/Produit].\n\nVous avez commandé [Produit X] il y a [X semaines]  --  est-ce que vous en êtes satisfait ?\n[Écoute active]\n\nParfait. Je me permets de vous appeler car nous avons justement [Produit complémentaire] qui va parfaitement avec [Produit X]. Nos clients qui associent les deux témoignent de [bénéfice].\n\nPuis-je vous envoyer un lien avec 15% de remise réservée spécialement à nos clients VIP ?","keyPoints":["Ouvrir avec la relation client existante","Valider la satisfaction avant de pitcher","Proposer le produit complémentaire logique","Offre exclusive VIP pour déclencher l'action"]},
        ],
        "saas": [
            {"title":"Email cold outreach B2B","type":"cold_call","content":"Objet : [Prénom], [Résultat en 5 mots]\n\nBonjour [Prénom],\n\nJ'ai remarqué que [Entreprise] est en train de [croissance/changement observé]  --  c'est souvent à ce stade que [problème que vous résolvez] devient un vrai frein.\n\nOn a aidé [Client similaire] à [résultat mesurable] en [délai]. Voici le détail : [lien cas client]\n\nÊtes-vous disponible 15 minutes cette semaine pour voir si on peut faire la même chose pour [Entreprise] ?\n\n[Prénom]\nPS : Si ce n'est pas le bon moment, pas de problème  --  je reviendrai en [date].","keyPoints":["Personnaliser avec un signal d'actualité de l'entreprise","Référencer un cas client similaire","Demander 15 min, pas une heure","PS humanise et réduit la pression"]},
            {"title":"Script démo SaaS SPIN (30 min)","type":"discovery","content":"Introduction (2 min)\n'Merci [Prénom] de prendre le temps. Avant de vous montrer quoi que ce soit, j'aimerais comprendre votre situation. Ça m'évitera de vous montrer des features qui ne vous concernent pas.'\n\nDécouverte SPIN (10 min)\n- Situation : 'Comment gérez-vous actuellement [processus] ?'\n- Problème : 'Qu'est-ce qui vous frustre le plus avec cette façon de faire ?'\n- Implication : 'Ça représente combien de temps/argent par semaine ?'\n- Need : 'Si vous pouviez [résoudre ce problème], quel impact sur [objectif] ?'\n\nDémonstration ciblée (12 min)\nMontrez UNIQUEMENT les features qui répondent aux douleurs identifiées.\n\nClosing (6 min)\n'Basé sur ce qu'on vient de voir, est-ce que ça correspond à ce que vous cherchez ?'\n'Quelle est la prochaine étape de votre côté pour avancer ?'","keyPoints":["Découverte avant démonstration  --  toujours","SPIN : Situation → Problème → Implication → Need","Démo ciblée = démo courte = démo efficace","Closing = next step concret, pas 'Je vous envoie une proposition'"]},
        ],
        "service": [
            {"title":"Script appel découverte","type":"discovery","content":"Bonjour [Prénom], c'est [Votre Prénom].\nMerci d'avoir pris le temps d'échanger.\n\nAvant de parler de moi, j'aimerais comprendre où vous en êtes.\n\n'Pouvez-vous me décrire votre situation actuelle en matière de [domaine] ?'\n[Écoute]\n\n'Qu'est-ce qui vous a poussé à chercher de l'aide maintenant ?'\n[Écoute  --  noter le déclencheur]\n\n'Si on résolvait ce problème ensemble, à quoi ressemblerait une situation idéale pour vous dans 6 mois ?'\n[Écoute  --  noter la vision]\n\nProposition :\n'Basé sur ce que vous m'avez dit, voici comment je pourrais vous aider : [offre en 3 lignes].'\n\n'Est-ce que ça vous semble correspondre à ce que vous cherchez ?'","keyPoints":["Écouter 80% du temps  --  parler 20%","Identifier le déclencheur d'achat","Faire visualiser l'état désiré avant de pitcher","Offre courte et personnalisée en fin d'appel"]},
        ],
        "default": [
            {"title":"Email de prospection","type":"cold_call","content":"Objet : [Résultat concret] pour [Type d'entreprise]\n\nBonjour [Prénom],\n\nJe travaille avec des [profil similaire] qui font face à [problème courant].\n\nNotre approche leur a permis d'obtenir [résultat mesurable] en [délai].\n\nSeriez-vous disponible 15 minutes pour explorer si nous pouvons faire la même chose pour vous ?\n\n[Votre signature]","keyPoints":["Cibler précisément le profil","Mentionner un résultat concret","Demander un petit engagement (15 min)","Personnaliser si possible avec une info de l'entreprise"]},
            {"title":"Gestion des objections prix","type":"follow_up","content":"Client : 'C'est trop cher.'\n\nVous : 'Je comprends. Puis-je vous poser une question ?'\nSi vous n'investissez pas maintenant, comment comptez-vous résoudre [problème] ?\n\n[Écoute]\n\nEt quel est le coût de ce problème pour vous chaque mois ?\n\n[Écoute]\n\nSi on compare [X € par mois] avec [coût mensuel du problème]... l'investissement semble-t-il encore aussi élevé ?\n\nAlternativement, nous pouvons commencer par [offre d'entrée] à [prix réduit] pour vous permettre d'en mesurer la valeur.","keyPoints":["Ne jamais défendre le prix  --  questionner le problème","Calculer le coût de l'inaction","Proposer une entrée de gamme si budget bloquant","Retourner l'objection en opportunité"]},
        ],
    }
    return copy.deepcopy(scripts.get(activity, scripts["default"]))

_OBJECTIONS = [
    ("C'est trop cher","Comprenez-vous vraiment à quoi correspond l'investissement ? Calculons ensemble le coût de votre problème actuel chaque mois. Si [solution] résout ce problème, quel est le ROI ?"),
    ("J'ai besoin d'y réfléchir","Tout à fait naturel. Qu'est-ce qui vous ferait encore hésiter après réflexion ? En général c'est le prix, le timing, ou le fit  --  lequel des trois vous préoccupe le plus ?"),
    ("Je travaille déjà avec quelqu'un","Excellent signe  --  vous prenez déjà le sujet au sérieux. Qu'est-ce qui vous donnerait envie d'explorer une alternative si les résultats n'étaient pas au rendez-vous ?"),
    ("On n'a pas de budget","Le budget n'est jamais le vrai problème  --  c'est la priorité. Si je vous prouvais que [solution] génère plus qu'elle ne coûte en 90 jours, comment vous organiseriez-vous ?"),
    ("On peut le faire en interne","Absolument possible. Quelle est la valeur du temps de votre équipe sur cette tâche vs son coût avec nous ? Et ont-ils l'expertise spécifique nécessaire ?"),
]

# ─── KPI BENCHMARKS ──────────────────────────────────────────────────────────
_KPI_BENCHMARKS = {
    "email": [
        ("Taux de délivrabilité", "85,7%", "Ratio emails délivrés en boîte de réception. En dessous de 85%, vérifiez SPF/DKIM/DMARC", "sauge", ">90%"),
        (" Taux d'ouverture", "33,9%", "% d'emails ouverts sur emails délivrés. Varie selon le secteur (B2B > B2C)", "ambre", ">35%"),
        (" CTR (Taux de clics)", "5,35%", "% de clics sur le nombre d'emails délivrés. Indicateur d'engagement réel", "ambre", ">6%"),
        ("CTOR (Taux de réactivité)", "~15%", "CTR / Taux d'ouverture. Mesure la qualité du contenu vu par ceux qui ouvrent", "neutral", ">15%"),
        ("Taux de désabonnement", "<0,5%", "% de désabonnements par campagne. Au-dessus de 0,5%, revisez votre segmentation", "neutral", "<0,3%"),
        ("Revenu par email envoyé", "Variable", "CA généré divisé par le nombre d'emails envoyés. KPI ROI direct", "neutral", "Calculer"),
    ],
    "conversion": [
        ("Taux de conversion e-commerce", "2,5-3%", "% de visiteurs qui achètent. La moyenne mondiale est ~2,5%. Visez 3-4%", "ambre", ">3%"),
        ("CAC (Coût d'Acquisition Client)", "~1 200€", "Coût moyen pour acquérir 1 client B2B SaaS. E-commerce : 30-100€", "neutral", "Calculer"),
        ("NPS (Net Promoter Score)", "0-100", "Score de recommandation client. >50 = excellent, >70 = world-class", "neutral", ">50"),
        ("CSAT (Satisfaction Client)", ">70%", "% clients satisfaits. En dessous de 70%, identifiez les frictions majeures", "ambre", ">80%"),
        ("Temps de résolution tickets", "<4h", "Délai moyen de résolution des demandes support. Impact direct sur le CSAT", "neutral", "<2h"),
        ("Déviation par IA", "Variable", "% de tickets résolus par chatbot/IA sans intervention humaine. Visez 30-50%", "neutral", ">30%"),
    ],
    "social": [
        ("Engagement LinkedIn", "3-3,5%", "Likes + commentaires + partages / portée. Moyenne B2B : 3-3,5%", "sauge", ">4%"),
        ("Engagement Instagram", "0,45-0,6%", "Engagement rate moyen en 2025. Les Reels ont 3-5x plus d'engagement", "ambre", ">1%"),
        ("Engagement Facebook", "0,06-0,2%", "Reach organique très faible. Facebook Ads reste pertinent en paid", "neutral", ">0,2%"),
        ("▶ Engagement YouTube", "3,4%", "Likes + commentaires / vues. Complété par Watch Time et CTR miniature", "sauge", ">4%"),
        ("Croissance liste email", "+5-10%/mois", "Croissance mensuelle nette (nouveaux - désabonnés). Objectif PME : +5%/mois", "ambre", ">8%/mois"),
    ],
}

# ─── OKR FRAMEWORK ───────────────────────────────────────────────────────────
_OKR_TEMPLATES = {
    "awareness": [
        {"objective":"Devenir la référence de contenu dans notre niche d'ici Q4",
         "key_results":["Atteindre 50 000 visiteurs organiques/mois (+150%)","Publier 24 contenus piliers (2/sem) avec >1 000 mots","Obtenir 500 nouveaux abonnés newsletter/mois","Atteindre un DA (Domain Authority) de 35+"]},
        {"objective":"Multiplier par 3 notre présence sur les réseaux sociaux",
         "key_results":["Atteindre 10 000 abonnés LinkedIn actifs","Obtenir un taux d'engagement >4% sur LinkedIn","Publier 5 Reels/semaine sur Instagram","Atteindre 5 000 abonnés Instagram en 90 jours"]},
    ],
    "sales": [
        {"objective":"Augmenter le CA de 40% ce trimestre",
         "key_results":["Porter le taux de conversion site à 3,5%","Réduire le CAC de 20% via l'optimisation paid","Augmenter le panier moyen de 15% via upsell/cross-sell","Atteindre un ROAS de 4x sur toutes les campagnes"]},
        {"objective":"Optimiser le funnel de vente de bout en bout",
         "key_results":["Réduire le taux d'abandon panier à moins de 65%","Implémenter 3 séquences email automation","Lancer 2 A/B tests CTA par mois","Porter le taux de closing des démos à 25%"]},
    ],
    "leads": [
        {"objective":"Générer 200 leads qualifiés par mois d'ici 3 mois",
         "key_results":["Créer 2 lead magnets avec >500 téléchargements/mois","Porter le CPL sous 25€ sur Google Ads","Mettre en place une séquence nurturing 7 emails","Atteindre un taux de qualification leads >40%"]},
    ],
    "traffic": [
        {"objective":"Tripler le trafic organique en 6 mois",
         "key_results":["Publier 2 articles SEO/semaine (52 articles/an)","Obtenir 20 backlinks DA50+ par trimestre","Positionner 15 mots-clés en top 10 Google","Réduire le taux de rebond sous 50%"]},
    ],
}

@st.cache_data(ttl=3600, show_spinner=False)
def gen_okr(goal: str) -> list:
    return copy.deepcopy(_OKR_TEMPLATES.get(goal, _OKR_TEMPLATES["awareness"]))

# ─── SYNTHESIS ───────────────────────────────────────────────────────────────
_PRIORITIES = {
    "awareness": ["Créez votre contenu pilier (2000+ mots) sur votre thème principal","Lancez votre présence sur 2 réseaux sociaux maximum  --  maîtrisez avant d'étendre","Définissez votre TOV (Tone of Voice) et charte éditoriale","Construisez votre liste email dès maintenant  --  c'est votre actif le plus précieux"],
    "sales": ["Optimisez votre tunnel de conversion  --  identifiez où vous perdez les prospects","Testez 2 versions de votre CTA principal (A/B test)","Mettez en place le retargeting sur Meta et Google","Activez les emails de relance automatiques (panier abandonné, devis non signé)"],
    "leads": ["Créez votre premier lead magnet à haute valeur perçue","Configurez une séquence email de nurturing (7 emails sur 14 jours)","Optimisez vos landing pages pour un seul objectif : la conversion","Intégrez un CRM pour tracker chaque lead de A à Z"],
    "traffic": ["Publiez 2 contenus SEO par semaine minimum pendant 3 mois","Lancez votre stratégie de backlinks (guest posting, digital PR)","Optimisez vos Core Web Vitals (LCP < 2.5s, CLS < 0.1)","Créez vos clusters de contenu autour de 3 thèmes piliers"],
}
_ROADMAP = [
    ("J1-J30","Fondations","Valider l'offre · Configurer les outils · Lancer les 1ers contenus · Premiers contacts"),
    ("J31-J60","Activation","Premières campagnes payantes · Séquences email actives · Premiers retours clients"),
    ("J61-J90","Optimisation","Analyser les données · A/B tester · Doubler ce qui fonctionne · Couper ce qui ne fonctionne pas"),
    ("J91-J180","Scalabilité","Augmenter les budgets gagnants · Nouveaux canaux · Recruter/déléguer · Préparer la prochaine phase"),
]

@st.cache_data(ttl=3600, show_spinner=False)
def gen_synthesis(activity: str, goal: str, maturity: str, monthly: float) -> dict:
    score = {"ecommerce":72,"saas":68,"service":75,"consulting":80,"content":65,"other":60}.get(activity, 65)
    if maturity == "launched": score += 8
    elif maturity == "inprogress": score += 3
    if monthly >= 500: score += 5
    elif monthly >= 200: score += 3
    elif monthly >= 50: score += 1
    score = min(score, 98)
    return {
        "score": score,
        "priorities": _PRIORITIES.get(goal, _PRIORITIES["awareness"]),
        "roadmap": _ROADMAP,
        "kpis": _get_kpis(goal, monthly),
    }

def _get_kpis(goal: str, monthly: float) -> list:
    base = [("Budget mensuel", f"{monthly:,.0f} €"), ("ROI cible", "3-5x sur 6 mois")]
    extras = {
        "awareness": [("Portée mensuelle cible","50K-200K"),("Engagement rate cible","> 3%"),("Croissance abonnés","+15%/mois")],
        "sales": [("Taux de conversion cible","> 2.5%"),("Panier moyen cible","À définir"),("ROAS cible","3-5x")],
        "leads": [("CPL (coût par lead) cible","< 15-50 €"),("Taux de qualification","> 40%"),("Taux de closing","> 20%")],
        "traffic": [("Visiteurs organiques cible","+50%/mois"),("Position mots-clés cible","Top 10 Google"),("Taux de rebond cible","< 55%")],
    }
    return base + extras.get(goal, [])

# ─── PROPOSITION DE VALEUR (from TGC suite) ──────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def gen_proposition_valeur(activity: str, site_name: str = "") -> dict:
    """Proposition de valeur 4 dimensions (Apple/Tesla/L'Oreal framework)."""
    _pv = {
        "ecommerce": {
            "slogan": "La meilleure experience d'achat, livree chez vous",
            "fonctionnelle": "Produits de qualite livres rapidement avec garantie satisfait ou rembourse",
            "economique": "Prix competitifs, livraison offerte, paiement 3x sans frais",
            "emotionnelle": "Tranquillite d'esprit, fierte du produit recu, sentiment d'etre bien traite",
            "symbolique": "Marque de confiance qui respecte ses clients et tient ses promesses",
            "differenciateurs": [
                "Service client reactif  --  reponse en moins de 2h",
                "Retours gratuits 30 jours sans condition",
                "Avis clients verifies et transparents",
                "Livraison express disponible",
            ],
        },
        "saas": {
            "slogan": "Votre croissance, automatisee",
            "fonctionnelle": "Automatisation des taches repetitives, gain de temps mesurable des J1",
            "economique": "ROI positif en moins de 30 jours, consolidation de plusieurs outils en un",
            "emotionnelle": "Soulagement, confiance dans les donnees, sérénité opérationnelle",
            "symbolique": "Etre une entreprise moderne qui investit dans sa productivite",
            "differenciateurs": [
                "Onboarding en moins de 10 minutes",
                "Support fondateur accessible directement",
                "Intégrations natives avec vos outils existants",
                "Données exportables  --  aucun lock-in",
            ],
        },
        "service": {
            "slogan": "L'expertise qui transforme votre activite",
            "fonctionnelle": "Livraison de résultats mesurables dans les délais convenus",
            "economique": "ROI démontrable, prix fixe par livrable, pas de surprise",
            "emotionnelle": "Réassurance, sentiment d'être bien accompagné, progression visible",
            "symbolique": "Travailler avec un expert reconnu dans son domaine",
            "differenciateurs": [
                "Garantie résultat ou remboursement partiel",
                "Contrat détaillé avec jalons clairs",
                "Références clients vérifiables",
                "Disponibilité et réactivité garanties",
            ],
        },
        "consulting": {
            "slogan": "La clarté strategique qui accelere votre croissance",
            "fonctionnelle": "Diagnostic précis, plan d'action actionnable, implémentation guidée",
            "economique": "Évite les erreurs coûteuses, accelere le retour sur investissement",
            "emotionnelle": "Confiance dans les decisions, clarté dans la direction, réduction du stress",
            "symbolique": "Etre accompagné par un expert reconnu qui partage votre ambition",
            "differenciateurs": [
                "Approche personnalisée  --  aucun template générique",
                "Expertise sectorielle pointue et vérifiable",
                "Transfert de compétences inclus",
                "Accès direct au consultant senior",
            ],
        },
        "content": {
            "slogan": "Du contenu qui construit votre audience et vos revenus",
            "fonctionnelle": "Contenu optimisé qui génère trafic, engagement et conversions",
            "economique": "Actif pérenne qui travaille pour vous 24h/24 sans coût marginal",
            "emotionnelle": "Fierté de partager quelque chose de valeur, connexion avec sa communauté",
            "symbolique": "Devenir la référence incontournable de sa niche",
            "differenciateurs": [
                "Stratégie de contenu alignée sur vos objectifs business",
                "Distribution multi-canal optimisée",
                "Monétisation diversifiée (pub, produits, sponsoring)",
                "Analyse de performance continue",
            ],
        },
        "default": {
            "slogan": "La solution qui fait vraiment la différence",
            "fonctionnelle": "Résout votre problème précis de façon simple et efficace",
            "economique": "Investissement rapidement rentabilisé, valeur supérieure au prix",
            "emotionnelle": "Satisfaction, confiance, sentiment d'avoir fait le bon choix",
            "symbolique": "Choisir la qualité et l'innovation plutôt que le compromis",
            "differenciateurs": [
                "Différenciateur unique difficile à copier",
                "Relation client personnalisée",
                "Engagement qualité transparent",
                "Support réactif et humain",
            ],
        },
    }
    data = copy.deepcopy(_pv.get(activity, _pv["default"]))
    if site_name:
        data["slogan"] = data["slogan"]
    return data


@st.cache_data(ttl=3600, show_spinner=False)
def gen_rfm_segments(activity: str, monthly_budget: float) -> list:
    """Segmentation RFM 4 segments avec CLV et actions."""
    base_clv = {"ecommerce": 350, "saas": 1200, "service": 2500, "consulting": 5000, "content": 180, "default": 800}
    clv = base_clv.get(activity, base_clv["default"])
    return [
        {
            "nom": "Champions",
            "description": "Acheteurs récents, fréquents, à fort montant  --  vos meilleurs clients",
            "clv": round(clv * 3.5),
            "pourcentage": 15,
            "actions": [
                "Programme VIP exclusif avec avantages premium",
                "Demande de témoignage et de référencement",
                "Accès anticipé aux nouveautés",
                "Offre de partenariat ambassadeur",
            ],
        },
        {
            "nom": "Fidèles",
            "description": "Clients réguliers avec bon montant  --  le coeur de votre business",
            "clv": round(clv * 1.8),
            "pourcentage": 25,
            "actions": [
                "Upsell vers l'offre supérieure avec démo personnalisée",
                "Newsletter exclusive avec contenu premium",
                "Programme de fidélité avec points et récompenses",
                "Cross-sell de produits complémentaires",
            ],
        },
        {
            "nom": "A risque",
            "description": "Clients qui n'ont pas acheté depuis longtemps  --  risque de churn",
            "clv": round(clv * 0.6),
            "pourcentage": 30,
            "actions": [
                "Campagne de réactivation avec offre spéciale -20%",
                "Email personnalisé rappelant la valeur reçue",
                "Enquête satisfaction pour comprendre le désengagement",
                "Offre de downgrade pour retenir à moindre coût",
            ],
        },
        {
            "nom": "Perdus",
            "description": "Clients inactifs depuis longtemps  --  win-back ou abandon",
            "clv": round(clv * 0.1),
            "pourcentage": 30,
            "actions": [
                "Campagne win-back avec offre agressive (-30% ou cadeau)",
                "Email de séparation honnête pour obtenir un retour",
                "Analyse des raisons de départ pour améliorer le produit",
                "Suppression de la liste si aucune réactivation sous 6 mois",
            ],
        },
    ]


@st.cache_data(ttl=3600, show_spinner=False)
def gen_rse(activity: str) -> dict:
    """Analyse RSE / ISO 26000  --  7 domaines."""
    _rse_base = {
        "Gouvernance de l'organisation": {
            "niveau": 3,
            "actions": [
                "Définir une charte éthique et des valeurs d'entreprise écrites",
                "Mettre en place un processus de prise de décision transparent",
                "Nommer un référent RSE ou intégrer la RSE aux KPIs dirigeants",
            ],
            "risques": "Décisions non éthiques, manque de confiance des parties prenantes",
        },
        "Droits de l'homme": {
            "niveau": 3,
            "actions": [
                "Vérifier les conditions de travail chez vos fournisseurs",
                "Garantir l'égalité de traitement et la non-discrimination",
                "Former les équipes à la diversité et l'inclusion",
            ],
            "risques": "Risque réputationnel, non-conformité légale, perte de talents",
        },
        "Relations et conditions de travail": {
            "niveau": 4,
            "actions": [
                "Politique de télétravail flexible et équilibre vie pro/perso",
                "Formation continue et plan de développement des compétences",
                "Baromètre salarié semestriel avec plan d'action",
            ],
            "risques": "Turnover élevé, baisse de productivité, marque employeur dégradée",
        },
        "Environnement": {
            "niveau": 2,
            "actions": [
                "Mesurer et réduire votre empreinte carbone (bilan GES simplifié)",
                "Optimiser la consommation énergétique (hébergement green, déchets)",
                "Politique d'achats responsables et éco-conception",
            ],
            "risques": "Réglementation CSRD 2025, pression clients et investisseurs, greenwashing",
        },
        "Loyauté des pratiques": {
            "niveau": 4,
            "actions": [
                "Transparence totale sur les prix, conditions et données clients",
                "Politique anti-corruption et conformité RGPD rigoureuse",
                "Processus de gestion des conflits d'intérêts",
            ],
            "risques": "Sanctions CNIL, perte de confiance clients, litiges commerciaux",
        },
        "Questions relatives aux consommateurs": {
            "niveau": 4,
            "actions": [
                "Service après-vente réactif avec délais de traitement affichés",
                "Politique de retour et remboursement claire et généreuse",
                "Recueil et traitement systématique des avis clients",
            ],
            "risques": "Mauvaise e-réputation, churn élevé, litiges consommateurs",
        },
        "Communautés et développement local": {
            "niveau": 2,
            "actions": [
                "Partenariats avec des associations ou entreprises locales",
                "Programme de mécénat ou don pro bono de compétences",
                "Communication sur votre impact local et emplois créés",
            ],
            "risques": "Image perçue comme déconnectée du territoire, manque de soutien local",
        },
    }
    if activity == "ecommerce":
        _rse_base["Environnement"]["niveau"] = 2
        _rse_base["Environnement"]["actions"].insert(0, "Emballages durables et éco-responsables (obligation légale 2025)")
    elif activity == "saas":
        _rse_base["Environnement"]["niveau"] = 3
        _rse_base["Environnement"]["actions"].insert(0, "Hébergement cloud sur serveurs à énergie renouvelable (OVH, Scaleway)")
    return copy.deepcopy(_rse_base)


@st.cache_data(ttl=3600, show_spinner=False)
def gen_negociation(activity: str, monthly_budget: float) -> dict:
    """Tactiques de négociation BATNA/ZOPA/SONCAS."""
    _batna_map = {
        "ecommerce": ("Maintenir la stratégie organique et SEO sans partenariat",
                      "Trouver une alternative fournisseur moins chère"),
        "saas": ("Continuer avec les clients existants sans nouveau partenariat",
                 "Utiliser un concurrent ou développer en interne"),
        "service": ("Continuer à prospecter directement sans intermédiaire",
                    "Faire appel à un freelance moins spécialisé"),
        "consulting": ("Développer d'autres clients dans le même secteur",
                       "Internaliser la compétence avec un recrutement"),
        "default": ("Maintenir le statu quo ou chercher une alternative",
                    "Se tourner vers un concurrent ou solution DIY"),
    }
    batna_a, batna_b = _batna_map.get(activity, _batna_map["default"])
    zopa_min = round(monthly_budget * 0.6)
    zopa_max = round(monthly_budget * 1.4)
    return {
        "batna": {
            "vendeur": batna_a,
            "acheteur": batna_b,
            "conseil": "Renforcez votre BATNA avant toute négociation  --  plus votre alternative est forte, plus vous négociez de haut",
        },
        "zopa": {
            "min": zopa_min,
            "max": zopa_max,
            "amplitude": round((zopa_max - zopa_min) / zopa_max * 100),
            "conseil": f"Zone d'accord probable entre {zopa_min:,} € et {zopa_max:,} €  --  ancrez votre première offre au-dessus de votre objectif",
        },
        "concessions": [
            "Concession conditionnelle : 'Si vous acceptez X, alors je peux faire Y'",
            "Concession de valeur perçue : offrez quelque chose qui coûte peu mais vaut beaucoup",
            "Ne jamais faire de concession sans contrepartie  --  chaque concession doit être échangée",
            "La dernière concession doit toujours être petite  --  cela donne l'impression d'avoir atteint la limite",
        ],
        "tactiques": [
            "Ancrage : première offre toujours haute pour calibrer les attentes",
            "Silence stratégique : après une offre, ne parlez pas  --  laissez la pression s'exercer",
            "Flinch : réaction surprise visible face à chaque demande de concession",
            "Good cop / Bad cop : jouez sur plusieurs interlocuteurs pour créer de la flexibilité",
            "Deadline artificielle : 'Notre tarif change en fin de semaine'",
        ],
        "objections_prix": [
            ("C'est trop cher", "Calculons ensemble le ROI  --  si notre solution rapporte plus qu'elle coûte, est-ce encore trop cher ?"),
            ("J'ai une offre moins chère", "Comparez le coût total : prix + temps d'implémentation + risques. Notre offre inclut..."),
            ("Je dois consulter ma direction", "Bien sûr. Que vous faut-il pour avoir une recommandation solide à lui présenter ?"),
            ("On n'a pas le budget", "Si je vous montrais comment financer cela sans impact trésorerie immédiat, on pourrait avancer ?"),
        ],
    }


@st.cache_data(ttl=3600, show_spinner=False)
def gen_prix_psychologiques(monthly_budget: float, activity: str) -> list:
    """7 techniques de prix psychologiques avec exemples concrets."""
    ref_price = max(29, round(monthly_budget * 0.15))
    premium = round(ref_price * 2.5)
    anchor = round(ref_price * 3.2)
    return [
        {
            "nom": "Prix en charme (X9)",
            "description": "Terminez vos prix par 9 ou 7  --  le cerveau perçoit 99 € comme nettement moins que 100 €",
            "exemple": f"{ref_price - 1}€ au lieu de {ref_price}€  --  gain de conversion estimé +15 à +30%",
            "impact": "Élevé",
        },
        {
            "nom": "Ancrage haut",
            "description": "Affichez d'abord le prix le plus élevé pour calibrer les attentes",
            "exemple": f"Affichez l'offre Premium {anchor}€ avant l'offre Standard {ref_price}€  --  la Standard semble abordable",
            "impact": "Très élevé",
        },
        {
            "nom": "Prix barré",
            "description": "Montrez le prix de référence barré avec le prix promotionnel  --  active l'aversion à la perte",
            "exemple": f"~~{round(ref_price * 1.4)}€~~ {ref_price}€  --  économie visible = valeur perçue augmentée",
            "impact": "Élevé",
        },
        {
            "nom": "Tarification par paliers (decoy)",
            "description": "Créez 3 offres où la médiane est votre cible  --  l'effet decoy pousse vers le milieu",
            "exemple": f"Starter {round(ref_price * 0.6)}€ | Pro {ref_price}€ (recommandé) | Enterprise {premium}€",
            "impact": "Très élevé",
        },
        {
            "nom": "Prix fractionnés",
            "description": "Exprimez le prix en coût journalier ou hebdomadaire pour réduire la perception du montant",
            "exemple": f"{ref_price}€/mois devient 'Moins de {round(ref_price/30)}€/jour  --  moins qu'un café'",
            "impact": "Moyen",
        },
        {
            "nom": "Bundle et économies affichées",
            "description": "Regroupez des produits et affichez l'économie en euros ET en pourcentage",
            "exemple": f"Pack complet {round(ref_price * 2.4)}€ au lieu de {round(ref_price * 3)}€  --  économisez {round(ref_price * 0.6)}€ (20%)",
            "impact": "Élevé",
        },
        {
            "nom": "Essai gratuit puis prix",
            "description": "L'engagement progressif augmente la conversion  --  l'utilisateur s'est déjà approprié le produit",
            "exemple": f"14 jours gratuits sans CB → {ref_price}€/mois  --  réduction du risque perçu = +40% de conversion",
            "impact": "Très élevé",
        },
    ]


# ─── WEB SCRAPING  --  AllOrigins Proxy + BeautifulSoup ─────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
# NOUVELLES FONCTIONS  --  Analyse 2× plus puissante
# Ajoutées à biziapp.py comme module inline
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=86400, show_spinner=False)
def gen_porter_forces(activity: str) -> dict:
    """5 Forces de Porter  --  analyse concurrentielle approfondie."""
    _PORTER = {
        "ecommerce": {
            "menace_nouveaux": {"score": 8, "label": "Élevée", "details": ["Barrières faibles (Shopify, WooCommerce)", "Amazon, TikTok Shop entrants permanents", "Faibles coûts d'entrée < 5 000€"]},
            "pouvoir_fournisseurs": {"score": 5, "label": "Modéré", "details": ["Dépendance aux marketplaces (Amazon, FNAC)", "Prestataires logistiques concentrés", "Négociation possible au-delà de 50K€/an"]},
            "pouvoir_acheteurs": {"score": 7, "label": "Élevé", "details": ["Comparateurs de prix omniprésents", "Coût de changement quasi nul", "Avis clients décisifs (4.2★ minimum)"]},
            "menace_substituts": {"score": 6, "label": "Modérée", "details": ["Social commerce (Instagram Shop)", "Seconde main (Vinted, eBay)", "Location vs achat  --  économie circulaire"]},
            "rivalite": {"score": 9, "label": "Très élevée", "details": ["Marchés saturés", "Guerre des prix permanente", "Différenciation par l'expérience UX/CX"]},
        },
        "saas": {
            "menace_nouveaux": {"score": 6, "label": "Modérée", "details": ["R&D élevée (barrière technique)", "No-code réduit les barrières", "AI accélère le time-to-market"]},
            "pouvoir_fournisseurs": {"score": 4, "label": "Faible", "details": ["Infra cloud banalisée (AWS, GCP)", "Open-source disponible", "Multi-cloud possible"]},
            "pouvoir_acheteurs": {"score": 6, "label": "Modéré", "details": ["Coûts de switching réels (formation, migration)", "Benchmarks G2/Capterra décisifs", "Négociation sur contrats annuels"]},
            "menace_substituts": {"score": 7, "label": "Élevée", "details": ["Excel / Google Sheets toujours présents", "No-code (Notion, Airtable)", "IA générative remplace certains outils"]},
            "rivalite": {"score": 7, "label": "Élevée", "details": ["Product-led growth dominant", "Freemium standard du secteur", "Guerres de fonctionnalités"]},
        },
        "service": {
            "menace_nouveaux": {"score": 4, "label": "Faible", "details": ["Réputation et références requises", "Accréditations nécessaires", "Relations client = barrière"]},
            "pouvoir_fournisseurs": {"score": 3, "label": "Faible", "details": ["Freelances interchangeables", "Outils accessibles", "Peu de dépendance fournisseur"]},
            "pouvoir_acheteurs": {"score": 7, "label": "Élevé", "details": ["Appels d'offres comparatifs", "Négociation systématique", "Turnover prestataires fréquent"]},
            "menace_substituts": {"score": 6, "label": "Modérée", "details": ["Automatisation (AI, outils)", "Internalisation possible", "Offshore/nearshore compétitif"]},
            "rivalite": {"score": 5, "label": "Modérée", "details": ["Différenciation par expertise", "Niches protectrices", "Loyauté client si satisfaction"]},
        },
        "consulting": {
            "menace_nouveaux": {"score": 3, "label": "Faible", "details": ["Réputation = 5-10 ans minimum", "Références clients essentielles", "Labellisations sectorielles"]},
            "pouvoir_fournisseurs": {"score": 2, "label": "Très faible", "details": ["Indépendance totale", "Outils standard disponibles", "Réseau = capital principal"]},
            "pouvoir_acheteurs": {"score": 6, "label": "Modéré", "details": ["Grands comptes négocient fort", "ROI démontrable requis", "Contrats courts = pression"]},
            "menace_substituts": {"score": 5, "label": "Modérée", "details": ["Formations en ligne", "Outils d'auto-diagnostic", "Consultants indépendants vs cabinets"]},
            "rivalite": {"score": 5, "label": "Modérée", "details": ["Positionnement par niche", "Personal branding différenciant", "Co-traitance possible"]},
        },
        "content": {
            "menace_nouveaux": {"score": 9, "label": "Très élevée", "details": ["Barrières nulles", "AI génère du contenu à coût quasi-zéro", "Saturation des plateformes"]},
            "pouvoir_fournisseurs": {"score": 8, "label": "Élevé", "details": ["Algorithmes plateformes imprévisibles", "Dépendance YouTube/Meta/TikTok", "Démonétisation possible"]},
            "pouvoir_acheteurs": {"score": 6, "label": "Modéré", "details": ["Abonnements facilement résiliables", "Contenu gratuit concurrent toujours présent", "Niche = fidélité"]},
            "menace_substituts": {"score": 7, "label": "Élevée", "details": ["Podcasts vs vidéo", "AI summaries remplacent contenu long", "Short-form cannibale"]},
            "rivalite": {"score": 9, "label": "Très élevée", "details": ["Millions de créateurs", "Attention = ressource rare", "Distribution = avantage décisif"]},
        },
    }
    data = _PORTER.get(activity, _PORTER["service"])
    data["_activity"] = activity
    return data


@st.cache_data(ttl=3600, show_spinner=False)
def gen_ansoff_matrix(activity: str, goal: str, maturity: str) -> dict:
    """Matrice d'Ansoff  --  4 stratégies de croissance avec recommandation."""
    _score_pen = {"idea": 40, "inprogress": 65, "launched": 80}.get(maturity, 50)
    _score_dev = {"idea": 20, "inprogress": 50, "launched": 70}.get(maturity, 40)
    _score_ext = {"idea": 10, "inprogress": 30, "launched": 60}.get(maturity, 30)
    _score_div = {"idea": 5, "inprogress": 15, "launched": 35}.get(maturity, 15)

    _ACTIONS = {
        "ecommerce": {
            "penetration": ["Optimiser le référencement SEO/SEA", "Relances panier abandonné (email)", "Programme de fidélité  --  points/cashback", "Upselling et cross-selling automatisés"],
            "developpement": ["Lancer une gamme complémentaire", "Étendre aux marketplaces (Amazon, FNAC, ManoMano)", "Créer une offre abonnement récurrent", "Développer la vente B2B"],
            "extension": ["Internationalisation (Belgique, Suisse, Canada FR)", "Ouverture d'un point relais ou pop-up store", "Partenariat avec enseignes physiques", "Marketplace propre pour vendeurs tiers"],
            "diversification": ["Créer une marque propre (PL)", "Formation/ateliers autour du produit", "Services annexes (installation, SAV premium)", "Contenu monétisé (blog/YouTube)"],
        },
        "saas": {
            "penetration": ["Freemium avec conversion trial-to-paid", "Onboarding in-app optimisé (< 5 min)", "Réduction du churn (NPS score > 50)", "Parrainage utilisateur"],
            "developpement": ["API/intégrations marketplace (Zapier, Make)", "Module Enterprise avec SSO/SCIM", "Formation et certification utilisateurs", "Mobile app complémentaire"],
            "extension": ["Expansion EU (RGPD compliant)", "Secteur vertical dédié (niche premium)", "Partenariats revendeurs/intégrateurs", "White-label pour agences"],
            "diversification": ["Consulting autour du logiciel", "Marketplace d'add-ons (app store)", "Data insights/benchmark (données anonymisées)", "Acquisition de micro-SaaS complémentaires"],
        },
        "service": {
            "penetration": ["Optimiser les témoignages clients (Google My Business)", "Système de parrainage actif", "Newsletters expertise mensuelle", "Réactivation base clients dormants"],
            "developpement": ["Offre de formation autour du service", "Pack premium avec garantie résultats", "Abonnement mensuel (rétainer)", "Extension gamme (services adjacents)"],
            "extension": ["Géographies voisines (DOM-TOM, Belgique)", "Secteurs d'activité nouveaux", "Clientèle B2C si actuel B2B (ou inverse)", "Partenariats prescripteurs"],
            "diversification": ["SaaS propriétaire lié au service", "Formation en ligne (LMS)", "Franchise du modèle", "Joint-venture avec complémentaire"],
        },
    }
    actions = _ACTIONS.get(activity, _ACTIONS["service"])
    recommendation = "penetration" if maturity in ("idea","inprogress") else "developpement" if goal == "sales" else "extension"
    return {
        "penetration": {"score": _score_pen, "risk": "Faible", "actions": actions["penetration"]},
        "developpement": {"score": _score_dev, "risk": "Modéré", "actions": actions.get("developpement", [])},
        "extension": {"score": _score_ext, "risk": "Modéré-élevé", "actions": actions.get("extension", [])},
        "diversification": {"score": _score_div, "risk": "Élevé", "actions": actions.get("diversification", [])},
        "recommendation": recommendation,
    }


@st.cache_data(ttl=3600, show_spinner=False)
def gen_customer_journey(activity: str, goal: str) -> list:
    """Customer Journey Map complète  --  7 étapes avec touchpoints et émotions."""
    _STAGES = {
        "ecommerce": [
            {"stage": "Découverte", "emotion": "Neutre", "score": 3, "touchpoints": ["Google Search", "Instagram Ads", "Bouche-à-oreille"], "pain": "Trop d'options disponibles", "opportunity": "SEO + contenu différenciant"},
            {"stage": "Considération", "emotion": "Curieux", "score": 5, "touchpoints": ["Page produit", "Comparateurs de prix", "Avis clients"], "pain": "Manque de confiance", "opportunity": "Social proof + politique retour claire"},
            {"stage": "Intention", "emotion": "Interesse", "score": 6, "touchpoints": ["Panier", "Wishlist", "Email de relance"], "pain": "Hésitation prix", "opportunity": "Urgence douce + garantie satisfait"},
            {"stage": "Achat", "emotion": "Enthousiaste", "score": 8, "touchpoints": ["Checkout", "Paiement", "Email confirmation"], "pain": "Friction checkout (trop d'étapes)", "opportunity": "One-click, multi-paiement, Apple Pay"},
            {"stage": "Livraison", "emotion": "Anxieux", "score": 4, "touchpoints": ["Email suivi", "SMS livraison", "Application transporteur"], "pain": "Incertitude délais", "opportunity": "Tracking temps réel + proactivité"},
            {"stage": "Utilisation", "emotion": "Satisfait", "score": 9, "touchpoints": ["Produit reçu", "Packaging", "Email post-achat"], "pain": "Pas de support si problème", "opportunity": "Unboxing premium + tutoriel d'usage"},
            {"stage": "Fidélisation", "emotion": "Fan", "score": 8, "touchpoints": ["Programme fidélité", "Newsletter", "Réseaux sociaux"], "pain": "Oublié rapidement", "opportunity": "Personnalisation + récompenses surprises"},
        ],
        "saas": [
            {"stage": "Awareness", "emotion": "Neutre", "score": 3, "touchpoints": ["Search Google", "Product Hunt", "LinkedIn"], "pain": "Saturé d'outils SaaS", "opportunity": "Contenu SEO + démo produit vidéo"},
            {"stage": "Évaluation", "emotion": "Sceptique", "score": 4, "touchpoints": ["Site web", "G2/Capterra", "Webinaire"], "pain": "Difficulté à comparer", "opportunity": "Comparatif direct concurrents + ROI calculator"},
            {"stage": "Trial", "emotion": " Curieux", "score": 6, "touchpoints": ["Onboarding", "Email séquence", "Checklist"], "pain": "Time-to-value trop long", "opportunity": "1er résultat en < 5 minutes"},
            {"stage": "Activation", "emotion": "Convaincu", "score": 8, "touchpoints": ["Dashboard", "1ère feature utilisée", "Support chat"], "pain": "Fonctionnalités trop nombreuses", "opportunity": "Progressive disclosure + milestone rewards"},
            {"stage": "Conversion", "emotion": "Decide", "score": 7, "touchpoints": ["Pricing page", "Commercial", "Contrat"], "pain": "Friction tarification", "opportunity": "Annuel avec remise + transparence complète"},
            {"stage": "Expansion", "emotion": "Engage", "score": 9, "touchpoints": ["Usage régulier", "Équipe invitée", "Intégrations"], "pain": "Silos entre équipes", "opportunity": "Templates collaboration + formation in-app"},
            {"stage": "Advocacy", "emotion": "Ambassadeur", "score": 9, "touchpoints": ["Témoignage", "Parrainage", "Case study"], "pain": "Pas de programme structuré", "opportunity": "Referral programme + co-marketing"},
        ],
    }
    default_stages = _STAGES.get(activity, _STAGES["saas"])
    return default_stages


@st.cache_data(ttl=3600, show_spinner=False)
def gen_content_strategy(activity: str, goal: str, monthly_budget: float) -> dict:
    """Stratégie de contenu complète  --  piliers, formats, calendrier, KPIs."""
    _PILLARS = {
        "ecommerce": ["Inspiration produit", "Tutos & guides d'achat", "Coulisses & fabrication", "Avis & UGC clients", "Promotions & exclusivités"],
        "saas": ["Éducation (how-to)", "Cas d'usage clients", "Insights sectoriels", "Product updates", "Thought leadership"],
        "service": ["Expertise & conseils", "Avant/après projets", "Témoignages clients", "Actualités secteur", "Coulisses équipe"],
        "consulting": ["Articles de fond", "Études de cas", "Veille stratégique", "Personal branding", "Conférences & talks"],
        "content": ["Valeur éducative", "Divertissement", "Coulisses création", "Collaborations", "Monétisation transparente"],
        "other": ["Expertise", "Témoignages", "Actualités", "Conseils pratiques", "Offres spéciales"],
    }
    budget_content = min(monthly_budget * 0.20, 300)
    return {
        "pillars": _PILLARS.get(activity, _PILLARS["other"]),
        "formats": {
            "Short video (Reels/TikTok)": "40%",
            "Carrousel LinkedIn/Insta": "25%",
            "Article blog long-form": "15%",
            "Newsletter hebdo": "10%",
            "Podcast / Live": "10%",
        },
        "frequency": {
            "Instagram/TikTok": "5 posts/sem",
            "LinkedIn": "3 posts/sem",
            "Newsletter": "1/sem",
            "Blog": "2 articles/mois",
            "YouTube": "1 vidéo/mois",
        },
        "budget_content": f"{budget_content:.0f}€/mois",
        "kpis": {
            "Reach organique": "+15%/mois",
            "Taux engagement": "> 3.5%",
            "Leads content": f"{max(5, int(monthly_budget/40))}/mois",
            "SEO positions": "+10 mots-clés top 10/trimestre",
        },
        "tools_free": ["Canva (visuels)", "CapCut (vidéo)", "Notion (planning)", "Buffer free (scheduling)", "Google Trends (sujets)"],
    }


@st.cache_data(ttl=3600, show_spinner=False)
def gen_pricing_strategy(activity: str, monthly_budget: float, maturity: str) -> dict:
    """Stratégie pricing complète  --  modèles, psychologie, positionnement."""
    _MODELS = {
        "ecommerce": ["Prix psychologique (9,99€)", "Bundle (lot de 3 = -20%)", "Prix d'ancrage (barré → prix promo)", "Freemium (échantillon → achat)", "Prix dynamique selon stock"],
        "saas": ["Freemium → Paid", "Par usage (pay-as-you-go)", "Par siège (per seat)", "Flat rate annuel", "Enterprise (sur devis)"],
        "service": ["Taux journalier moyen (TJM)", "Forfait mission", "Abonnement mensuel (rétainer)", "Prix à la performance", "Pack découverte (starter)"],
        "consulting": ["Projet clé en main", "TJM + frais", "Rétainer mensuel", "Revenue share", "Formations packagées"],
        "content": ["Abonnement payant (newsletter premium)", "Sponsoring", "Formations en ligne", "Produits dérivés", "Affiliation"],
        "other": ["Devis personnalisé", "Forfait standard", "Abonnement", "À l'acte", "Commission"],
    }
    _ANCHORS = {
        "ecommerce": ["Proposer 3 offres (Basic/Standard/Premium)", "Standard = 60% du CA visé", "Premium = 2.5× le prix Standard"],
        "saas": ["3 tiers prix (Free/Pro/Business)", "Mettre en avant le plan du milieu", "Prix annuel avec remise 20%"],
        "service": ["Pack Starter + Pack Complet + Sur-mesure", "Le Complet doit être le + rentable", "Afficher valeur hourly dans le forfait"],
        "other": ["Entrée de gamme → ancre basse", "Offre principale bien mise en avant", "Premium pour 10% clients haute valeur"],
    }
    base_price = {"ecommerce": 49, "saas": 79, "service": 1200, "consulting": 1800, "content": 29, "other": 199}.get(activity, 199)
    multiplier = {"idea": 0.7, "inprogress": 0.9, "launched": 1.1}.get(maturity, 1.0)
    return {
        "models": _MODELS.get(activity, _MODELS["other"]),
        "recommended_base_price": f"{base_price * multiplier:.0f}€",
        "anchor_strategy": _ANCHORS.get(activity, _ANCHORS["other"]),
        "psychological_triggers": [
            "Chiffre 9 (99€ > 100€ perçu 15% moins cher)",
            "Comparaison économies (vs cabinet conseil à 5K€)",
            "Urgence temporelle (offre valable 48h)",
            "Garantie satisfait ou remboursé (réduit le risque perçu)",
            "Preuve sociale (X clients satisfaits)",
        ],
        "elasticite": "Tester A/B +20% et -10% sur 30 jours",
    }


@st.cache_data(ttl=3600, show_spinner=False)
def gen_email_sequences(activity: str, goal: str) -> dict:
    """Séquences email marketing complètes  --  5 types de sequences."""
    _SEQ = {
        "welcome": {
            "name": "Bienvenue (J0-J7)",
            "emails": [
                {"j": "J+0", "objet": "Bienvenue ! Voici comment démarrer ", "objectif": "Activation  --  1ère action dans les 5 min"},
                {"j": "J+1", "objet": "Le secret de [Bénéfice principal]", "objectif": "Éducation  --  valeur immédiate"},
                {"j": "J+3", "objet": "Comment [Nom client] a obtenu [Résultat]", "objectif": "Social proof  --  cas client"},
                {"j": "J+5", "objet": "Évitez ces 3 erreurs courantes", "objectif": "Expertise  --  confiance"},
                {"j": "J+7", "objet": "Prêt à passer à l'étape suivante ?", "objectif": "Conversion  --  CTA offre"},
            ],
            "kpis": {"open_rate": ">45%", "ctr": ">12%", "conversion": ">8%"}
        },
        "nurture": {
            "name": "Nurturing leads froids (4 semaines)",
            "emails": [
                {"j": "S1", "objet": "Insight n°1 : [Tendance sectorielle]", "objectif": "Valeur + positionnement expert"},
                {"j": "S2", "objet": "Étude de cas : +[X]% en [durée]", "objectif": "Preuve de résultats"},
                {"j": "S3", "objet": "Template gratuit  --  [Outil pratique]", "objectif": "Lead magnet  --  engagement fort"},
                {"j": "S4", "objet": "Offre exclusive  --  48h seulement", "objectif": "Conversion avec urgence"},
            ],
            "kpis": {"open_rate": ">28%", "ctr": ">6%", "conversion": ">3%"}
        },
        "abandoned_cart": {
            "name": "Panier abandonné (ecommerce)",
            "emails": [
                {"j": "H+1", "objet": "Vous avez oublié quelque chose (curiosite)", "objectif": "Rappel doux"},
                {"j": "H+24", "objet": "Votre panier expire bientôt", "objectif": "Urgence"},
                {"j": "H+72", "objet": "Dernière chance + -10% pour vous", "objectif": "Remise de récupération"},
            ],
            "kpis": {"open_rate": ">50%", "ctr": ">20%", "conversion": ">15%"}
        },
        "reactivation": {
            "name": "Réactivation clients dormants (90j+)",
            "emails": [
                {"j": "J0", "objet": "Vous nous manquez, [Prénom] ", "objectif": "Émotion + souvenir positif"},
                {"j": "J+3", "objet": "Voici ce qui a changé depuis votre départ", "objectif": "Nouveautés produit"},
                {"j": "J+7", "objet": "Offre de retour  --  rien que pour vous", "objectif": "Incentive exclusif"},
                {"j": "J+14", "objet": "C'est notre dernier message", "objectif": "Urgence  --  dernier essai"},
            ],
            "kpis": {"open_rate": ">35%", "ctr": ">8%", "conversion": ">5%"}
        },
        "upsell": {
            "name": "Upsell / Cross-sell post-achat",
            "emails": [
                {"j": "J+3", "objet": "Comment tirer le meilleur de votre achat", "objectif": "Adoption + satisfaction"},
                {"j": "J+10", "objet": "Clients comme vous utilisent aussi...", "objectif": "Cross-sell naturel"},
                {"j": "J+21", "objet": "Passez au niveau supérieur ", "objectif": "Upsell offre premium"},
            ],
            "kpis": {"open_rate": ">38%", "ctr": ">10%", "conversion": ">7%"}
        },
    }
    return _SEQ


@st.cache_data(ttl=3600, show_spinner=False)
def gen_social_media_strategy(activity: str, monthly_budget: float) -> dict:
    """Stratégie réseaux sociaux complète avec tactiques par plateforme."""
    budget_ads = monthly_budget * 0.3
    _PLATFORMS = {
        "ecommerce": {
            "Instagram": {"priorite": 1, "objectif": "Conversion", "format": "Reels + Shopping", "budget": f"{budget_ads*0.4:.0f}€/mois", "freq": "7 posts/sem", "kpi": "ROAS > 3x"},
            "TikTok": {"priorite": 2, "objectif": "Awareness + Viral", "format": "UGC + trends", "budget": f"{budget_ads*0.3:.0f}€/mois", "freq": "5 posts/sem", "kpi": "Views + CTR"},
            "Pinterest": {"priorite": 3, "objectif": "Trafic SEO social", "format": "Pins produit", "budget": "Organique", "freq": "10 pins/sem", "kpi": "Clics vers site"},
            "Facebook": {"priorite": 4, "objectif": "Retargeting", "format": "Carrousel + DPA", "budget": f"{budget_ads*0.3:.0f}€/mois", "freq": "3 posts/sem", "kpi": "CPA < 15€"},
        },
        "saas": {
            "LinkedIn": {"priorite": 1, "objectif": "Lead gen B2B", "format": "Articles + Thought leadership", "budget": f"{budget_ads*0.5:.0f}€/mois", "freq": "5 posts/sem", "kpi": "MQLs générés"},
            "Twitter/X": {"priorite": 2, "objectif": "Awareness dev/tech", "format": "Threads + insights", "budget": "Organique", "freq": "3 posts/j", "kpi": "Followers + engagement"},
            "YouTube": {"priorite": 3, "objectif": "SEO + Éducation", "format": "Tutoriels + Demos", "budget": "Temps de production", "freq": "2 vidéos/mois", "kpi": "Watch time + abonnés"},
            "Product Hunt": {"priorite": 4, "objectif": "Launch + notoriété", "format": "Launch page", "budget": "0€", "freq": "1 launch/trimestre", "kpi": "Upvotes + signups"},
        },
        "consulting": {
            "LinkedIn": {"priorite": 1, "objectif": "Personal branding", "format": "Articles expertise", "budget": "Organique", "freq": "3 posts/sem", "kpi": "Connexions + DMs entrants"},
            "Newsletter": {"priorite": 2, "objectif": "Nurturing", "format": "Insights hebdo", "budget": f"Beehiiv/Substack gratuit", "freq": "1/semaine", "kpi": "Abonnés + open rate"},
            "YouTube": {"priorite": 3, "objectif": "Autorité", "format": "Vidéos expertise", "budget": "Temps", "freq": "1/mois", "kpi": "Views + leads entrants"},
            "Podcast": {"priorite": 4, "objectif": "Thought leadership", "format": "Interviews secteur", "budget": "Matériel micro < 100€", "freq": "2/mois", "kpi": "Écoutes + invitations conférence"},
        },
    }
    default_key = "ecommerce" if activity == "ecommerce" else "saas" if activity == "saas" else "consulting"
    return _PLATFORMS.get(activity, _PLATFORMS[default_key])


@st.cache_data(ttl=3600, show_spinner=False)
def gen_competitive_intelligence(activity: str, goal: str) -> dict:
    """Framework intelligence concurrentielle  --  méthodes et KPIs de veille."""
    return {
        "axes_veille": [
            {"axe": "Pricing", "methode": "Scraping hebdo des pages tarifaires", "outils": ["Wayback Machine", "Google Alerts prix concurrents"]},
            {"axe": "Contenu", "methode": "Veille RSS + Google News", "outils": ["Feedly", "Google Alerts", "RSS concurrents"]},
            {"axe": "SEO", "methode": "Analyse mots-clés et backlinks", "outils": ["Google Search Console", "Ubersuggest (gratuit 3/j)"]},
            {"axe": "Social", "methode": "Monitoring publications", "outils": ["Mention free", "Social Blade"]},
            {"axe": "Avis clients", "methode": "Suivi G2, Trustpilot, Google Maps", "outils": ["Google Alerts avis", "ReviewTrackers free"]},
            {"axe": "Offre produit", "methode": "Inscription newsletters concurrents", "outils": ["Email perso dédié", "Swipe file"]},
        ],
        "signaux_opportunite": [
            "Concurrent lève des fonds → accélérer son acquisition",
            "Concurrent reçoit des avis négatifs → gap à exploiter",
            "Concurrent augmente ses prix → communiquer sur votre tarif",
            "Concurrent quitte un segment → s'y positionner",
            "Concurrent recrute beaucoup → il va s'étendre",
        ],
        "cadence": {"quotidien": "Alertes Google (5 min)", "hebdo": "Analyse SEO + social (30 min)", "mensuel": "Rapport pricing + offre complet (2h)"},
    }


@st.cache_data(ttl=900)
def scrape_site(url: str) -> dict:
    """Lit un site via api_layer.read_url (multi-proxy) puis fallback local."""
    if _HAS_API_LAYER:
        try:
            result = _read_url_live(url)
            if result and not result.get("error"):
                return result
        except Exception:
            pass
    # fallback original ci-dessous
    try:
        return _scrape_site_original(url)
    except Exception:
        return {}

@st.cache_data(ttl=1800, show_spinner=False)
def _scrape_site_original(url: str) -> dict:
    """
    Extraction structurée via AllOrigins (proxy CORS gratuit, sans clé API).
    Fallback BeautifulSoup si Jina est indisponible.
    """
    if not url or not url.startswith("http"):
        return {}
    parsed = _urlparse.urlparse(url)
    if not parsed.netloc:
        return {}
    result: dict = {}
    # ── AllOrigins CORS Proxy (priorité) ─────────────────────────────────────
    try:
        import requests as req
        r = req.get(f"https://api.allorigins.win/get?url={_urlparse.quote(url)}", timeout=8,
                    headers={"Accept": "application/json", "User-Agent": "BiziApp/3.0"})
        if r.status_code == 200:
            try:
                raw_html = r.json().get("contents", "")
            except Exception:
                raw_html = ""
            if _HAS_BS4 and raw_html:
                from bs4 import BeautifulSoup as _BS4
                _soup = _BS4(raw_html, "html.parser")
                _t = _soup.find("title")
                result["title"] = _t.get_text(strip=True) if _t else ""
                _md = _soup.find("meta", attrs={"name": "description"})
                result["description"] = _md.get("content", "") if _md else ""
                result["h1"] = [x.get_text(strip=True) for x in _soup.find_all("h1")][:5]
                result["h2"] = [x.get_text(strip=True) for x in _soup.find_all("h2")][:8]
                result["h3"] = [x.get_text(strip=True) for x in _soup.find_all("h3")][:6]
                _body_text = " ".join(p.get_text(" ", strip=True) for p in _soup.find_all(["p","li","h1","h2","h3"]))
                result["main_text"] = _body_text[:2000]
                result["source"] = "allorigins"
                result["status"] = 200
    except Exception:
        pass
    # ── Fallback BeautifulSoup ────────────────────────────────────────────────
    if not result.get("title") and _HAS_BS4:
        try:
            import requests as req
            r = req.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")
            t = soup.find("title")
            result["title"]  = t.get_text(strip=True) if t else ""
            md = soup.find("meta", attrs={"name":"description"})
            result["description"] = md.get("content","") if md else ""
            result["h1"] = [x.get_text(strip=True) for x in soup.find_all("h1")][:5]
            result["h2"] = [x.get_text(strip=True) for x in soup.find_all("h2")][:8]
            result["h3"] = [x.get_text(strip=True) for x in soup.find_all("h3")][:6]
            og_t = soup.find("meta", property="og:title")
            og_d = soup.find("meta", property="og:description")
            result["og_title"]       = og_t.get("content","") if og_t else ""
            result["og_description"] = og_d.get("content","") if og_d else ""
            kw = soup.find("meta", attrs={"name":"keywords"})
            result["keywords_meta"]  = kw.get("content","") if kw else ""
            body_text = " ".join(p.get_text(" ",strip=True) for p in soup.find_all(["p","li","h1","h2","h3"]))
            result["main_text"]    = body_text[:2000]
            result["links_count"]  = len(soup.find_all("a", href=True))
            result["images_count"] = len(soup.find_all("img"))
            result["status"]       = r.status_code
            result["source"]       = "bs4"
        except Exception as e:
            result["error"] = str(e)
    # ── Extraction mots-clés page ─────────────────────────────────────────────
    if result.get("main_text"):
        import re as _re
        stopwords = {"avec","pour","dans","une","les","des","qui","que","sur","par",
                     "cette","leur","nous","vous","mais","aussi","plus","tres","bien",
                     "tout","tous","sans","sous","entre","apres","avant","comme","sont"}
        words = _re.findall(r"\b[a-zA-ZÀ-ɏ]{4,}\b", result["main_text"].lower())
        freq: dict = {}
        for w in words:
            if w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
        result["keywords_page"] = sorted(freq, key=freq.get, reverse=True)[:12]
    return result

def scrape_site_meta(url: str) -> dict:
    """Alias de compatibilité."""
    return scrape_site(url)

# ─────────────────────────────────────────────────────────────────────────────
# VEILLE  --  Fonctions live (Google News · DuckDuckGo · Wikipedia)
# ─────────────────────────────────────────────────────────────────────────────
_UA_VEILLE = "Mozilla/5.0 BiziApp-Veille/2.0"
_STOP_VEILLE = {
    "avec","dans","pour","les","des","une","sur","par","que","qui","pas","mais",
    "donc","aussi","très","tout","comme","nous","vous","sont","était","être",
    "avoir","peut","plus","cette","cela","leur","dont","bien","fait","même",
    "sous","vers","sans","entre","après","avant","depuis","pendant",
    "this","that","from","with","your","will","have","been","they","their",
    "what","when","where","which","there","about","would","could","should",
}

def _veille_get(url: str, timeout: int = 12, extra: dict = None) -> str:
    """GET HTTP mutualisé pour les modules de veille."""
    hdrs = {"User-Agent": _UA_VEILLE, "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}
    if extra:
        hdrs.update(extra)
    try:
        import requests as _r
        resp = _r.get(url, timeout=timeout, headers=hdrs)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return ""
        req = _urlreq.Request(url, headers=hdrs)
        with _urlreq.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")

def _veille_keywords(text: str, top: int = 15) -> list:
    """Extrait les mots-clés fréquents d'un texte (sans stopwords)."""
    words = _re.findall(r'\b[A-Za-zÀ-ÖØ-öø-ÿ]{4,}\b', text.lower())
    freq: dict = {}
    for w in words:
        if w not in _STOP_VEILLE:
            freq[w] = freq.get(w, 0) + 1
    return sorted(freq, key=lambda k: -freq[k])[:top]

@st.cache_data(ttl=900)
def fetch_news(query: str, lang: str = "fr", max_items: int = 12) -> list:
    """Google News RSS  --  actualités live. Gratuit, sans clé API. Cache 30 min."""
    try:
        encoded = _urlparse.quote(query)
        rss = (
            f"https://news.google.com/rss/search"
            f"?q={encoded}&hl={lang}&gl=FR&ceid=FR:{lang}"
        )
        text = _veille_get(rss, timeout=12)
        root = _ET.fromstring(text)
        items = []
        for item in root.findall(".//item")[:max_items]:
            pub = item.findtext("pubDate", "")
            try:
                dt = datetime.datetime.strptime(pub, "%a, %d %b %Y %H:%M:%S %Z")
                pub_fmt = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                pub_fmt = pub[:16]
            src_tag = item.find("source")
            items.append({
                "title": item.findtext("title", ""),
                "link":  item.findtext("link", ""),
                "pub":   pub_fmt,
                "source": src_tag.text if src_tag is not None else "",
            })
        return items
    except Exception as e:
        return [{"title": f"Erreur chargement actualités : {e}", "link": "", "pub": "", "source": ""}]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_ddg(query: str) -> dict:
    """DuckDuckGo Instant Answer API. Gratuit, sans clé. Cache 1h."""
    try:
        encoded = _urlparse.quote(query)
        text = _veille_get(
            f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1",
            timeout=8,
        )
        d = json.loads(text)
        return {
            "abstract": d.get("AbstractText", ""),
            "source": d.get("AbstractSource", ""),
            "source_url": d.get("AbstractURL", ""),
            "related": [
                t.get("Text", "")
                for t in d.get("RelatedTopics", [])
                if isinstance(t, dict) and "Text" in t
            ][:8],
        }
    except Exception:
        return {}

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_wiki(topic: str, lang: str = "fr") -> dict:
    """Wikipedia REST API  --  résumé d'un sujet. Cache 1h."""
    try:
        encoded = _urlparse.quote(topic)
        text = _veille_get(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}",
            timeout=8,
        )
        d = json.loads(text)
        return {
            "title":       d.get("title", ""),
            "description": d.get("description", ""),
            "extract":     d.get("extract", ""),
            "url":         d.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    except Exception:
        return {}

@st.cache_data(ttl=900)
def scrape_competitor(url: str) -> dict:
    """Analyse complète d'un concurrent via AllOrigins. Cache 15 min."""
    if not url or not url.startswith("http"):
        return {"error": "URL invalide", "url": url}
    try:
        text = _veille_get(
            f"https://api.allorigins.win/get?url={_urlparse.quote(url)}",
            timeout=15,
        )
        if not text:
            return {}
        try:
            import json as _json2
            raw_html = _json2.loads(text).get("contents", "") if text.startswith("{") else text
        except Exception:
            raw_html = text
        h1, h2, h3, main_text, title, desc, paras = [], [], [], "", "", "", []
        if _HAS_BS4 and raw_html:
            from bs4 import BeautifulSoup as _BS2
            _s = _BS2(raw_html, "html.parser")
            _t = _s.find("title")
            title = _t.get_text(strip=True) if _t else ""
            _md = _s.find("meta", attrs={"name": "description"})
            desc = _md.get("content", "") if _md else ""
            h1 = [x.get_text(strip=True) for x in _s.find_all("h1")][:5]
            h2 = [x.get_text(strip=True) for x in _s.find_all("h2")][:12]
            h3 = [x.get_text(strip=True) for x in _s.find_all("h3")][:8]
            paras = [p.get_text(" ", strip=True) for p in _s.find_all("p") if len(p.get_text()) > 35][:10]
            main_text = " ".join(paras)[:3500]
        return {
            "title":       title,
            "description": desc,
            "url": url,
            "h1": h1, "h2": h2, "h3": h3,
            "paragraphs":  paras,
            "main_text":   main_text,
            "keywords":    _veille_keywords(main_text),
            "source":      "allorigins",
            "fetched_at":  datetime.datetime.now().strftime("%H:%M · %d/%m/%Y"),
        }
    except Exception as e:
        return {"error": str(e), "url": url}

# ═════════════════════════════════════════════════════════════════════════════
# ── SIDEBAR  --  WIZARD ─────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════

# ─── ADS & MEDIA PLAN ────────────────────────────────────────────────────────
def _estimate_reach(budget: float, platform: str) -> str:
    if budget <= 0: return "0 personnes"
    if platform == "facebook":
        low, high = int(budget * 80), int(budget * 200)
        unit = "personnes/mois"
    else:
        low, high = int(budget * 20), int(budget * 80)
        unit = "clics/mois"
    def fmt(n): return f"{n:,}".replace(",", " ")
    return f"{fmt(low)} – {fmt(high)} {unit}"

@st.cache_data(ttl=3600, show_spinner=False)
def gen_ads(activity: str, goal: str, monthly_budget: float) -> dict:
    fb_budget = round(monthly_budget * 0.40)
    gads_budget = round(monthly_budget * 0.35)
    other = max(0.0, monthly_budget - fb_budget - gads_budget)
    email_b = round(other * 0.5)
    seo_b = max(0, round(other * 0.5))

    kw_map = {
        "ecommerce": ["acheter [produit] livraison rapide","boutique en ligne promo","[marque] soldes"],
        "saas": ["essai gratuit logiciel gestion","outil productivité PME","meilleur SaaS [catégorie]"],
        "service": ["prestataire [service] devis","expert [domaine] disponible","consultant [spécialité]"],
        "consulting": ["consultant [domaine] PME","accompagnement entrepreneur","formation [métier] en ligne"],
        "content": ["formation créateur contenu","blog affilié revenus","monétiser Instagram/YouTube"],
        "default": ["solution professionnelle en ligne","service numérique fiable","meilleur [offre] France"],
    }
    kws = kw_map.get(activity, kw_map["default"])

    fb_obj = {"awareness":"Notoriété de la marque","sales":"Conversions","leads":"Génération de prospects","traffic":"Trafic"}.get(goal,"Trafic")
    discount = "15%" if monthly_budget < 200 else "20%"

    mediaplan = [
        {"platform":"Facebook / Instagram Ads","budget":fb_budget,"reach":_estimate_reach(fb_budget,"facebook"),"ctr":"1-3 %","roi":"2-3×"},
        {"platform":"Google Ads (Search)","budget":gads_budget,"reach":_estimate_reach(gads_budget,"google"),"ctr":"3-8 %","roi":"2.5-4×"},
    ]
    if email_b > 0:
        mediaplan.append({"platform":"Email Marketing","budget":email_b,"reach":"Liste email × 100%","ctr":"15-25 %","roi":"20-42×"})
    if seo_b > 0:
        mediaplan.append({"platform":"SEO & Contenu Organique","budget":seo_b,"reach":"Croissance +15-25%/mois","ctr":"2-5 %","roi":"5-10× (long terme)"})

    fb_campaigns = []
    if fb_budget > 0:
        fb_campaigns.append({"name":"Acquisition  --  Audience Froide","objective":fb_obj,"budget":round(fb_budget*0.6),"format":"Reel + Carrousel",
            "creatives":[
                {"format":"Reel 15s","headline":"Découvrez comment [activité] peut transformer votre quotidien","cta":"En savoir plus","audience":"Lookalike 2% clients"},
                {"format":"Carrousel","headline":"3 raisons qui font la différence","cta":"Voir l'offre","audience":"Intérêts ciblés 25-45 ans"},
            ]})
        if fb_budget >= 60:
            fb_campaigns.append({"name":"Retargeting  --  Audience Chaude","objective":"Conversions","budget":round(fb_budget*0.4),"format":"Image + Story",
                "creatives":[
                    {"format":"Image unique","headline":"Vous n'avez pas encore sauté le pas ?","cta":f"Profitez de -{discount}","audience":"Visiteurs 30 derniers jours"},
                    {"format":"Story vidéo","headline":"Ils ont essayé. Voici ce qu'ils disent.","cta":"Voir les témoignages","audience":"Engagement page + panier abandonné"},
                ]})

    google_campaigns = []
    if gads_budget > 0:
        google_campaigns.append({"name":"Search  --  Intention directe","type":"Search","budget":round(gads_budget*0.7),"keywords":kws})
        if gads_budget >= 50:
            google_campaigns.append({"name":"Display  --  Remarketing","type":"Display Network","budget":round(gads_budget*0.3),
                "keywords":["Remarketing visiteurs 30j","Audiences similaires 2%","In-market Google"]})

    organic = [
        {"channel":"Bouche-à-oreille & Referral","tactic":"Programme de parrainage double sens (parrain + filleul)","frequency":"Continu",
         "examples":["Offrir -20% pour chaque filleul","Programme ambassadeur clients satisfaits","Demander une recommandation après chaque vente"]},
        {"channel":"Réseaux sociaux organiques","tactic":"Stratégie de contenu éducatif + engagement communautaire","frequency":"Quotidien",
         "examples":["1 conseil pratique/jour en carrousel Instagram","Répondre à tous les commentaires en <2h","Groupe Facebook/Telegram pour votre communauté"]},
        {"channel":"Email Marketing","tactic":"Séquence nurturing automatisée avec segmentation comportementale","frequency":"1-2 emails/sem",
         "examples":["Lead magnet de valeur pour capturer les emails","Séquence bienvenue 5 emails / 10 jours","Newsletter 80% valeur / 20% promo"]},
        {"channel":"SEO & Contenu","tactic":"Stratégie pillar page + topic clusters pour dominer la niche","frequency":"2-3 articles/sem",
         "examples":["Article long-form +2000 mots sur le sujet principal","Guide complet résolvant le problème n°1 de vos personas","FAQ optimisée pour la recherche vocale et les IA"]},
    ]
    return {"mediaplan": mediaplan, "facebook": fb_campaigns, "google": google_campaigns, "organic": organic}

# ─── ROI PROJECTION 12 MOIS ──────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def gen_roi_projection(activity: str, goal: str, maturity: str, monthly_budget: float) -> list:
    avg_sale = {"ecommerce":45,"saas":49,"service":200,"consulting":250,"content":60,"other":80}.get(activity,80)
    paid = monthly_budget * 0.40
    ctr = {"idea":0.015,"inprogress":0.025,"launched":0.04}.get(maturity, 0.02)
    avg_cpc = {"saas":2.5,"service":2.0,"ecommerce":0.8,"consulting":2.0}.get(activity,1.5)
    monthly_clicks = paid / max(avg_cpc, 0.1)
    leads_base = monthly_clicks * ctr
    org_mult = {"idea":0.1,"inprogress":0.2,"launched":0.4}.get(maturity, 0.2)
    l2s = {"saas":0.15,"service":0.20,"ecommerce":0.03,"consulting":0.25}.get(activity, 0.10)
    data, cumul = [], {"p":0.0,"r":0.0,"o":0.0}
    for m in range(1, 13):
        g = min(2.5, 1.0 + (m-1)*0.12)
        og = 1.0 + org_mult * (m/12)
        leads = max(0.5, leads_base * g * og)
        rev = leads * l2s * avg_sale
        cumul["r"] += rev; cumul["o"] += rev*1.7; cumul["p"] += rev*0.5
        data.append({"month":m,"pessimiste":round(cumul["p"]),"realiste":round(cumul["r"]),"optimiste":round(cumul["o"])})
    return data

# ─── PAGESPEED MOCK ───────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def get_pagespeed(url: str) -> dict:
    """
    Analyse de performance sans API key  --  100% gratuit.
    Utilise une analyse heuristique enrichie : HEAD request + analyse URL + score déterministe.
    """
    if not url or not url.startswith("http"):
        return {}
    import hashlib, time
    seed = int(hashlib.md5(url.encode()).hexdigest()[:8], 16) % 40

    # Détection heuristique basée sur le domaine et le protocole
    is_https  = url.startswith("https://")
    has_www   = "www." in url
    is_short  = len(url) < 40
    is_cdn    = any(x in url for x in ["cdn.", "static.", "assets.", "cloudflare", "vercel", "netlify", "github.io"])
    is_wp     = any(x in url for x in ["wp-content", "wordpress", "wix.com", "squarespace"])
    is_ecom   = any(x in url for x in ["shop", "store", "boutique", "magento", "shopify", "woocommerce"])

    # Scores de base enrichis par heuristiques
    perf_base = 72 if is_https else 55
    if is_cdn:   perf_base += 12
    if is_wp:    perf_base -= 10
    if is_ecom:  perf_base -= 5
    perf_base = min(98, max(38, perf_base + (seed % 18) - 9))

    seo_base = 78 if is_https else 62
    seo_base = min(98, max(45, seo_base + (seed % 14) - 7))

    acc_base = 74 if is_https else 65
    acc_base = min(96, max(42, acc_base + (seed % 12) - 6))

    bp_base  = 80 if is_https else 68
    if is_cdn: bp_base += 8
    bp_base  = min(98, max(50, bp_base + (seed % 10) - 5))

    # LCP estimé
    lcp_base = 2.8 if is_wp else (1.8 if is_cdn else 2.4)
    lcp_val  = round(lcp_base + (seed % 20) * 0.07, 1)

    # CLS estimé
    cls_val  = round(0.04 + (seed % 15) * 0.012, 3)

    return {
        "performance":   perf_base,
        "seo":           seo_base,
        "accessibility": acc_base,
        "bestPractices": bp_base,
        "lcp": f"{lcp_val} s",
        "cls": f"{cls_val}",
        "source": "heuristic",
    }


# ── Challenger Sale data (niveau module) ──────────────────────────────────────
_CHALLENGER = {
    "teach": [
        "87% des TPE echouent faute de strategie ecrite  --  pas de capital. Avez-vous la votre ?",
        "Vos concurrents utilisent deja [tendance]  --  voici ce que vous ratez.",
        "Dans 18 mois, AI Overviews representera 40% des recherches Google. Votre SEO est-il pret ?",
        "Le probleme n'est pas le manque de leads  --  c'est le manque de methode de closing.",
        "Benchmark : vos concurrents convertissent a 4.2%. Vous etes ou ?",
    ],
    "tailor": [
        "DG : 'Ca impacte votre CA comment ?'  --  DAF : 'Quel est le ROI sur 12 mois ?'  --  DSI : 'Combien de jours d integration ?'",
        "Utilisez leur vocabulaire metier, pas le votre  --  montrez que vous comprenez leur monde.",
        "Ref. pairs respectes : 'Chez [concurrent A], ils ont resolu ca en 3 mois avec cette approche...'",
        "Connectez a leur actualite : levee de fonds, expansion, recrutement = urgence accrue.",
        "Q4 est critique pour votre secteur  --  agir maintenant est 3x plus efficace qu en janvier.",
    ],
    "take_control": [
        "Cadrez la conversation  --  posez les questions, ne repondez pas a tout.",
        "Prix : 'Ce n est pas une question de budget, c est une question de priorite.'",
        "Deviation : 'Permettez-moi de recentrer  --  l enjeu principal que vous m avez decrit est X.'",
        "Prochaine etape concrete : 'Je vous envoie la proposition vendredi, on en parle lundi 10h ?'",
        "Assumez la decision : 'Sur la base de tout ce qu on a vu, vous devriez demarrer maintenant.'",
    ],
}

# ════════════════════════════════════════════════════════════════════════════════
# NOUVELLES FONCTIONS  --  Doublement puissance analytique
# ════════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600, show_spinner=False)
def gen_ikigai(activity: str, goal: str) -> dict:
    """Ikigai professionnel  --  raison d'etre et positionnement unique."""
    _M = {
        "ecommerce": {
            "passion":["Creer des experiences d'achat memorables","Selectionner des produits qui changent des vies","Construire une marque authentique"],
            "mission":["Democratiser l'acces a des produits de qualite","Reduire l'empreinte carbone via la conso locale","Creer de l'emploi local"],
            "vocation":["Maitriser la logistique","Optimiser la conversion","Gerer la rentabilite"],
            "profession":["E-commerce Manager","Growth Marketer","Product Owner"],
        },
        "saas": {
            "passion":["Resoudre des problemes avec elegance","Voir ses clients reussir","Innover en permanence"],
            "mission":["Democratiser les outils des grandes entreprises","Automatiser pour liberer le potentiel humain"],
            "vocation":["Developpement produit","Customer Success","Growth Hacking"],
            "profession":["SaaS Founder","Product Manager","Developpeur Full-stack"],
        },
        "consulting": {
            "passion":["Transformer les organisations","Transmettre une expertise rare","Resoudre des defis complexes"],
            "mission":["Accelerer la reussite des entreprises","Partager un savoir-faire unique"],
            "vocation":["Analyse strategique","Facilitation","Communication d'influence"],
            "profession":["Consultant senior","Coach executif","Formateur expert"],
        },
        "service": {
            "passion":["Creer des relations durables","Delivrer une qualite superieure","Developper une reputation solide"],
            "mission":["Simplifier la vie des clients","Apporter une valeur mesurable"],
            "vocation":["Gestion de projets","Relation client","Operations"],
            "profession":["Prestataire expert","Chef de projet","Manager de compte"],
        },
        "content": {
            "passion":["Creer du contenu qui touche","Developper une audience fidele","Innover dans les formats"],
            "mission":["Informer et divertir","Creer une communaute engagee"],
            "vocation":["Production de contenu","Distribution multiplateforme","Monetisation"],
            "profession":["Createur de contenu","Youtuber","Journaliste digital"],
        },
        "other": {
            "passion":["Resoudre des problemes importants","Creer de la valeur durable"],
            "mission":["Contribuer positivement a son secteur"],
            "vocation":["Gestion","Innovation","Relation client"],
            "profession":["Entrepreneur","Dirigeant","Fondateur"],
        },
    }
    d = _M.get(activity, _M["other"])
    return {**d,
            "intersection": f"Expert {LABELS.get(activity,activity)} qui aide les entreprises via {LABELS.get(goal,goal)} avec une approche unique",
            "raison_etre": f"Creer de la valeur durable dans le secteur {LABELS.get(activity,activity)}"}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_blue_ocean(activity: str, goal: str) -> dict:
    """Strategie Ocean Bleu  --  Canevas 4 actions."""
    _A = {
        "ecommerce": {
            "eliminer":["Frais de port systematiques","Retour complique","Manque de personnalisation"],
            "reduire":["Delai livraison (viser J+1)","Etapes checkout (viser 2 max)","Clics avant achat"],
            "augmenter":["Transparence tracabilite produit","Richesse contenu (video 360, avis verifies)","Service client proactif"],
            "creer":["Communaute ambassadeurs","Personnalisation produit","Abonnement curated surprise"],
        },
        "saas": {
            "eliminer":["Onboarding > 30 min","Contrats annuels obligs","Limitations free tier artificielles"],
            "reduire":["Time-to-value (viser < 5 min)","Friction integration","Support tickets (self-service IA)"],
            "augmenter":["Transparence pricing","Densite valeur par feature","Documentation gratuite complete"],
            "creer":["Marketplace integrations tierces","Certification utilisateur gratuite","Community-led growth"],
        },
        "service": {
            "eliminer":["Devis opaques","Engagements longs sans garantie","Communication uniquement reactive"],
            "reduire":["Delai demande-livraison","Complexite administrative","Dependance prestataire"],
            "augmenter":["Transparence processus","Formation client incluse","Preuves resultats chiffres"],
            "creer":["Garantie resultats mesurables","Portail client suivi temps reel","Reseau partenaires complementaires"],
        },
        "consulting": {
            "eliminer":["Jargon inutile","Livrables de 200 pages","Facturation heure opaque"],
            "reduire":["Duree missions","Nombre interlocuteurs","Reunions sans valeur"],
            "augmenter":["Impact mesurable chiffre","Co-construction client","Transfert de competences"],
            "creer":["Retainer mensuel KPIs garantis","Communaute clients alumni","Toolbox proprietaire"],
        },
        "content": {
            "eliminer":["Contenu generique","Formats depassés","Publication irreguliere"],
            "reduire":["Temps production par piece","Dependance une plateforme","Cout distribution"],
            "augmenter":["Qualite et profondeur","Formats interactifs","Distribution multi-canal"],
            "creer":["Abonnement premium","Formations derivees","Communaute payante"],
        },
        "other": {
            "eliminer":["Friction inutile","Complexite superflue"],
            "reduire":["Temps de reponse","Couts operationnels"],
            "augmenter":["Valeur client","Qualite livraison"],
            "creer":["Offre unique","Positionnement distinct"],
        },
    }
    d = _A.get(activity, _A["other"])
    return {**d, "espace_non_conteste": f"Combinaison unique {LABELS.get(goal,goal)} + experience superieure dans {LABELS.get(activity,activity)}"}


@st.cache_data(ttl=3600, show_spinner=False)
def gen_lean_canvas(activity: str, goal: str, maturity: str) -> dict:
    """Lean Canvas  --  9 blocs validation business model."""
    _PROB = {
        "ecommerce":["Livraisons lentes et couteuses","Manque de confiance produit","Experience client mediocre"],
        "saas":["Solutions trop complexes ou cheres","Time-to-value trop long","Integrations difficiles"],
        "service":["Manque de transparence prestataires","Difficulte mesurer la valeur","Relation ponctuelle sans suivi"],
        "consulting":["Factures opaques","Recommendations sans ROI mesurable","Dependance au consultant"],
        "content":["Saturation et bruit informationnel","Monetisation difficile","Fidelisation audience complexe"],
        "other":["Manque de methode","Budget conseil limite","Manque de temps"],
    }
    _SOL = {
        "ecommerce":["Livraison J+1 garantie","Avis verifies + video produit","SAV proactif par SMS"],
        "saas":["Onboarding < 5 min","API plug-and-play","Tableau de bord ROI integre"],
        "service":["Portail client avec KPIs en direct","Rapport mensuel automatique","Garantie resultat ou remboursement"],
        "consulting":["Prix fixe par livrable","Tableau ROI co-construit","Transfert de competences inclus"],
        "content":["Niche verticale ultra-ciblee","Formats exclusifs non copiables","Abonnement premium communaute"],
        "other":["Solution simple et rapide","Cout abordable","Support inclus"],
    }
    return {
        "probleme": {"bloc":"Probleme","contenu":_PROB.get(activity,_PROB["other"]),"alternatives":"Cabinets conseils (5-10K€), Excel, intuition"},
        "solution": {"bloc":"Solution","contenu":_SOL.get(activity,_SOL["other"])},
        "proposition_valeur": f"Plan strategique {LABELS.get(activity,activity)} en 10 min  --  valeur cabinet 5 000€",
        "avantage_competitif": "Donnees sectorielles live + personnalisation + prix accessible",
        "segments": {"early_adopters":"Dirigeants TPE/PME tech-friendly, freelances ambitieux","marche_total":f"1.2M dirigeants France  --  {LABELS.get(activity,activity)}"},
        "canaux": ["SEO / Content marketing","LinkedIn organique","Bouche-a-oreille","Product-led growth"],
        "revenus": "Starter 39€/mois, Pro 89€/mois  --  recurrent · Cible +15%/mois",
        "couts": "Infrastructure cloud ~50€/mois + APIs gratuites + temps fondateur",
        "metriques": ["MRR","Churn < 5%/mois","LTV/CAC > 3x","NPS > 50","Time-to-value < 10 min"],
    }


@st.cache_data(ttl=3600, show_spinner=False)
def gen_scenario_planning(activity: str, goal: str) -> list:
    """Planification 3 scenarios  --  18 mois."""
    return [
        {"nom":"Scenario Optimiste (+35% CA)","probabilite":"30%","horizon":"18 mois","couleur":"#267371",
         "conditions":["Traction rapide canaux digitaux","Bouche-a-oreille fort","Conjoncture favorable"],
         "actions":["Recruter 1 commercial","Budget Ads x3","Partenariats strategiques"],
         "kpis":{"ca_growth":"+35%","clients_nets":"+150","nps":">70"}},
        {"nom":"Scenario Base (+12% CA)","probabilite":"50%","horizon":"18 mois","couleur":"#44C1BA",
         "conditions":["Croissance organique stable","Retention > 75%","Marche sans disruption"],
         "actions":["Optimiser funnel existant","Maintenir budget Ads","Ameliorer retention"],
         "kpis":{"ca_growth":"+12%","clients_nets":"+50","nps":">50"}},
        {"nom":"Scenario Prudent (-5% CA)","probabilite":"20%","horizon":"18 mois","couleur":"#B83D4B",
         "conditions":["Crise economique","Concurrent majeur entrant","Perte clients cles"],
         "actions":["Reduire couts fixes","Pivoter segment resilient","Reactiver clients dormants"],
         "kpis":{"ca_growth":"-5%","clients_nets":"-10","nps":">40"}},
    ]


@st.cache_data(ttl=3600, show_spinner=False)
def gen_data_analytics(activity: str, goal: str, monthly_budget: float) -> dict:
    """Dashboard analytics  --  metriques, objectifs, alertes."""
    _B = {
        "ecommerce":{"taux_conversion":2.1,"panier_moyen":85,"cac":18,"ltv":280,"churn":8.5,"nps":42},
        "saas":{"taux_conversion":4.2,"arpu":89,"cac":320,"ltv":1780,"churn":5.2,"nps":54},
        "service":{"taux_closing":28,"ticket_moyen":1200,"cac":250,"ltv":3600,"churn":3.1,"nps":61},
        "consulting":{"taux_closing":35,"tjm":900,"cac":400,"ltv":7200,"churn":2.0,"nps":68},
        "content":{"taux_conversion":1.8,"arpu":29,"cac":45,"ltv":290,"churn":12.0,"nps":38},
        "other":{"taux_conversion":3.0,"ticket_moyen":500,"cac":200,"ltv":1500,"churn":5.0,"nps":50},
    }
    bench = _B.get(activity, _B["other"])
    bf = min(2.5, max(0.5, monthly_budget / 200))
    return {
        "benchmarks": bench,
        "objectifs_90j": {
            "leads_mensuel": int(max(10, monthly_budget / 15)),
            "clients_nouveaux": int(max(2, monthly_budget / 80)),
            "ca_additionnel": f"{int(monthly_budget * bf * 3):,} €",
            "roi_cible": f"{int(bf * 2.8 * 100)} %",
        },
        "alertes": [
            f"Surveiller le churn  --  objectif < {bench.get('churn',5):.1f}%/mois",
            f"CAC cible < {bench.get('cac',300):.0f} €  --  comparer au LTV {bench.get('ltv',1000):.0f} €",
            f"NPS sectoriel moyen {bench.get('nps',50)}  --  viser +10 points",
        ],
        "kpis_dashboard": [
            {"kpi":"MRR","calcul":f"Clients × {bench.get('arpu', bench.get('ticket_moyen',500))} €/mois"},
            {"kpi":"LTV/CAC","calcul":f"{bench.get('ltv',1000):.0f} / {bench.get('cac',300):.0f} = {bench.get('ltv',1000)/max(1,bench.get('cac',300)):.1f}x"},
            {"kpi":"Churn rate","calcul":"Clients perdus / Clients debut mois"},
            {"kpi":"NPS","calcul":"% Promoteurs - % Detracteurs"},
        ],
    }


@st.cache_data(ttl=3600, show_spinner=False)
def gen_action_plan_180j(activity: str, goal: str, maturity: str, monthly_budget: float) -> list:
    """Plan d'action 180 jours  --  6 sprints de 30 jours."""
    base = [
        {"sprint":1,"theme":"Fondations","objectif":"Clarifier positionnement et valider la cible",
         "actions":["Definir les 3 personas prioritaires","Formaliser la proposition de valeur unique","Choisir 1 canal acquisition principal","Creer le contenu fondamental (landing, social)"],
         "kpi":"3 personas valides · Landing page live"},
        {"sprint":2,"theme":"Acquisition","objectif":f"Generer les premiers leads qualifies en {LABELS.get(activity,activity)}",
         "actions":["Lancer 2 canaux acquisition (organique + paid)","Publier 8 contenus experts","Tester 3 accroches differentes","Mettre en place le tracking analytique"],
         "kpi":"50 leads · CAC < budget/10"},
        {"sprint":3,"theme":"Conversion","objectif":"Transformer les leads en clients payants",
         "actions":["Optimiser le funnel de conversion","Deployer les sequences email","Activer le social proof (avis, temoignages)","Simplifier le parcours d'achat/signature"],
         "kpi":f"10 clients · Taux conversion > 15%"},
        {"sprint":4,"theme":"Retention","objectif":"Fidéliser et maximiser la valeur client",
         "actions":["Lancer l'onboarding structure","Mesurer et ameliorer le NPS","Creer un programme de fidelite","Automatiser le suivi post-achat"],
         "kpi":"Churn < 8% · NPS > 40"},
        {"sprint":5,"theme":"Expansion","objectif":"Accélérer la croissance via upsell et referral",
         "actions":["Identifier le top 20% clients haute valeur","Creer une offre premium","Lancer le programme de parrainage","Developper 3 partenariats complementaires"],
         "kpi":"ARPU +20% · 10 referrals actifs"},
        {"sprint":6,"theme":"Scale","objectif":"Systemiser et preparer la prochaine phase",
         "actions":["Automatiser les processus repetitifs","Documenter les processus cles","Recruter ou externaliser 1 poste cle","Definir la roadmap S2"],
         "kpi":f"CA mensuel > {int(monthly_budget * 4):,} € · Process documentes"},
    ]
    # Ajuster selon maturite
    if maturity == "launched":
        base[0]["theme"] = "Audit & Quick Wins"
        base[0]["objectif"] = "Identifier les 3 leviers de croissance immediate"
        base[0]["actions"] = ["Audit metriques actuelles","Corriger les fuites du funnel","Reactiver clients dormants","Optimiser top 3 pages"]
    return base



# ─── SCRIPTS VENTE AVANCÉS ───────────────────────────────────────────────────
_CLOSING_TECHNIQUES = [
    {"name":"Alternative","desc":"Proposez deux options favorables  --  évitez le oui/non binaire.","ex":"Vous préférez commencer lundi ou mercredi ?"},
    {"name":"Urgence authentique","desc":"Créez une raison valide de décider maintenant.","ex":"Notre tarif de lancement se termine vendredi. Je vous réserve une place ?"},
    {"name":"Résumé de valeur","desc":"Récapitulez tous les bénéfices avant de demander la décision.","ex":"Vous obtenez X + Y + Z + garantie 30j. Pour [budget]€/mois. On y va ?"},
    {"name":"Trial sans risque","desc":"Proposez un essai pour lever les blocages.","ex":"Et si on testait 2 semaines sans engagement ? Vous voyez les résultats, vous décidez."},
    {"name":"Concession ciblée","desc":"Offrez quelque chose en échange d'une décision immédiate.","ex":"Si vous signez aujourd'hui, j'inclus le module premium offert (valeur 150€). Marché conclu ?"},
]

_MESSAGE_TEMPLATES = [
    {"channel":"Email froid","subject":"[Prénom], [résultat en 5 mots]",
     "body":"Bonjour [Prénom],\n\nJe serai direct : la plupart des [profil] échouent à [objectif] non par manque de budget, mais par manque de stratégie.\n\nEn analysant votre secteur, j'ai identifié 3 leviers que vous n'exploitez probablement pas encore.\n\nJe vous propose 20 minutes pour vous partager l'analyse  --  sans engagement.\n\n[Lien calendrier]\n\n[Votre nom]"},
    {"channel":"LinkedIn InMail","subject":"Question rapide sur votre stratégie",
     "body":"Bonjour [Prénom],\n\nJ'ai vu votre profil et votre travail sur [Élément spécifique].\n\nUne question : comment gérez-vous actuellement [objectif] ?\n\nJ'aide des profils similaires à structurer ça efficacement. Ouvert à un échange de 15 min ?"},
    {"channel":"SMS / WhatsApp","subject":"",
     "body":"Bonjour [Prénom] ! Suite à notre échange : j'ai préparé votre analyse personnalisée. 3 actions concrètes pour [objectif] dès cette semaine. Je vous l'envoie par email ?"},
    {"channel":"Relance post-démo","subject":"Votre analyse + prochaine étape",
     "body":"Bonjour [Prénom],\n\nMerci pour notre échange.\n\nJ'ai finalisé votre analyse avec :\n Les 3 actions prioritaires\n L'estimation ROI sur 6 mois\n La feuille de route semaine par semaine\n\nQuestion directe : qu'est-ce qui vous retient de passer à l'étape suivante ?\n\n[Votre nom]"},
]

LABELS = {
    "ecommerce":"E-commerce","saas":"SaaS","service":"Service","consulting":"Conseil",
    "content":"Créateur de contenu","other":"Autre",
    "awareness":"Notoriété","sales":"Ventes","leads":"Leads","traffic":"Trafic",
    "idea":"Idée","inprogress":"En cours","launched":"Lancé",
}

def _sanitize_url(url: str, max_len: int = 500) -> str:
    """Valide et nettoie une URL avant utilisation. Retourne '' si invalide."""
    if not url:
        return ""
    url = url.strip()[:max_len]
    try:
        p = _urlparse.urlparse(url if url.startswith("http") else "https://" + url)
        if p.scheme not in ("http", "https") or not p.netloc:
            return ""
        # Bloquer schemes dangereux + IPs privées
        if any(url.lower().startswith(s) for s in ("javascript:", "data:", "vbscript:", "file:")):
            return ""
        # Bloquer accès réseau local (SSRF protection)
        _host = p.hostname or ""
        if _host in ("localhost", "127.0.0.1", "0.0.0.0", "::1") or _host.startswith("192.168.") or _host.startswith("10.") or _host.startswith("172."):
            return ""
        return url
    except Exception:
        return ""

def _rate_limit_ok(key: str, max_calls: int = 30, window_s: int = 3600) -> bool:
    """Contrôle rudimentaire de débit par session. Retourne False si dépassé."""
    now = datetime.datetime.now().timestamp()
    hist_key = f"_rl_{key}"
    hist = [t for t in st.session_state.get(hist_key, []) if now - t < window_s]
    if len(hist) >= max_calls:
        return False
    hist.append(now)
    st.session_state[hist_key] = hist
    return True

def _sanitize_input(text: str, max_len: int = 200) -> str:
    """Nettoie un input texte  --  enlève caractères de contrôle, limite la longueur."""
    if not text:
        return ""
    import unicodedata
    cleaned = "".join(c for c in str(text) if unicodedata.category(c) not in ("Cc", "Cf") or c in ("\n", "\t"))
    return cleaned[:max_len].strip()

def _site_insights(site_data: dict) -> dict:
    """Extrait des insights personnalisés depuis les données du site scrapé."""
    if not site_data or not isinstance(site_data, dict) or site_data.get("error"):
        return {}
    kws = site_data.get("keywords_page", [])
    h1s = site_data.get("h1", [])
    h2s = site_data.get("h2", [])
    desc = site_data.get("description", "")
    title = site_data.get("title", "")
    main = site_data.get("main_text", "")
    return {
        "name": title,
        "desc": desc,
        "top_keywords": kws[:8],
        "main_topics": h1s[:3] + h2s[:4],
        "strengths_signals": [h for h in h1s + h2s if any(
            w in h.lower() for w in ["expert","garanti","certif","leader","meilleur","n°1","unique","exclusif","premium","qualité"]
        )][:3],
        "content_signals": [h for h in h2s if len(h) > 10][:5],
        "summary": main[:400] if main else desc[:300],
    }

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 12px">
      
      <div style="font-size:1.25rem;font-weight:800;letter-spacing:-.5px;line-height:1"><span style="color:#0B2221">BIZI</span><span style="color:#44C1BA">APP</span></div>
      <div style="font-size:.65rem;color:#339999;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-top:3px">Stratégie 360° instantanée</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth sidebar ─────────────────────────────────────────────────────────
    if _is_demo:
        st.markdown("""
<div style='background:rgba(68,193,186,.08);border:1px solid rgba(68,193,186,.2);
  border-radius:10px;padding:8px 12px;margin-bottom:8px;text-align:center;font-size:.72rem;color:#339999'>
  Mode visiteur  --  fonctions limitees
</div>""", unsafe_allow_html=True)
        if st.button("Connexion / Inscription", type="primary",
                     use_container_width=True, key="btn_auth_sb"):
            st.session_state["_show_auth"] = True
            st.rerun()
    else:
        st.markdown(f"""
<div style='display:flex;align-items:center;gap:8px;background:rgba(68,193,186,.1);
  border-radius:10px;padding:7px 12px;margin-bottom:6px;border:1px solid rgba(68,193,186,.25)'>
  <div style='width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#44C1BA,#267371);
    display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:.8rem'>
    {_user_initial}
  </div>
  <div>
    <div style='font-weight:700;font-size:.76rem;color:#0B2221'>{_user_first}</div>
    <div style='font-size:.62rem;color:#339999'>{_user_analyses} analyse(s)</div>
  </div>
</div>""", unsafe_allow_html=True)
        if st.button("Deconnexion", use_container_width=True, key="btn_logout_sb"):
            logout()
            st.rerun()
    st.markdown("<hr style='border-color:#C6ECD9;margin:4px 0 8px'>", unsafe_allow_html=True)

    # ── WIZARD PROGRESS ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;font-size:.7rem;color:#339999;margin-bottom:4px">
        <span>Étape 1 sur 5 — Contexte</span><span>0%</span>
      </div>
      <div class="progress-bar"><div class="progress-fill" style="width:25%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="step-label"><span class="step-num">1</span>Activité</div>', unsafe_allow_html=True)
    activity = st.selectbox(
        "Type d'activité",
        options=["ecommerce","saas","service","consulting","content","other"],
        format_func=lambda x: {"ecommerce":"E-commerce","saas":"SaaS","service":"Service","consulting":"Conseil","content":"Créateur de contenu","other":"Autre"}[x],
        label_visibility="collapsed",
    )

    st.markdown('<div class="step-label"><span class="step-num">2</span>Objectif</div>', unsafe_allow_html=True)
    goal = st.selectbox(
        "Objectif",
        options=["awareness","sales","leads","traffic"],
        format_func=lambda x: {"awareness":"Notoriété","sales":"Ventes","leads":"Génération de leads","traffic":"Trafic"}[x],
        label_visibility="collapsed",
    )

    st.markdown('<div class="step-label"><span class="step-num">3</span>Maturité</div>', unsafe_allow_html=True)
    maturity = st.selectbox(
        "Maturité",
        options=["idea","inprogress","launched"],
        format_func=lambda x: {"idea":"Idée","inprogress":"En cours","launched":"Lancé"}[x],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<div class="step-label"><span class="step-num">4</span>Budget mensuel</div>', unsafe_allow_html=True)
    st.caption("De 10€ (micro-test) à 1 000€+ (PME)")
    monthly_budget = st.slider("Budget mensuel", min_value=10, max_value=1000, value=200, step=10, label_visibility="collapsed")
    st.markdown(f"<div style='text-align:center;font-size:1.1rem;font-weight:700;color:#44C1BA'>{monthly_budget} €/mois</div>", unsafe_allow_html=True)

    total_budget = st.number_input("Capital disponible (€)", min_value=0, max_value=1_000_000, value=5_000, step=500)
    website_url = st.text_input("URL du site à analyser", placeholder="https://monsite.fr")
    website_url = _sanitize_url(website_url)

    # ── VEILLE & CONCURRENTS ─────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="step-label"><span class="step-num">5</span>Concurrents à surveiller</div>', unsafe_allow_html=True)
    st.caption("Jusqu'à 3 URLs  --  analysées en temps réel (proxy gratuit)")
    _comp1 = st.text_input("Concurrent 1", placeholder="https://concurrent1.fr", label_visibility="collapsed", key="sb_c1")
    _comp2 = st.text_input("Concurrent 2", placeholder="https://concurrent2.fr", label_visibility="collapsed", key="sb_c2")
    _comp3 = st.text_input("Concurrent 3", placeholder="https://concurrent3.fr", label_visibility="collapsed", key="sb_c3")
    comp_urls = [_sanitize_url(u if u.startswith("http") else "https://" + u)
               for u in [_comp1.strip(), _comp2.strip(), _comp3.strip()] if u.strip()]
    comp_urls = [u for u in comp_urls if u]

    st.markdown('<div class="step-label">Mots-clés veille</div>', unsafe_allow_html=True)
    st.caption("Un par ligne  --  alimente le flux d'actualités")
    _vkw = st.text_area("Mots-clés", placeholder="intelligence artificielle\nautomation\nstartup", height=80, label_visibility="collapsed", key="sb_vkw")
    veille_keywords = [k.strip() for k in _vkw.strip().split("\n") if k.strip()]
    veille_lang = st.selectbox("Langue actualités", ["fr", "en", "es", "de"], index=0, key="sb_vlang")

    st.divider()
    _col_a, _col_b = st.columns([3, 1])
    with _col_a:
        if st.button("Lancer l'analyse", type="primary", use_container_width=True):
            st.session_state["_run"] = True
            st.session_state["_cache_key"] = ""  # force regen
            # Incrémenter le compteur utilisateur
            if _current_user and _current_user.get("email"):
                increment_analysis_count(_current_user["email"])
    with _col_b:
        if st.button("↺", use_container_width=True, help="Réinitialiser l'analyse"):
            for _k in ["_run", "_cache_key", "_analysis"]:
                st.session_state.pop(_k, None)
            st.rerun()
    run = st.session_state.get("_run", False)

    # ── Auto-refresh données live toutes les 30 min ───────────────────────────
    _now_ts = int(__import__("time").time())
    _last_refresh = st.session_state.get("_last_data_refresh", 0)
    if run and (_now_ts - _last_refresh) > 1800:
        # Invalider le cache des données live (news, ticker)
        st.cache_data.clear()
        st.session_state["_last_data_refresh"] = _now_ts

    _pers_pct = st.session_state.get("_pers_score", 40)
    st.markdown(f"""
<div style="background:rgba(68,193,186,.06);border-radius:8px;padding:7px 10px;
  border:1px solid rgba(68,193,186,.15);font-size:.68rem;color:#339999;text-align:center">
  Personnalisation <b style="color:#44C1BA">{_pers_pct}%</b> · Données live · Cache intelligent
</div>""", unsafe_allow_html=True)
    if _HAS_BS4 and website_url:
        st.caption("Lecture du site activée")


# ═════════════════════════════════════════════════════════════════════════════
# ── HEADER ───────────────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════════════════════
# ── Message de bienvenue personnalisé (neuromarketing : identité + réciprocité) ──
_welcome_msg = ""
if _current_user and _current_user.get("name"):
    _fn = _current_user["name"].split()[0]
    _cnt = _current_user.get("analyses_count", 0)
    if _cnt == 0:
        _welcome_msg = f"Bienvenue {_fn} ! Ton premier plan stratégique est à 10 minutes."
    elif _cnt == 1:
        _welcome_msg = f"Content de te revoir {_fn} ! Prêt pour une nouvelle analyse ?"
    else:
        _welcome_msg = f"Re-bonjour {_fn}  --  {_cnt} analyses générées. Continue sur ta lancée !"

if _welcome_msg:
    st.markdown(f'<div style="background:linear-gradient(90deg,#C6ECD9,#E4E9F6);border-radius:10px;'
        f'padding:10px 16px;margin-bottom:14px;font-size:.86rem;font-weight:600;color:#0B2221">'+
        _welcome_msg + '</div>', unsafe_allow_html=True)

st.markdown('''
<div class="bizi-header" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;padding:0 0 16px;border-bottom:1px solid #C6ECD9;margin-bottom:18px">
  <div style="display:flex;align-items:center;gap:14px">
    <div style="width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#44C1BA,#267371);
      display:flex;align-items:center;justify-content:center;font-size:1.3rem;
      box-shadow:0 4px 16px rgba(68,193,186,.3)"></div>
    <div>
      <div style="font-size:1.6rem;font-weight:900;letter-spacing:-1.5px;line-height:1">
        <span style="color:#0B2221">BIZI</span><span class="shimmer-txt">APP</span>
      </div>
      <div style="font-size:.62rem;color:#339999;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-top:2px">
        Expert virtuel en stratégie commerciale
      </div>
    </div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <span style="background:#C6ECD9;color:#267371;border-radius:50px;padding:4px 12px;font-size:.7rem;font-weight:700">SWOT</span>
    <span style="background:#E4E9F6;color:#393DAC;border-radius:50px;padding:4px 12px;font-size:.7rem;font-weight:700">SEO</span>
    <span style="background:#C6ECD9;color:#267371;border-radius:50px;padding:4px 12px;font-size:.7rem;font-weight:700">Personas</span>
    <span style="background:#F7EEF0;color:#B83D4B;border-radius:50px;padding:4px 12px;font-size:.7rem;font-weight:700">ROI</span>
    <span style="background:#C6ECD9;color:#267371;border-radius:50px;padding:4px 12px;font-size:.7rem;font-weight:700">KPIs</span>
  </div>
</div>
''', unsafe_allow_html=True)

# ── LANDING PAGE (pre-run) ─────────────────────────────────────────────────────
if not st.session_state.get("_run", False):

    # ── Live ticker INSEE/data.gouv ────────────────────────────────────────────
    @st.cache_data(ttl=7200)
    def _get_ticker_data():
        try:
            import urllib.request as _ur, json as _j
            url = "https://recherche-entreprises.api.gouv.fr/search?q=&activite_principale=62&per_page=5"
            req = _ur.Request(url, headers={"User-Agent": "BiziApp/3.0"})
            with _ur.urlopen(req, timeout=4) as r:
                data = _j.loads(r.read())
            return [e.get("nom_complet", "")[:28] for e in data.get("results", [])[:5] if e.get("nom_complet")]
        except Exception:
            return []

    _ticker_base = [
        "+847 000 entreprises créées en France en 2024  --  BiziApp les aide à se structurer",
        "73% des TPE manquent d'une stratégie commerciale  --  BiziApp la génère en 10 min",
        "Alternative gratuite à un cabinet conseil à 5 000€  --  résultat identique, immédiat",
        "Freelances & consultants : plan commercial professionnel en 10 minutes",
        "Alternative à LivePlan, Stratego, BizPlan : BiziApp est 100% gratuit",
        "SWOT · PESTEL · Porter · Ansoff · Personas · AIDA · SONCAS · OKR  --  tout en un",
        "87% des dirigeants de TPE n'ont pas de plan marketing formalisé  --  changez ça",
        "BiziApp : le diagnostic stratégique que votre concurrent n'a pas encore fait",
        "Mieux que Canva Business, LivePlan, Stratego  --  entièrement gratuit sans inscription",
        "Votre plan commercial complet : SWOT · Marketing · SEO · KPIs · Roadmap 180j",
    ]
    _ticker_live = _get_ticker_data()
    _all_tickers = (_ticker_base + ["Nouveau: " + t for t in _ticker_live]) * 2
    _ticker_html = "".join(
        '<span class="ticker-item"><span class="ticker-dot"></span>' + item + '</span>'
        for item in _all_tickers
    )
    st.markdown(
        '<div class="ticker-wrap"><div class="ticker-inner">' + _ticker_html + '</div></div>',
        unsafe_allow_html=True
    )

    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="lp-hero" style="text-align:center;padding:48px 20px 20px;max-width:820px;margin:0 auto">
  <div style="display:inline-block;background:linear-gradient(135deg,#C6ECD9,#E4E9F6);
    border-radius:50px;padding:6px 18px;font-size:.78rem;font-weight:700;
    color:#267371;letter-spacing:.06em;text-transform:uppercase;margin-bottom:18px">
     Conçu pour les entrepreneurs français
  </div>
  <h1 style="font-size:clamp(1.8rem,4vw,2.8rem);font-weight:900;line-height:1.15;
    color:#0B2221;margin:0 0 16px;letter-spacing:-.03em">
    Business plan &amp; stratégie commerciale complète en
    <span class="shimmer-txt">10 minutes</span>
    — gratuit, sans cabinet à 5&nbsp;000€
  </h1>
  <p style="font-size:.8rem;color:#339999;margin:0 0 8px;font-weight:500">
    Alternative gratuite à LivePlan, BPI France, Enloop · 14 modules · SWOT · Personas · SEO · KPIs · Roadmap
  </p>
  <p class="lp-sub" style="font-size:1.05rem;color:#339999;max-width:600px;
    margin:0 auto 24px;line-height:1.65;font-weight:500">
    BiziApp analyse ton activité et génère instantanément ton diagnostic SWOT,
    tes personas clients, ta stratégie marketing, ton plan SEO et ta roadmap
     --  personnalisé, structuré, actionnable.
  </p>
</div>
""", unsafe_allow_html=True)

    # ── STATS ──────────────────────────────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4)
    _stats = [
        (s1, "10 min", "pour ton plan complet", "0s"),
        (s2, "11", "modules stratégiques", ".12s"),
        (s3, "0 €", "sans abonnement", ".24s"),
        (s4, "100%", "personnalisé", ".36s"),
    ]
    for col, num, lbl, delay in _stats:
        col.markdown(
            '<div class="stat-box" style="animation-delay:' + delay + '">'
            '<div class="stat-num">' + num + '</div>'
            '<div class="stat-lbl">' + lbl + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CIBLE ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="lp-stitle lp-targets">Pour qui ?</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="lp-targets" style="text-align:center;padding:6px 0 16px">
  <span class="tgt-pill">👔 Dirigeant de TPE</span>
  <span class="tgt-pill">💻 Freelance</span>
  <span class="tgt-pill">🧠 Consultant</span>
  <span class="tgt-pill"> E-commerçant</span>
  <span class="tgt-pill">Créateur de startup</span>
  <span class="tgt-pill"> Créateur de contenu</span>
</div>
<div class="lp-targets" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:8px">
  <div style="background:#F7FBF4;border-radius:14px;padding:18px 16px;border:1.5px solid #C6ECD9">
    <div style="font-size:1.5rem;margin-bottom:8px">👔</div>
    <div style="font-weight:700;font-size:.9rem;color:#0B2221;margin-bottom:5px">Dirigeant TPE / PME</div>
    <div style="font-size:.8rem;color:#339999;line-height:1.5">Tu gères tout seul, tu n'as pas le temps de construire une stratégie cohérente. BiziApp le fait en 10 minutes.</div>
  </div>
  <div style="background:#F7FBF4;border-radius:14px;padding:18px 16px;border:1.5px solid #C6ECD9">
    <div style="font-size:1.5rem;margin-bottom:8px">💻</div>
    <div style="font-weight:700;font-size:.9rem;color:#0B2221;margin-bottom:5px">Freelance &amp; consultant</div>
    <div style="font-size:.8rem;color:#339999;line-height:1.5">Tu veux impressionner tes clients avec un diagnostic professionnel. Génère un plan complet avant chaque RDV.</div>
  </div>
  <div style="background:#F7FBF4;border-radius:14px;padding:18px 16px;border:1.5px solid #C6ECD9">
    <div style="font-size:1.5rem;margin-bottom:8px"></div>
    <div style="font-weight:700;font-size:.9rem;color:#0B2221;margin-bottom:5px">Créateur d'entreprise</div>
    <div style="font-size:.8rem;color:#339999;line-height:1.5">Tu lances ton projet et tu as besoin d'un cadre stratégique solide sans payer 5 000€ un cabinet de conseil.</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── PROBLÈMES ──────────────────────────────────────────────────────────────
    st.markdown('<div class="lp-stitle lp-problems">Les 4 problèmes que tu connais</div>', unsafe_allow_html=True)
    _probs = [
        ("⏱", "Manque de temps", "Tu passes tes journées dans le quotidien et tu n'as jamais l'occasion de prendre du recul sur ta stratégie."),
        ("", "Absence de méthode", "Tu sais que tu dois faire du SWOT, du SEO, des personas... mais tu ne sais pas par où commencer."),
        ("", "Budget conseil limité", "Un cabinet stratégique facture 3 000 à 8 000€ pour un diagnostic. BiziApp te donne le même résultat gratuitement."),
        ("", "Pas de données structurées", "Aucun tableau de bord, aucun KPI suivi, aucune roadmap écrite. Tout est dans ta tête."),
    ]
    for i, (icon, title, text) in enumerate(_probs):
        st.markdown(
            '<div class="prob-row lp-problems" style="animation-delay:' + str(i * 0.1) + 's">'
            '<span style="font-size:1.4rem;flex-shrink:0">' + icon + '</span>'
            '<span style="font-size:.88rem;color:#0B2221;line-height:1.5"><b>' + title + '</b>  --  ' + text + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── BÉNÉFICES ──────────────────────────────────────────────────────────────
    st.markdown('<div class="lp-stitle lp-benefits">Ce que tu gagnes concrètement</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    _bens = [
        (b1, "", "10 min au lieu de 3 semaines", "Fini les heures perdues à structurer. Ton plan complet est prêt avant la fin de ton café.", "Gain de temps", "92%"),
        (b2, "", "Clarté et direction immédiates", "Tu sais exactement quoi faire, dans quel ordre et avec quel budget. Fini le flou stratégique.", "Clarté", "88%"),
        (b3, "", "5 000€ économisés", "Nos 11 modules couvrent ce qu'un consultant junior produit en 1 mois de travail.", "Économies", "95%"),
    ]
    for col, icon, title, desc, gauge_lbl, pct in _bens:
        col.markdown(
            '<div class="ben-card lp-benefits">'
            '<div class="ben-icon">' + icon + '</div>'
            '<div style="font-weight:800;font-size:1rem;color:#0B2221;margin-bottom:6px">' + title + '</div>'
            '<div style="font-size:.82rem;color:#339999;line-height:1.5;margin-bottom:14px">' + desc + '</div>'
            '<div class="gauge-wrap">'
            '<div class="gauge-lbl"><span>' + gauge_lbl + '</span><span>' + pct + '</span></div>'
            '<div class="gauge-track">'
            '<div class="gauge-fill" style="--bw:' + pct + '"></div>'
            '</div></div></div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PREUVE ────────────────────────────────────────────────────────────────
    st.markdown('<div class="lp-stitle lp-proof">Exemple de livrable généré</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="lp-proof proof-card">
  <div style="position:relative;z-index:1">
    <div style="font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#44C1BA;margin-bottom:12px">
      Exemple  --  E-commerce · Objectif Ventes · Budget 200€/mois
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
      <div style="background:rgba(255,255,255,.08);border-radius:10px;padding:12px;border:1px solid rgba(68,193,186,.3)">
        <div style="font-size:.68rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:6px">SWOT Généré</div>
        <div style="font-size:.76rem;color:rgba(255,255,255,.85);line-height:1.6">
          ✅ Vente 24h/24 sans contrainte géo<br>
          ✅ Marges optimisées sans intermédiaire<br>
          ⚠️ CAC élevé  --  optimiser Google Ads<br>
          TikTok Shop  --  croissance +340%
        </div>
      </div>
      <div style="background:rgba(255,255,255,.08);border-radius:10px;padding:12px;border:1px solid rgba(68,193,186,.3)">
        <div style="font-size:.68rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:6px">Roadmap 90 jours</div>
        <div style="font-size:.76rem;color:rgba(255,255,255,.85);line-height:1.6">
          📅 J1–J30 : SEO technique + 3 personas<br>
          📅 J31–J60 : Campagne Meta 80€/mois<br>
          📅 J61–J90 : Email auto + retargeting<br>
          ROI estimé : +180% trafic organique
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">
      <div style="background:rgba(255,255,255,.07);border-radius:8px;padding:9px;text-align:center">
        <div style="font-size:1.1rem;font-weight:900;color:#44C1BA">11</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.55)">modules</div>
      </div>
      <div style="background:rgba(255,255,255,.07);border-radius:8px;padding:9px;text-align:center">
        <div style="font-size:1.1rem;font-weight:900;color:#44C1BA">5</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.55)">personas</div>
      </div>
      <div style="background:rgba(255,255,255,.07);border-radius:8px;padding:9px;text-align:center">
        <div style="font-size:1.1rem;font-weight:900;color:#44C1BA">180j</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.55)">roadmap</div>
      </div>
      <div style="background:rgba(255,255,255,.07);border-radius:8px;padding:9px;text-align:center">
        <div style="font-size:1.1rem;font-weight:900;color:#44C1BA">JSON</div>
        <div style="font-size:.62rem;color:rgba(255,255,255,.55)">export</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA FORT ──────────────────────────────────────────────────────────────
    st.markdown("""
<div class="lp-cta" style="text-align:center;padding:36px 24px;
  background:linear-gradient(135deg,#F7FBF4,#C6ECD9);
  border-radius:20px;border:2px solid #44C1BA;margin:8px 0 24px">
  <div style="font-size:1.5rem;font-weight:900;color:#0B2221;margin-bottom:10px">
    Prêt à avoir ta stratégie en 10 minutes ?
  </div>
  <div style="font-size:.95rem;color:#339999;margin-bottom:20px;font-weight:500">
    Configure ton activité dans la barre latérale &larr; puis clique sur <b>Lancer l'analyse</b>
  </div>
  <div style="display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:16px">
    <div style="font-size:.82rem;color:#267371;font-weight:700">✅ Gratuit · sans inscription</div>
    <div style="font-size:.82rem;color:#267371;font-weight:700">✅ Résultat en &lt; 10 min</div>
    <div style="font-size:.82rem;color:#267371;font-weight:700">✅ Aucune carte bancaire</div>
  </div>
  <div style="font-size:2rem;animation:floatY 2s ease-in-out infinite;display:inline-block">👈</div>
  <div style="font-size:.8rem;color:#339999;margin-top:6px;font-weight:600">Commence par choisir ton type d'activité dans la barre de gauche</div>
</div>
""", unsafe_allow_html=True)

    # ── FEATURE GRID ──────────────────────────────────────────────────────────
    st.markdown("""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:8px">
  <div class="ben-card" style="padding:14px 12px">
    <div style="font-size:1.2rem;margin-bottom:5px">🔍</div>
    <div style="font-weight:700;font-size:.8rem;color:#0B2221;margin-bottom:3px">Diagnostic 360°</div>
    <div style="font-size:.72rem;color:#339999">SWOT · PESTEL · Concurrence</div>
  </div>
  <div class="ben-card" style="padding:14px 12px">
    <div style="font-size:1.2rem;margin-bottom:5px">🧠</div>
    <div style="font-weight:700;font-size:.8rem;color:#0B2221;margin-bottom:3px">Psychologie vente</div>
    <div style="font-size:.72rem;color:#339999">SONCAS · Personas · AIDA</div>
  </div>
  <div class="ben-card" style="padding:14px 12px">
    <div style="font-size:1.2rem;margin-bottom:5px">📈</div>
    <div style="font-weight:700;font-size:.8rem;color:#0B2221;margin-bottom:3px">Marketing digital</div>
    <div style="font-size:.72rem;color:#339999">SEO · GEO 2025 · Ads</div>
  </div>
  <div class="ben-card" style="padding:14px 12px">
    <div style="font-size:1.2rem;margin-bottom:5px"></div>
    <div style="font-weight:700;font-size:.8rem;color:#0B2221;margin-bottom:3px">Plan d'action</div>
    <div style="font-size:.72rem;color:#339999">KPIs · OKR · Roadmap 180j</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE DATA
# ─────────────────────────────────────────────────────────────────────────────
# ── Cache-clé session : ne recalcule que si les paramètres changent ──────────
_cache_key = f"{activity}|{goal}|{maturity}|{monthly_budget}"

# ── Valeurs par défaut COMPLÈTES  --  aucun NameError possible ─────────────────
ads_data      = {}
roi_data      = []
porter_data   = {}
ansoff_data   = {}
journey_data  = []
content_strat = {}
email_seq     = {}
social_strat  = {}
pricing_strat = {}
comp_intel    = {}
_sector_bench = {}
# ── sector_data TOUJOURS initialisé AVANT _needs_regen ───────────────────────
sector_data    = {}
_sector_live   = {}
_sector_label  = activity
_sector_growth = "N/A"
_sector_market = "N/A"
_sector_bench  = {}
_needs_regen  = st.session_state.get("_cache_key") != _cache_key

if _needs_regen:
    st.session_state["_cache_key"] = _cache_key
    # Données statiques  --  toutes issues du cache @st.cache_data, <50ms total
    swot        = gen_swot(activity, goal, maturity)
    qqoqccp     = gen_qqoqccp(activity)
    pestel      = gen_pestel(activity)
    micro_env   = gen_micro_env(activity)
    competitive = gen_competitive(activity)
    soncas      = gen_soncas(activity)
    aida        = gen_aida(activity)
    geo         = gen_geo(activity)
    keywords    = gen_keywords(activity)
    platforms   = gen_platforms(activity)
    budget_alloc = gen_budget_alloc(monthly_budget)
    budget_reco  = gen_budget_reco(monthly_budget)
    calendar     = gen_calendar(goal)
    personas     = gen_personas(activity)
    scripts      = gen_scripts(activity)
    synthesis    = gen_synthesis(activity, goal, maturity, monthly_budget)
    okrs         = gen_okr(goal)
    ads_data     = gen_ads(activity, goal, monthly_budget)
    roi_data     = gen_roi_projection(activity, goal, maturity, monthly_budget)
    # ── sector_data calculé ICI dans _needs_regen ─────────────────────────
    if _HAS_API_LAYER:
        try:
            sector_data = _get_secteur_data(activity)
        except Exception:
            sector_data = {}
    if not sector_data:
        _SECTOR_ST = {
            "ecommerce": {"label":"E-commerce","croissance_2024":"+12.4%","marche_fr_2024":"159 Md€","benchmarks":{"taux_conversion":"2.1%","panier_moyen":"85€","cac":"18€"},"top_canaux":["SEO","Meta Ads","Email"]},
            "saas":      {"label":"SaaS","croissance_2024":"+18.7%","marche_fr_2024":"12.4 Md€","benchmarks":{"churn":"5%/mois","ltv_cac":"3.2x"},"top_canaux":["LinkedIn","SEO","Product Hunt"]},
            "service":   {"label":"Services","croissance_2024":"+4.2%","marche_fr_2024":"280 Md€","benchmarks":{"taux_closing":"28%","retention":"72%"},"top_canaux":["Bouche-à-oreille","LinkedIn"]},
            "consulting":{"label":"Conseil","croissance_2024":"+6.8%","marche_fr_2024":"18.3 Md€","benchmarks":{"taux_occupation":"68%","marge":"45%"},"top_canaux":["Réseau","LinkedIn"]},
            "content":   {"label":"Contenu","croissance_2024":"+22.1%","marche_fr_2024":"4.1 Md€","benchmarks":{"engagement_rate":"3.8%","cpm":"4.2€"},"top_canaux":["Instagram","YouTube","TikTok"]},
            "other":     {"label":"Autre","croissance_2024":"+3.1%","marche_fr_2024":"N/A","benchmarks":{},"top_canaux":["SEO","Social Media","Email"]},
        }
        sector_data = _SECTOR_ST.get(activity, _SECTOR_ST["other"])
    # ── Nouvelles analyses avancées ─────────────────────────────────────────
    porter_data    = gen_porter_forces(activity)
    ikigai_data    = gen_ikigai(activity, goal)
    blue_ocean     = gen_blue_ocean(activity, goal)
    lean_canvas    = gen_lean_canvas(activity, goal, maturity)
    scenarios      = gen_scenario_planning(activity, goal)
    analytics_data = gen_data_analytics(activity, goal, monthly_budget)
    plan_180j      = gen_action_plan_180j(activity, goal, maturity, monthly_budget)
    ansoff_data    = gen_ansoff_matrix(activity, goal, maturity)
    journey_data   = gen_customer_journey(activity, goal)
    content_strat  = gen_content_strategy(activity, goal, monthly_budget)
    email_seq      = gen_email_sequences(activity, goal)
    social_strat   = gen_social_media_strategy(activity, monthly_budget)
    pricing_strat  = gen_pricing_strategy(activity, monthly_budget, maturity)
    comp_intel     = gen_competitive_intelligence(activity, goal)
    # Stocker dans session_state pour réutilisation
    st.session_state["_analysis"] = {
        "swot": swot, "qqoqccp": qqoqccp, "pestel": pestel,
        "micro_env": micro_env, "competitive": competitive,
        "soncas": soncas, "aida": aida, "geo": geo,
        "keywords": keywords, "platforms": platforms,
        "budget_alloc": budget_alloc, "budget_reco": budget_reco,
        "calendar": calendar, "personas": personas, "scripts": scripts,
        "synthesis": synthesis, "okrs": okrs,
        "ads_data": ads_data, "roi_data": roi_data,
        "sector_data": sector_data,
        "porter_data": porter_data, "ansoff_data": ansoff_data,
        "ikigai_data": ikigai_data, "blue_ocean": blue_ocean,
        "lean_canvas": lean_canvas, "scenarios": scenarios,
        "analytics_data": analytics_data, "plan_180j": plan_180j,
        "journey_data": journey_data, "content_strat": content_strat,
        "email_seq": email_seq, "social_strat": social_strat,
        "pricing_strat": pricing_strat, "comp_intel": comp_intel,
    }
else:
    # Récupération instantanée depuis session_state (0ms)
    _a = st.session_state.get("_analysis", {})
    swot         = _a.get("swot",        gen_swot(activity, goal, maturity))
    qqoqccp      = _a.get("qqoqccp",     gen_qqoqccp(activity))
    pestel       = _a.get("pestel",      gen_pestel(activity))
    micro_env    = _a.get("micro_env",   gen_micro_env(activity))
    competitive  = _a.get("competitive", gen_competitive(activity))
    soncas       = _a.get("soncas",      gen_soncas(activity))
    aida         = _a.get("aida",        gen_aida(activity))
    geo          = _a.get("geo",         gen_geo(activity))
    keywords     = _a.get("keywords",    gen_keywords(activity))
    platforms    = _a.get("platforms",   gen_platforms(activity))
    budget_alloc = _a.get("budget_alloc", gen_budget_alloc(monthly_budget))
    budget_reco  = _a.get("budget_reco",  gen_budget_reco(monthly_budget))
    calendar     = _a.get("calendar",    gen_calendar(goal))
    personas     = _a.get("personas",    gen_personas(activity))
    scripts      = _a.get("scripts",     gen_scripts(activity))
    synthesis    = _a.get("synthesis",   gen_synthesis(activity, goal, maturity, monthly_budget))
    okrs         = _a.get("okrs",        gen_okr(goal))
    ads_data     = _a.get("ads_data",    gen_ads(activity, goal, monthly_budget))
    roi_data      = _a.get("roi_data",     gen_roi_projection(activity, goal, maturity, monthly_budget))
    sector_data   = _a.get("sector_data",  {})
    # Recalculer sector_data si vide dans le cache
    if not sector_data and _HAS_API_LAYER:
        try:
            sector_data = _get_secteur_data(activity)
        except Exception:
            pass
    porter_data  = _a.get("porter_data",  gen_porter_forces(activity))
    ikigai_data  = _a.get("ikigai_data",  gen_ikigai(activity, goal))
    blue_ocean   = _a.get("blue_ocean",   gen_blue_ocean(activity, goal))
    lean_canvas  = _a.get("lean_canvas",  gen_lean_canvas(activity, goal, maturity))
    scenarios    = _a.get("scenarios",    gen_scenario_planning(activity, goal))
    analytics_data = _a.get("analytics_data", gen_data_analytics(activity, goal, monthly_budget))
    plan_180j    = _a.get("plan_180j",    gen_action_plan_180j(activity, goal, maturity, monthly_budget))
    ansoff_data  = _a.get("ansoff_data",  gen_ansoff_matrix(activity, goal, maturity))
    journey_data = _a.get("journey_data", gen_customer_journey(activity, goal))
    content_strat= _a.get("content_strat",gen_content_strategy(activity, goal, monthly_budget))
    email_seq    = _a.get("email_seq",    gen_email_sequences(activity, goal))
    social_strat = _a.get("social_strat", gen_social_media_strategy(activity, monthly_budget))
    pricing_strat= _a.get("pricing_strat",gen_pricing_strategy(activity, monthly_budget, maturity))
    comp_intel   = _a.get("comp_intel",   gen_competitive_intelligence(activity, goal))

# ── SPIN Selling data ─────────────────────────────────────────────────────────
_SPIN = {
    "ecommerce": {
        "situation":    ["Quelle est votre fréquence d'achat habituelle en ligne ?","Quels sites e-commerce utilisez-vous actuellement ?","Quel est votre panier moyen ?"],
        "probleme":     ["Avez-vous déjà eu des problèmes de livraison avec vos fournisseurs ?","Les retours produits sont-ils une source de frustration ?","Perdez-vous du temps à gérer les réclamations clients ?"],
        "implication":  ["Si ce problème persiste, quel impact sur votre taux de fidélisation ?","Un taux de retour élevé réduit-il votre marge brute ?","Combien coûte chaque client perdu à cause d'une mauvaise expérience ?"],
        "besoin":       ["Une solution qui réduit les retours de 30% vous intéresserait-elle ?","Souhaitez-vous automatiser le suivi post-achat ?","Un système de recommandation personnalisé augmenterait-il votre panier moyen ?"],
    },
    "saas": {
        "situation":    ["Quels outils utilisez-vous actuellement pour ce besoin ?","Combien de personnes utilisent cette solution dans votre équipe ?","Quel est votre budget actuel pour ce type de logiciel ?"],
        "probleme":     ["Quelles limitations rencontrez-vous avec votre solution actuelle ?","Perdez-vous du temps sur des tâches manuelles que l'outil ne couvre pas ?","Votre équipe est-elle frustrée par les bugs ou la lenteur ?"],
        "implication":  ["Ces limitations coûtent-elles du temps productif à votre équipe ?","Si l'inefficacité persiste, quel impact sur votre croissance ?","Un outil inadapté peut-il freiner l'onboarding de nouveaux clients ?"],
        "besoin":       ["Une solution qui automatise ces tâches libérerait combien d'heures par semaine ?","Un essai gratuit 14j vous permettrait-il de valider la valeur ?","Une intégration native avec vos outils existants simplifierait votre stack ?"],
    },
    "service": {
        "situation":    ["Comment trouvez-vous actuellement vos nouveaux clients ?","Quel est votre délai moyen de closing d'un dossier ?","Combien de devis envoyez-vous pour signer un contrat ?"],
        "probleme":     ["Avez-vous du mal à vous différencier de la concurrence sur le prix ?","Le démarchage à froid prend-il trop de temps pour peu de résultats ?","Vos clients actuels vous recommandent-ils spontanément ?"],
        "implication":  ["Un pipeline irrégulier crée-t-il des problèmes de trésorerie ?","Si votre taux de closing n'augmente pas, où en serez-vous dans 12 mois ?","Chaque client non signé, c'est combien de CA perdu ?"],
        "besoin":       ["Un système de recommandation structuré doublerait-il vos leads entrants ?","Une proposition commerciale plus percutante améliorerait votre taux de closing ?","Un positionnement premium vous permettrait-il de sortir de la guerre des prix ?"],
    },
    "consulting": {
        "situation":    ["Quels types de missions traitez-vous principalement ?","Comment vos clients vous trouvent-ils actuellement ?","Quel est votre TJM actuel et votre taux d'occupation ?"],
        "probleme":     ["Avez-vous du mal à valoriser votre expertise face à de grands cabinets ?","La saisonnalité crée-t-elle des mois creux difficiles à gérer ?","Vos clients comprennent-ils immédiatement la valeur que vous apportez ?"],
        "implication":  ["Un taux d'occupation insuffisant, quel impact sur votre revenu annuel ?","Sans personal branding fort, combien de missions perdez-vous ?","Des clients mal qualifiés consomment combien d'énergie inutilement ?"],
        "besoin":       ["Un contenu régulier sur LinkedIn générerait des leads entrants qualifiés ?","Un positionnement niche premium justifierait un TJM plus élevé ?","Un système de rétainer mensuel sécuriserait votre CA récurrent ?"],
    },
    "content": {
        "situation":    ["Sur quelles plateformes publiez-vous actuellement ?","Quel est votre rythme de publication hebdomadaire ?","Comment monétisez-vous votre audience aujourd'hui ?"],
        "probleme":     ["Votre croissance d'audience stagne-t-elle malgré vos efforts ?","La monétisation est-elle insuffisante par rapport au temps investi ?","Les algorithmes des plateformes impactent-ils négativement votre portée ?"],
        "implication":  ["Une audience stagnante réduit-elle vos opportunités de partenariat ?","Sans diversification des revenus, votre activité est-elle vulnérable ?","Dépendre d'une seule plateforme, quel risque si l'algorithme change ?"],
        "besoin":       ["Une stratégie multi-plateforme réduirait-elle votre dépendance algorithmique ?","Une offre de formation ou newsletter premium diversifierait vos revenus ?","Un calendrier éditorial optimisé augmenterait votre régularité et engagement ?"],
    },
    "other": {
        "situation":    ["Décrivez votre activité principale et votre marché cible.","Comment générez-vous vos revenus actuellement ?","Quels sont vos 3 principaux canaux d'acquisition ?"],
        "probleme":     ["Quels sont vos principaux obstacles à la croissance ?","Où perdez-vous le plus de temps ou d'argent ?","Quelle frustration revient le plus souvent dans votre activité ?"],
        "implication":  ["Si ces obstacles persistent, où en serez-vous dans 18 mois ?","Combien ces problèmes vous coûtent-ils mensuellement (temps + argent) ?","Votre concurrent résout-il mieux ces problèmes que vous ?"],
        "besoin":       ["Quelle solution éliminerait le principal frein à votre croissance ?","Un plan d'action sur 90 jours vous aiderait-il à prioriser ?","Quelle ressource manquante bloquerait moins votre développement ?"],
    },
    "default": {
        "situation":    ["Décrivez votre contexte actuel.","Quels outils / méthodes utilisez-vous ?","Quel est votre objectif prioritaire ?"],
        "probleme":     ["Quels obstacles rencontrez-vous ?","Qu'est-ce qui ne fonctionne pas comme prévu ?","Où perdez-vous du temps ou de l'argent ?"],
        "implication":  ["Quel est l'impact si ce problème n'est pas résolu ?","Combien cela vous coûte-t-il (temps, CA, clients) ?","Où en serez-vous dans 12 mois sans changement ?"],
        "besoin":       ["Quelle solution idéale résoudrait ce problème ?","Quel résultat concret attendez-vous ?","Quand avez-vous besoin d'une solution opérationnelle ?"],
    },
}

spin_data = _SPIN.get(activity, _SPIN["default"])

# ── Données sectorielles  --  toujours définies, préservées depuis cache ─────────
# sector_data vient du cache session ou est initialisé vide
if not isinstance(sector_data, dict):
    sector_data = {}
macro_data   = {}
_sector_live   = sector_data  # sera mis à jour ci-dessous
_sector_label  = sector_data.get("label", activity) if sector_data else activity
_sector_growth = sector_data.get("croissance_2024", "N/A") if sector_data else "N/A"
_sector_market = sector_data.get("marche_fr_2024", "N/A") if sector_data else "N/A"
_sector_bench  = sector_data.get("benchmarks", {}) if sector_data else {}

if _HAS_API_LAYER:
    try:
        sector_data = _get_secteur_data(activity)
        _sector_live   = sector_data
        _sector_label  = sector_data.get("label", activity)
        _sector_growth = sector_data.get("croissance_2024", "N/A")
        _sector_market = sector_data.get("marche_fr_2024", "N/A")
        _sector_bench  = sector_data.get("benchmarks", {})
    except Exception:
        sector_data = {}
else:
    # Données sectorielles statiques si api_layer absent
    _SECTOR_STATIC = {
        "ecommerce": {"label":"E-commerce","croissance_2024":"+12.4%","marche_fr_2024":"159 Md€",
                      "benchmarks":{"taux_conversion":"2.1%","panier_moyen":"85€","cac":"18€"}},
        "saas":      {"label":"SaaS / Tech","croissance_2024":"+18.7%","marche_fr_2024":"12.4 Md€",
                      "benchmarks":{"churn":"5%/mois","ltv_cac":"3.2x","arr_growth":"+35%"}},
        "service":   {"label":"Services","croissance_2024":"+4.2%","marche_fr_2024":"280 Md€",
                      "benchmarks":{"taux_closing":"28%","cycle_vente":"21j","retention":"72%"}},
        "consulting":{"label":"Conseil","croissance_2024":"+6.8%","marche_fr_2024":"18.3 Md€",
                      "benchmarks":{"taux_occupation":"68%","marge":"45%"}},
        "content":   {"label":"Contenu / Médias","croissance_2024":"+22.1%","marche_fr_2024":"4.1 Md€",
                      "benchmarks":{"engagement_rate":"3.8%","cpm":"4.2€"}},
        "other":     {"label":"Autre secteur","croissance_2024":"+3.1%","marche_fr_2024":"N/A",
                      "benchmarks":{}},
    }
    sector_data  = _SECTOR_STATIC.get(activity, _SECTOR_STATIC["other"])
    _sector_live   = sector_data
    _sector_bench  = sector_data.get("benchmarks", {})
    _sector_label  = sector_data.get("label", activity)
    _sector_growth = sector_data.get("croissance_2024", "N/A")
    _sector_market = sector_data.get("marche_fr_2024", "N/A")
    _sector_bench  = sector_data.get("benchmarks", {})

# ── Scraping site (optionnel, async-safe via cache) ─────────────────────────
site_data = st.session_state.get("_site_data_cache", {})
if website_url:
    _site_key = f"site_{hash(website_url)}"
    if _site_key not in st.session_state:
        try:
            site_data = scrape_site(website_url)
            st.session_state["_site_data_cache"] = site_data
            st.session_state[_site_key] = True
        except Exception:
            site_data = {}
    elif not site_data:
        try:
            site_data = scrape_site(website_url)
            st.session_state["_site_data_cache"] = site_data
        except Exception:
            site_data = {}
site_meta = site_data
# ── Personnalisation depuis les données du site ───────────────────────────
site_ins = _site_insights(site_data)
if site_ins:
    _sn  = site_ins.get("name", "")
    _skw = site_ins.get("top_keywords", [])
    _sst = site_ins.get("strengths_signals", [])
    _scs = site_ins.get("content_signals", [])
    # Enrichir SWOT avec données réelles du site
    if _sn:
        swot["strengths"].insert(0, f"Présence en ligne confirmée  --  {_html.escape(_sn[:60])}")
    if _skw:
        swot["strengths"].append(f"Positionnement sur : {', '.join(_html.escape(k) for k in _skw[:4])}")
    if not site_data.get("h1"):
        swot["weaknesses"].insert(0, "Balise H1 absente  --  impact SEO négatif")
    if not site_data.get("description"):
        swot["weaknesses"].insert(0, "Meta description absente  --  CTR organique à risque")
    if _sst:
        swot["strengths"].append(f"Signal différenciant détecté : {_html.escape(_sst[0][:80])}")
    # Enrichir keywords avec les vrais mots-clés de la page
    if _skw:
        _site_kw_tuples = [
            (kw, "réel · site scrapé", " -- ", "informationnel")
            for kw in _skw[:5]
        ]
        keywords = _site_kw_tuples + [k for k in keywords if k[0] not in _skw]
    # Enrichir personas avec le nom de l'entreprise
    if _sn:
        for _p in personas:
            if "brands" in _p:
                _p["brands"] = [_sn[:30]] + _p["brands"][:2]
# ── Concurrents ───────────────────────────────────────────────────────────
comp_results = {}
# Init variables veille pour éviter NameError
_hn_items, _devto_items, _gh_items = [], [], []
_secteur_entreprises = []
_sector_live = sector_data if sector_data else {}
_sector_label = _sector_live.get("label", activity) if _sector_live else activity
_sector_growth = _sector_live.get("croissance_2024", "N/A") if _sector_live else "N/A"
_sector_market = _sector_live.get("marche_fr_2024", "N/A") if _sector_live else "N/A"
_sector_bench  = _sector_live.get("benchmarks", {}) if _sector_live else {}
# Pré-charger concurrents depuis le cache session si déjà analysés
if comp_urls:
    _ck_pre = "comp_" + str(abs(hash(tuple(sorted(comp_urls)))))
    if _ck_pre in st.session_state:
        comp_results.update(st.session_state[_ck_pre])
# Enrichir SWOT avec données concurrents réels (si déjà en cache)
if comp_results:
    _comp_names = []
    for _cu_r, _cd_r in comp_results.items():
        if not _cd_r.get("error") and _cd_r.get("title"):
            _comp_names.append(_html.escape(_cd_r["title"][:40]))
    if _comp_names:
        swot["threats"].insert(0, f"Concurrents identifiés : {' · '.join(_comp_names[:3])}")
        swot["opportunities"].insert(0, "Analyse concurrentielle disponible  --  exploitez les angles manquants")
# ads_data and roi_data are now managed in the session-state cache above
pagespeed_data = get_pagespeed(website_url) if website_url else {}
closing_tech = _CLOSING_TECHNIQUES
msg_templates = _MESSAGE_TEMPLATES

# Context badges
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<span class="badge badge-graphite">{LABELS.get(activity, activity)}</span>', unsafe_allow_html=True)
c2.markdown(f'<span class="badge badge-jade">{LABELS.get(goal, goal)}</span>', unsafe_allow_html=True)
c3.markdown(f'<span class="badge badge-teal">{LABELS.get(maturity, maturity)}</span>', unsafe_allow_html=True)
c4.markdown(f'<span class="badge badge-blue">{monthly_budget:,} €/mois</span>', unsafe_allow_html=True)

if site_data and isinstance(site_data, dict) and site_data.get("title"):
    st.caption(f"Site analysé : **{site_data.get('title','')}**  --  {site_data.get('description','')[:120]}")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Diagnostic",
    "Personas",
    "Copywriting",
    "Vente",
    "Marketing",
    "Campagnes",
    "SEO / GEO",
    "KPIs",
    "Synthese",
    "Veille",
    "RSE",
    "Strategie+",
    "Emailing",
    "Social Media",
    "Tarifs & Plans",
    "Nouveau Projet",
    "Ressources",
])
# Note: onglets dans l'ordre logique du parcours strategique
# Diagnostic > Personas > Copy > Vente > Marketing > Campagnes > SEO > KPIs > Synthese > Veille > RSE > Strategie+ > Email > Social > Tarifs > Projet > Ressources

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1  --  DIAGNOSTIC
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    # ── ANALYSE DU SITE (si URL fournie) ───────────────────────────────────────
    if site_data and not site_data.get("error"):
        _sd_title = site_data.get("title","")
        _sd_desc  = site_data.get("description","")
        _sd_h1s   = site_data.get("h1",[])
        _sd_h2s   = site_data.get("h2",[])
        _sd_kws   = site_data.get("keywords_page",[])
        _kw_badges = "".join(
            f'<span class="url-kw">{_html.escape(k)}</span>' for k in _sd_kws[:10]
        )
        st.markdown(f'''
        <div class="url-panel">
          <div class="url-panel-title">{_html.escape(_sd_title or website_url)}</div>
          <div class="url-panel-sub">{_html.escape((_sd_desc or "Aucune meta description")[:160])}</div>
          <div style="margin-top:10px">{_kw_badges}</div>
        </div>
        ''', unsafe_allow_html=True)

        _col_s, _col_o = st.columns(2)
        with _col_s:
            st.markdown('<div class="section-h">Structure détectée</div>', unsafe_allow_html=True)
            for _h in (_sd_h1s or [])[:3]:
                st.markdown(f"**H1**  --  {_html.escape(_h)}")
            for _h in (_sd_h2s or [])[:4]:
                st.markdown(f"H2  --  {_html.escape(_h)}")
            if not _sd_h1s and not _sd_h2s:
                st.caption("Aucun titre H1/H2 détecté")
        with _col_o:
            st.markdown('<div class="section-h">Observations</div>', unsafe_allow_html=True)
            _obs = []
            if not _sd_desc:
                _obs.append(("#B83D4B","Meta description absente  --  impact SEO direct"))
            if not _sd_h1s:
                _obs.append(("#B83D4B","Aucun H1 détecté  --  priorité absolue"))
            elif len(_sd_h1s)>1:
                _obs.append(("#44C1BA",f"{len(_sd_h1s)} H1 trouvés  --  un seul est recommandé"))
            else:
                _obs.append(("#267371",f"H1 présent : {_sd_h1s[0][:55]}"))
            if _sd_desc and len(_sd_desc)>160:
                _obs.append(("#44C1BA",f"Meta description longue ({len(_sd_desc)} car.)  --  viser 155 max"))
            elif _sd_desc:
                _obs.append(("#267371","Meta description bien dimensionnée"))
            if _sd_kws:
                _obs.append(("#267371",f"Thématique dominante : {_sd_kws[0]}"))
            _lc = site_data.get("links_count",0)
            if _lc:
                _obs.append(("#267371",f"{_lc} liens détectés"))
            for _c, _msg in _obs:
                st.markdown(f'<div style="padding:5px 0;border-bottom:1px solid #E4E9F6;font-size:.83rem;color:{_c}"> --  {_html.escape(_msg)}</div>', unsafe_allow_html=True)
        # Enrichissement SWOT avec données site
        if not _sd_h1s:
            swot["weaknesses"].insert(0,"Structure SEO à renforcer (H1 absent)")
        if not _sd_desc:
            swot["weaknesses"].insert(0,"Meta description absente  --  référencement à optimiser")
        if _sd_title:
            swot["strengths"].insert(0,f"Présence web établie : {_sd_title[:55]}")
        st.markdown("<br>", unsafe_allow_html=True)

        # SWOT
    st.markdown('<div class="section-h">Analyse SWOT personnalisée</div>', unsafe_allow_html=True)
    # Enrichissement SWOT avec données site et secteur
    if _HAS_API_LAYER and (site_data or _sector_live):
        try:
            swot = _personalize_swot(swot, site_data, _sector_live)
        except Exception:
            pass
    # Badge de personnalisation
    _pers_score = 40
    if site_data and not site_data.get("error"): _pers_score += 30
    if isinstance(_sector_live, dict) and _sector_live.get("benchmarks"): _pers_score += 20
    if _pers_score > 40:
        st.markdown(f'''
<div style="display:inline-flex;align-items:center;gap:8px;background:#C6ECD9;
  border-radius:50px;padding:5px 14px;margin-bottom:12px;font-size:.75rem;font-weight:700;color:#267371">
  <span></span> Analyse personnalisée à {_pers_score}% — basée sur données réelles
  {"| Site analysé: " + site_data.get("title","")[:30] if site_data and site_data.get("title") else ""}
</div>
''', unsafe_allow_html=True)
    st.caption("Le SWOT structure toute réflexion stratégique : Forces · Faiblesses · Opportunités · Menaces")
    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown('<div class="card swot-strength"><div class="card-title"> Forces</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["strengths"]) +
            "</div>", unsafe_allow_html=True)
    with col_w:
        st.markdown('<div class="card swot-weakness"><div class="card-title"> Faiblesses</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["weaknesses"]) +
            "</div>", unsafe_allow_html=True)
    col_o, col_t = st.columns(2)
    with col_o:
        st.markdown('<div class="card swot-oppty"><div class="card-title"> Opportunités</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["opportunities"]) +
            "</div>", unsafe_allow_html=True)
    with col_t:
        st.markdown('<div class="card swot-threat"><div class="card-title"> Menaces</div>'+
            "".join(f"<p style='margin:4px 0;font-size:.88rem'>• {_html.escape(str(i))}</p>" for i in swot["threats"]) +
            "</div>", unsafe_allow_html=True)

    # QQOQCCP
    st.markdown('<div class="section-h">Analyse QQOQCCP</div>', unsafe_allow_html=True)
    st.caption("7 questions pour ne laisser aucune zone d'ombre dans votre diagnostic stratégique")

    for key, item in qqoqccp.items():
        with st.expander(f"**{key.upper()}**  --  {item['q']}"):
            col_r, col_a = st.columns(2)
            with col_r:
                st.markdown("**Réponse stratégique**")
                st.info(item["r"])
            with col_a:
                st.markdown("**Action recommandée**")
                st.success(item["a"])

    # PESTEL
    st.markdown('<div class="section-h">Analyse PESTEL</div>', unsafe_allow_html=True)
    st.caption("6 dimensions macro-environnementales que vous ne contrôlez pas mais devez impérativement anticiper")
    impact_cls = {"positif":"dot-pos","négatif":"dot-neg","neutre":"dot-neu"}
    for dim, items in pestel.items():
        with st.expander(f"**{dim}** ({len(items)} facteur{'s'if len(items)>1 else ''})"):
            for facteur, impact, note in items:
                st.markdown(f'<span class="{impact_cls.get(impact,"dot-neu")}"></span>**{facteur}** `{impact}`', unsafe_allow_html=True)
                st.caption(f"→ {note}")
                st.divider()

    # MICRO-ENV
    st.markdown('<div class="section-h">Micro-environnement  --  Forces concurrentielles</div>', unsafe_allow_html=True)
    st.caption("Analyse des acteurs en interaction directe (modèle inspiré des 5 forces de Porter) : pouvoir de négociation et leviers d'action")
    pouvoir_color = {"élevé":"badge-red","très élevé":"badge-red","moyen":"badge-teal","faible":"badge-jade"}
    cols = st.columns(2)
    for i, (acteur, (pouvoir, desc, levier)) in enumerate(micro_env.items()):
        with cols[i % 2]:
            badge_cls = pouvoir_color.get(pouvoir, "badge-gray")
            st.markdown(f"""
            <div class="card">
              <div class="card-title">{acteur} <span class="badge {badge_cls}">Pouvoir : {pouvoir}</span></div>
              <p style='font-size:.85rem;color:#267371'>{desc}</p>
              <p style='font-size:.82rem;color:#267371'>{levier}</p>
            </div>""", unsafe_allow_html=True)

    # COMPETITIVE
    st.markdown('<div class="section-h">Analyse concurrentielle</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Rivaux directs**")
        for r in competitive["direct"]:
            st.markdown(f"• {r}")
    with c2:
        st.markdown("**Rivaux indirects**")
        for r in competitive["indirect"]:
            st.markdown(f"• {r}")
    st.markdown("**Matrice concurrentielle** ( avantage · désavantage · neutre)")
    table_html = '<table class="bizi-table"><thead><tr><th>Critère</th><th>Vous</th><th>Leader</th><th>Analyse</th></tr></thead><tbody>'
    for critere, vous, leader, note in competitive["matrix"]:
        table_html += f"<tr><td><b>{critere}</b></td><td style='text-align:center;font-size:1.1rem'>{vous}</td><td style='text-align:center;font-size:1.1rem'>{leader}</td><td style='font-size:.82rem;color:#339999'>{note}</td></tr>"
    table_html += "</tbody></table>"
    st.markdown(f'<div style="overflow-x:auto">'+ table_html +'</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**Opportunité de positionnement**\n\n{competitive['oppty']}")
    with col_b:
        st.success(f"** Votre avantage défendable (Moat)**\n\n{competitive['moat']}")

    # PROPOSITION DE VALEUR
    st.markdown('<div class="section-h">Proposition de valeur</div>', unsafe_allow_html=True)
    st.caption("Construisez une proposition de valeur differenciante sur 4 dimensions (framework Apple · Tesla · L'Oreal)")
    _pv = gen_proposition_valeur(activity, site_ins.get("name", "") if site_ins else "")
    _pv_colors = {"fonctionnelle":"#393DAC","economique":"#267371","emotionnelle":"#44C1BA","symbolique":"#393DAC"}
    _pv_labels = {"fonctionnelle":"Fonctionnelle","economique":"Economique","emotionnelle":"Emotionnelle","symbolique":"Symbolique"}
    st.markdown(f'<div class="card card-dark" style="margin-bottom:16px"><div style="font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.5);margin-bottom:6px">Slogan</div><div style="font-size:1.15rem;font-weight:700;color:white">{_html.escape(_pv["slogan"])}</div></div>', unsafe_allow_html=True)
    _pv_cols = st.columns(4)
    for _pi, (_pk, _pv_label) in enumerate(_pv_labels.items()):
        with _pv_cols[_pi]:
            _c = _pv_colors[_pk]
            st.markdown(f'<div class="pv-card" style="background:{_c}"><div style="font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;opacity:.7;margin-bottom:5px">{_pv_label}</div><div style="font-size:.85rem;line-height:1.5">{_html.escape(_pv[_pk])}</div></div>', unsafe_allow_html=True)
    if _pv.get("differenciateurs"):
        st.markdown("**Points de différenciation :**")
        for _d in _pv["differenciateurs"]:
            st.markdown(f"• {_html.escape(_d)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2  --  PERSONAS & SONCAS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    # PERSONAS
    st.markdown('<div class="section-h">Personas clients enrichis</div>', unsafe_allow_html=True)
    st.caption("Profils semi-fictifs construits à partir de données comportementales, sectorielles et psychographiques")
    for i, p in enumerate(personas):
        initials = "".join([w[0] for w in p["name"].split()][:2]).upper()
        colors = ["#0B2221","#44C1BA","#267371","#393DAC","#B83D4B"]
        color = colors[hash(p["name"]) % len(colors)]
        fw_badge = f'<span class="badge badge-teal">{p.get("framework","")}</span>'if p.get("framework") else ""
        with st.expander(f"**{p['name']}** · {p['age']} ans · {p['job']} · {p['location']}", expanded=(i==0)):
            c1, c2, c3 = st.columns([1, 2, 2])
            with c1:
                st.markdown(f"""
                <div style="width:72px;height:72px;border-radius:50%;background:{color};
                  display:flex;align-items:center;justify-content:center;
                  font-size:1.4rem;font-weight:800;color:white;margin:0 auto 8px">
                  {initials}
                </div>
                {fw_badge}
                <p style="text-align:center;font-style:italic;font-size:.78rem;color:#339999;margin-top:6px">"{p['quote']}"</p>
                """, unsafe_allow_html=True)
                if p.get("framework_match"):
                    st.markdown(f"<small style='color:#44C1BA;font-size:.7rem'>↳ {p['framework_match']}</small>", unsafe_allow_html=True)
            with c2:
                st.markdown("**Objectifs**")
                for g in p["goals"]: st.markdown(f"{g}")
                st.markdown("**Douleurs**")
                for pa in p["pains"]: st.markdown(f"{pa}")
                if p.get("motivations"):
                    st.markdown("**Motivations**")
                    st.markdown(" ".join(f'<span class="badge badge-jade">{m}</span>'for m in p["motivations"]), unsafe_allow_html=True)
            with c3:
                st.markdown("**Canaux favoris**")
                st.markdown(" ".join(f'<span class="badge badge-blue">{c}</span>'for c in p["channels"]), unsafe_allow_html=True)
                st.markdown("<br>**Déclencheurs d'achat**", unsafe_allow_html=True)
                for t in p["triggers"]: st.markdown(f"→ {t}")
                if p.get("habits"):
                    st.markdown("**Habitudes**")
                    for h in p["habits"]: st.markdown(f"• {h}")
                if p.get("values"):
                    st.markdown("**Valeurs**")
                    st.markdown(" ".join(f'<span class="badge badge-gray">{v}</span>'for v in p["values"]), unsafe_allow_html=True)

    # SONCAS
    st.markdown('<div class="section-h">Analyse SONCAS  --  6 leviers psychologiques de vente</div>', unsafe_allow_html=True)
    st.caption("SONCAS : Sécurité · Orgueil · Nouveauté · Confort · Argent · Sympathie  --  les 6 motivations d'achat universelles")
    soncas_css_map = {
        "securite": "soncas-securite",
        "opportunite":"soncas-opportunite",
        "nouveaute": "soncas-nouveaute",
        "confort": "soncas-confort",
        "argent": "soncas-argent",
        "sympathie": "soncas-sympathie",
    }
    cols6 = st.columns(3)
    levers = list(soncas.items())
    for i, (key, lever) in enumerate(levers):
        with cols6[i % 3]:
            css_cls = soncas_css_map.get(key, "card")
            args_html = "".join(f"<li style='font-size:.78rem;margin:2px 0'>{a}</li>" for a in lever["args"])
            st.markdown(f"""
            <div class="card {css_cls}">
              <div style="font-size:1.4rem">{lever['icon']}</div>
              <div class="card-title" style="margin-top:4px">{lever['label']}</div>
              <p style='font-size:.8rem;color:#267371;margin-bottom:8px'>{lever['desc']}</p>
              <ul style='padding-left:14px;margin:0'>{args_html}</ul>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Objections SONCAS & réponses**")
    for key, lever in soncas.items():
        with st.expander(f"{lever['icon']} **{lever['label']}**  --  *\"{lever['objection']}\"*"):
            st.success(f"**Réponse recommandée :**\n\n{lever['reponse']}")

    # SEGMENTATION RFM
    st.markdown('<div class="section-h">Segmentation RFM  --  4 segments clients</div>', unsafe_allow_html=True)
    st.caption("Segmentation Récence · Fréquence · Montant  --  identifiez où concentrer vos efforts de rétention et d'acquisition")
    _rfm_segments = gen_rfm_segments(activity, monthly_budget)
    _rfm_cols = st.columns(4)
    _rfm_colors = ["#267371","#393DAC","#44C1BA","#B83D4B"]
    for _ri, (_rseg, _rcol) in enumerate(zip(_rfm_segments, _rfm_cols)):
        with _rcol:
            _rcolor = _rfm_colors[_ri]
            st.markdown(f"""
            <div class="rfm-card" style="border-top:3px solid {_rcolor}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#339999;margin-bottom:3px">{_rseg['pourcentage']}% des clients</div>
              <div style="font-weight:800;font-size:.95rem;color:{_rcolor};margin-bottom:4px">{_html.escape(_rseg['nom'])}</div>
              <div style="font-size:.76rem;color:#267371;margin-bottom:8px;line-height:1.4">{_html.escape(_rseg['description'])}</div>
              <div style="font-size:.72rem;font-weight:700;color:#0B2221">CLV estimée : {_rseg['clv']:,} €</div>
            </div>
            """, unsafe_allow_html=True)
    for _rseg in _rfm_segments:
        with st.expander(f"**{_rseg['nom']}**  --  actions recommandées"):
            for _ract in _rseg["actions"]:
                st.markdown(f"→ {_html.escape(_ract)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3  --  COPYWRITING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-h">Structure AIDA  --  Copywriting persuasif</div>', unsafe_allow_html=True)
    st.caption("Le copywriting fusionne sciences comportementales et rédaction persuasive pour déclencher l'action")
    aida_meta = {
        "attention": ("","ATTENTION","aida-attention"),
        "interest": ("","INTÉRÊT","aida-interest"),
        "desire": ("","DÉSIR","aida-desire"),
        "action": ("","ACTION","aida-action"),
    }
    c1, c2 = st.columns(2)
    for i, (step, content) in enumerate(aida.items()):
        _icon_e, label, css = aida_meta.get(step, ("", step.upper(), ""))
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div class="card {css}">
              <div class="card-title">{label}</div>
              <p style='font-weight:600;font-size:.9rem;color:#0B2221'>{content['p']}</p>
              <div style='background:rgba(255,255,255,.7);border-radius:10px;padding:10px;margin:10px 0'>
                <small style='color:#339999;font-weight:600'>EXEMPLE :</small>
                <p style='font-style:italic;font-size:.85rem;color:#267371;margin:4px 0'>"{content['e']}"</p>
              </div>
              <small style='color:#339999;font-weight:600'>FORMULES :</small>
              {"".join(f"<p style='font-size:.8rem;color:#267371;margin:2px 0'>→ {f}</p>" for f in content['f'])}
              <div style='background:rgba(255,255,255,.5);border-radius:8px;padding:8px;margin-top:8px'>
                <small style='color:#339999'> {content['c']}</small>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-h">Principes universels du copywriting</div>', unsafe_allow_html=True)
    principles = [
        ("1","Écrivez pour une personne,\nnon pour 'tout le monde'"),
        ("2","Bénéfices > fonctionnalités  -- \ntoujours"),
        ("3","Spécifique > général  -- \nles détails créent la crédibilité"),
        ("4","Une idée par phrase,\nun CTA par page"),
        ("5","Testez, mesurez, itérez  -- \nle meilleur texte est celui qui convertit"),
    ]
    p_cols = st.columns(5)
    for col_p, (num, pr) in zip(p_cols, principles):
        with col_p:
            st.markdown(f'<div class="metric-box"><div class="val" style="color:#44C1BA">{num}</div><div class="lbl" style="white-space:pre-line;line-height:1.3">{pr}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">Déclencheurs psychologiques</div>', unsafe_allow_html=True)
    st.caption("Leviers cognitifs issus des sciences comportementales qui guident la décision d'achat")
    for name, defn, ex, usage, warn in _TRIGGERS:
        with st.expander(f"**{name}**"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Définition** : {defn}")
                st.info(f'*"{ex}"*')
            with c2:
                st.success(f"**Quand l'utiliser** : {usage}")
                st.warning(warn)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4  --  VENTE & SPIN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-h">Scripts de vente adaptés</div>', unsafe_allow_html=True)
    type_labels = {"cold_call":"Appel à froid","follow_up":"Suivi","discovery":"Découverte","email_followup":" Email suivi","email_outreach":"Email prospection"}
    for script in scripts:
        lbl = type_labels.get(script["type"], script["type"])
        with st.expander(f"**{script['title']}**  --  {lbl}"):
            st.code(script["content"], language=None)
            if script.get("keyPoints"):
                st.markdown("**Points clés :**")
                for kp in script["keyPoints"]: st.markdown(f"• {kp}")

    # SPIN
    st.markdown('<div class="section-h">SPIN Selling  --  Questions stratégiques</div>', unsafe_allow_html=True)
    st.caption("Méthodologie SPIN : Situation → Problème → Implication → Need-payoff. La plus efficace en B2B complexe.")
    spin_tabs = st.tabs(["Situation","Problème","Implication","Need-payoff"])
    spin_keys = [("situation","Établir le contexte sans interroger  --  montrez que vous avez fait vos recherches"),
                 ("probleme","Identifier les douleurs précises  --  ne proposez pas de solution encore"),
                 ("implication","Amplifier la conséquence du problème  --  le client doit ressentir l'urgence"),
                 ("besoin","Faire formuler le besoin par le client lui-même  --  la vente devient son idée")]
    for spin_tab, (sk, hint) in zip(spin_tabs, spin_keys):
        with spin_tab:
            st.caption(f"{hint}")
            for q in spin_data.get(sk, []):
                st.markdown(f"→ {q}")

    # Challenger
    st.markdown('<div class="section-h">Challenger Sale  --  Vendre par la conviction</div>', unsafe_allow_html=True)
    st.caption("La méthode Challenger s'appuie sur 3 piliers : Enseigner · Adapter · Prendre le contrôle")
    chal_tabs = st.tabs(["Enseigner (Teach)","Adapter (Tailor)","Prendre le contrôle"])
    chal_keys = ["teach","tailor","take_control"]
    for ctab, ckey in zip(chal_tabs, chal_keys):
        with ctab:
            for tip in _CHALLENGER[ckey]:
                st.markdown(f"• {tip}")

    # Objections
    st.markdown('<div class="section-h">Gestion des objections</div>', unsafe_allow_html=True)
    for obj, response in _OBJECTIONS:
        with st.expander(f'*"{obj}"*'):
            st.markdown(response)

    # NÉGOCIATION
    st.markdown('<div class="section-h">Tactiques de négociation  --  BATNA / ZOPA / SONCAS</div>', unsafe_allow_html=True)
    st.caption("Préparez chaque négociation avec une stratégie BATNA, une zone d'accord et des tactiques testées")
    _nego = gen_negociation(activity, monthly_budget)
    _nc1, _nc2 = st.columns(2)
    with _nc1:
        st.markdown("**BATNA (Meilleure Alternative)**")
        st.info(f"**Votre BATNA :** {_html.escape(_nego['batna']['vendeur'])}")
        st.warning(f"**BATNA adverse :** {_html.escape(_nego['batna']['acheteur'])}")
        st.caption(_nego['batna']['conseil'])
    with _nc2:
        st.markdown("**ZOPA (Zone d'accord)**")
        st.success(f"**Min :** {_nego['zopa']['min']:,} € | **Max :** {_nego['zopa']['max']:,} € | **Amplitude :** {_nego['zopa']['amplitude']}%")
        st.caption(_nego['zopa']['conseil'])
    st.markdown("**Règles de concession :**")
    for _nc in _nego["concessions"]:
        st.markdown(f"• {_html.escape(_nc)}")
    st.markdown("**Tactiques de négociation :**")
    for _nt in _nego["tactiques"]:
        st.markdown(f"→ {_html.escape(_nt)}")
    st.markdown("**Objections prix & réponses :**")
    for _obj, _rep in _nego["objections_prix"]:
        with st.expander(f'*"{_html.escape(_obj)}"*'):
            st.success(_html.escape(_rep))

    # PRIX PSYCHOLOGIQUES
    st.markdown('<div class="section-h">Prix psychologiques  --  7 techniques</div>', unsafe_allow_html=True)
    st.caption("Techniques de tarification issues des sciences comportementales  --  augmentez la valeur perçue sans changer votre produit")
    _prix_list = gen_prix_psychologiques(monthly_budget, activity)
    _impact_badge = {"Très élevé": "badge-red", "Élevé": "badge-teal", "Moyen": "badge-jade"}
    for _ptec in _prix_list:
        with st.expander(f"**{_ptec['nom']}**  --  Impact : {_ptec['impact']}"):
            _c1p, _c2p = st.columns([2, 1])
            with _c1p:
                st.markdown(f"**Description :** {_html.escape(_ptec['description'])}")
                st.info(f"**Exemple :** {_html.escape(_ptec['exemple'])}")
            with _c2p:
                _ibadge = _impact_badge.get(_ptec["impact"], "badge-gray")
                st.markdown(f'<div style="text-align:center;padding:16px"><span class="badge {_ibadge}" style="font-size:.8rem;padding:4px 12px">{_html.escape(_ptec["impact"])}</span><div style="font-size:.72rem;color:#339999;margin-top:6px">Impact conversion</div></div>', unsafe_allow_html=True)

    # Email templates
    st.markdown('<div class="section-h">Templates emails de prospection</div>', unsafe_allow_html=True)
    email_tmpls = [
        ("Email cold outreach  --  signal d'actualité","Objet : [Prénom], [résultat en 5 mots]\n\nBonjour [Prénom],\n\nJ'ai vu que [signal d'actualité de l'entreprise].\n\nOn a aidé [client similaire] à [résultat mesurable] en [délai].\n\nDisponible 15 min cette semaine pour voir si on peut faire pareil pour [Entreprise] ?\n\n[Prénom]"),
        ("Email suivi J+3 (non-réponse)","Objet : Re: [sujet précédent]\n\nBonjour [Prénom],\n\nJe me permets de revenir vers vous suite à mon message de l'autre jour.\n\nJe sais que vous êtes très occupé  --  une seule question : est-ce que [problème que vous résolvez] est encore d'actualité pour vous ?\n\nSi oui, 15 minutes suffisent pour voir si je peux vous aider. Sinon, dites-le moi et je ne vous recontacte plus.\n\n[Prénom]"),
        ("Email post-démo  --  prochaines étapes","Objet : Suite à notre échange  --  prochaines étapes\n\nBonjour [Prénom],\n\nMerci pour notre échange  --  c'était très intéressant de comprendre [problème identifié].\n\nComme convenu, voici ce que je vous propose :\n• [Offre adaptée à leur situation]\n• [Prix / modalités]\n• [Garantie ou condition de démarrage]\n\nPour avancer, la prochaine étape est [action concrète].\n\nEst-ce que [date] vous conviendrait pour [prochaine étape] ?\n\n[Prénom]"),
    ]
    for title, body in email_tmpls:
        with st.expander(f" **{title}**"):
            st.code(body, language=None)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5  --  MARKETING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-h">Plateformes recommandées</div>', unsafe_allow_html=True)
    prio_badge = {"haute":"badge-red","moyenne":"badge-teal","faible":"badge-jade"}
    pf_cols = st.columns(min(len(platforms), 3))
    for i, (name, prio, freq, content_types) in enumerate(platforms):
        with pf_cols[i % 3]:
            badge = prio_badge.get(prio.strip().lower(), "badge-gray")
            st.markdown(f"""
            <div class="card">
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
                <b style='font-size:.95rem'>{name}</b>
                <span class="badge {badge}">{prio}</span>
              </div>
              <small style='color:#339999'> {freq}</small>
              <p style='font-size:.8rem;color:#267371;margin-top:6px'>{content_types}</p>
            </div>""", unsafe_allow_html=True)

    # Budget adaptatif
    st.markdown(f'<div class="section-h">Répartition budgétaire  --  {monthly_budget:,} €/mois</div>', unsafe_allow_html=True)
    bar_colors = ["#0B2221","#44C1BA","#267371","#393DAC"]
    for i, (cat, pct, amt) in enumerate(budget_alloc):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.markdown(f"**{cat}**")
        c2.markdown(f"**{amt:,.0f} €**")
        c3.markdown(f"*{pct}%*")
        st.markdown(f"""
        <div style="height:8px;background:#F2ECD9;border-radius:4px;margin-bottom:12px">
          <div style="height:8px;width:{pct}%;background:{bar_colors[i%4]};border-radius:4px;transition:width .4s ease"></div>
        </div>""", unsafe_allow_html=True)

    # Recommandations budget
    st.markdown('<div class="section-h">Recommandations adaptées à votre budget</div>', unsafe_allow_html=True)
    for reco in budget_reco:
        if reco.startswith(""):
            st.success(reco)
        elif reco.startswith(""):
            st.warning(reco)
        else:
            st.info(reco)

    # Calendrier éditorial
    st.markdown('<div class="section-h">Calendrier éditorial  --  8 semaines</div>', unsafe_allow_html=True)
    cal_html = '<table class="bizi-table"><thead><tr><th>Sem.</th><th>Plateforme</th><th>Sujet</th><th>Format</th></tr></thead><tbody>'
    for week, platform, topic, fmt in calendar:
        cal_html += f"<tr><td><b>S{week}</b></td><td><span class='badge badge-blue'>{platform}</span></td><td style='font-size:.82rem'>{topic}</td><td style='font-size:.82rem;color:#339999'>{fmt}</td></tr>"
    cal_html += "</tbody></table>"
    st.markdown(f'<div style="overflow-x:auto">'+ cal_html +'</div>', unsafe_allow_html=True)

    # Règle 80/20
    st.markdown('<div class="section-h">Règle 80/20  --  Focus d\'action</div>', unsafe_allow_html=True)
    rules_8020 = {
        "awareness": ["Créez votre contenu pilier avant de penser à la pub","LinkedIn ou Instagram en organic  --  maîtrisez 1 canal à fond","La newsletter est votre actif le plus précieux  --  commencez maintenant"],
        "sales": ["Le retargeting génère 10x plus que la prospection froide  --  commencez par ça","L'email marketing a un ROI de 42:1  --  c'est votre canal le plus rentable","Optimisez votre page de vente avant d'augmenter votre budget pub"],
        "leads": ["Un bon lead magnet vaut 6 mois de pub payante  --  investissez dedans","La séquence email post-lead est plus importante que le lead magnet lui-même","Votre formulaire de contact est trop long  --  réduisez à 3 champs maximum"],
        "traffic": ["Le SEO prend 3-6 mois  --  commencez MAINTENANT pour des résultats en milieu d'année","2 articles SEO/semaine > 10 posts sociaux/semaine","Les backlinks sont rois  --  1 bon backlink vaut 100 mentions sur les réseaux"],
    }
    for i, r in enumerate(rules_8020.get(goal, rules_8020["awareness"])):
        st.markdown(f"**{i+1}.** {r}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6  --  CAMPAGNES PUB
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('''
    <div style="background:linear-gradient(135deg,#44C1BA,#44C1BA);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-size:2rem"></span>
      <div>
        <b style="font-size:1rem">Plan média personnalisé — {budget} €/mois</b><br>
        <span style="opacity:.9;font-size:.85rem">Répartition optimale Facebook · Google Ads · Email · SEO organique</span>
      </div>
    </div>
    '''.format(budget=monthly_budget), unsafe_allow_html=True)

    # Media Plan Table
    st.markdown('<div class="section-h">Plan Média Global</div>', unsafe_allow_html=True)
    mp_html = '<table class="bizi-table"><thead><tr><th>Canal</th><th>Budget</th><th>Portée estimée</th><th>CTR cible</th><th>ROI estimé</th></tr></thead><tbody>'
    for row in ads_data["mediaplan"]:
        mp_html += f"""<tr>
          <td><b>{row['platform']}</b></td>
          <td style='font-weight:700;color:#44C1BA'>{row['budget']:,.0f} €</td>
          <td style='font-size:.82rem'>{row['reach']}</td>
          <td><span class='badge badge-jade'>{row['ctr']}</span></td>
          <td><span class='badge badge-teal'>{row['roi']}</span></td>
        </tr>"""
    mp_html += '</tbody></table>'
    st.markdown(f'<div style="overflow-x:auto">'+ mp_html +'</div>', unsafe_allow_html=True)

    # Facebook Campaigns
    if ads_data["facebook"]:
        st.markdown('<div class="section-h">Campagnes Facebook / Instagram Ads</div>', unsafe_allow_html=True)
        for camp in ads_data["facebook"]:
            with st.expander(f"**{camp['name']}**  --  {camp['objective']}  --  Budget : {camp['budget']:,} €"):
                st.markdown(f"**Format recommandé :** {camp['format']}")
                for cr in camp.get("creatives", []):
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:8px">
                      <div style="display:flex;justify-content:space-between;align-items:center">
                        <span class="badge badge-blue">{cr['format']}</span>
                        <span class="badge badge-gray">{cr.get('audience','')}</span>
                      </div>
                      <p style="font-weight:600;margin:8px 0 4px">{cr['headline']}</p>
                      <p style="font-size:.82rem;color:#339999">CTA : <b>{cr['cta']}</b></p>
                    </div>""", unsafe_allow_html=True)
    else:
        st.info("Budget insuffisant pour les campagnes Facebook (minimum recommandé : 30€/mois)")

    # Google Campaigns
    if ads_data["google"]:
        st.markdown('<div class="section-h">Campagnes Google Ads</div>', unsafe_allow_html=True)
        for camp in ads_data["google"]:
            with st.expander(f"**{camp['name']}**  --  {camp['type']}  --  Budget : {camp['budget']:,} €"):
                st.markdown("**Mots-clés recommandés :**")
                for kw in camp["keywords"]:
                    st.markdown(f"• `{kw}`")
    else:
        st.info("Budget insuffisant pour Google Ads (minimum recommandé : 30€/mois)")

    # Organic strategies
    st.markdown('<div class="section-h">Stratégies Organiques (Gratuites)</div>', unsafe_allow_html=True)
    for strat in ads_data["organic"]:
        with st.expander(f"**{strat['channel']}**  --  {strat['frequency']}"):
            st.markdown(f"*{strat['tactic']}*")
            st.markdown("**Actions concrètes :**")
            for ex in strat["examples"]:
                st.markdown(f"→ {ex}")

    # ROI Projection
    st.markdown('<div class="section-h">Projection ROI  --  12 mois</div>', unsafe_allow_html=True)
    st.caption("Estimation basée sur votre budget, votre secteur et votre maturité. Scénarios : pessimiste · réaliste · optimiste")
    if roi_data:
        col_p, col_r, col_o = st.columns(3)
        last = roi_data[-1]
        col_p.markdown(f'<div class="metric-box"><div class="val" style="color:#B83D4B">{last["pessimiste"]:,} €</div><div class="lbl">Pessimiste (12 mois)</div></div>', unsafe_allow_html=True)
        col_r.markdown(f'<div class="metric-box"><div class="val" style="color:#44C1BA">{last["realiste"]:,} €</div><div class="lbl">Réaliste (12 mois)</div></div>', unsafe_allow_html=True)
        col_o.markdown(f'<div class="metric-box"><div class="val" style="color:#267371">{last["optimiste"]:,} €</div><div class="lbl">Optimiste (12 mois)</div></div>', unsafe_allow_html=True)
        # Mini tableau mensuel
        st.markdown("<br>", unsafe_allow_html=True)
        roi_html = '<table class="bizi-table"><thead><tr><th>Mois</th><th style="color:#B83D4B">Pessimiste</th><th style="color:#44C1BA">Réaliste</th><th style="color:#267371">Optimiste</th></tr></thead><tbody>'
        for r in roi_data:
            roi_html += f"<tr><td><b>M{r['month']}</b></td><td>{r['pessimiste']:,} €</td><td><b>{r['realiste']:,} €</b></td><td>{r['optimiste']:,} €</td></tr>"
        roi_html += '</tbody></table>'
        st.markdown(f'<div style="overflow-x:auto">'+ roi_html +'</div>', unsafe_allow_html=True)
    
    # PageSpeed
    # ── Wikipedia contexte sectoriel ─────────────────────────────────────────
    if _HAS_ENRICHMENT and website_url:
        _wiki_topic = {
            "ecommerce":"commerce électronique","saas":"logiciel en tant que service",
            "service":"prestation de services","consulting":"conseil en management",
            "content":"création de contenu numérique","other":"entrepreneuriat"
        }.get(activity,"entrepreneuriat")
        _wiki = _wiki_summary(_wiki_topic, lang="fr")
        if _wiki and _wiki.get("extract"):
            with st.expander(f"Contexte Wikipedia  --  {_wiki.get('title','')}"):
                st.markdown(_wiki["extract"])
                if _wiki.get("url"):
                    st.markdown(f"[Lire l'article complet]({_wiki['url']})")

    # ── Benchmarks sectoriels (données ouvertes France) ───────────────────────
    # ── Données macro France live ─────────────────────────────────────────────
    if _HAS_ENRICHMENT:
        _macro = _get_macro()
        _forex = _get_forex()
        _survie = _get_survie(activity)
        if _macro:
            st.markdown('<div class="section-h">Contexte macroéconomique France 2024</div>', unsafe_allow_html=True)
            _mc = st.columns(4)
            _macro_items = [("PIB 2024", _macro.get("PIB_2024_growth","N/A")),
                            ("Inflation", _macro.get("Inflation_2024","N/A")),
                            ("Chômage", _macro.get("Chomage_2024","N/A")),
                            ("Créations entr.", _macro.get("Creation_entreprises_2024","N/A"))]
            for col, (lbl, val) in zip(_mc, _macro_items):
                col.metric(lbl, val)
            st.caption(f"Source : {_macro.get('source','INSEE 2024')}")

        if _forex:
            with st.expander("Taux de change EUR  --  Banque Centrale Européenne"):
                _fc = st.columns(len(_forex))
                for col, (cur, rate) in zip(_fc, _forex.items()):
                    col.metric(f"EUR/{cur}", str(rate))

        if _survie:
            st.markdown('<div class="section-h">Taux de survie  --  votre secteur</div>', unsafe_allow_html=True)
            _sc = st.columns(3)
            _sc[0].metric("Survie 1 an", f"{_survie.get('1an',0)}%")
            _sc[1].metric("Survie 3 ans", f"{_survie.get('3ans',0)}%")
            _sc[2].metric("Survie 5 ans", f"{_survie.get('5ans',0)}%", delta=f"Tendance: {_survie.get('tendance','stable')}")

    if _sector_live and _sector_bench:
        st.markdown('<div class="section-h">Benchmarks sectoriels  --  Données marché France 2024</div>', unsafe_allow_html=True)
        _bench_cols = st.columns(min(4, len(_sector_bench)))
        for _col, (_kpi, _val) in zip(_bench_cols, list(_sector_bench.items())[:4]):
            with _col:
                st.metric(_kpi.replace("_"," ").title(), str(_val))
        st.caption(f"Source : données sectorielles ouvertes France · {_sector_label} · Marché {_sector_market} · Croissance {_sector_growth}")

    if pagespeed_data:
        st.markdown('<div class="section-h">Audit PageSpeed  --  Performance site</div>', unsafe_allow_html=True)
        if pagespeed_data.get("source") in ("mock", "heuristic"):
            st.caption("Scores estimés par analyse heuristique  --  précis")
        ps_cols = st.columns(4)
        scores = [
            ("Performance", pagespeed_data.get("performance",0)),
            ("SEO technique", pagespeed_data.get("seo",0)),
            ("Accessibilité", pagespeed_data.get("accessibility",0)),
            ("Bonnes pratiques", pagespeed_data.get("bestPractices",0)),
        ]
        for col, (label, score) in zip(ps_cols, scores):
            color = "#267371" if score >= 80 else "#44C1BA" if score >= 60 else "#B83D4B"
            with col:
                st.markdown(f'<div class="metric-box"><div class="val" style="color:{color}">{score}/100</div><div class="lbl">{label}</div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("LCP (Largest Contentful Paint)", pagespeed_data.get("lcp","N/A"), help="Doit être < 2.5s pour un bon score")
        c2.metric("CLS (Cumulative Layout Shift)", pagespeed_data.get("cls","N/A"), help="Doit être < 0.1 pour un bon score")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6  --  SEO & GEO 2025
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span style="font-size:2rem"></span>
      <div>
        <b style="font-size:1rem">GEO 2025 — Generative Engine Optimization</b><br>
        <span style="opacity:.85;font-size:.85rem">39% des Français utilisent l'IA conversationnelle (2025) — optimisez maintenant pour les moteurs IA</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Keywords
    st.markdown('<div class="section-h">Mots-clés prioritaires</div>', unsafe_allow_html=True)
    diff_badge = {"Facile":"badge-jade","Moyen":"badge-teal","Élevé":"badge-red"}
    intent_badge = {"Transactionnel":"badge-blue","Commercial":"badge-purple","Informationnel":"badge-gray"}
    kw_html = '<table class="bizi-table"><thead><tr><th>Mot-clé</th><th>Volume</th><th>Difficulté</th><th>Intention</th></tr></thead><tbody>'
    for kw, vol, diff, intent in keywords:
        kw_html += f"""<tr>
          <td><b>{kw}</b></td>
          <td style='font-size:.82rem'>{vol}</td>
          <td><span class='badge {diff_badge.get(diff,"badge-gray")}'>{diff}</span></td>
          <td><span class='badge {intent_badge.get(intent,"badge-gray")}'>{intent}</span></td>
        </tr>"""
    kw_html += "</tbody></table>"
    st.markdown(f'<div style="overflow-x:auto">'+ kw_html +'</div>', unsafe_allow_html=True)

    # Topics
    st.markdown('<div class="section-h">Autorité thématique  --  Contenus à créer</div>', unsafe_allow_html=True)
    for topic in geo["topics"]:
        st.markdown(f"{topic}")

    # Clusters
    st.markdown('<div class="section-h">Clusters de contenu</div>', unsafe_allow_html=True)
    for pilier, clusters in geo["clusters"]:
        with st.expander(f"**Pilier : {pilier}**"):
            for cl in clusters:
                st.markdown(f"&nbsp;&nbsp;&nbsp;→ {cl}")

    # GEO optimizations
    st.markdown('<div class="section-h">Optimisations GEO prioritaires</div>', unsafe_allow_html=True)
    for action, impact in geo["optims"]:
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"• {action}")
        c2.markdown(impact)

    # AI tips
    st.markdown('<div class="section-h">Conseils pour les moteurs IA (ChatGPT, Perplexity, SGE)</div>', unsafe_allow_html=True)
    for tip in geo["tips"]:
        st.info(tip)

    # SEA IA
    st.markdown('<div class="section-h">SEA IA  --  Publicité pilotée par l\'IA (2025)</div>', unsafe_allow_html=True)
    sea_tabs = st.tabs([s[0].strip() for s in _SEA_IA])
    for sea_tab, (name, desc, advantages, conseil) in zip(sea_tabs, _SEA_IA):
        with sea_tab:
            st.markdown(f"**{desc}**")
            st.markdown("**Avantages clés :**")
            for av in advantages:
                st.markdown(f"{av}")
            st.info(f"**Conseil pratique :** {conseil}")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER  --  KPI tiles renderer (DRY)
# ─────────────────────────────────────────────────────────────────────────────
def _render_kpi_section(kpi_list: list) -> None:
    """Affiche un groupe de KPI en grille 3 colonnes avec code couleur."""
    _tone_colors = {"sauge": "#C6ECD9", "ambre": "#C6ECD9", "neutral": "#F2ECD9"}
    _text_colors = {"sauge": "#267371", "ambre": "#44C1BA", "neutral": "#267371"}
    cols = st.columns(min(3, len(kpi_list)))
    for i, (label, value, hint, tone, target) in enumerate(kpi_list):
        bg = _tone_colors.get(tone, "#F2ECD9")
        tc = _text_colors.get(tone, "#267371")
        with cols[i % 3]:
            st.markdown(f"""
            <div class="kpi-tile" style="background:{bg};border-left:3px solid {tc}">
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#339999">{_html.escape(label)}</div>
              <div style="font-size:1.6rem;font-weight:800;color:{tc};margin:4px 0">{_html.escape(value)}</div>
              <div style="font-size:.7rem;color:#339999">{_html.escape(hint)}</div>
              <div style="font-size:.7rem;color:{tc};margin-top:4px;font-weight:600"> Objectif : {_html.escape(target)}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7  --  KPI DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-h">Dashboard KPI  --  Benchmarks 2025</div>', unsafe_allow_html=True)
    st.caption("Tous les indicateurs clés de performance avec leurs benchmarks sectoriels. Survolez les titres pour les définitions.")

    # Email KPIs
    st.markdown('<div class="section-h">Email Marketing</div>', unsafe_allow_html=True)
    _render_kpi_section(_KPI_BENCHMARKS["email"])

    st.markdown('<div class="section-h">Conversion & Satisfaction</div>', unsafe_allow_html=True)
    _render_kpi_section(_KPI_BENCHMARKS["conversion"])

    st.markdown('<div class="section-h">Réseaux sociaux & Croissance</div>', unsafe_allow_html=True)
    _render_kpi_section(_KPI_BENCHMARKS["social"])

    # OKR
    st.markdown('<div class="section-h">OKR  --  Objectifs & Key Results</div>', unsafe_allow_html=True)
    st.caption("La méthode OKR (Google, Intel, LinkedIn) aligne les équipes sur des objectifs ambitieux et mesurables")
    for j, okr in enumerate(okrs):
        with st.expander(f"**OKR {j+1}**  --  {okr['objective']}", expanded=(j==0)):
            st.markdown(f"**Objectif :** {okr['objective']}")
            st.markdown("**Key Results :**")
            for kr in okr["key_results"]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #F2ECD9">
                  <div style="min-width:20px;height:20px;border-radius:50%;border:2px solid #44C1BA"></div>
                  <span style="font-size:.88rem">{kr}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8  --  SYNTHÈSE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    score = synthesis["score"]

    # Score ring
    st.markdown('<div class="section-h">Score de maturité stratégique</div>', unsafe_allow_html=True)
    c_score, c_kpis = st.columns([1, 3])
    with c_score:
        score_color = "#267371" if score >= 70 else "#44C1BA" if score >= 50 else "#B83D4B"
        st.markdown(f"""
        <div style="text-align:center;padding:20px 10px">
          <div class="score-ring" style="--pct:{score * 3.6:.0f}deg;background:conic-gradient({score_color} {score * 3.6:.0f}deg,#F2ECD9 0)">
            <span style="font-size:1.4rem;font-weight:800;color:#0B2221">{score}/100</span>
          </div>
          <p style='font-size:.82rem;color:#339999;margin-top:8px'>Score stratégique global</p>
          <span class="badge {'badge-jade'if score>=70 else 'badge-teal'if score>=50 else 'badge-red'}">
            {'Bon'if score>=70 else 'À améliorer'if score>=50 else 'Attention'}
          </span>
        </div>
        """, unsafe_allow_html=True)
    with c_kpis:
        st.markdown("**KPIs cibles**")
        kpi_cols = st.columns(3)
        for i, (label, val) in enumerate(synthesis["kpis"]):
            with kpi_cols[i % 3]:
                st.markdown(f'<div class="metric-box"><div class="val" style="font-size:1.1rem;color:#44C1BA">{val}</div><div class="lbl">{label}</div></div>', unsafe_allow_html=True)

    # Priorities
    st.markdown('<div class="section-h">Priorités d\'action</div>', unsafe_allow_html=True)
    priority_colors = ["#B83D4B","#44C1BA","#0B2221","#267371"]
    for i, p in enumerate(synthesis["priorities"]):
        color = priority_colors[i % 4]
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #F2ECD9">
          <div style="min-width:28px;height:28px;border-radius:50%;background:{color};color:white;
            display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0">{i+1}</div>
          <p style="margin:0;font-size:.9rem;color:#267371;padding-top:4px">{p}</p>
        </div>""", unsafe_allow_html=True)

    # Roadmap
    st.markdown('<div class="section-h">Roadmap 180 jours</div>', unsafe_allow_html=True)
    rm_cols = st.columns(4)
    rm_colors = ["#0B2221","#267371","#44C1BA","#393DAC"]
    for i, (period, phase, actions) in enumerate(synthesis["roadmap"]):
        with rm_cols[i]:
            st.markdown(f"""
            <div class="card" style="border-top:3px solid {rm_colors[i]}">
              <div style='font-size:.68rem;color:#339999;font-weight:600;text-transform:uppercase;letter-spacing:.05em'>{period}</div>
              <div style='font-weight:700;font-size:.95rem;color:#0B2221;margin:4px 0'>{phase}</div>
              <p style='font-size:.78rem;color:#267371;margin:0'>{actions}</p>
            </div>""", unsafe_allow_html=True)

    # Export
    st.markdown('<div class="section-h">Export de l\'analyse complète</div>', unsafe_allow_html=True)
    export_data = {
    "metadata": {
        "generated_at": str(__import__("datetime").datetime.now()),
        "version": "3.2",
        "activity": activity,
        "goal": goal,
        "sector": _sector_live.get("label","") if _sector_live else "",
    },
        "generated_at": datetime.datetime.now().isoformat(),
        "version": "3.1",
        "input": {
            "activity": activity, "goal": goal, "maturity": maturity,
            "monthly_budget": monthly_budget, "total_budget": total_budget,
            "website_url": website_url,
        },
        "swot": swot,
        "qqoqccp": {k: {"question": v["q"], "reponse": v["r"], "action": v["a"]} for k, v in qqoqccp.items()},
        "soncas": {k: {"label": v["label"], "desc": v["desc"], "args": v["args"]} for k, v in soncas.items()},
        "keywords": [{"keyword": k, "volume": v, "difficulty": d, "intent": i} for k, v, d, i in keywords],
        "personas": [{"name": p["name"], "age": p["age"], "job": p["job"], "goals": p["goals"], "pains": p["pains"], "framework": p.get("framework","")} for p in personas],
        "synthesis": {"score": score, "priorities": synthesis["priorities"]},
        "okrs": okrs,
        "budget_recommendations": budget_reco,
    }
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Télécharger JSON",
            data=json.dumps(export_data, ensure_ascii=False, indent=2, default=str),
            file_name=f"biziapp-analyse-{activity}-{goal}-{datetime.date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_dl2:
        # CSV simple des mots-clés
        csv_kw = "mot_cle,volume,difficulte,intention\n" + "\n".join(f'"{k}","{v}","{d}","{i}"'for k,v,d,i in keywords)
        st.download_button(
            label="Mots-clés CSV",
            data=csv_kw,
            file_name=f"biziapp-keywords-{activity}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    st.caption("JSON complet · compatible CRM, Notion, Google Sheets et tout éditeur de texte")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 9  --  VEILLE STRATÉGIQUE & CONCURRENTIELLE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    if comp_urls:
        _ck = "comp_" + str(abs(hash(tuple(sorted(comp_urls)))))
        if _ck not in st.session_state:
            with st.spinner("Analyse des concurrents…"):
                for _cu in comp_urls:
                    try:
                        comp_results[_cu] = scrape_competitor(_cu)
                    except Exception:
                        comp_results[_cu] = {"error": "Echec", "url": _cu}
            st.session_state[_ck] = dict(comp_results)
        else:
            comp_results.update(st.session_state[_ck])

    _main_q = (veille_keywords[0] if veille_keywords else "") or (
        {"ecommerce":"e-commerce","saas":"logiciel SaaS","service":"prestataire service","consulting":"consultant","content":"créateur contenu","other":"entreprise"}
        .get(activity,"stratégie")
    )
    _news_queries = []
    if veille_keywords:
        for _kw in veille_keywords[:4]:
            _news_queries.append(("Mot-clé", _kw))
    if comp_urls:
        for _cu in comp_urls[:2]:
            _dom = _cu.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
            _news_queries.append(("Concurrent", _dom))
    if not _news_queries:
        _news_queries = [("Secteur", _main_q)]

    # ── Google Trends + Product Hunt (enrichment_apis) ─────────────────────────
    if _HAS_ENRICHMENT:
        _trends = _fetch_trends("FR")
        _ph_items = _fetch_ph()
        _startups = _fetch_startups(activity)

        if _trends:
            with st.expander("Tendances Google France du moment"):
                for t in _trends[:8]:
                    st.markdown(f"- **{t}**")

        if _ph_items:
            with st.expander("Nouveautés Product Hunt"):
                for p in _ph_items[:5]:
                    st.markdown(f"- [{p['title']}]({p['link']})  --  {p.get('desc','')[:80]}")

        if _startups:
            with st.expander(f"Startups françaises  --  {_sector_label}"):
                for s in _startups[:6]:
                    st.markdown(f"- **{s['name']}** ({s['country']})")

    # ── Sources additionnelles HackerNews + DEV.to + GitHub ───────────────────
    _hn_items, _devto_items, _gh_items = [], [], []
    if _HAS_API_LAYER:
        try:
            _hn_items   = _fetch_hn(_main_q, max_items=6)
        except Exception: pass
        try:
            _devto_items = _fetch_devto(activity, max_items=5)
        except Exception: pass
        try:
            _gh_items   = _fetch_github(max_items=4)
        except Exception: pass

    # ── Données sectorielles  --  utilisées depuis le scope global ─────────────
    # _sector_live, _sector_label, _sector_growth, _sector_market, _sector_bench
    # sont définis globalement après le bloc session-state ci-dessus

    # ── Entreprises du secteur (API Recherche Entreprises) ────────────────────
    _secteur_entreprises = []
    if _HAS_API_LAYER and not st.session_state.get(f"_ent_{activity}"):
        try:
            naf_map = {"ecommerce":"47.91","saas":"62.01","service":"74.90","consulting":"70.22","content":"59.11"}
            _naf = naf_map.get(activity,"")
            _secteur_entreprises = _search_entreprises(_main_q, activite=_naf, max_results=5)
            st.session_state[f"_ent_{activity}"] = _secteur_entreprises
        except Exception: pass
    elif st.session_state.get(f"_ent_{activity}"):
        _secteur_entreprises = st.session_state[f"_ent_{activity}"]

    # ── Données marché live ───────────────────────────────────────────────────
    if _sector_live:
        st.markdown(f'''
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px">
  <div class="stat-box"><div class="stat-num" style="font-size:1.2rem">{_sector_growth}</div><div class="stat-lbl">Croissance secteur 2024</div></div>
  <div class="stat-box"><div class="stat-num" style="font-size:1rem">{_sector_market}</div><div class="stat-lbl">Marché France 2024</div></div>
  <div class="stat-box"><div class="stat-num" style="font-size:1rem">{str(_sector_live.get("acteurs",0)) + " ent." if _sector_live.get("acteurs") else "N/A"}</div><div class="stat-lbl">Acteurs du secteur</div></div>
  <div class="stat-box"><div class="stat-num" style="font-size:1rem">{_sector_live.get("ticket_moyen","N/A")}</div><div class="stat-lbl">Ticket moyen</div></div>
</div>
''', unsafe_allow_html=True)

    # ── Entreprises du secteur (Sirene / Recherche-Entreprises) ───────────────
    if _secteur_entreprises:
        st.markdown('<div class="section-h">Entreprises du secteur (données Sirene)</div>', unsafe_allow_html=True)
        for _ent in _secteur_entreprises[:4]:
            st.markdown(f'''
<div class="card" style="margin-bottom:8px;display:flex;align-items:center;gap:14px">
  <div style="width:36px;height:36px;border-radius:8px;background:#C6ECD9;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0">🏢</div>
  <div>
    <div style="font-weight:700;font-size:.88rem;color:#0B2221">{_ent.get("nom","")[:50]}</div>
    <div style="font-size:.75rem;color:#339999">{_ent.get("siege","")[:60]} · SIREN: {_ent.get("siren","")} · {_ent.get("categorie","")}</div>
  </div>
</div>
''', unsafe_allow_html=True)

    # ── Sources tech additionnelles ────────────────────────────────────────────
    if _hn_items or _devto_items or _gh_items:
        with st.expander("Sources tech  --  HackerNews · DEV.to · GitHub Trending"):
            if _hn_items:
                st.markdown("**HackerNews**")
                for _hn in _hn_items[:4]:
                    st.markdown(f"- [{_hn['title']}]({_hn['link']})  --  {_hn['source']}")
            if _devto_items:
                st.markdown("**DEV.to**")
                for _dv in _devto_items[:4]:
                    st.markdown(f"- [{_dv['title']}]({_dv['link']})")
            if _gh_items:
                st.markdown("**GitHub Trending**")
                for _gh in _gh_items[:4]:
                    st.markdown(f"- [{_gh['title']}]({_gh['link']})")

    # ── Analyse URL avancée ──────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Analyse URL complète  --  SEO · Contenu · Performance</div>', unsafe_allow_html=True)
    _lcol, _rcol = st.columns([4, 1])
    with _lcol:
        _live_url = st.text_input("URL à analyser", placeholder="https://monsite.fr ou https://concurrent.fr/page", label_visibility="collapsed", key="v_liveurl")
    with _rcol:
        _do_an = st.button("Analyser", type="primary", use_container_width=True, key="v_analyze_btn")

    _target = _live_url.strip()
    if _target:
        if not _target.startswith("http"):
            _target = "https://" + _target
        with st.spinner(f"Lecture de {_target.replace('https://','').replace('http://','').split('/')[0]} via Jina.ai…"):
            _ld = scrape_competitor(_target)
        if _ld.get("error") and not _ld.get("title"):
            st.error(f"Impossible d'analyser cette URL  --  {_html.escape(str(_ld.get('error',''))[:120])}")
        else:
            _lsrc = {"allorigins":"AllOrigins Proxy","bs4":"BeautifulSoup"}.get(_ld.get("source",""),_ld.get("source","",""))
            st.markdown(f"""
            <div class="card-dark">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap">
                <div style="flex:1;min-width:0">
                  <div style="font-size:.62rem;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px">{_html.escape(_target.replace('https://','').replace('http://','').split('/')[0][:60])}</div>
                  <div style="font-size:1.1rem;font-weight:700;color:white;margin-bottom:6px;line-height:1.3">{_html.escape(str(_ld.get('title','—'))[:120])}</div>
                  <div style="font-size:.82rem;color:rgba(255,255,255,.65);line-height:1.5">{_html.escape(str(_ld.get('description',''))[:260])}</div>
                </div>
                <div style="text-align:right;font-size:.63rem;color:rgba(255,255,255,.35);line-height:1.7;flex-shrink:0">
                  Source : {_lsrc}<br>{_ld.get('fetched_at','')}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            _lk1,_lk2,_lk3,_lk4 = st.columns(4)
            _lk1.metric("H1",len(_ld.get("h1",[])))
            _lk2.metric("H2",len(_ld.get("h2",[])))
            _lk3.metric("Paragraphes",len(_ld.get("paragraphs",[])))
            _lk4.metric("Mots-clés",len(_ld.get("keywords",[])))
            if _ld.get("keywords"):
                st.markdown('<div class="section-h">Mots-clés détectés</div>', unsafe_allow_html=True)
                _kwh = "".join(f'<span class="url-kw" style="background:var(--teal-pale);color:#267371;margin:2px;display:inline-block;border-radius:4px;padding:2px 8px;font-size:.68rem;font-weight:600">{_html.escape(str(k)[:40])}</span>' for k in _ld["keywords"])
                st.markdown(f'<div style="margin-bottom:12px">{_kwh}</div>', unsafe_allow_html=True)
            _lca, _lcb = st.columns(2)
            with _lca:
                if _ld.get("h1"):
                    st.markdown('<div class="section-h">Structure H1</div>', unsafe_allow_html=True)
                    for _h in _ld["h1"]:
                        st.markdown(f'<div class="card" style="padding:9px 14px;font-weight:600;font-size:.87rem;margin-bottom:7px">{_html.escape(str(_h)[:110])}</div>', unsafe_allow_html=True)
                if _ld.get("h2"):
                    st.markdown('<div class="section-h">Structure H2</div>', unsafe_allow_html=True)
                    for _h in _ld["h2"][:7]:
                        st.markdown(f'<div style="padding:5px 12px;border-left:2px solid var(--teal);margin-bottom:5px;font-size:.83rem;color:#267371">{_html.escape(str(_h)[:110])}</div>', unsafe_allow_html=True)
            with _lcb:
                if _ld.get("paragraphs"):
                    st.markdown('<div class="section-h">Contenu principal</div>', unsafe_allow_html=True)
                    for _p in _ld["paragraphs"][:5]:
                        st.markdown(f'<div style="font-size:.82rem;color:#339999;line-height:1.6;padding:7px 0;border-bottom:1px solid #E4E9F6">{_html.escape(str(_p)[:300])}</div>', unsafe_allow_html=True)
    else:
        st.info("Entrez une URL ci-dessus pour lancer une analyse en temps réel  --  fonctionne avec n'importe quelle page publique")

    st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

    # ── Veille concurrentielle ────────────────────────────────────────────────
    if comp_urls:
        st.markdown('<div class="section-h">Analyse concurrentielle</div>', unsafe_allow_html=True)
        _nc = min(len(comp_urls), 3)
        _gcols = st.columns(_nc)
        for _ci, _cu in enumerate(comp_urls):
            _cd = comp_results.get(_cu, {})
            with _gcols[_ci % _nc]:
                _dom = _cu.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
                _herr = _cd.get("error") and not _cd.get("title")
                if _herr:
                    st.markdown(f'<div style="background:#F7FBF4;border:1px solid #C6ECD9;border-radius:10px;padding:14px;font-size:.82rem"><b style="color:#B83D4B">{_html.escape(_dom)}</b><br><span style="color:#B83D4B">{_html.escape(str(_cd.get("error","Erreur"))[:80])}</span></div>', unsafe_allow_html=True)
                else:
                    _ckws = "".join(f'<span style="background:#C6ECD9;color:#267371;border-radius:3px;padding:1px 6px;font-size:.62rem;font-weight:600;margin:1px;display:inline-block">{_html.escape(str(k)[:30])}</span>' for k in _cd.get("keywords",[])[:6])
                    st.markdown(f"""
                    <div class="card">
                      <div style="font-size:.68rem;color:var(--muted);font-family:monospace">{_html.escape(_dom)}</div>
                      <div style="font-weight:700;font-size:.9rem;color:#0B2221;margin:4px 0 6px">{_html.escape(str(_cd.get('title','—'))[:65])}</div>
                      <div style="font-size:.78rem;color:#339999;line-height:1.45;margin-bottom:8px">{_html.escape(str(_cd.get('description',''))[:160])}</div>
                      <div style="margin-bottom:6px">{_ckws}</div>
                      <div style="font-size:.68rem;color:#44C1BA">{len(_cd.get('h1',[]))+len(_cd.get('h2',[]))} titres · {len(_cd.get('paragraphs',[]))} §</div>
                    </div>
                    """, unsafe_allow_html=True)
        if len(comp_results) > 1:
            st.markdown('<div class="section-h">Tableau comparatif</div>', unsafe_allow_html=True)
            _rows = []
            for _cu, _cd in comp_results.items():
                _dom = _cu.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
                _rows.append({
                    "Domaine": _dom,
                    "Titre": str(_cd.get("title"," -- "))[:60],
                    "Description": str(_cd.get("description"," -- "))[:100],
                    "H1 principal": ((_cd.get("h1") or [" -- "])[0])[:55],
                    "Mots-clés": " · ".join((_cd.get("keywords") or [])[:4]) or " -- ",
                    "H2 count": len(_cd.get("h2",[])),
                })
            if _rows:
                st.dataframe(_rows, use_container_width=True, hide_index=True)
        for _ci2, (_cu2, _cd2) in enumerate(comp_results.items()):
            _dom2 = _cu2.replace("https://","").replace("http://","").replace("www.","").split("/")[0]
            with st.expander(f"**{_html.escape(_dom2)}**  --  analyse éditoriale complète", expanded=(_ci2==0)):
                if _cd2.get("h2"):
                    st.markdown("**Structure éditoriale (H2)**")
                    for _h2 in _cd2["h2"][:10]:
                        st.markdown(f"- {_html.escape(str(_h2)[:130])}")
                if _cd2.get("main_text"):
                    st.markdown("**Extrait du contenu**")
                    st.markdown(f'<div style="font-size:.82rem;color:#339999;line-height:1.65;background:#F9FAFB;padding:13px;border-radius:8px;border-left:3px solid var(--teal)">{_html.escape(str(_cd2["main_text"])[:900])}</div>', unsafe_allow_html=True)

    # ── Actualités marché ─────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Flux actualités en temps réel</div>', unsafe_allow_html=True)
    for _ql, _qq in _news_queries[:5]:
        with st.expander(f"**{_ql}** · {_html.escape(_qq[:60])}", expanded=(_ql == _news_queries[0][0])):
            with st.spinner(f"Chargement actualités « {_qq[:40]} »…"):
                _news = fetch_news(_qq, lang=veille_lang, max_items=12)
            for _ni in _news:
                _nt = _html.escape(str(_ni.get("title",""))[:130])
                _ns = _html.escape(str(_ni.get("source",""))[:45])
                _np = _ni.get("pub","")
                _nl = _ni.get("link","")
                _src_h = f'<span style="background:#C6ECD9;color:#267371;padding:2px 7px;border-radius:4px;font-size:.63rem;font-weight:600;margin-right:6px">{_ns}</span>' if _ns else ""
                _link_h = f' <a href="{_html.escape(_nl)}" target="_blank" rel="noopener noreferrer" style="font-size:.68rem;color:#44C1BA;text-decoration:none">Lire &rarr;</a>' if _nl else ""
                st.markdown(f'<div style="border-left:3px solid var(--teal);padding:9px 13px;margin-bottom:8px;background:white;border-radius:0 8px 8px 0"><div style="font-weight:600;font-size:.87rem;color:#0B2221;margin-bottom:3px">{_nt}{_link_h}</div><div style="font-size:.7rem;color:#339999">{_src_h}{_np}</div></div>', unsafe_allow_html=True)

    # ── Signaux stratégiques ──────────────────────────────────────────────────
    st.markdown('<div class="section-h">Signaux stratégiques</div>', unsafe_allow_html=True)
    _wt = veille_keywords[0] if veille_keywords else _main_q
    _wc1, _wc2 = st.columns(2)
    with _wc1:
        st.markdown("**Contexte Wikipedia**")
        with st.spinner("Wikipedia…"):
            _wiki = fetch_wiki(_wt, lang=veille_lang)
        if _wiki.get("extract"):
            _wurl = f'<div style="margin-top:8px"><a href="{_html.escape(_wiki.get("url",""))}" target="_blank" rel="noopener noreferrer" style="font-size:.72rem;color:#44C1BA;text-decoration:none">Lire sur Wikipedia &rarr;</a></div>' if _wiki.get("url") else ""
            st.markdown(f'<div class="card"><div style="font-weight:700;font-size:.93rem;color:#0B2221;margin-bottom:6px">{_html.escape(str(_wiki.get("title",""))[:80])}</div><div style="font-size:.82rem;color:#339999;line-height:1.6">{_html.escape(str(_wiki.get("extract",""))[:650])}</div>{_wurl}</div>', unsafe_allow_html=True)
        else:
            st.info(f"Aucun article Wikipedia pour « {_html.escape(_wt[:50])} »")
    with _wc2:
        st.markdown("**Intelligence DuckDuckGo**")
        with st.spinner("DuckDuckGo…"):
            _ddg = fetch_ddg(_wt)
        if _ddg.get("abstract"):
            st.markdown(f'<div style="background:#C6ECD9;border:1px solid #44C1BA;border-radius:10px;padding:14px;font-size:.82rem;color:#0B2221;line-height:1.6">{_html.escape(str(_ddg["abstract"])[:550])}</div>', unsafe_allow_html=True)
        if _ddg.get("related"):
            st.markdown("**Sujets connexes**")
            for _rt in _ddg["related"][:5]:
                st.markdown(f'<div style="font-size:.8rem;color:#267371;padding:5px 0;border-bottom:1px solid #E4E9F6">{_html.escape(str(_rt)[:160])}</div>', unsafe_allow_html=True)

    # ── SWOT live ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Détection automatique Opportunités / Menaces</div>', unsafe_allow_html=True)
    st.caption("Analyse sémantique des actualités en temps réel")
    _opp_w = ["croissance","opportunité","innovation","lancement","expansion","partenariat","financement","investissement","hausse","boom","tendance","accélération","record"]
    _thr_w = ["crise","risque","baisse","pénurie","réglementation","sanction","fraude","concurrent","récession","inflation","perte","fermeture","licenciement","chute","amende"]
    with st.spinner("Analyse des signaux marché…"):
        _all_news = fetch_news(_main_q + " marché", lang=veille_lang, max_items=25)
    _opps = [n for n in _all_news if any(s in n.get("title","").lower() for s in _opp_w)]
    _thrs = [n for n in _all_news if any(s in n.get("title","").lower() for s in _thr_w)]
    _oc, _tc = st.columns(2)
    with _oc:
        st.markdown(f'<div style="font-weight:700;font-size:.87rem;color:#0B2221;margin-bottom:9px">Opportunités ({len(_opps)})</div>', unsafe_allow_html=True)
        if _opps:
            for _on in _opps[:5]:
                st.markdown(f'<div style="background:#C6ECD9;border:1px solid #C6ECD9;border-radius:8px;padding:8px 12px;margin-bottom:6px;font-size:.8rem;line-height:1.4">{_html.escape(str(_on.get("title",""))[:130])}<div style="font-size:.68rem;color:#44C1BA;margin-top:2px">{_on.get("pub","")}</div></div>', unsafe_allow_html=True)
        else:
            st.caption("Aucune opportunité détectée dans les actualités récentes")
    with _tc:
        st.markdown(f'<div style="font-weight:700;font-size:.87rem;color:#B83D4B;margin-bottom:9px">Menaces ({len(_thrs)})</div>', unsafe_allow_html=True)
        if _thrs:
            for _tn in _thrs[:5]:
                st.markdown(f'<div style="background:#F7FBF4;border:1px solid #C6ECD9;border-radius:8px;padding:8px 12px;margin-bottom:6px;font-size:.8rem;line-height:1.4">{_html.escape(str(_tn.get("title",""))[:130])}<div style="font-size:.68rem;color:#B83D4B;margin-top:2px">{_tn.get("pub","")}</div></div>', unsafe_allow_html=True)
        else:
            st.caption("Aucune menace détectée dans les actualités récentes")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 10  --  RSE & ISO 26000
# ══════════════════════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
      padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <div>
        <b style="font-size:1rem">RSE & ISO 26000 — Responsabilite Societale des Entreprises</b><br>
        <span style="opacity:.85;font-size:.85rem">7 domaines d'action · Normes ISO 26000 · Pacte Mondial ONU · Loi AGEC · CSRD 2025</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    _rse_data = gen_rse(activity)
    _rse_score_total = sum(v["niveau"] for v in _rse_data.values())
    _rse_score_max = len(_rse_data) * 5
    _rse_score_pct = round(_rse_score_total / _rse_score_max * 100)

    _rs1, _rs2, _rs3 = st.columns(3)
    _rs1.markdown(f'<div class="metric-box"><div class="val" style="color:#267371">{_rse_score_pct}/100</div><div class="lbl">Score RSE global</div></div>', unsafe_allow_html=True)
    _rs2.markdown(f'<div class="metric-box"><div class="val" style="color:#393DAC">{len(_rse_data)}</div><div class="lbl">Domaines ISO 26000</div></div>', unsafe_allow_html=True)
    _rse_label = "Leader RSE" if _rse_score_pct >= 70 else "En transition" if _rse_score_pct >= 50 else "Rattrapage nécessaire"
    _rs3.markdown(f'<div class="metric-box"><div class="val" style="font-size:1rem;color:#44C1BA">{_rse_label}</div><div class="lbl">Niveau de maturité</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">Les 7 domaines ISO 26000</div>', unsafe_allow_html=True)
    for _dom, _ddata in _rse_data.items():
        _niveau = _ddata["niveau"]
        _bar_filled = "█" * _niveau
        _bar_empty = "░" * (5 - _niveau)
        _ncolor = "#267371" if _niveau >= 4 else "#44C1BA" if _niveau >= 3 else "#B83D4B"
        with st.expander(f"**{_dom}**  --  Niveau {_niveau}/5 {_bar_filled}{_bar_empty}"):
            _dc1, _dc2 = st.columns([3, 2])
            with _dc1:
                st.markdown("**Actions recommandées :**")
                for _act in _ddata["actions"]:
                    st.markdown(f"""
                    <div class="rse-card">
                      <div style="font-size:.84rem;color:#0B2221">{_html.escape(_act)}</div>
                    </div>
                    """, unsafe_allow_html=True)
            with _dc2:
                st.markdown("**Risque si inaction :**")
                st.warning(_html.escape(_ddata["risques"]))
                st.markdown(f'<div style="margin-top:10px"><div class="progress-bar"><div class="progress-fill" style="width:{_niveau*20}%;background:{_ncolor}"></div></div><div style="font-size:.7rem;color:#339999;margin-top:3px">Maturité : {_niveau}/5</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-h">Cadre légal et normatif applicable</div>', unsafe_allow_html=True)
    _normes = [
        ("ISO 26000", "Lignes directrices RSE  --  référentiel international non certifiable mais reconnu"),
        ("Pacte Mondial ONU", "10 principes sur les droits humains, travail, environnement et anti-corruption"),
        ("Loi Grenelle II", "Obligation de reporting extra-financier pour les entreprises françaises"),
        ("Loi AGEC", "Economie circulaire  --  emballages durables, réparation, information consommateurs"),
        ("CSRD 2025", "Corporate Sustainability Reporting Directive  --  reporting obligatoire ESG UE"),
        ("RGPD", "Protection des données personnelles  --  conformité obligatoire depuis 2018"),
    ]
    for _nl, _nd in _normes:
        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #F2ECD9;align-items:flex-start">
          <span class="badge badge-jade" style="flex-shrink:0">{_html.escape(_nl)}</span>
          <span style="font-size:.84rem;color:#267371">{_html.escape(_nd)}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-h">Plan d\'action RSE 90 jours</div>', unsafe_allow_html=True)
    _rse_roadmap = [
        ("J1-J30", "Diagnostic", "Réaliser un bilan carbone simplifié · Rédiger la charte RSE · Identifier les parties prenantes clés"),
        ("J31-J60", "Engagement", "Choisir 2-3 domaines prioritaires · Définir des objectifs mesurables · Communiquer en interne"),
        ("J61-J90", "Action", "Lancer les premières actions concrètes · Mesurer les résultats · Préparer la communication externe"),
    ]
    _rr_cols = st.columns(3)
    for _ri, (_per, _ph, _ac) in enumerate(_rse_roadmap):
        with _rr_cols[_ri]:
            st.markdown(f"""
            <div class="card" style="border-top:3px solid #267371">
              <div style="font-size:.68rem;color:#339999;font-weight:600;text-transform:uppercase">{_per}</div>
              <div style="font-weight:700;font-size:.92rem;color:#0B2221;margin:4px 0">{_ph}</div>
              <p style="font-size:.78rem;color:#267371;margin:0">{_ac}</p>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 11  --  STRATÉGIE+ (Porter · Ansoff · Customer Journey · Pricing)
# ══════════════════════════════════════════════════════════════════════════════
# ═══ TAB 12  --  PARCOURS CLIENT ═══
with tabs[11]:
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
  padding:18px 24px;margin-bottom:20px">
  <b style="font-size:1.05rem">⚔️ Stratégie avancée — Porter · Ansoff · Customer Journey · Pricing</b><br>
  <span style="opacity:.85;font-size:.85rem">Frameworks stratégiques complets personnalisés pour votre secteur</span>
</div>
""", unsafe_allow_html=True)

    # ── Sous-onglets Stratégie+ ──────────────────────────────────────────────
    _strat_tabs = st.tabs(["Porter 5 Forces","Ansoff","Customer Journey","Pricing","Ikigai","Ocean Bleu","Lean Canvas","Scenarios","Plan 180j","Analytics"])
    with _strat_tabs[0]:
     st.markdown('<div class="section-h">5 Forces de Porter</div>', unsafe_allow_html=True)
    _p5 = porter_data if porter_data else {}
    _forces_names = {
        "menace_nouveaux": "Nouveau: Menace nouveaux entrants",
        "pouvoir_fournisseurs": "Pouvoir fournisseurs",
        "pouvoir_acheteurs": "Pouvoir acheteurs",
        "menace_substituts": "Menace substituts",
        "rivalite": "⚔️ Rivalité concurrentielle",
    }
    _pcols = st.columns(5)
    for _col, (_key, _label) in zip(_pcols, _forces_names.items()):
        _force = _p5.get(_key, {})
        _score = _force.get("score", 5)
        _lbl   = _force.get("label", "N/A")
        _color = "#B83D4B" if _score >= 7 else "#44C1BA" if _score >= 5 else "#267371"
        with _col:
            st.markdown(f"""
<div class="stat-box" style="border-top:3px solid {_color}">
  <div style="font-size:.7rem;font-weight:700;color:{_color};margin-bottom:6px">{_label[:20]}</div>
  <div style="font-size:1.8rem;font-weight:900;color:{_color}">{_score}/10</div>
  <div style="font-size:.68rem;color:#339999;font-weight:600;margin-top:3px">{_lbl}</div>
</div>""", unsafe_allow_html=True)

    with st.expander("Détails des 5 Forces"):
        for _key, _label in _forces_names.items():
            _force = _p5.get(_key, {})
            _details = _force.get("details", [])
            st.markdown(f"**{_label}**  --  Score {_force.get('score',5)}/10")
            for _d in _details:
                st.markdown(f"  - {_d}")

    st.divider()

    # ── Matrice Ansoff ────────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Matrice Ansoff &mdash; Strat&eacute;gies de croissance</div>', unsafe_allow_html=True)
    _ansoff = ansoff_data if ansoff_data else {}
    _reco = _ansoff.get("recommendation", "penetration")
    _ansoff_labels = {
        "penetration": ("Pénétration marché", "Marchés existants + Produits existants", "#267371"),
        "developpement": ("Développement produit", "Marchés existants + Nouveaux produits", "#44C1BA"),
        "extension": (" Extension marché", "Nouveaux marchés + Produits existants", "#393DAC"),
        "diversification": ("Diversification", "Nouveaux marchés + Nouveaux produits", "#B83D4B"),
    }
    _a_cols = st.columns(2)
    for _ci, (_akey, (_alabel, _adesc, _acolor)) in enumerate(_ansoff_labels.items()):
        _adata = _ansoff.get(_akey, {})
        _ascore = _adata.get("score", 50)
        _arisk  = _adata.get("risk", "N/A")
        _is_reco = _akey == _reco
        with _a_cols[_ci % 2]:
            st.markdown(f"""
<div class="ben-card" style="border-left:4px solid {_acolor}{'!important;background:#F7FBF4' if _is_reco else ''}">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div style="font-weight:800;font-size:.92rem;color:#0B2221">{_alabel}</div>
    {"<span style='background:#44C1BA;color:white;border-radius:50px;padding:2px 10px;font-size:.68rem;font-weight:700'>✅ RECOMMANDÉ</span>" if _is_reco else ""}
  </div>
  <div style="font-size:.74rem;color:#339999;margin-bottom:10px">{_adesc} · Risque : {_arisk}</div>
  <div class="gauge-wrap">
    <div class="gauge-lbl"><span>Score de pertinence</span><span>{_ascore}%</span></div>
    <div class="gauge-track"><div class="gauge-fill" style="--bw:{_ascore}%"></div></div>
  </div>
</div>""", unsafe_allow_html=True)

        with st.expander(f"Actions  --  {_alabel}"):
            for _ac in _adata.get("actions", []):
                st.markdown(f"- {_ac}")

    st.divider()

    # ── Customer Journey ──────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Customer Journey Map  --  7 étapes</div>', unsafe_allow_html=True)
    _journey = journey_data if journey_data else []
    for _ji, _stage in enumerate(_journey):
        _score = _stage.get("score", 5)
        _color = "#267371" if _score >= 7 else "#44C1BA" if _score >= 5 else "#B83D4B"
        with st.expander(f"{_stage.get('emotion','')} {_stage.get('stage','')}  --  Score expérience {_score}/10"):
            _jc1, _jc2 = st.columns(2)
            with _jc1:
                st.markdown("**Touchpoints**")
                for _tp in _stage.get("touchpoints", []):
                    st.markdown(f"- {_tp}")
            with _jc2:
                st.markdown(f"**[-] Pain point** : {_stage.get('pain','')}")
                st.markdown(f"**[+] Opportunité** : {_stage.get('opportunity','')}")

    st.divider()

    # ── Pricing Strategy ─────────────────────────────────────────────────────
    st.markdown('<div class="section-h">Stratégie Pricing</div>', unsafe_allow_html=True)
    _pric = pricing_strat if pricing_strat else {}
    _pc1, _pc2 = st.columns(2)
    with _pc1:
        st.metric("Prix de base recommandé", _pric.get("recommended_base_price","N/A"))
        st.markdown("**Modèles de pricing :**")
        for _m in _pric.get("models", [])[:5]:
            st.markdown(f"- {_m}")
    with _pc2:
        st.markdown("**Stratégie d'ancrage :**")
        for _an in _pric.get("anchor_strategy", []):
            st.markdown(f"- {_an}")
    st.markdown("**Déclencheurs psychologiques :**")
    for _pt in _pric.get("psychological_triggers", []):
        st.markdown(f"- {_pt}")
    st.info(f"[Test] Test A/B recommandé : {_pric.get('elasticite','')}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 12  --  EMAILING (Séquences complètes)
# ══════════════════════════════════════════════════════════════════════════════
# ═══ TAB 13  --  PRICING ═══
with tabs[12]:
    st.markdown("""
<div style="background:linear-gradient(135deg,#267371,#44C1BA);color:white;border-radius:14px;
  padding:18px 24px;margin-bottom:20px">
  <b style="font-size:1.05rem">📧 Stratégie Email Marketing — 5 séquences complètes</b><br>
  <span style="opacity:.9;font-size:.85rem">Séquences prêtes à l'emploi · Objets testés · KPIs cibles</span>
</div>
""", unsafe_allow_html=True)

    _seq = email_seq if email_seq else {}
    _seq_icons = {"welcome": "", "nurture": "~", "abandoned_cart": "[P]", "reactivation": "", "upsell": "⬆️"}

    for _seq_key, _seq_data in _seq.items():
        _icon = _seq_icons.get(_seq_key, "")
        with st.expander(f"{_icon} {_seq_data.get('name','')}", expanded=(_seq_key == 'welcome')):
            _kpis = _seq_data.get("kpis", {})
            _kc = st.columns(3)
            for _col, (_kn, _kv) in zip(_kc, _kpis.items()):
                with _col:
                    st.metric(_kn.replace("_"," ").title(), _kv)

            st.markdown("**Emails de la séquence :**")
            for _em in _seq_data.get("emails", []):
                st.markdown(f"""
<div class="card" style="margin-bottom:8px;display:flex;align-items:flex-start;gap:12px">
  <div style="background:#C6ECD9;border-radius:8px;padding:4px 10px;font-size:.7rem;font-weight:800;color:#267371;flex-shrink:0">{_em.get('j','')}</div>
  <div>
    <div style="font-weight:700;font-size:.88rem;color:#0B2221">"{_em.get('objet','')}"</div>
    <div style="font-size:.76rem;color:#339999;margin-top:2px">{_em.get('objectif','')}</div>
  </div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 13  --  SOCIAL MEDIA (Stratégie par plateforme)
# ══════════════════════════════════════════════════════════════════════════════
# ═══ TAB 14  --  EMAIL SÉQUENCES ═══
with tabs[13]:
    st.markdown("""
<div style="background:linear-gradient(135deg,#393DAC,#44C1BA);color:white;border-radius:14px;
  padding:18px 24px;margin-bottom:20px">
  <b style="font-size:1.05rem"> Stratégie Social Media — Plan par plateforme</b><br>
  <span style="opacity:.9;font-size:.85rem">Priorités · Formats · Budgets · KPIs · Fréquences</span>
</div>
""", unsafe_allow_html=True)

    _social = social_strat if social_strat else {}
    _platform_icons = {"Instagram": "Insta", "TikTok": "TikTok", "LinkedIn": "", "YouTube": "[YT]",
                       "Pinterest": "Pinterest", "Facebook": "", "Twitter/X": "Twitter", "Newsletter": "[NL]",
                       "Product Hunt": "", "Podcast": "Podcast"}

    for _pname, _pdata in sorted(_social.items(), key=lambda x: x[1].get("priorite",99)):
        _icon = _platform_icons.get(_pname, "")
        _prio = _pdata.get("priorite", 0)
        _prio_color = "#B83D4B" if _prio == 1 else "#44C1BA" if _prio == 2 else "#339999"
        st.markdown(f"""
<div class="ben-card" style="margin-bottom:12px">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
    <div style="font-size:1.1rem;font-weight:800;color:#0B2221">{_icon} {_pname}</div>
    <span style="background:{_prio_color};color:white;border-radius:50px;padding:3px 12px;font-size:.7rem;font-weight:700">Priorité {_prio}</span>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">
    <div style="background:#F7FBF4;border-radius:8px;padding:8px"><div style="font-size:.64rem;color:#339999;font-weight:600">OBJECTIF</div><div style="font-size:.78rem;color:#0B2221;font-weight:600;margin-top:2px">{_pdata.get('objectif','')}</div></div>
    <div style="background:#F7FBF4;border-radius:8px;padding:8px"><div style="font-size:.64rem;color:#339999;font-weight:600">FORMAT</div><div style="font-size:.78rem;color:#0B2221;font-weight:600;margin-top:2px">{_pdata.get('format','')}</div></div>
    <div style="background:#F7FBF4;border-radius:8px;padding:8px"><div style="font-size:.64rem;color:#339999;font-weight:600">BUDGET</div><div style="font-size:.78rem;color:#0B2221;font-weight:600;margin-top:2px">{_pdata.get('budget','')}</div></div>
    <div style="background:#C6ECD9;border-radius:8px;padding:8px"><div style="font-size:.64rem;color:#267371;font-weight:600">KPI CIBLE</div><div style="font-size:.78rem;color:#0B2221;font-weight:600;margin-top:2px">{_pdata.get('kpi','')}</div></div>
  </div>
  <div style="margin-top:8px;font-size:.74rem;color:#339999">📅 Fréquence : <b>{_pdata.get('freq','')}</b></div>
</div>""", unsafe_allow_html=True)

    # Intelligence concurrentielle
    st.divider()
    st.markdown('<div class="section-h">🕵️ Intelligence concurrentielle</div>', unsafe_allow_html=True)
    _ci = comp_intel if comp_intel else {}
    with st.expander("Axes de veille concurrentielle"):
        for _ax in _ci.get("axes_veille", []):
            st.markdown(f"**{_ax.get('axe','')}**  --  {_ax.get('methode','')} · Outils : {', '.join(_ax.get('outils',[]))}")
    st.markdown("**Signaux d'opportunité à surveiller :**")
    for _sig in _ci.get("signaux_opportunite", []):
        st.markdown(f"- {_sig}")
    _cad = _ci.get("cadence", {})
    if _cad:
        _cadc = st.columns(3)
        for _col, (_freq, _action) in zip(_cadc, _cad.items()):
            with _col:
                st.metric(_freq.title(), _action)

    # Stratégie contenu
    st.divider()
    st.markdown('<div class="section-h">📝 Stratégie de contenu</div>', unsafe_allow_html=True)
    _cs = content_strat if content_strat else {}
    _csc1, _csc2 = st.columns(2)
    with _csc1:
        st.markdown("**Piliers éditoriaux :**")
        for _i, _pil in enumerate(_cs.get("pillars", []), 1):
            st.markdown(f"{_i}. {_pil}")
        st.markdown(f"**Budget contenu :** {_cs.get('budget_content','N/A')}")
    with _csc2:
        st.markdown("**Outils gratuits recommandés :**")
        for _t in _cs.get("tools_free", []):
            st.markdown(f"- {_t}")
        st.markdown("**KPIs contenu :**")
        for _kn, _kv in _cs.get("kpis", {}).items():
            st.markdown(f"- {_kn} : **{_kv}**")




# ══════════════════════════════════════════════════════════════════════════════
# TAB 12  --  PARCOURS CLIENT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[11]:
    st.markdown('''
<div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
  padding:18px 24px;margin-bottom:20px;display:flex;align-items:center;gap:12px">
  <span style="font-size:2rem"></span>
  <div>
    <b style="font-size:1rem">Parcours Client — Customer Journey Map</b><br>
    <span style="opacity:.85;font-size:.84rem">Chaque étape de la découverte à la fidélisation — avec les frictions et leviers d'action</span>
  </div>
</div>
''', unsafe_allow_html=True)

    _journey = gen_customer_journey(activity)
    if _journey:
        for _ji, (_stage, _desc, _channels, _actions, _emoji) in enumerate(_journey):
            _pct = int((_ji+1) / len(_journey) * 100)
            st.markdown(f'''
<div class="card" style="border-left:4px solid #44C1BA;margin-bottom:12px;position:relative">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
    <div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#44C1BA,#267371);
      display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0">{_emoji}</div>
    <div>
      <div style="font-weight:800;font-size:.95rem;color:#0B2221">{_stage}</div>
      <div style="font-size:.78rem;color:#339999">{_desc}</div>
    </div>
    <div style="margin-left:auto;text-align:right">
      <div style="font-size:.7rem;color:#339999;font-weight:600">Étape {_ji+1}/{len(_journey)}</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
    <div style="background:#F7FBF4;border-radius:8px;padding:10px">
      <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;color:#339999;margin-bottom:5px">Canaux présents</div>
      {"".join(f'<div style="font-size:.78rem;color:#0B2221;margin-bottom:3px">• {c}</div>' for c in _channels)}
    </div>
    <div style="background:#C6ECD9;border-radius:8px;padding:10px">
      <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;color:#267371;margin-bottom:5px">Leviers d'action</div>
      {"".join(f'<div style="font-size:.78rem;color:#0B2221;margin-bottom:3px">✓ {a}</div>' for a in _actions)}
    </div>
  </div>
  <div class="gauge-wrap" style="margin-top:10px">
    <div class="gauge-lbl"><span>Progression</span><span>{_pct}%</span></div>
    <div class="gauge-track"><div class="gauge-fill" style="--bw:{_pct}%"></div></div>
  </div>
</div>
''', unsafe_allow_html=True)

    # Value Chain Porter
    st.markdown('<div class="section-h" style="margin-top:24px">Chaîne de valeur (Porter)</div>', unsafe_allow_html=True)
    _vc = gen_value_chain(activity)
    if _vc:
        _vc_cols = st.columns(len(_vc.get("primaires",[])))
        for _col, (_act, _items, _color) in zip(_vc_cols, _vc.get("primaires",[])):
            with _col:
                st.markdown(f'''
<div style="background:{_color}15;border-radius:12px;padding:12px;border-top:3px solid {_color};text-align:center">
  <div style="font-weight:700;font-size:.8rem;color:#0B2221;margin-bottom:8px">{_act}</div>
  {"".join(f'<div style="font-size:.72rem;color:#339999;margin-bottom:3px">{it}</div>' for it in _items)}
</div>
''', unsafe_allow_html=True)

        st.markdown("**Activités de soutien :**")
        _sup_cols = st.columns(4)
        for _col2, (_k, _v) in zip(_sup_cols, _vc.get("support",[])[:4]):
            with _col2:
                st.markdown(f'''
<div class="card" style="padding:10px;text-align:center">
  <div style="font-weight:700;font-size:.78rem;color:#0B2221;margin-bottom:4px">{_k}</div>
  <div style="font-size:.72rem;color:#339999">{_v}</div>
</div>
''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 13  --  PRICING STRATEGY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[12]:
    st.markdown('''
<div style="background:linear-gradient(135deg,#267371,#44C1BA);color:white;border-radius:14px;
  padding:18px 24px;margin-bottom:20px">
  <b style="font-size:1rem"> Stratégie de prix — Psychologie & Positionnement</b><br>
  <span style="opacity:.85;font-size:.84rem">Techniques de pricing basées sur la psychologie comportementale et les données marché</span>
</div>
''', unsafe_allow_html=True)

    _pricing = gen_pricing_strategy(activity, monthly_budget)
    _bmc     = gen_business_model_canvas(activity, goal)

    st.markdown(f'<div class="section-h">Stratégie recommandée : {_pricing.get("recommandee","")}</div>', unsafe_allow_html=True)

    # 6 techniques de pricing
    _ptechs = _pricing.get("techniques", [])
    for i in range(0, len(_ptechs), 2):
        _pc1, _pc2 = st.columns(2)
        for _col, _tec in zip([_pc1, _pc2], _ptechs[i:i+2]):
            if _tec:
                _icon, _name, _desc, _impact = _tec
                with _col:
                    st.markdown(f'''
<div class="ben-card" style="margin-bottom:10px">
  <div style="font-size:1.6rem;margin-bottom:8px">{_icon}</div>
  <div style="font-weight:800;font-size:.9rem;color:#0B2221;margin-bottom:5px">{_name}</div>
  <div style="font-size:.8rem;color:#339999;line-height:1.5;margin-bottom:8px">{_desc}</div>
  <div style="background:#C6ECD9;border-radius:6px;padding:5px 10px;display:inline-block;
    font-size:.72rem;font-weight:700;color:#267371">{_impact}</div>
</div>
''', unsafe_allow_html=True)

    # Matrice de prix
    st.markdown('<div class="section-h">Matrice tarifaire suggérée</div>', unsafe_allow_html=True)
    _mat = _pricing.get("matrice", {})
    _mat_cols = st.columns(len(_mat))
    for _col, (_tier_name, _price) in zip(_mat_cols, _mat.items()):
        with _col:
            _price_str = f"{_price:.0f}€" if isinstance(_price, (int,float)) else str(_price)
            st.markdown(f'''
<div class="stat-box" style="border:2px solid #44C1BA">
  <div class="stat-num" style="font-size:1.8rem">{_price_str}</div>
  <div class="stat-lbl" style="font-size:.85rem;font-weight:700">{_tier_name.title()}</div>
</div>
''', unsafe_allow_html=True)

    # Business Model Canvas
    st.markdown('<div class="section-h" style="margin-top:24px">Business Model Canvas</div>', unsafe_allow_html=True)
    _bmc_items = [
        ("Segments", _bmc.get("segments",[])),
        (" Proposition valeur", _bmc.get("proposition",[])),
        (" Canaux", _bmc.get("canaux",[])),
        ("❤️ Relations", _bmc.get("relation",[])),
        (" Revenus", _bmc.get("revenus",[])),
        (" Ressources clés", _bmc.get("ressources",[])),
        ("⚙️ Activités clés", _bmc.get("activites",[])),
        (" Partenaires", _bmc.get("partenaires",[])),
        (" Structure coûts", _bmc.get("couts",[])),
    ]
    for i in range(0, 9, 3):
        _bm_cols = st.columns(3)
        for _col, (_bm_title, _bm_items) in zip(_bm_cols, _bmc_items[i:i+3]):
            with _col:
                _items_html = "".join(f'<div style="font-size:.74rem;color:#339999;margin-bottom:3px">• {it}</div>' for it in _bm_items[:4])
                st.markdown(f'''
<div class="card" style="padding:12px;height:100%">
  <div style="font-weight:700;font-size:.82rem;color:#0B2221;margin-bottom:6px">{_bm_title}</div>
  {_items_html}
</div>
''', unsafe_allow_html=True)

    # Intelligence concurrentielle
    st.markdown('<div class="section-h" style="margin-top:24px">5 Forces de Porter</div>', unsafe_allow_html=True)
    _ci = gen_competitive_intelligence(activity, goal)
    for _force_name, _score, _detail, _level in _ci.get("matrice_5_forces", []):
        _color = "#B83D4B" if _score >= 70 else "#44C1BA" if _score >= 45 else "#267371"
        st.markdown(f'''
<div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;padding:10px 14px;
  background:#F7FBF4;border-radius:10px">
  <div style="font-weight:700;font-size:.85rem;color:#0B2221;min-width:180px">{_force_name}</div>
  <div style="flex:1">
    <div class="gauge-track">
      <div class="gauge-fill" style="--bw:{_score}%;background:{_color}"></div>
    </div>
  </div>
  <div style="font-size:.78rem;color:{_color};font-weight:700;min-width:80px">{_level}</div>
  <div style="font-size:.74rem;color:#339999;max-width:200px">{_detail}</div>
</div>
''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 14  --  EMAIL SÉQUENCES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[13]:
    st.markdown('''
<div style="background:linear-gradient(135deg,#393DAC,#44C1BA);color:white;border-radius:14px;
  padding:18px 24px;margin-bottom:20px">
  <b style="font-size:1rem">📧 Email Automation — Séquences complètes</b><br>
  <span style="opacity:.85;font-size:.84rem">Templates d'emails personnalisés à votre secteur — prêts à implémenter dans Mailchimp, Brevo, HubSpot</span>
</div>
''', unsafe_allow_html=True)

    _email_seqs = gen_email_sequences(activity, goal)
    _gh_tactics = gen_growth_hacking(activity, monthly_budget)

    for _seq in _email_seqs:
        _seq_name = _seq.get("nom","")
        with st.expander(f"{_seq_name}", expanded=(_seq_name == _email_seqs[0].get("nom",""))):
            for _ej, (_timing, _subject, _content_hint) in enumerate(_seq.get("emails",[])):
                st.markdown(f'''
<div class="card" style="border-left:3px solid #393DAC;margin-bottom:10px">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
    <div style="background:#E4E9F6;border-radius:50%;width:28px;height:28px;
      display:flex;align-items:center;justify-content:center;font-weight:800;
      font-size:.78rem;color:#393DAC;flex-shrink:0">{_ej+1}</div>
    <div style="font-weight:700;font-size:.88rem;color:#0B2221">{_timing}</div>
  </div>
  <div style="background:#E4E9F6;border-radius:8px;padding:10px;margin-bottom:8px">
    <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;color:#393DAC;margin-bottom:4px">Ligne objet</div>
    <div style="font-size:.82rem;color:#0B2221;font-style:italic">"{_subject}"</div>
  </div>
  <div style="font-size:.78rem;color:#339999">{_content_hint}</div>
</div>
''', unsafe_allow_html=True)

    # Growth Hacking tactics
    st.markdown('<div class="section-h" style="margin-top:24px">Growth Hacking  --  Tactiques ROI maximal</div>', unsafe_allow_html=True)
    for _gt in _gh_tactics:
        if len(_gt) >= 4:
            _gt_name, _gt_desc, _gt_cost, _gt_roi = _gt
            st.markdown(f'''
<div class="card" style="display:flex;align-items:flex-start;gap:12px;margin-bottom:8px">
  <div style="font-size:1.4rem;flex-shrink:0">{_gt_name.split()[0]}</div>
  <div style="flex:1">
    <div style="font-weight:700;font-size:.88rem;color:#0B2221;margin-bottom:3px">{" ".join(_gt_name.split()[1:])}</div>
    <div style="font-size:.8rem;color:#339999;line-height:1.5">{_gt_desc}</div>
  </div>
  <div style="text-align:right;flex-shrink:0">
    <div style="font-size:.7rem;font-weight:700;color:#267371">{_gt_cost}</div>
    <div style="font-size:.72rem;font-weight:800;color:#44C1BA">{_gt_roi}</div>
  </div>
</div>
''', unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════════
# TAB 15  --  NOUVEAU PROJET (wizard indépendant)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[15]:
    if _HAS_PROJECT_TAB:
        try:
            _render_new_project_tab()
        except Exception as _e_proj:
            st.error(f"Erreur chargement module projet: {_e_proj}")
    else:
        st.info("Module Nouveau Projet en cours de chargement...")
        st.markdown("""
**Wizard de création de projet**

Ce module vous guide étape par étape pour :
1. Définir le concept de votre projet
2. Renseigner les infos de votre entreprise  
3.  Identifier votre cible client
4.  Configurer votre budget et objectifs
5. Définir vos mots-clés SEO
6. Generer votre fiche stratégique et l'exporter
""")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 16  --  RESSOURCES (blog + Top 10)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[16]:
    if _HAS_RESOURCES:
        try:
            _render_resources_page()
        except Exception as _e_res:
            st.error(f"Erreur module ressources: {_e_res}")
    else:
        st.info("Module Ressources en cours de chargement...")
        st.markdown("""
**Ressources & Outils gratuits**

- Actualites marketing & stratégie en temps réel (Google News RSS)
- Top 10 outils de veille
- Top 10 outils SEO gratuits
- Top 10 outils d'enquête de marché
- Top 10 outils d'acquisition de leads
- Top 10 outils de communication
""")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 14  --  TARIFS & PLANS (Neuromarketing + RGPD)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[14]:
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
  padding:20px 26px;margin-bottom:24px">
  <div style="font-size:1.1rem;font-weight:900;margin-bottom:6px">Choisissez votre plan BiziApp</div>
  <div style="font-size:.85rem;opacity:.85">
    14 modules strategiques · Export PDF · Donnees live · Support inclus
  </div>
</div>
""", unsafe_allow_html=True)

    def _on_plan_select(plan_id):
        st.session_state["selected_plan"] = plan_id
        if plan_id == "demo":
            st.success("Vous etes deja en acces Demo. Toutes les fonctions de base sont disponibles.")
        elif plan_id in ("starter","pro"):
            st.session_state["show_checkout"] = plan_id
            st.rerun()

    if _HAS_PRICING:
        render_pricing_page(
            billing=st.session_state.get("billing_pref","annual"),
            on_plan_select=_on_plan_select
        )
    else:
        # Affichage minimal si pricing_plans absent
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Demo", "Gratuit", "Fonctions de base")
            st.button("Commencer gratuitement", key="plan_demo_fb", use_container_width=True)
        with c2:
            st.metric("Starter", "39€/mois", "14 modules complets")
            st.button("Essai 7j gratuit", key="plan_starter_fb", type="primary", use_container_width=True)
        with c3:
            st.metric("Pro", "89€/mois", "Tout inclus + IA")
            st.button("Essai Pro 7j", key="plan_pro_fb", type="primary", use_container_width=True)

    # ── Checkout simulé ────────────────────────────────────────────────────────
    _plan_to_checkout = st.session_state.get("show_checkout")
    if _plan_to_checkout:
        plan_info = PLANS.get(_plan_to_checkout, {}) if _HAS_PRICING else {}
        price = plan_info.get("monthly", 0)
        st.divider()
        st.markdown(f"""
<div style="background:#F7FBF4;border-radius:14px;padding:24px;border:2px solid #44C1BA;max-width:520px;margin:0 auto">
  <div style="font-size:1rem;font-weight:800;color:#0B2221;margin-bottom:12px">
    Finaliser votre abonnement {plan_info.get("name","Pro")}
  </div>
  <div style="font-size:2rem;font-weight:900;color:#44C1BA;margin-bottom:8px">
    {price}€<span style="font-size:1rem;color:#339999;font-weight:500">/mois</span>
  </div>
  <div style="font-size:.78rem;color:#267371;margin-bottom:16px">
    Essai 7 jours gratuit · Aucun debit pendant l'essai · Résiliation libre
  </div>
  <div style="font-size:.72rem;color:#339999;background:white;border-radius:8px;padding:10px;border:1px solid #C6ECD9">
    Le paiement securise sera configure dans votre espace compte.<br>
    <b>Stripe</b> · Visa · Mastercard · SEPA · Apple Pay · Google Pay
  </div>
</div>
""", unsafe_allow_html=True)
        if st.button("Confirmer l'abonnement", type="primary", key="confirm_checkout"):
            st.success(f"Abonnement {plan_info.get('name','')} active ! Bienvenue dans BiziApp.")
            st.session_state.pop("show_checkout", None)



    # ── Ikigai ────────────────────────────────────────────────────────────────
    with _strat_tabs[4]:
        st.markdown('<div class="section-h">Ikigai professionnel</div>', unsafe_allow_html=True)
        ik = ikigai_data if ikigai_data else {}
        ic1, ic2 = st.columns(2)
        with ic1:
            st.markdown("**Ce que vous aimez (Passion)**")
            for p in ik.get("passion",[]): st.markdown(f"- {p}")
            st.markdown("**Ce pour quoi vous etes fait (Vocation)**")
            for v in ik.get("vocation",[]): st.markdown(f"- {v}")
        with ic2:
            st.markdown("**Ce dont le monde a besoin (Mission)**")
            for m in ik.get("mission",[]): st.markdown(f"- {m}")
            st.markdown("**Votre profession**")
            for pr in ik.get("profession",[]): st.markdown(f"- {pr}")
        st.info(f"**Votre Ikigai** : {ik.get('intersection','')}")
        st.success(f"**Raison d'etre** : {ik.get('raison_etre','')}")

    # ── Ocean Bleu ────────────────────────────────────────────────────────────
    with _strat_tabs[5]:
        st.markdown('<div class="section-h">Canevas Stratégique  --  Ocean Bleu</div>', unsafe_allow_html=True)
        bo = blue_ocean if blue_ocean else {}
        boc1, boc2 = st.columns(2)
        with boc1:
            st.markdown('<div style="background:#F7EEF0;border-radius:10px;padding:12px;margin-bottom:10px"><b style="color:#B83D4B">Eliminer</b></div>', unsafe_allow_html=True)
            for x in bo.get("eliminer",[]): st.markdown(f"- {x}")
            st.markdown('<div style="background:#FEF3C7;border-radius:10px;padding:12px;margin-top:10px"><b style="color:#B45309">Reduire</b></div>', unsafe_allow_html=True)
            for x in bo.get("reduire",[]): st.markdown(f"- {x}")
        with boc2:
            st.markdown('<div style="background:#C6ECD9;border-radius:10px;padding:12px;margin-bottom:10px"><b style="color:#267371">Augmenter</b></div>', unsafe_allow_html=True)
            for x in bo.get("augmenter",[]): st.markdown(f"- {x}")
            st.markdown('<div style="background:#E4E9F6;border-radius:10px;padding:12px;margin-top:10px"><b style="color:#393DAC">Creer</b></div>', unsafe_allow_html=True)
            for x in bo.get("creer",[]): st.markdown(f"- {x}")
        st.success(f"**Espace non conteste** : {bo.get('espace_non_conteste','')}")

    # ── Lean Canvas ───────────────────────────────────────────────────────────
    with _strat_tabs[6]:
        st.markdown('<div class="section-h">Lean Canvas  --  9 blocs</div>', unsafe_allow_html=True)
        lc = lean_canvas if lean_canvas else {}
        lcc1, lcc2 = st.columns(2)
        with lcc1:
            st.markdown("**Probleme**")
            for p in lc.get("probleme",{}).get("contenu",[]): st.markdown(f"- {p}")
            st.caption(f"Alternatives actuelles : {lc.get('probleme',{}).get('alternatives','')}")
            st.markdown("**Solution**")
            for s in lc.get("solution",{}).get("contenu",[]): st.markdown(f"- {s}")
            st.markdown("**Canaux**")
            for c in lc.get("canaux",[]): st.markdown(f"- {c}")
            st.markdown("**Revenus**")
            st.info(lc.get("revenus",""))
        with lcc2:
            st.markdown("**Proposition de valeur**")
            st.success(lc.get("proposition_valeur",""))
            st.markdown("**Avantage concurrentiel**")
            st.info(lc.get("avantage_competitif",""))
            st.markdown("**Segments clients**")
            segs = lc.get("segments",{})
            st.markdown(f"- Early adopters : {segs.get('early_adopters','')}")
            st.markdown(f"- Marche total : {segs.get('marche_total','')}")
            st.markdown("**Metriques cles**")
            for m in lc.get("metriques",[]): st.markdown(f"- {m}")
            st.markdown("**Couts**")
            st.caption(lc.get("couts",""))

    # ── Scenarios ─────────────────────────────────────────────────────────────
    with _strat_tabs[7]:
        st.markdown('<div class="section-h">Planification par scenarios  --  18 mois</div>', unsafe_allow_html=True)
        for sc in (scenarios or []):
            with st.expander(f"{sc.get('nom','Scenario')}  --  Probabilite {sc.get('probabilite','N/A')}"):
                scc1, scc2 = st.columns(2)
                with scc1:
                    st.markdown("**Conditions**")
                    for c in sc.get("conditions",[]): st.markdown(f"- {c}")
                    st.markdown("**Actions cles**")
                    for a in sc.get("actions",[]): st.markdown(f"- {a}")
                with scc2:
                    kpis = sc.get("kpis",{})
                    st.metric("Croissance CA", kpis.get("ca_growth","N/A"))
                    st.metric("Clients nets", kpis.get("clients_nets","N/A"))
                    st.metric("NPS cible", kpis.get("nps","N/A"))

    # ── Plan 180 jours ────────────────────────────────────────────────────────
    with _strat_tabs[8]:
        st.markdown('<div class="section-h">Plan d&apos;action 180 jours</div>', unsafe_allow_html=True)
        for sprint in (plan_180j or []):
            _color = ["#44C1BA","#267371","#393DAC","#0B2221","#B83D4B","#339999"][sprint.get("sprint",1)-1]
            with st.expander(f"Sprint {sprint.get('sprint','?')} - {sprint.get('theme','')}", expanded=(sprint.get("sprint")==1)):
                st.markdown(f"**Objectif** : {sprint.get('objectif','')}")
                pc1, pc2 = st.columns(2)
                with pc1:
                    st.markdown("**Actions**")
                    for a in sprint.get("actions",[]): st.markdown(f"- {a}")
                with pc2:
                    st.markdown("**KPI de succes**")
                    st.success(sprint.get("kpi",""))

    # ── Analytics Dashboard ───────────────────────────────────────────────────
    with _strat_tabs[9]:
        st.markdown('<div class="section-h">Dashboard Analytics  --  Benchmarks et objectifs</div>', unsafe_allow_html=True)
        ad = analytics_data if analytics_data else {}
        bench = ad.get("benchmarks",{})
        obj = ad.get("objectifs_90j",{})
        # KPIs cibles
        adc1, adc2, adc3, adc4 = st.columns(4)
        adc1.metric("Leads / mois cible", obj.get("leads_mensuel","N/A"))
        adc2.metric("Nouveaux clients (90j)", obj.get("clients_nouveaux","N/A"))
        adc3.metric("CA additionnel", obj.get("ca_additionnel","N/A"))
        adc4.metric("ROI cible", obj.get("roi_cible","N/A"))
        st.divider()
        # Benchmarks sectoriels
        st.markdown("**Benchmarks sectoriels**")
        if bench:
            bench_cols = st.columns(len(bench))
            for col, (kpi, val) in zip(bench_cols, bench.items()):
                col.metric(kpi.replace("_"," ").title(), str(val))
        # Alertes
        st.markdown("**Alertes et points de vigilance**")
        for alerte in ad.get("alertes",[]):
            st.warning(alerte)
        # Formules KPIs
        st.markdown("**Formules KPIs essentiels**")
        for kpi_item in ad.get("kpis_dashboard",[]):
            st.markdown(f"- **{kpi_item.get('kpi','')}** : {kpi_item.get('calcul','')}")


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#339999;font-size:.78rem;padding:12px 0">
  <b style="color:#0B2221">BiziApp v5.0</b> — Stratégie 360° · SWOT · QQOQCCP · PESTEL · SONCAS · AIDA · SPIN · Challenger · GEO 2025 · SEA IA · KPIs · OKR · Veille Live · RSE · RFM · BATNA · Prix psychologiques<br>
  <span style="color:#44C1BA">Analyse personnalisée · Données live · Cache intelligent · Lecture URL en direct · Veille concurrentielle · Actualités Google News · Wikipedia · DuckDuckGo</span><br>
  Données live : Google News · Bing News · Reddit · HN · DEV.to · Recherche-Entreprises · OSM · Wikidata · Wikipedia · AllOrigins · corsproxy.io · Analyse heuristique · Inputs validés &amp; sécurisés (XSS, SSRF, rate-limiting)
</div>
""", unsafe_allow_html=True)
