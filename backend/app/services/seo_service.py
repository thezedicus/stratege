from app.models.schemas import AnalysisInput

# Keywords with real sector-relevant terms (no placeholders)
KEYWORDS_BY_SECTOR: dict = {
    "ecommerce": [
        {"keyword": "boutique en ligne livraison rapide",        "volume": "10K-100K", "difficulty": "Élevé",  "intent": "Transactionnel"},
        {"keyword": "acheter en ligne paiement sécurisé",       "volume": "10K-100K", "difficulty": "Élevé",  "intent": "Transactionnel"},
        {"keyword": "meilleur site e-commerce France",           "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "avis client boutique fiable",               "volume": "1K-10K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "comparatif boutique en ligne",              "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "comment choisir boutique en ligne sécurisée","volume": "1K-10K",  "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "promotion soldes vente flash",              "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Transactionnel"},
    ],
    "saas": [
        {"keyword": "logiciel gestion PME gratuit",              "volume": "10K-100K", "difficulty": "Élevé",  "intent": "Transactionnel"},
        {"keyword": "alternative logiciel concurrent",           "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "meilleur outil gestion TPE",                "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "comment automatiser sa gestion d'entreprise","volume": "1K-10K",  "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "prix logiciel SaaS abonnement mensuel",     "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "logiciel SaaS pour startup",                "volume": "500-5K",   "difficulty": "Facile", "intent": "Transactionnel"},
        {"keyword": "outil productivité équipe télétravail",     "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
    ],
    "service": [
        {"keyword": "consultant freelance en ligne",             "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "prestataire service en ligne tarif",        "volume": "500-5K",   "difficulty": "Facile", "intent": "Transactionnel"},
        {"keyword": "comment trouver un expert en ligne",        "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Informationnel"},
        {"keyword": "devis service numérique rapide",            "volume": "1K-10K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "avis consultant freelance fiable",          "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "accompagnement individuel en ligne",        "volume": "1K-10K",   "difficulty": "Facile", "intent": "Transactionnel"},
    ],
    "website": [
        {"keyword": "créer site vitrine professionnel",          "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Transactionnel"},
        {"keyword": "site web artisan artisanat local",          "volume": "1K-10K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "présence en ligne PME TPE",                 "volume": "500-5K",   "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "référencement local Google Maps",           "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Transactionnel"},
        {"keyword": "fiche Google My Business optimisation",     "volume": "1K-10K",   "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "site vitrine pas cher WordPress",           "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Transactionnel"},
    ],
    "consulting": [
        {"keyword": "consultant stratégie entreprise freelance", "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "accompagnement dirigeant TPE PME",          "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "conseil business plan démarrage",           "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Informationnel"},
        {"keyword": "mentor entrepreneur en ligne",              "volume": "1K-10K",   "difficulty": "Facile", "intent": "Transactionnel"},
        {"keyword": "diagnostic stratégique PME gratuit",        "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
    ],
    "content": [
        {"keyword": "créateur de contenu formation",             "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Informationnel"},
        {"keyword": "stratégie contenu réseaux sociaux",         "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Informationnel"},
        {"keyword": "blog affilié revenus passifs",              "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "newsletter abonnés fidélisation",           "volume": "1K-10K",   "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "monétiser audience YouTube Instagram",      "volume": "5K-50K",   "difficulty": "Élevé",  "intent": "Commercial"},
    ],
    "application": [
        {"keyword": "application mobile iOS Android",            "volume": "10K-100K", "difficulty": "Élevé",  "intent": "Transactionnel"},
        {"keyword": "télécharger app gratuite",                  "volume": "10K-100K", "difficulty": "Élevé",  "intent": "Transactionnel"},
        {"keyword": "meilleure application",                     "volume": "10K-100K", "difficulty": "Élevé",  "intent": "Commercial"},
        {"keyword": "app sans abonnement",                       "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "avis application mobile",                   "volume": "1K-10K",   "difficulty": "Facile", "intent": "Commercial"},
    ],
    "default": [
        {"keyword": "solution en ligne professionnelle",         "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "service numérique fiable",                  "volume": "500-5K",   "difficulty": "Facile", "intent": "Transactionnel"},
        {"keyword": "comment démarrer une activité en ligne",    "volume": "5K-50K",   "difficulty": "Moyen",  "intent": "Informationnel"},
        {"keyword": "meilleure solution pour entrepreneurs",     "volume": "1K-10K",   "difficulty": "Moyen",  "intent": "Commercial"},
        {"keyword": "avis et comparatif solutions web",          "volume": "500-5K",   "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "guide complet démarrage activité web",      "volume": "500-5K",   "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "astuce entrepreneur débutant",              "volume": "1K-5K",    "difficulty": "Facile", "intent": "Informationnel"},
    ],
}

ON_PAGE_CHECKLIST = [
    {"item": "Balises title optimisées (50-60 caractères)",           "status": "warning", "recommendation": "Incluez le mot-clé principal en début de title, format recommandé : 'Mot-clé | Nom de marque'"},
    {"item": "Meta descriptions incitatives (150-160 caractères)",    "status": "warning", "recommendation": "Rédigez une meta avec un verbe d'action et le bénéfice principal, incluez le mot-clé naturellement"},
    {"item": "Hiérarchie des titres H1/H2/H3 correcte",              "status": "ok",      "recommendation": "Structure correcte — assurez-vous qu'il n'y a qu'un seul H1 par page, unique et descriptif"},
    {"item": "Images avec balises ALT descriptives",                  "status": "error",   "recommendation": "Chaque image doit avoir un attribut alt descriptif incluant le mot-clé contextuel si pertinent"},
    {"item": "Vitesse de chargement < 3 secondes",                   "status": "warning", "recommendation": "Compressez les images en WebP, activez la mise en cache navigateur, utilisez un CDN comme Cloudflare"},
    {"item": "Design responsive mobile-first validé",                 "status": "ok",      "recommendation": "Passez le test Google Mobile-Friendly et corrigez tout élément non cliquable sur mobile"},
    {"item": "HTTPS actif et certificat SSL valide",                  "status": "ok",      "recommendation": "Indispensable pour le SEO et la confiance utilisateur — vérifiez l'absence de contenu mixte"},
    {"item": "Sitemap XML soumis à Google Search Console",            "status": "warning", "recommendation": "Créez sitemap.xml, soumettez-le dans Search Console pour accélérer l'indexation"},
    {"item": "Données structurées Schema.org présentes",              "status": "error",   "recommendation": "Ajoutez les schémas JSON-LD appropriés (Product, FAQ, Organization, LocalBusiness) selon votre activité"},
    {"item": "URLs courtes et descriptives avec mots-clés",           "status": "ok",      "recommendation": "Format : /categorie/sous-categorie-mot-cle — évitez les paramètres URL et les IDs numériques"},
    {"item": "Maillage interne structuré (3+ liens par page)",        "status": "warning", "recommendation": "Chaque page clé doit recevoir au moins 3 liens internes de pages ayant de l'autorité"},
    {"item": "Temps de réponse serveur < 200ms (TTFB)",               "status": "warning", "recommendation": "Passez sur un hébergeur SSD, activez OPcache PHP, envisagez un CDN pour les ressources statiques"},
]

GEO_TIPS = [
    "Structurez votre contenu en réponses directes aux questions (format FAQ avec schema.org) — les IA comme ChatGPT et Perplexity privilégient ces formats pour leurs réponses",
    "Rédigez des résumés exécutifs clairs en début d'article (TLDR en 2-3 phrases) que les moteurs génératifs peuvent citer directement",
    "Créez des pages d'autorité thématique approfondies (pillar pages > 2 000 mots) plutôt que du contenu superficiel éparpillé",
    "Intégrez des données originales et propriétaires (études, sondages, statistiques maison) — les IA les citent comme sources fiables",
    "Optimisez pour les questions conversationnelles longues : 'comment faire X sans Y', 'quelle est la meilleure façon de Z pour les débutants'",
    "Maintenez une présence cohérente sur les annuaires de référence sectoriels et Wikipedia — les LLMs leur accordent une forte autorité",
    "Obtenez des mentions et backlinks dans des médias reconnus (presse, blogs d'autorité) — les IA s'appuient sur ces signaux",
    "Publiez régulièrement du contenu frais (1-2 articles/semaine minimum) car les LLMs valorisent les sources récentes et actives",
]


def generate_seo(data: AnalysisInput) -> dict:
    keywords = KEYWORDS_BY_SECTOR.get(data.activityType, KEYWORDS_BY_SECTOR["default"])
    audit = list(ON_PAGE_CHECKLIST)  # shallow copy is fine here (no mutation)

    # SEO budget = 10% of monthly budget
    seo_budget = max(5, round(data.monthlyBudget * 0.10))
    # Google Ads uses the SEA portion = 35% of monthly budget
    sea_budget = max(5, round(data.monthlyBudget * 0.35))

    campaigns = _generate_google_ads(data, sea_budget)

    trending = _generate_trending(data.activityType)

    return {
        "keywords": keywords,
        "onPageAudit": audit,
        "geoTips": GEO_TIPS,
        "googleAds": campaigns,
        "trendingTopics": trending,
    }


def _generate_google_ads(data: AnalysisInput, total_budget: float) -> list:
    goal_map = {
        "awareness": ("Campagne Notoriété Search", "Search — Brand Awareness", "Maximiser les impressions"),
        "sales":     ("Campagne Conversion Search", "Search — Conversions",     "CPA cible"),
        "leads":     ("Campagne Génération Leads",  "Search + Display",         "Maximiser les conversions"),
        "traffic":   ("Campagne Trafic Search",     "Search — Clics",           "CPC max amélioré"),
    }
    name, camp_type, bid = goal_map.get(data.goal, goal_map["traffic"])

    # Sector-specific keyword examples (no generic placeholders)
    kw_map = {
        "ecommerce":   ["acheter [produit] pas cher", "livraison 24h [produit]", "[marque] promotions"],
        "saas":        ["logiciel [catégorie] essai gratuit", "alternative [concurrent] moins cher", "[fonctionnalité] en ligne"],
        "service":     ["prestataire [service] devis rapide", "expert [domaine] freelance", "consultant [spécialité] tarif"],
        "website":     ["créer site web [ville]", "[profession] en ligne [ville]", "site vitrine [activité]"],
        "consulting":  ["consultant [domaine] PME", "accompagnement stratégique [secteur]", "audit [domaine] gratuit"],
        "content":     ["créer contenu [plateforme]", "formation [sujet] en ligne", "monétiser blog [thème]"],
        "application": ["app [fonction] iOS Android", "télécharger [app] gratuit", "meilleure app [usage]"],
        "default":     ["solution [besoin] professionnel", "[service] en ligne fiable", "meilleur [produit] France"],
    }
    main_kws = kw_map.get(data.activityType, kw_map["default"])

    campaigns = [{
        "campaign": name,
        "keywords": main_kws,
        "budget": round(total_budget * 0.65),
        "bidStrategy": bid,
    }]

    if total_budget >= 40:
        campaigns.append({
            "campaign": "Retargeting Display",
            "keywords": ["Audiences similaires (Lookalike)", "Remarketing visiteurs 30 jours", "In-market audiences Google"],
            "budget": round(total_budget * 0.25),
            "bidStrategy": "CPC max",
        })

    if total_budget >= 100:
        campaigns.append({
            "campaign": "Campagne Concurrentiels",
            "keywords": ["concurrent n°1 avis", "concurrent n°2 alternative", "meilleur [catégorie] vs concurrent"],
            "budget": round(total_budget * 0.10),
            "bidStrategy": "CPC max amélioré",
        })

    return campaigns


def _generate_trending(activity: str) -> list:
    trends_map = {
        "ecommerce":   [("Commerce conversationnel IA",  "hausse"), ("Livraison verte",          "hausse"), ("Social commerce TikTok",  "hausse"), ("Publicité traditionnelle", "baisse"), ("Commerce mobile",         "stable")],
        "saas":        [("IA générative intégrée",       "hausse"), ("No-code / Low-code",       "hausse"), ("Sécurité des données",    "hausse"), ("Logiciels perpetuel",      "baisse"), ("Abonnement usage-based",  "hausse")],
        "service":     [("Coaching en ligne async",      "hausse"), ("Micro-missions freelance", "hausse"), ("Plateformes de mise en relation", "hausse"), ("Agences généralistes",   "baisse"), ("Spécialisation niche",   "hausse")],
        "website":     [("SEO local Google Maps",        "hausse"), ("Sites ultra-rapides Core Web Vitals", "hausse"), ("Référencement vocal",   "hausse"), ("Flash intros",           "baisse"), ("Accessibilité WCAG",     "hausse")],
        "default":     [("IA et automatisation",         "hausse"), ("Durabilité et éthique",   "hausse"), ("Personnalisation",        "hausse"), ("Publicité outbound",      "baisse"), ("Marketing de contenu",   "stable")],
    }
    pairs = trends_map.get(activity, trends_map["default"])
    return [{"topic": t, "trend": d} for t, d in pairs]
