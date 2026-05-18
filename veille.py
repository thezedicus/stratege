"""
veille.py — BiziVeille : Intelligence Stratégique & Concurrentielle
Streamlit · Python 3.9+

APIs gratuites, sans clé :
  Jina.ai Reader  → https://r.jina.ai/{url}     (lecture URL → markdown)
  Google News RSS → news.google.com/rss/search   (actualités live)
  DuckDuckGo IA   → api.duckduckgo.com           (contexte marché)
  Wikipedia REST  → wikipedia.org/api/rest_v1    (définitions secteur)
"""

import json
import datetime
import html as _html
import urllib.parse as _urlparse
import urllib.request as _urlreq
import xml.etree.ElementTree as _ET
import re
import streamlit as st

# ── Optional ──────────────────────────────────────────────────────────────────
try:
    import requests as _req
    _HAS_REQ = True
except ImportError:
    _HAS_REQ = False

try:
    from bs4 import BeautifulSoup as _BS
    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BiziVeille — Intelligence Stratégique",
    page_icon=":material/radar:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — charte Stratège
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
:root{
  --graphite:#0F172A;--graphite2:#1E293B;--graphite-mute:#475569;
  --ambre:#D97706;--ambre-soft:#FBBF24;--ambre-pale:#FEF3C7;
  --sauge:#047857;--sauge-soft:#10B981;--sauge-pale:#D1FAE5;
  --ivoire:#FAF8F4;--brume:#F2EFE8;--craie:#E7E2D6;
  --encre:#1A1A1A;--muted:#6B7280;--border:#E5E7EB;
  --danger:#B91C1C;--danger-pale:#FEE2E2;
  --warn:#C2410C;--warn-pale:#FFEDD5;
  --info:#1D4ED8;--info-pale:#DBEAFE;
}
*,*::before,*::after{box-sizing:border-box}
html,body,[class*="css"]{
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  -webkit-font-smoothing:antialiased;color:var(--encre)
}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1.25rem!important;max-width:1340px}
[data-testid="stSidebar"]{background:#F8F7F4;border-right:1px solid var(--craie)}
[data-testid="stSidebar"] label{font-weight:500;font-size:.88rem}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid var(--craie);background:transparent}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent;border:none;border-bottom:2px solid transparent;margin-bottom:-2px;padding:10px 16px;font-size:.76rem;font-weight:600;color:var(--muted);letter-spacing:.05em;text-transform:uppercase;transition:color .2s,border-color .2s}
[data-testid="stTabs"] [aria-selected="true"]{color:var(--graphite)!important;border-bottom-color:var(--ambre)!important}
[data-testid="stTabs"] [data-baseweb="tab"]:hover{color:var(--graphite)}

/* ── Cards ── */
.card{background:white;border:1px solid var(--craie);border-radius:12px;padding:18px 20px;margin-bottom:14px;transition:box-shadow .2s}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,.07)}
.card-dark{background:linear-gradient(135deg,var(--graphite) 0%,var(--graphite2) 100%);color:white;border-radius:12px;padding:20px 24px;margin-bottom:14px}
.card-amber{background:var(--ambre-pale);border:1px solid #FCD34D;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.card-green{background:var(--sauge-pale);border:1px solid #6EE7B7;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.card-blue{background:var(--info-pale);border:1px solid #93C5FD;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.card-red{background:var(--danger-pale);border:1px solid #FCA5A5;border-radius:10px;padding:14px 18px;margin-bottom:10px}

/* ── Section headers ── */
.section-h{display:flex;align-items:center;gap:10px;margin:22px 0 14px;font-weight:700;font-size:1rem;color:var(--graphite)}
.section-h::before{content:"";width:4px;height:16px;background:var(--ambre);border-radius:2px;flex-shrink:0}

/* ── Header ── */
.bizi-header{display:flex;align-items:center;gap:16px;padding:0 0 18px;border-bottom:1px solid var(--craie);margin-bottom:22px}
.logo-bizi{font-size:1.8rem;font-weight:800;color:var(--graphite);letter-spacing:-1.5px;line-height:1}
.logo-app{font-size:1.8rem;font-weight:800;color:var(--ambre);letter-spacing:-1.5px;line-height:1}
.header-sub{font-size:.68rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;font-weight:500;margin-top:3px}

/* ── News ── */
.news-item{border-left:3px solid var(--ambre);padding:10px 14px;margin-bottom:9px;background:white;border-radius:0 8px 8px 0;transition:border-color .2s}
.news-item:hover{border-color:var(--ambre-soft)}
.news-title{font-weight:600;font-size:.88rem;color:var(--graphite);margin-bottom:4px;line-height:1.35}
.news-meta{font-size:.7rem;color:var(--muted)}
.news-source{background:var(--ambre-pale);color:#92400E;padding:2px 7px;border-radius:4px;font-size:.63rem;font-weight:600;margin-right:6px}

/* ── Tags ── */
.kw-tag{display:inline-block;background:var(--ambre-pale);color:#92400E;border-radius:4px;padding:2px 8px;font-size:.65rem;font-weight:600;margin:2px}
.kw-tag-blue{display:inline-block;background:var(--info-pale);color:#1E40AF;border-radius:4px;padding:2px 8px;font-size:.65rem;font-weight:600;margin:2px}
.kw-tag-green{display:inline-block;background:var(--sauge-pale);color:#065F46;border-radius:4px;padding:2px 8px;font-size:.65rem;font-weight:600;margin:2px}

/* ── Live badge ── */
.badge-live{display:inline-flex;align-items:center;gap:5px;background:#D1FAE5;color:#065F46;border-radius:20px;padding:4px 11px;font-size:.65rem;font-weight:700;letter-spacing:.03em}
.pulse{width:6px;height:6px;border-radius:50%;background:#10B981;animation:pulse-anim 1.5s infinite;flex-shrink:0}
@keyframes pulse-anim{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(1.4)}}

/* ── Sidebar ── */
.step-label{display:flex;align-items:center;gap:8px;font-weight:600;font-size:.78rem;color:var(--graphite);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.04em}
.step-num{width:20px;height:20px;border-radius:50%;background:var(--ambre);color:white;font-size:.62rem;font-weight:800;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}

/* ── Feature grid ── */
.feat-card{background:white;border:1px solid var(--craie);border-radius:12px;padding:20px;min-height:110px;transition:box-shadow .2s}
.feat-card:hover{box-shadow:0 4px 20px rgba(0,0,0,.08)}
.feat-icon{width:32px;height:32px;background:var(--ambre-pale);border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}

/* ── Competitor card ── */
.comp-card{background:white;border:1px solid var(--craie);border-radius:12px;padding:16px;transition:border-color .2s;height:100%}
.comp-card:hover{border-color:var(--ambre)}
.comp-url{font-size:.68rem;color:var(--muted);font-family:monospace;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-bottom:4px}
.comp-title{font-weight:700;font-size:.92rem;color:var(--graphite);margin-bottom:6px;line-height:1.3}

.sep{height:1px;background:var(--craie);margin:20px 0}

button[kind="primary"]{background:var(--graphite)!important;border:none!important;transition:background .2s!important}
button[kind="primary"]:hover{background:var(--graphite2)!important}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
_UA = "Mozilla/5.0 BiziVeille/1.0 (+https://github.com/thezedicus/stratege)"
_STOP_FR = {
    "avec","dans","pour","les","des","une","sur","par","que","qui","pas","mais",
    "donc","aussi","très","tout","comme","nous","vous","sont","était","être",
    "avoir","peut","plus","cette","cela","leur","dont","plus","bien","fait",
    "même","sous","vers","sans","entre","après","avant","depuis","pendant",
    "this","that","from","with","your","will","have","been","they","their",
    "what","when","where","which","there","about","would","could","should",
}

# ─────────────────────────────────────────────────────────────────────────────
# HTTP HELPER
# ─────────────────────────────────────────────────────────────────────────────
def _http_get(url, timeout=12, extra_headers=None):
    """GET HTTP — requests si dispo, sinon urllib. Retourne body str."""
    hdrs = {"User-Agent": _UA, "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}
    if extra_headers:
        hdrs.update(extra_headers)
    if _HAS_REQ:
        resp = _req.get(url, timeout=timeout, headers=hdrs)
        resp.raise_for_status()
        return resp.text
    req = _urlreq.Request(url, headers=hdrs)
    with _urlreq.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _extract_domain(url):
    try:
        p = _urlparse.urlparse(url if url.startswith("http") else "https://" + url)
        return p.netloc.replace("www.", "")
    except Exception:
        return url


def _clean(text, max_len=200):
    return _html.escape(str(text or ""))[:max_len]


def _extract_keywords(text, top=15):
    words = re.findall(r'\b[A-Za-zÀ-ÖØ-öø-ÿ]{4,}\b', text.lower())
    freq = {}
    for w in words:
        if w not in _STOP_FR and len(w) > 3:
            freq[w] = freq.get(w, 0) + 1
    return sorted(freq, key=lambda k: -freq[k])[:top]


# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCHERS — tous cachés
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=900)   # 15 min
def scrape_url(url):
    """Lit une URL via Jina.ai Reader (+ fallback BS4). Retourne dict structuré."""
    if not url or not url.startswith("http"):
        return {"error": "URL invalide", "url": url}
    try:
        text = _http_get(
            f"https://r.jina.ai/{url}",
            timeout=15,
            extra_headers={"Accept": "text/plain"},
        )
        lines = text.split("\n")

        def meta(prefix):
            return next(
                (l.replace(prefix, "").strip() for l in lines if l.startswith(prefix)), ""
            )

        skip = {"Title:", "URL:", "Description:", "Published", "Warning", "Markdown", "Links"}
        body = [l for l in lines if not any(l.startswith(s) for s in skip)]

        h1 = [l.lstrip("# ").strip() for l in body if l.startswith("# ") and 3 < len(l) < 160][:5]
        h2 = [l.lstrip("## ").strip() for l in body if l.startswith("## ") and 3 < len(l) < 160][:12]
        h3 = [l.lstrip("### ").strip() for l in body if l.startswith("### ") and 3 < len(l) < 120][:8]
        paras = [l for l in body if l and not l.startswith("#") and len(l) > 35]
        main_text = " ".join(paras)[:3500]

        return {
            "title": meta("Title:"),
            "description": meta("Description:"),
            "url": url,
            "h1": h1, "h2": h2, "h3": h3,
            "paragraphs": paras[:10],
            "main_text": main_text,
            "keywords": _extract_keywords(main_text),
            "source": "jina",
            "fetched_at": datetime.datetime.now().strftime("%H:%M · %d/%m/%Y"),
        }
    except Exception as e_jina:
        # Fallback BeautifulSoup
        if _HAS_BS4 and _HAS_REQ:
            try:
                r = _req.get(url, timeout=10, headers={"User-Agent": _UA})
                soup = _BS(r.text, "html.parser")
                title = soup.title.string.strip() if soup.title else ""
                desc = ""
                for m in soup.find_all("meta"):
                    n = m.get("name", m.get("property", "")).lower()
                    if n in ("description", "og:description"):
                        desc = m.get("content", "")
                        break
                h1 = [t.get_text(strip=True) for t in soup.find_all("h1")][:5]
                h2 = [t.get_text(strip=True) for t in soup.find_all("h2")][:10]
                paras = [t.get_text(strip=True) for t in soup.find_all("p")
                         if len(t.get_text(strip=True)) > 40][:10]
                main_text = " ".join(paras)[:2500]
                return {
                    "title": title, "description": desc, "url": url,
                    "h1": h1, "h2": h2, "h3": [],
                    "paragraphs": paras[:8],
                    "main_text": main_text,
                    "keywords": _extract_keywords(main_text),
                    "source": "bs4",
                    "fetched_at": datetime.datetime.now().strftime("%H:%M · %d/%m/%Y"),
                }
            except Exception:
                pass
        return {"error": str(e_jina), "url": url}


@st.cache_data(ttl=1800)  # 30 min
def fetch_news(query, lang="fr", max_items=12):
    """Google News RSS — gratuit, sans clé API."""
    try:
        encoded = _urlparse.quote(query)
        rss_url = (
            f"https://news.google.com/rss/search"
            f"?q={encoded}&hl={lang}&gl=FR&ceid=FR:{lang}"
        )
        text = _http_get(rss_url, timeout=12)
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
                "link": item.findtext("link", ""),
                "pub": pub_fmt,
                "source": src_tag.text if src_tag is not None else "",
            })
        return items
    except Exception as e:
        return [{"title": f"Erreur chargement : {e}", "link": "", "pub": "", "source": ""}]


@st.cache_data(ttl=3600)  # 1h
def fetch_ddg(query):
    """DuckDuckGo Instant Answer API."""
    try:
        encoded = _urlparse.quote(query)
        text = _http_get(
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


@st.cache_data(ttl=3600)
def fetch_wiki(topic, lang="fr"):
    """Wikipedia REST API — résumé d'un sujet."""
    try:
        encoded = _urlparse.quote(topic)
        text = _http_get(
            f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}",
            timeout=8,
        )
        d = json.loads(text)
        return {
            "title": d.get("title", ""),
            "description": d.get("description", ""),
            "extract": d.get("extract", ""),
            "url": d.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    except Exception:
        return {}


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 14px">
      <div style="font-size:1.3rem;font-weight:800;letter-spacing:-.8px;line-height:1">
        <span style="color:#0F172A">BIZI</span><span style="color:#D97706">VEILLE</span>
      </div>
      <div style="font-size:.62rem;color:#8A8A8A;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-top:4px">
        Intelligence stratégique · Live
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="step-label"><span class="step-num">1</span>Secteur / marché</div>',
                unsafe_allow_html=True)
    secteur = st.text_input(
        "Secteur", placeholder="ex : CRM SaaS, e-commerce mode…",
        label_visibility="collapsed", key="sb_secteur"
    )

    st.markdown('<div class="step-label"><span class="step-num">2</span>Mots-clés veille</div>',
                unsafe_allow_html=True)
    st.caption("Un mot-clé par ligne")
    kw_raw = st.text_area(
        "Mots-clés", placeholder="intelligence artificielle\nstartup\nautomation",
        height=100, label_visibility="collapsed", key="sb_kw"
    )
    keywords_list = [k.strip() for k in kw_raw.strip().split("\n") if k.strip()]

    st.divider()
    st.markdown('<div class="step-label"><span class="step-num">3</span>URLs concurrentes</div>',
                unsafe_allow_html=True)
    st.caption("Jusqu'à 5 — analysées en parallèle")
    comp_urls_raw = []
    for i in range(5):
        u = st.text_input(
            f"Concurrent {i+1}", placeholder=f"https://concurrent{i+1}.fr",
            label_visibility="collapsed", key=f"sb_comp_{i}"
        )
        if u.strip():
            comp_urls_raw.append(u.strip())

    st.divider()
    lang = st.selectbox(
        "Langue actualités", ["fr", "en", "es", "de"],
        index=0, key="sb_lang"
    )
    max_news = st.slider("Actualités par requête", 5, 20, 10, key="sb_max_news")

    st.divider()
    if st.button("Lancer la veille", type="primary", use_container_width=True):
        st.session_state["_vrun"] = True
        st.session_state["_vts"] = datetime.datetime.now().strftime("%H:%M:%S")

    if st.session_state.get("_vrun") and st.button("Réinitialiser", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("_v"):
                del st.session_state[k]
        st.rerun()

    run = st.session_state.get("_vrun", False)

    if run:
        ts = st.session_state.get("_vts", "")
        st.markdown(f"""
        <div class="badge-live" style="margin-top:10px;justify-content:center">
          <div class="pulse"></div>
          Veille active · {ts}
        </div>
        """, unsafe_allow_html=True)

    st.caption("Cache 15 min (URLs) · 30 min (news) · 1h (DDG/Wiki)")

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bizi-header">
  <div>
    <div style="display:flex;gap:0">
      <span class="logo-bizi">BIZI</span><span class="logo-app">VEILLE</span>
    </div>
    <div class="header-sub">Intelligence Stratégique &amp; Concurrentielle · Données live</div>
  </div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:12px">
    <div class="badge-live"><div class="pulse"></div>Connecté · APIs actives</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LANDING (pre-run)
# ─────────────────────────────────────────────────────────────────────────────
if not run:
    st.markdown("""
    <div style="text-align:center;padding:36px 0 28px">
      <div style="font-size:1.75rem;font-weight:800;color:#0F172A;margin-bottom:8px;letter-spacing:-.5px">
        Votre radar stratégique permanent
      </div>
      <div style="font-size:.95rem;color:#6B7280;max-width:580px;margin:0 auto;line-height:1.6">
        Analysez vos concurrents en temps réel, suivez les actualités de votre marché
        et détectez les opportunités — sans clé API, sans abonnement.
      </div>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("Lecture URL live",
         "Jina.ai Reader extrait titres, structure, mots-clés et contenu de n'importe quelle page en quelques secondes."),
        ("Veille concurrentielle",
         "Analysez jusqu'à 5 concurrents simultanément : positionnement, architecture éditoriale, thématiques clés."),
        ("Actualités marché",
         "Google News RSS en temps réel par secteur, mots-clés et nom de concurrent. Détection des signaux faibles."),
        ("Signaux stratégiques",
         "Wikipedia + DuckDuckGo pour contextualiser votre marché, identifier tendances et opportunités SWOT."),
        ("SWOT automatique",
         "Détection automatique d'opportunités et menaces dans le flux d'actualités via analyse sémantique."),
        ("Export JSON",
         "Téléchargez l'intégralité des données collectées : URLs, news, concurrents, mots-clés."),
    ]

    cols = st.columns(3)
    for i, (title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feat-card">
              <div style="font-weight:700;font-size:.9rem;color:#0F172A;margin-bottom:6px">{title}</div>
              <div style="font-size:.8rem;color:#6B7280;line-height:1.55">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.info("Remplissez le formulaire dans la barre latérale puis cliquez sur **Lancer la veille**")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# COMPUTED VARS
# ─────────────────────────────────────────────────────────────────────────────
comp_urls = [
    (u if u.startswith("http") else "https://" + u)
    for u in comp_urls_raw
]
main_query = secteur or (keywords_list[0] if keywords_list else "stratégie digitale")
all_queries = []
if secteur:
    all_queries.append(("Secteur", secteur))
for kw in keywords_list[:4]:
    all_queries.append(("Mot-clé", kw))
for url in comp_urls[:2]:
    all_queries.append(("Concurrent", _extract_domain(url)))
if not all_queries:
    all_queries = [("Veille", "stratégie digitale")]

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Analyse URL",
    "Veille Concurrentielle",
    "Actualités Marché",
    "Signaux Stratégiques",
    "Export",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — ANALYSE URL EN DIRECT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-h">Analyse URL en temps réel</div>', unsafe_allow_html=True)

    col_url, col_btn = st.columns([4, 1])
    with col_url:
        live_url = st.text_input(
            "URL", placeholder="https://monsite.fr ou https://concurrent.fr/page",
            label_visibility="collapsed", key="tab_url"
        )
    with col_btn:
        do_analyze = st.button("Analyser", type="primary", use_container_width=True)

    target = live_url.strip()
    if target:
        if not target.startswith("http"):
            target = "https://" + target

        with st.spinner(f"Lecture de {_extract_domain(target)} via Jina.ai…"):
            d = scrape_url(target)

        if "error" in d and not d.get("title"):
            st.error(f"Impossible d'analyser cette URL — {_clean(d.get('error',''), 150)}")
        else:
            # ── Header card ──────────────────────────────────────────────────
            src_label = {"jina": "Jina.ai Reader", "bs4": "BeautifulSoup"}.get(
                d.get("source", ""), d.get("source", "")
            )
            st.markdown(f"""
            <div class="card-dark">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap">
                <div style="flex:1;min-width:0">
                  <div style="font-size:.62rem;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px">
                    {_clean(_extract_domain(target), 60)}
                  </div>
                  <div style="font-size:1.15rem;font-weight:700;color:white;margin-bottom:8px;line-height:1.3">
                    {_clean(d.get('title','—'), 130)}
                  </div>
                  <div style="font-size:.83rem;color:rgba(255,255,255,.65);line-height:1.55">
                    {_clean(d.get('description',''), 280)}
                  </div>
                </div>
                <div style="text-align:right;flex-shrink:0;font-size:.63rem;color:rgba(255,255,255,.35);line-height:1.7">
                  Source : {src_label}<br>
                  {d.get('fetched_at','')}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── KPIs ─────────────────────────────────────────────────────────
            kc1, kc2, kc3, kc4 = st.columns(4)
            kc1.metric("Titres H1", len(d.get("h1", [])))
            kc2.metric("Titres H2", len(d.get("h2", [])))
            kc3.metric("Paragraphes", len(d.get("paragraphs", [])))
            kc4.metric("Mots-clés", len(d.get("keywords", [])))

            # ── Keywords ─────────────────────────────────────────────────────
            kws = d.get("keywords", [])
            if kws:
                st.markdown('<div class="section-h">Mots-clés détectés</div>', unsafe_allow_html=True)
                kw_html = "".join(
                    f'<span class="kw-tag">{_clean(k)}</span>' for k in kws
                )
                st.markdown(f'<div style="margin-bottom:4px">{kw_html}</div>',
                            unsafe_allow_html=True)

            # ── Structure + Contenu ───────────────────────────────────────────
            col_left, col_right = st.columns(2)
            with col_left:
                if d.get("h1"):
                    st.markdown('<div class="section-h">Structure H1</div>', unsafe_allow_html=True)
                    for h in d["h1"]:
                        st.markdown(
                            f'<div class="card" style="padding:10px 14px;font-weight:600;'
                            f'font-size:.87rem;margin-bottom:8px">{_clean(h, 110)}</div>',
                            unsafe_allow_html=True,
                        )
                if d.get("h2"):
                    st.markdown('<div class="section-h">Structure H2</div>', unsafe_allow_html=True)
                    for h in d["h2"][:8]:
                        st.markdown(
                            f'<div style="padding:6px 12px;border-left:2px solid var(--ambre);'
                            f'margin-bottom:6px;font-size:.83rem;color:#374151">{_clean(h, 110)}</div>',
                            unsafe_allow_html=True,
                        )

            with col_right:
                if d.get("paragraphs"):
                    st.markdown('<div class="section-h">Contenu principal</div>', unsafe_allow_html=True)
                    for p in d["paragraphs"][:6]:
                        st.markdown(
                            f'<div style="font-size:.82rem;color:#4B5563;line-height:1.6;'
                            f'padding:8px 0;border-bottom:1px solid #F3F4F6">'
                            f'{_clean(p, 320)}</div>',
                            unsafe_allow_html=True,
                        )

            # ── H3 ───────────────────────────────────────────────────────────
            if d.get("h3"):
                st.markdown('<div class="section-h">Sous-rubriques H3</div>', unsafe_allow_html=True)
                cols_h3 = st.columns(3)
                for i, h in enumerate(d["h3"]):
                    with cols_h3[i % 3]:
                        st.markdown(
                            f'<div class="card-amber" style="padding:8px 12px;'
                            f'font-size:.8rem;font-weight:500">{_clean(h, 90)}</div>',
                            unsafe_allow_html=True,
                        )
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:30px">
          <div style="font-size:.95rem;font-weight:600;color:#374151;margin-bottom:8px">
            Entrez une URL pour lancer l'analyse
          </div>
          <div style="font-size:.8rem;color:#9CA3AF">
            Fonctionne avec n'importe quelle page publique ·
            Articles · Sites concurrents · Pages produit · Landing pages
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VEILLE CONCURRENTIELLE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-h">Analyse multi-concurrents</div>', unsafe_allow_html=True)

    if not comp_urls:
        st.info("Ajoutez jusqu'à 5 URLs concurrentes dans la barre latérale pour lancer la comparaison")
    else:
        with st.spinner(f"Analyse de {len(comp_urls)} concurrent(s)…"):
            comp_results = {url: scrape_url(url) for url in comp_urls}

        st.success(f"{len(comp_results)} concurrent(s) analysé(s) · Cache 15 min")

        # ── Cards grid ───────────────────────────────────────────────────────
        ncols = min(len(comp_urls), 3)
        grid_cols = st.columns(ncols)

        for i, (url, d) in enumerate(comp_results.items()):
            with grid_cols[i % ncols]:
                domain = _extract_domain(url)
                has_err = "error" in d and not d.get("title")
                if has_err:
                    st.markdown(f"""
                    <div class="card-red" style="min-height:160px">
                      <div class="comp-url">{domain}</div>
                      <div style="font-weight:700;color:#991B1B;font-size:.9rem;margin:6px 0">
                        Site inaccessible
                      </div>
                      <div style="font-size:.76rem;color:#B91C1C">
                        {_clean(d.get('error','Erreur inconnue'), 100)}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    kw_html = "".join(
                        f'<span class="kw-tag">{_clean(k)}</span>'
                        for k in d.get("keywords", [])[:6]
                    ) or '<span style="color:#9CA3AF;font-size:.72rem">Aucun mot-clé</span>'
                    h_count = len(d.get("h1", [])) + len(d.get("h2", []))
                    st.markdown(f"""
                    <div class="comp-card">
                      <div class="comp-url">{domain}</div>
                      <div class="comp-title">{_clean(d.get('title','—'), 65)}</div>
                      <div style="font-size:.78rem;color:#6B7280;margin-bottom:10px;line-height:1.45">
                        {_clean(d.get('description',''), 160)}
                      </div>
                      <div style="margin-bottom:10px">{kw_html}</div>
                      <div style="font-size:.68rem;color:#9CA3AF">
                        {h_count} titres · {len(d.get('paragraphs',[]))} paragraphes
                        · {d.get('source','?')}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

        # ── Comparison table ─────────────────────────────────────────────────
        st.markdown('<div class="section-h">Tableau comparatif</div>', unsafe_allow_html=True)
        rows = []
        for url, d in comp_results.items():
            rows.append({
                "Domaine": _extract_domain(url),
                "Titre": (d.get("title") or "—")[:65],
                "Description": (d.get("description") or "—")[:110],
                "H1 principal": (d.get("h1") or ["—"])[0][:60],
                "Top mots-clés": " · ".join((d.get("keywords") or [])[:4]) or "—",
                "H2 count": len(d.get("h2", [])),
            })
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)

        # ── Deep dive ────────────────────────────────────────────────────────
        st.markdown('<div class="section-h">Analyse éditoriale détaillée</div>', unsafe_allow_html=True)
        for i, (url, d) in enumerate(comp_results.items()):
            domain = _extract_domain(url)
            with st.expander(f"**{domain}** — structure & contenu complet", expanded=(i == 0)):
                if d.get("h2"):
                    st.markdown("**Architecture éditoriale (H2)**")
                    for h in d["h2"][:10]:
                        st.markdown(f"- {_clean(h, 130)}")

                if d.get("main_text"):
                    st.markdown("**Extrait du contenu**")
                    st.markdown(
                        f'<div style="font-size:.82rem;color:#4B5563;line-height:1.65;'
                        f'background:#F9FAFB;padding:14px;border-radius:8px;'
                        f'border-left:3px solid var(--ambre)">'
                        f'{_clean(d["main_text"], 900)}</div>',
                        unsafe_allow_html=True,
                    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ACTUALITÉS MARCHÉ
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-h">Flux d\'actualités en temps réel</div>', unsafe_allow_html=True)

    if not all_queries:
        st.info("Définissez un secteur ou des mots-clés dans la barre latérale")
    else:
        for label, q in all_queries:
            badge = {
                "Secteur": "card-blue", "Mot-clé": "card-amber", "Concurrent": "card-green", "Veille": "card"
            }.get(label, "card")

            with st.expander(f"**{label}** · {q}", expanded=(label == all_queries[0][0])):
                with st.spinner(f"Chargement actualités « {q} »…"):
                    news = fetch_news(q, lang=lang, max_items=max_news)

                if not news:
                    st.warning("Aucune actualité trouvée")
                else:
                    for item in news:
                        title = _clean(item.get("title", ""), 130)
                        source = _clean(item.get("source", ""), 45)
                        pub = item.get("pub", "")
                        link = item.get("link", "")

                        src_html = f'<span class="news-source">{source}</span>' if source else ""
                        link_html = (
                            f' <a href="{link}" target="_blank" '
                            f'style="font-size:.68rem;color:#D97706;text-decoration:none">'
                            f'Lire &rarr;</a>'
                            if link else ""
                        )
                        st.markdown(f"""
                        <div class="news-item">
                          <div class="news-title">{title}{link_html}</div>
                          <div class="news-meta">{src_html}{pub}</div>
                        </div>
                        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SIGNAUX STRATÉGIQUES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-h">Contextualisation & signaux marché</div>', unsafe_allow_html=True)

    wiki_topic = secteur or (keywords_list[0] if keywords_list else "")

    if wiki_topic:
        col_wiki, col_ddg = st.columns(2)

        with col_wiki:
            st.markdown('<div class="section-h">Contexte Wikipedia</div>', unsafe_allow_html=True)
            with st.spinner("Wikipedia…"):
                wiki = fetch_wiki(wiki_topic, lang=lang)
            if wiki.get("extract"):
                url_html = (
                    f'<div style="margin-top:10px">'
                    f'<a href="{wiki["url"]}" target="_blank" '
                    f'style="font-size:.72rem;color:#D97706;text-decoration:none">'
                    f'Lire sur Wikipedia &rarr;</a></div>'
                    if wiki.get("url") else ""
                )
                st.markdown(f"""
                <div class="card">
                  <div style="font-weight:700;font-size:.95rem;color:#0F172A;margin-bottom:8px">
                    {_clean(wiki.get('title',''), 80)}
                  </div>
                  <div style="font-size:.62rem;color:var(--muted);margin-bottom:8px;text-transform:uppercase;font-weight:600">
                    {_clean(wiki.get('description',''), 80)}
                  </div>
                  <div style="font-size:.82rem;color:#4B5563;line-height:1.65">
                    {_clean(wiki.get('extract',''), 700)}
                  </div>
                  {url_html}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"Aucun article Wikipedia pour « {wiki_topic} »")

        with col_ddg:
            st.markdown('<div class="section-h">Intelligence DuckDuckGo</div>', unsafe_allow_html=True)
            with st.spinner("DuckDuckGo…"):
                ddg = fetch_ddg(wiki_topic)
            if ddg.get("abstract"):
                src_html = (
                    f'<div style="margin-top:8px;font-size:.7rem;color:#92400E">'
                    f'Source : {_clean(ddg["source"], 40)}</div>'
                    if ddg.get("source") else ""
                )
                st.markdown(f"""
                <div class="card-amber">
                  <div style="font-size:.83rem;color:#1F2937;line-height:1.65">
                    {_clean(ddg['abstract'], 550)}
                  </div>
                  {src_html}
                </div>
                """, unsafe_allow_html=True)
            if ddg.get("related"):
                st.markdown("**Sujets connexes détectés**")
                for topic in ddg["related"][:6]:
                    st.markdown(
                        f'<div style="font-size:.8rem;color:#374151;padding:5px 0;'
                        f'border-bottom:1px solid #F3F4F6">{_clean(topic, 160)}</div>',
                        unsafe_allow_html=True,
                    )
    else:
        st.info("Renseignez un secteur ou des mots-clés pour voir les signaux stratégiques")

    # ── SWOT live depuis les actualités ──────────────────────────────────────
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">SWOT marché — détection automatique</div>',
                unsafe_allow_html=True)
    st.caption("Analyse sémantique des actualités pour détecter opportunités et menaces")

    opp_signals = [
        "croissance","opportunité","innovation","lancement","expansion","partenariat",
        "financement","levée de fonds","hausse","record","investissement","nouveau marché",
        "acquisition","fusion","tendance","boom","accélération",
    ]
    threat_signals = [
        "crise","risque","baisse","pénurie","réglementation","sanction","fraude",
        "concurrent","guerre","litige","récession","inflation","perte","fermeture",
        "licenciement","effondrement","chute","plainte","amende",
    ]

    scan_query = main_query + " marché"
    with st.spinner("Analyse des signaux dans les actualités…"):
        all_news = fetch_news(scan_query, lang=lang, max_items=25)

    opps = [n for n in all_news
            if any(s in n.get("title", "").lower() for s in opp_signals)]
    threats = [n for n in all_news
               if any(s in n.get("title", "").lower() for s in threat_signals)]

    col_o, col_t = st.columns(2)
    with col_o:
        st.markdown(
            f'<div style="font-weight:700;font-size:.88rem;color:#065F46;margin-bottom:10px">'
            f'Opportunités ({len(opps)})</div>',
            unsafe_allow_html=True,
        )
        if opps:
            for n in opps[:6]:
                st.markdown(
                    f'<div class="card-green" style="padding:9px 13px;margin-bottom:7px;'
                    f'font-size:.8rem;line-height:1.4">'
                    f'{_clean(n.get("title",""), 130)}'
                    f'<div style="font-size:.68rem;color:#059669;margin-top:3px">'
                    f'{n.get("pub","")}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="font-size:.82rem;color:#9CA3AF">'
                'Aucune opportunité détectée dans les actualités récentes</div>',
                unsafe_allow_html=True,
            )

    with col_t:
        st.markdown(
            f'<div style="font-weight:700;font-size:.88rem;color:#991B1B;margin-bottom:10px">'
            f'Menaces ({len(threats)})</div>',
            unsafe_allow_html=True,
        )
        if threats:
            for n in threats[:6]:
                st.markdown(
                    f'<div class="card-red" style="padding:9px 13px;margin-bottom:7px;'
                    f'font-size:.8rem;line-height:1.4">'
                    f'{_clean(n.get("title",""), 130)}'
                    f'<div style="font-size:.68rem;color:#DC2626;margin-top:3px">'
                    f'{n.get("pub","")}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="font-size:.82rem;color:#9CA3AF">'
                'Aucune menace détectée dans les actualités récentes</div>',
                unsafe_allow_html=True,
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-h">Export du rapport de veille</div>', unsafe_allow_html=True)

    # Build export
    export = {
        "metadata": {
            "app": "BiziVeille v1.0",
            "secteur": secteur,
            "keywords": keywords_list,
            "competitors": [_extract_domain(u) for u in comp_urls],
            "lang": lang,
            "generated_at": datetime.datetime.now().isoformat(),
        },
        "news": {},
        "competitors": {},
        "signals": {},
    }

    for label, q in all_queries:
        export["news"][f"{label}_{q}"] = fetch_news(q, lang=lang, max_items=15)

    for url in comp_urls:
        dom = _extract_domain(url)
        d = comp_results.get(url, scrape_url(url))
        export["competitors"][dom] = {
            "url": url,
            "title": d.get("title", ""),
            "description": d.get("description", ""),
            "keywords": d.get("keywords", []),
            "h1": d.get("h1", []),
            "h2": d.get("h2", []),
            "main_text": d.get("main_text", "")[:1000],
        }

    if wiki_topic:
        export["signals"]["wikipedia"] = fetch_wiki(wiki_topic, lang=lang)
        export["signals"]["duckduckgo"] = fetch_ddg(wiki_topic)

    export_str = json.dumps(export, ensure_ascii=False, indent=2)
    fname = f"veille_{secteur.replace(' ','_') if secteur else 'rapport'}_{datetime.date.today()}.json"

    # Summary card
    n_news = sum(len(v) for v in export["news"].values())
    st.markdown(f"""
    <div class="card-dark">
      <div style="font-size:1.05rem;font-weight:700;color:white;margin-bottom:14px">
        Rapport de veille complet
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;text-align:center">
        <div>
          <div style="font-size:1.6rem;font-weight:800;color:#FBBF24">{len(comp_urls)}</div>
          <div style="font-size:.68rem;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.05em">Concurrents</div>
        </div>
        <div>
          <div style="font-size:1.6rem;font-weight:800;color:#FBBF24">{n_news}</div>
          <div style="font-size:.68rem;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.05em">Actualités</div>
        </div>
        <div>
          <div style="font-size:1.6rem;font-weight:800;color:#FBBF24">{len(keywords_list)}</div>
          <div style="font-size:.68rem;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.05em">Mots-clés</div>
        </div>
        <div>
          <div style="font-size:1.6rem;font-weight:800;color:#FBBF24">{len(export_str)//1024} Ko</div>
          <div style="font-size:.68rem;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:.05em">Données</div>
        </div>
      </div>
      <div style="margin-top:14px;font-size:.7rem;color:rgba(255,255,255,.35)">
        Généré le {datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Télécharger le rapport JSON",
        data=export_str,
        file_name=fname,
        mime="application/json",
        use_container_width=True,
        type="primary",
    )

    st.markdown('<div class="section-h">Aperçu des métadonnées</div>', unsafe_allow_html=True)
    st.json(export["metadata"])
