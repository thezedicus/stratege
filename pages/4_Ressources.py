"""
pages/4_Ressources.py — Top 10 ressources gratuites par catégorie
Veille · SEO · Enquête de marché · Acquisition leads · Communication
"""
import streamlit as st

st.set_page_config(
    page_title="Top 10 Ressources Gratuites — BiziApp",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""<style>
:root{--teal:#44C1BA;--jade:#267371;--dark:#0B2221;--light:#F7FBF4;--card:#C6ECD9}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--light)}
.top-card{background:white;border-radius:14px;border:1.5px solid var(--card);padding:18px 20px;
  margin-bottom:12px;display:flex;align-items:flex-start;gap:14px;
  transition:box-shadow .2s,transform .2s}
.top-card:hover{box-shadow:0 6px 22px rgba(68,193,186,.14);transform:translateY(-1px);border-color:var(--teal)}
.rank-badge{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#44C1BA,#267371);
  color:white;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1rem;flex-shrink:0}
.rank-badge.gold{background:linear-gradient(135deg,#F59E0B,#D97706)}
.rank-badge.silver{background:linear-gradient(135deg,#9CA3AF,#6B7280)}
.rank-badge.bronze{background:linear-gradient(135deg,#CD7C2A,#A05C1C)}
.cat-header{background:linear-gradient(135deg,#0B2221,#267371);color:white;border-radius:14px;
  padding:20px 24px;margin:28px 0 16px}
.tool-name{font-weight:800;font-size:.95rem;color:#0B2221;margin-bottom:4px}
.tool-desc{font-size:.82rem;color:#339999;line-height:1.5;margin-bottom:6px}
.tool-why{font-size:.78rem;color:#267371;font-weight:600}
.free-badge{background:#C6ECD9;color:#267371;border-radius:50px;padding:2px 10px;font-size:.68rem;font-weight:700}
.pro-badge{background:#E4E9F6;color:#393DAC;border-radius:50px;padding:2px 10px;font-size:.68rem;font-weight:700}
</style>""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:32px 20px 24px">
  <h1 style="font-size:2rem;font-weight:900;color:#0B2221;margin-bottom:8px">🏆 Top 10 Ressources Gratuites</h1>
  <p style="color:#339999;font-size:1rem;max-width:600px;margin:0 auto">
    Sélection des meilleurs outils et sites pour développer votre business — 100% gratuit ou freemium
  </p>
</div>
""", unsafe_allow_html=True)

CATEGORIES = {
    "🔍 Top 10 Sites de Veille Stratégique": {
        "desc": "Surveiller votre marché, vos concurrents et les tendances sans payer",
        "color": "#267371",
        "tools": [
            ("Google Alerts","alerts.google.com","Alertes email gratuites sur n'importe quel mot-clé — incontournable","✅ Gratuit","🏆 Le must absolu pour surveiller son secteur"),
            ("Feedly","feedly.com","Agrégateur RSS qui centralise tous vos flux d'actualité en un lieu","✅ Gratuit","📰 Idéal pour lire 50 sources en 15 min/jour"),
            ("Twitter/X Listes","x.com","Créez des listes privées de concurrents et influenceurs à suivre","✅ Gratuit","🐦 Temps réel — parfait pour la veille instantanée"),
            ("Reddit","reddit.com","Communautés sectorielles ultra-actives — r/entrepreneur, r/marketing...","✅ Gratuit","💬 Ce que pense vraiment votre cible"),
            ("Product Hunt","producthunt.com","Découvrez les nouveaux outils SaaS et tendances tech chaque jour","✅ Gratuit","🚀 Veille innovation produit"),
            ("Similarweb (free)","similarweb.com","Trafic estimé de vos concurrents — données précieuses en version gratuite","⚡ Freemium","📊 Intelligence concurrentielle basique"),
            ("Mention (free)","mention.com","Surveille les mentions de votre marque sur le web et les réseaux","⚡ Freemium","🔔 Réputation & mentions brand"),
            ("SpyFu (free)","spyfu.com","Mots-clés et publicités de vos concurrents — 10 requêtes/jour gratuit","⚡ Freemium","🕵️ Espionnez les pubs concurrentes"),
            ("Talkwalker Alerts","talkwalker.com/alerts","Alternative gratuite à Google Alerts — meilleure couverture web","✅ Gratuit","🔔 Meilleure précision que Google Alerts"),
            ("HackerNews","news.ycombinator.com","Tech & startups — les tendances que le marché adoptera dans 2 ans","✅ Gratuit","💡 Signaux faibles tech et business"),
        ]
    },
    "🔑 Top 10 Outils SEO Gratuits": {
        "desc": "Améliorer votre référencement naturel sans débourser un centime",
        "color": "#393DAC",
        "tools": [
            ("Google Search Console","search.google.com/search-console","L'outil officiel Google pour suivre votre SEO — indispensable","✅ 100% Gratuit","🏆 Commencez ici — données officielles Google"),
            ("Google Keyword Planner","ads.google.com","Volumes de recherche officiels Google — accès via compte Google Ads","✅ Gratuit","📊 Source primaire pour les volumes"),
            ("Ubersuggest (free)","neilpatel.com/ubersuggest","Analyse SEO complète — 3 requêtes/jour gratuites","⚡ Freemium","🔍 Top pour débutants"),
            ("AnswerThePublic","answerthepublic.com","Questions que pose votre audience — or pour le contenu SEO","⚡ Freemium","❓ Générez des idées d'articles en 1 clic"),
            ("Screaming Frog (free)","screamingfrog.co.uk","Crawl technique de votre site — 500 URLs gratuites","⚡ Freemium","🕷️ Audit technique indispensable"),
            ("GTmetrix","gtmetrix.com","Vitesse de chargement — Core Web Vitals — essentiel SEO 2025","✅ Gratuit","⚡ Vitesse = classement Google"),
            ("PageSpeed Insights","pagespeed.web.dev","Score de performance officiel Google — mobile first","✅ Gratuit","📱 Optimisation mobile obligatoire"),
            ("Ahrefs Webmaster Tools","ahrefs.com/webmaster-tools","Backlinks et erreurs SEO de votre site — gratuit pour proprio","✅ Gratuit (proprio)","🔗 Analyse backlinks sans payer"),
            ("MozBar","moz.com/products/pro/seo-toolbar","Extension Chrome — DA/PA des pages en temps réel","✅ Gratuit","🔧 Extension Chrome utile quotidiennement"),
            ("Google Trends","trends.google.com","Tendances de recherche par pays et période — or pour le contenu","✅ 100% Gratuit","📈 Timing parfait pour votre contenu"),
        ]
    },
    "📊 Top 10 Sites pour Enquêtes de Marché": {
        "desc": "Comprendre votre marché et valider vos hypothèses sans budget études",
        "color": "#44C1BA",
        "tools": [
            ("Google Forms","forms.google.com","Créez des sondages illimités et collectez des réponses gratuitement","✅ 100% Gratuit","🏆 Le plus simple — parfait pour débuter"),
            ("Typeform (free)","typeform.com","Formulaires beaux et engageants — 10 réponses/mois gratuit","⚡ Freemium","🎨 Taux de complétion x2 vs formulaires classiques"),
            ("SurveyMonkey (free)","surveymonkey.fr","10 questions · 40 réponses — suffisant pour valider une idée","⚡ Freemium","📝 Référence mondiale de l'enquête en ligne"),
            ("INSEE data.gouv.fr","data.gouv.fr","Données socio-économiques France — officielles et gratuites","✅ Gratuit","🇫🇷 Données de marché France fiables"),
            ("Eurostat","ec.europa.eu/eurostat","Statistiques européennes officielles — marché EU sans frais","✅ Gratuit","🇪🇺 Indispensable pour expansion Europe"),
            ("Statista (free)","statista.com","Statistiques sectorielles — aperçus gratuits très utiles","⚡ Freemium","📊 Données consolidées par secteur"),
            ("Reddit","reddit.com","Posez vos questions directement à votre cible — réponses authentiques","✅ Gratuit","💬 Verbatims clients ultra-précieux"),
            ("Hotjar (free)","hotjar.com","Heatmaps et enregistrements — comprendre le comportement sur site","⚡ Freemium","🖱️ Voir ce que font vraiment vos visiteurs"),
            ("Google Consumer Surveys","surveys.google.com","Sondages ciblés — coût par réponse très faible","⚡ Payant abordable","🎯 Ciblage démographique précis"),
            ("LinkedIn Polls","linkedin.com","Sondages dans votre réseau pro — réponses qualifiées en 24h","✅ Gratuit","💼 Parfait pour B2B et consulting"),
        ]
    },
    "🎯 Top 10 Sites pour Acquisition de Leads": {
        "desc": "Générer des prospects qualifiés sans exploser votre budget marketing",
        "color": "#B83D4B",
        "tools": [
            ("LinkedIn (organique)","linkedin.com","Publication régulière + personal branding = leads entrants B2B","✅ Gratuit","🏆 Meilleur canal B2B en 2025 — ROI exceptionnel"),
            ("Google My Business","business.google.com","Référencement local gratuit — appels et visites qualifiés","✅ 100% Gratuit","📍 Incontournable pour tout business local"),
            ("Lemlist (free trial)","lemlist.com","Séquences email cold outreach — 14j gratuit + templates","⚡ Freemium","📧 Meilleur ROI du cold email automatisé"),
            ("Hunter.io (free)","hunter.io","Trouvez les emails pro de vos prospects — 25/mois gratuit","⚡ Freemium","🔍 Indispensable pour le cold outreach"),
            ("Calendly (free)","calendly.com","Booking en ligne — réduisez la friction à 0 pour vos RDV","✅ Gratuit","📅 +40% de RDV pris avec un lien Calendly"),
            ("Beehiiv / Substack","beehiiv.com","Newsletter gratuite — construisez votre liste email sans coût","✅ Gratuit","📬 Votre liste email = votre actif le plus précieux"),
            ("Product Hunt","producthunt.com","Lancement public — des milliers de leads qualifiés en 24h","✅ Gratuit","🚀 Launch = pic de leads qualitatifs"),
            ("Malt / Crème de la Crème","malt.fr","Plateformes freelance — leads entrants sans prospection","⚡ Commission","💼 Idéal pour valider son offre service"),
            ("Facebook Groups","facebook.com","Groupes sectoriels — apporter de la valeur = leads entrants","✅ Gratuit","👥 Communautés actives par niche"),
            ("Trustpilot / Avis Google","trustpilot.com","Les avis positifs génèrent des leads passifs automatiquement","⚡ Freemium","⭐ 93% des acheteurs lisent les avis avant d'acheter"),
        ]
    },
    "📣 Top 10 Outils pour une Meilleure Communication": {
        "desc": "Communiquer efficacement avec vos clients et prospects sans budget agence",
        "color": "#339999",
        "tools": [
            ("Canva","canva.com","Créez des visuels pro en minutes — bibliothèque de templates massive","✅ Gratuit","🏆 Le Photoshop du pauvre — mais vraiment puissant"),
            ("Buffer (free)","buffer.com","Planifiez vos posts sur 3 réseaux sociaux gratuitement","✅ Gratuit","📅 Publiez sans y penser tous les matins"),
            ("CapCut","capcut.com","Éditeur vidéo mobile — parfait pour Reels et TikTok","✅ Gratuit","🎬 Créez des vidéos pro depuis votre téléphone"),
            ("Notion","notion.so","Centralisez votre communication et stratégie éditoriale","✅ Gratuit","🗂️ Le cerveau de votre stratégie contenu"),
            ("Mailchimp (free)","mailchimp.com","500 contacts · 1000 emails/mois — parfait pour débuter l'emailing","✅ Gratuit","📧 L'outil email marketing de référence"),
            ("Loom","loom.com","Enregistrez des vidéos screen + webcam — parfait pour la prospection","✅ Gratuit","🎥 Les vidéos Loom convertissent 3x mieux que le texte"),
            ("ChatGPT (free)","chat.openai.com","IA pour rédiger emails, posts, scripts, articles à la volée","✅ Gratuit","🤖 Multipliez votre productivité rédactionnelle par 5"),
            ("Brevo (ex-Sendinblue)","brevo.com","300 emails/jour gratuits — outil email + SMS marketing complet","✅ Gratuit","📬 La meilleure alternative gratuite à Mailchimp"),
            ("Zoom (free)","zoom.us","Visioconférence 40 min · 100 participants — parfait pour les RDV","✅ Gratuit","📹 Standard de la visio professionnelle"),
            ("Google Workspace Gratuit","workspace.google.com","Gmail pro · Meet · Drive · Docs · Slides — suite complète gratuite","✅ Gratuit","🏢 La suite pro complète pour commencer"),
        ]
    },
}

# ── NAVIGATION ANCRÉE ─────────────────────────────────────────────────────────
cat_names = list(CATEGORIES.keys())
cols_nav = st.columns(len(cat_names))
for col, cat in zip(cols_nav, cat_names):
    with col:
        icon = cat.split()[0]
        st.markdown(f"""
<div style="text-align:center;background:white;border:1.5px solid #C6ECD9;border-radius:10px;
  padding:10px 6px;cursor:pointer;font-size:.76rem;font-weight:700;color:#267371">
  {icon}<br>{" ".join(cat.split()[2:4])}
</div>""", unsafe_allow_html=True)

# ── CONTENU ────────────────────────────────────────────────────────────────────
for cat_name, cat_data in CATEGORIES.items():
    st.markdown(f"""
<div class="cat-header">
  <h2 style="margin:0 0 6px;font-size:1.3rem;font-weight:900">{cat_name}</h2>
  <p style="margin:0;opacity:.88;font-size:.85rem">{cat_data["desc"]}</p>
</div>
""", unsafe_allow_html=True)

    for rank, (name, url, desc, free_label, why) in enumerate(cat_data["tools"], 1):
        rank_class = "gold" if rank == 1 else "silver" if rank == 2 else "bronze" if rank == 3 else ""
        badge_class = "free-badge" if "Gratuit" in free_label else "pro-badge"
        st.markdown(f"""
<div class="top-card">
  <div class="rank-badge {rank_class}">#{rank}</div>
  <div style="flex:1">
    <div class="tool-name">
      {name}
      <span class="{badge_class}" style="margin-left:8px">{free_label}</span>
    </div>
    <div class="tool-desc">{desc}</div>
    <div class="tool-why">💡 {why}</div>
    <a href="https://{url}" target="_blank" style="font-size:.72rem;color:#44C1BA;font-weight:700;
      text-decoration:none;display:inline-block;margin-top:6px">Accéder → {url}</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""---
<div style="text-align:center;padding:20px;font-size:.8rem;color:#339999">
  <strong>BiziApp Ressources</strong> · Sélection mise à jour régulièrement ·
  Aucun partenariat commercial — recommandations 100% indépendantes<br>
  <a href="/" style="color:#44C1BA;font-weight:700">← Retour à BiziApp</a>
</div>
""", unsafe_allow_html=True)
