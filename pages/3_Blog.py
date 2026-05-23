"""
pages/3_Blog.py — Blog SEO BiziApp
Articles mis à jour automatiquement via flux RSS gratuits
"""
import streamlit as st
import urllib.request as _ur
import xml.etree.ElementTree as _ET
import datetime, re, html

st.set_page_config(
    page_title="Blog Stratégie & Marketing — BiziApp",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""<style>
:root{--teal:#44C1BA;--jade:#267371;--dark:#0B2221;--light:#F7FBF4;--card:#C6ECD9}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--light)}
.blog-card{background:white;border-radius:16px;border:1.5px solid var(--card);padding:20px;margin-bottom:14px;
  transition:box-shadow .2s,transform .2s;cursor:pointer}
.blog-card:hover{box-shadow:0 8px 28px rgba(68,193,186,.15);transform:translateY(-2px);border-color:var(--teal)}
.blog-tag{display:inline-block;background:var(--card);color:var(--jade);border-radius:50px;
  padding:3px 12px;font-size:.72rem;font-weight:700;margin-right:6px}
.blog-source{font-size:.7rem;color:#339999;font-weight:600}
.blog-date{font-size:.7rem;color:#339999}
.seo-meta{background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
  padding:20px 24px;margin-bottom:24px}
</style>""", unsafe_allow_html=True)

# ── SEO META HEADER ──────────────────────────────────────────────────────────
st.markdown("""
<div class="seo-meta">
  <h1 style="margin:0 0 8px;font-size:1.6rem;font-weight:900">📝 Blog Stratégie & Marketing</h1>
  <p style="margin:0;opacity:.88;font-size:.9rem">
    Articles experts mis à jour en temps réel · Stratégie commerciale · Marketing digital ·
    SEO · Growth hacking · Entrepreneuriat · Veille marché
  </p>
</div>
""", unsafe_allow_html=True)

# ── SOURCES RSS GRATUITES ────────────────────────────────────────────────────
RSS_SOURCES = [
    {"name": "HubSpot Blog", "url": "https://blog.hubspot.com/marketing/rss.xml", "tag": "Marketing"},
    {"name": "Neil Patel", "url": "https://neilpatel.com/fr/blog/feed/", "tag": "SEO"},
    {"name": "Moz Blog", "url": "https://moz.com/blog/feed", "tag": "SEO"},
    {"name": "Seth Godin", "url": "https://seths.blog/feed/", "tag": "Stratégie"},
    {"name": "Harvard Biz Review", "url": "http://feeds.hbr.org/harvardbusiness", "tag": "Business"},
    {"name": "Entrepreneur.com", "url": "https://www.entrepreneur.com/latest.rss", "tag": "Entrepreneuriat"},
    {"name": "Search Engine Journal", "url": "https://www.searchenginejournal.com/feed/", "tag": "SEO"},
    {"name": "Content Marketing Institute", "url": "https://contentmarketinginstitute.com/feed/", "tag": "Contenu"},
]

# Articles maison (statiques, toujours dispo, fort SEO)
STATIC_ARTICLES = [
    {
        "title": "Comment créer une stratégie commerciale complète en 10 minutes avec BiziApp",
        "summary": "Découvrez comment BiziApp génère automatiquement votre SWOT, vos personas, votre plan SEO et votre roadmap 180 jours — sans expertise marketing préalable.",
        "tag": "Stratégie", "date": "2025-06", "source": "BiziApp",
        "slug": "strategie-commerciale-10-minutes",
        "keywords": ["stratégie commerciale", "plan marketing", "SWOT automatique", "BiziApp"],
        "read_time": "5 min",
    },
    {
        "title": "Les 5 erreurs fatales des entrepreneurs TPE en matière de marketing digital",
        "summary": "73% des TPE françaises n'ont pas de stratégie marketing formalisée. Voici les 5 pièges les plus courants et comment les éviter avec des outils gratuits.",
        "tag": "Marketing", "date": "2025-06", "source": "BiziApp",
        "slug": "erreurs-marketing-tpe",
        "keywords": ["marketing digital TPE", "erreurs marketing", "stratégie TPE"],
        "read_time": "7 min",
    },
    {
        "title": "SWOT 2025 : la méthode complète pour analyser votre entreprise",
        "summary": "Le SWOT reste l'outil stratégique le plus puissant pour les entrepreneurs. Apprenez à l'utiliser correctement avec des exemples concrets par secteur.",
        "tag": "Stratégie", "date": "2025-05", "source": "BiziApp",
        "slug": "swot-methode-complete-2025",
        "keywords": ["SWOT", "analyse SWOT 2025", "forces faiblesses opportunités menaces"],
        "read_time": "8 min",
    },
    {
        "title": "SEO local en 2025 : dominez Google Maps et générez des leads sans publicité",
        "summary": "Le SEO local est le levier d'acquisition le plus rentable pour les PME. Voici la stratégie complète pour apparaître en premier sur Google Maps dans votre zone.",
        "tag": "SEO", "date": "2025-05", "source": "BiziApp",
        "slug": "seo-local-2025-google-maps",
        "keywords": ["SEO local", "Google Maps 2025", "référencement local", "PME"],
        "read_time": "9 min",
    },
    {
        "title": "Personas client : comment créer des profils précis qui boostent vos ventes",
        "summary": "Un persona bien construit augmente votre taux de conversion de 30%. Découvrez la méthode SONCAS appliquée à la création de personas B2C et B2B.",
        "tag": "Marketing", "date": "2025-04", "source": "BiziApp",
        "slug": "personas-client-methode-soncas",
        "keywords": ["personas client", "SONCAS", "buyer persona", "segmentation client"],
        "read_time": "6 min",
    },
    {
        "title": "GEO 2025 : optimiser son contenu pour l'IA (ChatGPT, Perplexity, Gemini)",
        "summary": "La Generative Engine Optimization est la nouvelle frontière du SEO. Comment apparaître dans les réponses IA quand vos clients cherchent vos services.",
        "tag": "SEO", "date": "2025-04", "source": "BiziApp",
        "slug": "geo-2025-optimisation-ia",
        "keywords": ["GEO 2025", "optimisation IA", "ChatGPT SEO", "Perplexity", "Gemini SEO"],
        "read_time": "7 min",
    },
]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_rss_articles(source_url: str, tag: str, source_name: str, max_items: int = 4) -> list:
    """Fetch RSS feed — gratuit, sans clé."""
    try:
        req = _ur.Request(source_url, headers={"User-Agent": "BiziApp/3.1"})
        with _ur.urlopen(req, timeout=6) as r:
            raw = r.read()
        root = _ET.fromstring(raw)
        items = []
        for item in root.findall(".//item")[:max_items]:
            title   = item.findtext("title","").strip()
            link    = item.findtext("link","").strip()
            desc    = item.findtext("description","") or ""
            pub     = item.findtext("pubDate","")[:16]
            desc_clean = re.sub(r"<[^>]+>","",html.unescape(desc))[:180]
            if title and link:
                items.append({
                    "title": title[:100],
                    "link": link,
                    "summary": desc_clean,
                    "tag": tag,
                    "date": pub,
                    "source": source_name,
                    "read_time": "3-5 min",
                })
        return items
    except Exception:
        return []

# ── FILTRES ───────────────────────────────────────────────────────────────────
tags_all = ["Tous", "Stratégie", "Marketing", "SEO", "Contenu", "Business", "Entrepreneuriat"]
selected_tag = st.selectbox("Filtrer par catégorie", tags_all, label_visibility="collapsed")

# ── ARTICLES MAISON ───────────────────────────────────────────────────────────
st.markdown("### ✍️ Articles BiziApp")
for art in STATIC_ARTICLES:
    if selected_tag == "Tous" or art["tag"] == selected_tag:
        st.markdown(f"""
<div class="blog-card">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px">
    <div style="flex:1">
      <div style="margin-bottom:8px">
        <span class="blog-tag">{art["tag"]}</span>
        <span class="blog-source">BiziApp · {art["date"]} · ⏱ {art["read_time"]}</span>
      </div>
      <div style="font-weight:800;font-size:.95rem;color:#0B2221;margin-bottom:6px">{art["title"]}</div>
      <div style="font-size:.82rem;color:#339999;line-height:1.55">{art["summary"]}</div>
      <div style="margin-top:10px;font-size:.72rem;color:#267371;font-weight:600">
        🔑 {" · ".join(art["keywords"][:3])}
      </div>
    </div>
    <div style="background:#C6ECD9;border-radius:10px;padding:8px 14px;font-size:.72rem;
      font-weight:700;color:#267371;white-space:nowrap;flex-shrink:0">Lire →</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ARTICLES LIVE RSS ─────────────────────────────────────────────────────────
st.markdown("### 🌐 Articles récents — Sources expertes")
all_live = []
with st.spinner("Chargement des articles récents..."):
    for src in RSS_SOURCES[:4]:  # 4 sources max pour la perf
        arts = fetch_rss_articles(src["url"], src["tag"], src["name"])
        all_live.extend(arts)

if all_live:
    for art in all_live[:12]:
        if selected_tag == "Tous" or art["tag"] == selected_tag:
            st.markdown(f"""
<div class="blog-card">
  <div style="margin-bottom:6px">
    <span class="blog-tag">{art["tag"]}</span>
    <span class="blog-source">{art["source"]}</span>
    <span class="blog-date"> · {art["date"]}</span>
  </div>
  <div style="font-weight:700;font-size:.9rem;color:#0B2221;margin-bottom:5px">{art["title"]}</div>
  <div style="font-size:.8rem;color:#339999;line-height:1.5">{art["summary"][:160]}</div>
  <a href="{art["link"]}" target="_blank" style="display:inline-block;margin-top:8px;
    color:#44C1BA;font-size:.76rem;font-weight:700;text-decoration:none">Lire l'article complet →</a>
</div>
""", unsafe_allow_html=True)
else:
    st.info("Articles live temporairement indisponibles — affichage des articles BiziApp uniquement.")

st.markdown("""---
<div style="text-align:center;padding:16px;font-size:.78rem;color:#339999">
  Blog BiziApp · Mis à jour automatiquement · Contenu libre de droits pour usage personnel<br>
  <strong>Mots-clés SEO</strong> : stratégie commerciale · plan marketing · SWOT · personas · SEO 2025 · GEO · growth hacking · TPE PME France
</div>
""", unsafe_allow_html=True)
