"""
resources_module.py — Articles de blog live + Pages ressources Top 10
Données statiques enrichies + flux RSS gratuits sans clé
"""
import streamlit as st
import urllib.request as _ur
import xml.etree.ElementTree as _ET
import urllib.parse as _up
import re as _re

# ── Articles blog live via Google News RSS (sans clé) ────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_blog_articles(topics: list = None) -> list:
    """Récupère les meilleurs articles récents sur la stratégie d'entreprise."""
    if topics is None:
        topics = ["stratégie commerciale TPE", "marketing digital PME", 
                  "SEO 2025 France", "growth hacking startup"]
    articles = []
    for topic in topics[:3]:
        url = f"https://news.google.com/rss/search?q={_up.quote(topic)}&hl=fr&gl=FR&ceid=FR:fr"
        try:
            req = _ur.Request(url, headers={"User-Agent": "BiziApp/3.2"})
            with _ur.urlopen(req, timeout=5) as r:
                root = _ET.fromstring(r.read())
            for item in root.findall(".//item")[:4]:
                title = (item.findtext("title") or "").strip()
                link  = (item.findtext("link") or "").strip()
                date  = (item.findtext("pubDate") or "")[:16]
                desc  = _re.sub(r'<[^>]+>', '', item.findtext("description") or "")[:200]
                src   = (item.findtext("source") or "Google News").strip()
                if title and link and not any(a["link"] == link for a in articles):
                    articles.append({"title": title, "link": link, 
                                     "date": date, "description": desc,
                                     "source": src, "topic": topic})
        except Exception:
            pass
    return articles[:16]


# ── Données Top 10 statiques (mises à jour périodiquement) ───────────────────

TOP10_VEILLE = [
    {"rank": 1, "name": "Google Alerts", "url": "https://www.google.fr/alerts",
     "desc": "Alertes email automatiques sur n'importe quel mot-clé. Le must absolu, gratuit et illimité.",
     "free": True, "tags": ["Email", "Gratuit", "Alertes"]},
    {"rank": 2, "name": "Feedly", "url": "https://feedly.com",
     "desc": "Agrégateur RSS puissant. Suivez des centaines de sources en un seul endroit. Plan gratuit généreux.",
     "free": True, "tags": ["RSS", "Gratuit", "Veille contenu"]},
    {"rank": 3, "name": "Mention Free", "url": "https://mention.com",
     "desc": "Monitoring mentions de marque sur le web et réseaux sociaux. 1 alerte gratuite.",
     "free": "Freemium", "tags": ["Social", "Marque", "Freemium"]},
    {"rank": 4, "name": "Reddit (search)", "url": "https://www.reddit.com/search",
     "desc": "Trouver des discussions sur votre secteur. Filtre 'New' pour veille en temps réel.",
     "free": True, "tags": ["Community", "Discussions", "Gratuit"]},
    {"rank": 5, "name": "Twitter/X Search", "url": "https://twitter.com/explore",
     "desc": "Recherche avancée par mot-clé, hashtag, compte. Veille temps réel incomparable.",
     "free": True, "tags": ["Social", "Temps réel", "Gratuit"]},
    {"rank": 6, "name": "HackerNews", "url": "https://news.ycombinator.com",
     "desc": "La référence tech mondiale. Indispensable pour suivre les tendances SaaS et startup.",
     "free": True, "tags": ["Tech", "Startup", "Gratuit"]},
    {"rank": 7, "name": "Product Hunt", "url": "https://www.producthunt.com",
     "desc": "Tous les nouveaux produits tech lancés chaque jour. Veille concurrentielle SaaS.",
     "free": True, "tags": ["SaaS", "Produits", "Tendances"]},
    {"rank": 8, "name": "Talkwalker Alerts", "url": "https://www.talkwalker.com/alerts",
     "desc": "Alternative Google Alerts plus puissante. Couverture web + social. Gratuit.",
     "free": True, "tags": ["Alertes", "Social", "Gratuit"]},
    {"rank": 9, "name": "BuzzSumo Free", "url": "https://buzzsumo.com",
     "desc": "Top contenus partagés par sujet. Identifier les tendances editoriales de votre secteur.",
     "free": "Freemium", "tags": ["Contenu", "Viral", "Freemium"]},
    {"rank": 10, "name": "DEV.to", "url": "https://dev.to",
     "desc": "Articles tech publiés quotidiennement. API publique gratuite pour automatiser la veille.",
     "free": True, "tags": ["Tech", "API", "Gratuit"]},
]

TOP10_SEO = [
    {"rank": 1, "name": "Google Search Console", "url": "https://search.google.com/search-console",
     "desc": "L'outil officiel Google. Analyse vos performances SEO, erreurs d'indexation, mots-clés réels. 100% gratuit.",
     "free": True, "tags": ["Officiel Google", "Gratuit", "Essentiel"]},
    {"rank": 2, "name": "Ubersuggest (Neil Patel)", "url": "https://neilpatel.com/ubersuggest",
     "desc": "Volume de recherche, difficulté, suggestions. 3 recherches/jour gratuites. Interface simple.",
     "free": "Freemium", "tags": ["Mots-clés", "Freemium", "Facile"]},
    {"rank": 3, "name": "Answer The Public", "url": "https://answerthepublic.com",
     "desc": "Toutes les questions posées sur un sujet. Idéal pour créer du contenu qui répond aux vraies recherches.",
     "free": "Freemium", "tags": ["Questions", "Contenu", "Freemium"]},
    {"rank": 4, "name": "Google Trends", "url": "https://trends.google.fr",
     "desc": "Tendances de recherche dans le temps. Identifier les saisonnalités et mots-clés en hausse. Gratuit.",
     "free": True, "tags": ["Tendances", "Gratuit", "Temporel"]},
    {"rank": 5, "name": "Screaming Frog (free 500 URLs)", "url": "https://www.screamingfrog.co.uk/seo-spider",
     "desc": "Audit technique SEO de votre site. Erreurs 404, balises, redirections. Gratuit jusqu'à 500 URLs.",
     "free": "Freemium", "tags": ["Audit", "Technique", "Freemium"]},
    {"rank": 6, "name": "Yoast SEO (WordPress)", "url": "https://yoast.com",
     "desc": "Plugin WordPress le plus utilisé. Optimise chaque page en temps réel. Version gratuite très complète.",
     "free": "Freemium", "tags": ["WordPress", "On-page", "Plugin"]},
    {"rank": 7, "name": "Moz Link Explorer", "url": "https://moz.com/link-explorer",
     "desc": "Analyser les backlinks. 10 requêtes/mois gratuites. DA (Domain Authority) de vos concurrents.",
     "free": "Freemium", "tags": ["Backlinks", "Freemium", "Autorité"]},
    {"rank": 8, "name": "Keyword Surfer (extension)", "url": "https://surferseo.com/keyword-surfer-extension",
     "desc": "Extension Chrome gratuite. Volume de recherche directement dans Google. Simple et efficace.",
     "free": True, "tags": ["Extension", "Chrome", "Gratuit"]},
    {"rank": 9, "name": "Google PageSpeed Insights", "url": "https://pagespeed.web.dev",
     "desc": "Performance technique de votre site (Core Web Vitals). Crucial pour le référencement Google. Gratuit.",
     "free": True, "tags": ["Performance", "Core Web Vitals", "Gratuit"]},
    {"rank": 10, "name": "Rank Math (WordPress)", "url": "https://rankmath.com",
     "desc": "Alternative Yoast avec schema.org avancé. Version gratuite très puissante.",
     "free": "Freemium", "tags": ["WordPress", "Schema", "Plugin"]},
]

TOP10_MARKET_RESEARCH = [
    {"rank": 1, "name": "Statista (free data)", "url": "https://www.statista.com",
     "desc": "Base de données statistiques mondiale. Nombreux graphiques accessibles gratuitement.",
     "free": "Freemium", "tags": ["Stats", "Mondial", "Graphiques"]},
    {"rank": 2, "name": "INSEE.fr", "url": "https://www.insee.fr",
     "desc": "Institut National de la Statistique français. Données démographiques, économiques, sectorielles. Tout gratuit.",
     "free": True, "tags": ["France", "Officiel", "Gratuit"]},
    {"rank": 3, "name": "data.gouv.fr", "url": "https://www.data.gouv.fr",
     "desc": "Open data français. Des milliers de datasets sur tous les secteurs. Accès API gratuit.",
     "free": True, "tags": ["Open data", "France", "API Gratuit"]},
    {"rank": 4, "name": "Google Forms", "url": "https://docs.google.com/forms",
     "desc": "Créer des enquêtes de satisfaction gratuitement. Diffuser via email ou lien. Analyse automatique.",
     "free": True, "tags": ["Enquêtes", "Gratuit", "Facile"]},
    {"rank": 5, "name": "SurveyMonkey (free)", "url": "https://www.surveymonkey.com",
     "desc": "Enquêtes professionnelles. 10 questions / 100 réponses gratuitement. Templates sectoriels.",
     "free": "Freemium", "tags": ["Enquêtes", "Pro", "Freemium"]},
    {"rank": 6, "name": "Typeform", "url": "https://www.typeform.com",
     "desc": "Formulaires conversationnels à fort taux de completion. Interface UX remarquable. Plan gratuit.",
     "free": "Freemium", "tags": ["UX", "Enquêtes", "Freemium"]},
    {"rank": 7, "name": "Eurostat", "url": "https://ec.europa.eu/eurostat",
     "desc": "Statistiques officielles de l'Union Européenne. Données sectorielles, économiques, sociales. Gratuit.",
     "free": True, "tags": ["Europe", "Officiel", "Gratuit"]},
    {"rank": 8, "name": "Think With Google", "url": "https://www.thinkwithgoogle.com",
     "desc": "Insights consommateurs et tendances par secteur. Études et rapports gratuits Google.",
     "free": True, "tags": ["Google", "Insights", "Gratuit"]},
    {"rank": 9, "name": "Similarweb (free)", "url": "https://www.similarweb.com",
     "desc": "Trafic de n'importe quel site web concurrent. Canaux d'acquisition. 5 visites/mois gratuites.",
     "free": "Freemium", "tags": ["Concurrence", "Trafic", "Freemium"]},
    {"rank": 10, "name": "Pappers.fr", "url": "https://www.pappers.fr",
     "desc": "Données légales et financières sur toutes les entreprises françaises. API gratuite. Chiffre d'affaires, bilans.",
     "free": True, "tags": ["France", "Entreprises", "API Gratuit"]},
]

TOP10_LEAD_ACQUISITION = [
    {"rank": 1, "name": "LinkedIn Free (profil + contenu)", "url": "https://www.linkedin.com",
     "desc": "Profil optimisé + publication régulière = 80% des leads B2B. Gratuit. Le ROI le plus élevé.",
     "free": True, "tags": ["B2B", "Contenu", "Gratuit"]},
    {"rank": 2, "name": "Google My Business", "url": "https://business.google.com",
     "desc": "Fiche Google Business Profile. Apparaître dans les recherches locales. 100% gratuit, indispensable.",
     "free": True, "tags": ["Local", "Google", "Gratuit"]},
    {"rank": 3, "name": "Hunter.io (free 25/mois)", "url": "https://hunter.io",
     "desc": "Trouver les emails professionnels de n'importe quelle entreprise. 25 recherches/mois gratuites.",
     "free": "Freemium", "tags": ["Prospection", "Emails", "Freemium"]},
    {"rank": 4, "name": "Lemlist (trial)", "url": "https://www.lemlist.com",
     "desc": "Cold emailing automatisé avec personnalisation. Essai gratuit 14j. Meilleur taux d'ouverture.",
     "free": "Trial", "tags": ["Cold email", "Automation", "Trial"]},
    {"rank": 5, "name": "Notion (CRM DIY)", "url": "https://www.notion.so",
     "desc": "Créer un CRM simple gratuitement avec Notion. Templates disponibles. Parfait pour démarrer.",
     "free": True, "tags": ["CRM", "DIY", "Gratuit"]},
    {"rank": 6, "name": "HubSpot CRM Free", "url": "https://www.hubspot.fr/products/crm",
     "desc": "CRM professionnel gratuit. Contacts illimités, pipeline de vente, emails. Le meilleur CRM gratuit.",
     "free": True, "tags": ["CRM", "Pro", "Gratuit"]},
    {"rank": 7, "name": "Calendly Free", "url": "https://calendly.com",
     "desc": "Prise de RDV automatique. Lien à partager, le prospect choisit son créneau. 1 lien gratuit.",
     "free": "Freemium", "tags": ["RDV", "Automatisation", "Freemium"]},
    {"rank": 8, "name": "Canva (visuels lead gen)", "url": "https://www.canva.com",
     "desc": "Créer des lead magnets (ebooks, checklists, guides) pour capturer des emails. Gratuit.",
     "free": "Freemium", "tags": ["Lead magnet", "Design", "Freemium"]},
    {"rank": 9, "name": "Beehiiv (newsletter)", "url": "https://www.beehiiv.com",
     "desc": "Créer une newsletter gratuite jusqu'à 2500 abonnés. Monétisation intégrée. Meilleure alternative Mailchimp.",
     "free": "Freemium", "tags": ["Newsletter", "Email", "Freemium"]},
    {"rank": 10, "name": "Typeform + Zapier", "url": "https://zapier.com",
     "desc": "Formulaire de capture → CRM automatique via Zapier (100 tasks/mois gratuit). Automatisation no-code.",
     "free": "Freemium", "tags": ["Automation", "No-code", "Freemium"]},
]

TOP10_COMMUNICATION = [
    {"rank": 1, "name": "Canva", "url": "https://www.canva.com",
     "desc": "Design graphique accessible à tous. Templates pour réseaux sociaux, présentations, flyers. Gratuit.",
     "free": "Freemium", "tags": ["Design", "Réseaux sociaux", "Gratuit"]},
    {"rank": 2, "name": "Buffer Free", "url": "https://buffer.com",
     "desc": "Planifier vos publications sur 3 réseaux sociaux gratuitement. 10 posts en attente max.",
     "free": "Freemium", "tags": ["Social media", "Planification", "Freemium"]},
    {"rank": 3, "name": "Notion (gestion éditoriale)", "url": "https://www.notion.so",
     "desc": "Calendrier éditorial, brief contenu, tracking publications. Templates gratuits disponibles.",
     "free": True, "tags": ["Calendrier", "Gestion", "Gratuit"]},
    {"rank": 4, "name": "CapCut", "url": "https://www.capcut.com",
     "desc": "Montage vidéo mobile et desktop. Sous-titres auto, effets, templates Reels/TikTok. Gratuit.",
     "free": True, "tags": ["Vidéo", "Reels", "TikTok"]},
    {"rank": 5, "name": "Mailchimp Free", "url": "https://mailchimp.com",
     "desc": "Email marketing jusqu'à 500 contacts et 1000 emails/mois gratuitement. Le plus simple.",
     "free": "Freemium", "tags": ["Email", "Newsletter", "Freemium"]},
    {"rank": 6, "name": "Loom Free", "url": "https://www.loom.com",
     "desc": "Enregistrer des vidéos d'écran avec votre webcam. Parfait pour les présentations et le contenu.",
     "free": "Freemium", "tags": ["Vidéo", "Ecran", "Freemium"]},
    {"rank": 7, "name": "Google Slides", "url": "https://slides.google.com",
     "desc": "Présentations professionnelles gratuites. Collaboration temps réel. Export PowerPoint.",
     "free": True, "tags": ["Présentation", "Collaboration", "Gratuit"]},
    {"rank": 8, "name": "Anchor (Spotify for Podcasters)", "url": "https://podcasters.spotify.com",
     "desc": "Créer, héberger et distribuer un podcast gratuitement sur toutes les plateformes.",
     "free": True, "tags": ["Podcast", "Distribution", "Gratuit"]},
    {"rank": 9, "name": "Pablo by Buffer", "url": "https://pablo.buffer.com",
     "desc": "Créer des visuels pour les réseaux sociaux en 30 secondes. Simple, rapide, gratuit.",
     "free": True, "tags": ["Visuels rapides", "Social", "Gratuit"]},
    {"rank": 10, "name": "Trello Free", "url": "https://trello.com",
     "desc": "Gestion de projet Kanban. Idéal pour organiser votre stratégie de communication. Gratuit.",
     "free": True, "tags": ["Kanban", "Gestion", "Gratuit"]},
]


def render_top10_card(item: dict):
    """Rend une carte Top 10."""
    free_badge = {
        True: ("✅ Gratuit", "#267371", "#C6ECD9"),
        "Freemium": ("🔄 Freemium", "#393DAC", "#E4E9F6"),
        "Trial": ("⏱ Essai gratuit", "#B83D4B", "#F7EEF0"),
    }.get(item.get("free", True), ("✅ Gratuit", "#267371", "#C6ECD9"))

    tags_html = " ".join(
        f'<span style="background:#F2ECD9;color:#339999;border-radius:4px;padding:1px 7px;font-size:.66rem;font-weight:600">{t}</span>'
        for t in item.get("tags", [])
    )
    return f"""
<div class="ben-card" style="margin-bottom:10px;display:flex;gap:14px;align-items:flex-start">
  <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#44C1BA,#267371);
    display:flex;align-items:center;justify-content:center;color:white;font-weight:900;font-size:.9rem;flex-shrink:0">
    {item["rank"]}
  </div>
  <div style="flex:1;min-width:0">
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px">
      <a href="{item["url"]}" target="_blank" style="font-weight:800;font-size:.92rem;color:#0B2221;text-decoration:none">
        {item["name"]} ↗
      </a>
      <span style="background:{free_badge[2]};color:{free_badge[1]};border-radius:50px;padding:1px 9px;font-size:.66rem;font-weight:700">
        {free_badge[0]}
      </span>
    </div>
    <div style="font-size:.8rem;color:#339999;line-height:1.5;margin-bottom:5px">{item["desc"]}</div>
    <div>{tags_html}</div>
  </div>
</div>"""


def render_resources_page():
    """Page ressources complète."""
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B2221,#267371);color:white;
  border-radius:16px;padding:24px 28px;margin-bottom:24px">
  <div style="font-size:1.3rem;font-weight:900;margin-bottom:6px">📚 Ressources & Outils gratuits</div>
  <div style="opacity:.88;font-size:.88rem">
    Sélection des meilleurs outils gratuits par catégorie · Mis à jour régulièrement · 
    Aucune affiliation rémunérée
  </div>
</div>
""", unsafe_allow_html=True)

    # Articles blog live
    st.markdown('<div class="section-h">📰 Actualités stratégie & marketing — Live</div>', unsafe_allow_html=True)
    with st.spinner("Chargement des derniers articles..."):
        articles = fetch_blog_articles()
    
    if articles:
        art_cols = st.columns(2)
        for i, art in enumerate(articles[:8]):
            with art_cols[i % 2]:
                st.markdown(f"""
<div class="ben-card" style="margin-bottom:8px;padding:12px 14px">
  <div style="font-size:.64rem;color:#44C1BA;font-weight:700;text-transform:uppercase;margin-bottom:4px">{art.get("source","")} · {art.get("date","")}</div>
  <a href="{art["link"]}" target="_blank" style="font-weight:700;font-size:.84rem;color:#0B2221;text-decoration:none;line-height:1.35;display:block;margin-bottom:4px">
    {art["title"][:90]}{"..." if len(art["title"]) > 90 else ""} ↗
  </a>
  <div style="font-size:.74rem;color:#339999;line-height:1.4">{art.get("description","")[:120]}{"..." if len(art.get("description","")) > 120 else ""}</div>
</div>""", unsafe_allow_html=True)
    else:
        st.info("Articles en cours de chargement... Actualisez la page dans quelques secondes.")

    st.divider()

    # Top 10 sections
    sections = [
        ("🕵️ Top 10 outils de veille", TOP10_VEILLE),
        ("🔑 Top 10 outils SEO gratuits", TOP10_SEO),
        ("📊 Top 10 outils d'enquête de marché", TOP10_MARKET_RESEARCH),
        ("🎯 Top 10 outils d'acquisition de leads", TOP10_LEAD_ACQUISITION),
        ("📣 Top 10 outils de communication", TOP10_COMMUNICATION),
    ]

    for section_title, items in sections:
        with st.expander(section_title, expanded=False):
            for item in items:
                st.markdown(render_top10_card(item), unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
