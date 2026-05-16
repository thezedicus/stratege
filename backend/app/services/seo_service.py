from app.models.schemas import AnalysisInput

KEYWORDS_BY_SECTOR = {
    "ecommerce": [
        {"keyword": "acheter [produit] en ligne", "volume": "10K-100K", "difficulty": "Élevé", "intent": "Transactionnel"},
        {"keyword": "[produit] pas cher livraison rapide", "volume": "1K-10K", "difficulty": "Moyen", "intent": "Transactionnel"},
        {"keyword": "meilleur [produit] 2024", "volume": "1K-10K", "difficulty": "Moyen", "intent": "Informationnel"},
        {"keyword": "avis [produit]", "volume": "1K-10K", "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "[produit] comparatif", "volume": "500-5K", "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "comment choisir [produit]", "volume": "1K-10K", "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "[produit] promotion soldes", "volume": "5K-50K", "difficulty": "Moyen", "intent": "Transactionnel"},
    ],
    "saas": [
        {"keyword": "logiciel [catégorie] gratuit", "volume": "10K-100K", "difficulty": "Élevé", "intent": "Transactionnel"},
        {"keyword": "alternative à [concurrent]", "volume": "1K-10K", "difficulty": "Moyen", "intent": "Commercial"},
        {"keyword": "meilleur outil [catégorie] PME", "volume": "500-5K", "difficulty": "Faible", "intent": "Commercial"},
        {"keyword": "comment automatiser [tâche]", "volume": "1K-10K", "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "prix [catégorie SaaS]", "volume": "500-5K", "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "[catégorie] pour startup", "volume": "500-5K", "difficulty": "Facile", "intent": "Transactionnel"},
    ],
    "default": [
        {"keyword": "[activité] professionnel", "volume": "1K-10K", "difficulty": "Moyen", "intent": "Commercial"},
        {"keyword": "[activité] pas cher", "volume": "500-5K", "difficulty": "Facile", "intent": "Transactionnel"},
        {"keyword": "comment [objectif principal]", "volume": "5K-50K", "difficulty": "Moyen", "intent": "Informationnel"},
        {"keyword": "meilleur [activité] France", "volume": "1K-10K", "difficulty": "Moyen", "intent": "Commercial"},
        {"keyword": "[activité] avis et test", "volume": "500-5K", "difficulty": "Facile", "intent": "Commercial"},
        {"keyword": "[activité] guide complet", "volume": "500-5K", "difficulty": "Facile", "intent": "Informationnel"},
        {"keyword": "[activité] débutant", "volume": "1K-5K", "difficulty": "Facile", "intent": "Informationnel"},
    ],
}

ON_PAGE_CHECKLIST = [
    {"item": "Balises title optimisées (50-60 chars)", "status": "warning", "recommendation": "Incluez le mot-clé principal en début de title, ex: '[Mot-clé] | [Marque]'"},
    {"item": "Meta descriptions (150-160 chars)", "status": "warning", "recommendation": "Rédigez une meta description incitative avec CTA et mot-clé naturellement intégré"},
    {"item": "Balises H1/H2/H3 hiérarchisées", "status": "ok", "recommendation": "Structure correcte — vérifiez qu'il n'y a qu'un seul H1 par page"},
    {"item": "Images avec balises ALT descriptives", "status": "error", "recommendation": "Toutes les images doivent avoir un attribut alt descriptif incluant le mot-clé si pertinent"},
    {"item": "Vitesse de chargement < 3 secondes", "status": "warning", "recommendation": "Compressez les images (WebP), activez la mise en cache, utilisez un CDN"},
    {"item": "Site responsive mobile-first", "status": "ok", "recommendation": "Passez le test Google Mobile-Friendly et corrigez les éléments non cliquables"},
    {"item": "HTTPS et certificat SSL valide", "status": "ok", "recommendation": "Indispensable pour le SEO et la confiance utilisateur"},
    {"item": "Sitemap XML soumis à Google Search Console", "status": "warning", "recommendation": "Créez et soumettez votre sitemap.xml pour accélérer l'indexation"},
    {"item": "Données structurées Schema.org", "status": "error", "recommendation": "Ajoutez les schémas JSON-LD appropriés (Product, FAQ, Organization, etc.)"},
    {"item": "URLs courtes et descriptives", "status": "ok", "recommendation": "Format recommandé : /categorie/nom-produit-mot-cle"},
    {"item": "Maillage interne cohérent", "status": "warning", "recommendation": "Chaque page doit pointer vers au moins 3 pages pertinentes du site"},
]

GEO_TIPS = [
    "Structurez votre contenu en réponses directes aux questions (FAQ schema) — les moteurs génératifs privilégient le format Q&A",
    "Rédigez des résumés exécutifs en début d'article (TLDR) que les IA peuvent citer directement",
    "Créez des pages d'autorité thématique approfondies (pillar pages) plutôt que du contenu superficiel",
    "Intégrez des données propriétaires, études de cas et statistiques originales que les IA citent comme sources",
    "Optimisez pour les questions conversationnelles : 'comment', 'pourquoi', 'quand', 'quel est le meilleur'",
    "Assurez une présence cohérente sur Wikipedia, Wikidata et les annuaires de référence sectorielle",
    "Obtenez des mentions dans des médias reconnus — les IA leur accordent une autorité forte",
    "Publiez régulièrement (fraîcheur du contenu appréciée par les moteurs génératifs)",
]


def generate_seo(data: AnalysisInput) -> dict:
    keywords = KEYWORDS_BY_SECTOR.get(data.activityType, KEYWORDS_BY_SECTOR["default"])
    audit = ON_PAGE_CHECKLIST.copy()

    ads_budget = round(data.monthlyBudget * 0.5)
    campaigns = _generate_google_ads(data, ads_budget)

    trending = [
        {"topic": f"IA et {data.activityType}", "trend": "hausse"},
        {"topic": f"{data.activityType} durable", "trend": "hausse"},
        {"topic": f"Automatisation {data.activityType}", "trend": "hausse"},
        {"topic": f"{data.activityType} mobile", "trend": "stable"},
        {"topic": "Marketing d'influence micro", "trend": "hausse"},
        {"topic": "Publicité traditionnelle", "trend": "baisse"},
    ]

    return {
        "keywords": keywords,
        "onPageAudit": audit,
        "geoTips": GEO_TIPS,
        "googleAds": campaigns,
        "trendingTopics": trending,
    }


def _generate_google_ads(data: AnalysisInput, total_budget: float) -> list:
    campaigns = []
    goal_campaign = {
        "awareness": {"name": "Campagne Notoriété Search", "type": "Search - Brand awareness", "bidStrategy": "Maximiser les impressions"},
        "sales": {"name": "Campagne Conversion Search", "type": "Search - Conversions", "bidStrategy": "CPA cible"},
        "leads": {"name": "Campagne Lead Gen", "type": "Search + Display", "bidStrategy": "Maximiser les conversions"},
        "traffic": {"name": "Campagne Trafic Search", "type": "Search - Clics", "bidStrategy": "CPC max amélioré"},
    }

    main_camp = goal_campaign.get(data.goal, goal_campaign["traffic"])
    campaigns.append({
        "campaign": main_camp["name"],
        "keywords": [f"[mot-clé principal 1]", f"[mot-clé principal 2]", f"[marque + secteur]"],
        "budget": round(total_budget * 0.6),
        "bidStrategy": main_camp["bidStrategy"],
    })

    if total_budget > 100:
        campaigns.append({
            "campaign": "Campagne Retargeting Display",
            "keywords": ["Audiences similaires", "Remarketing visiteurs", "Intent audiences Google"],
            "budget": round(total_budget * 0.25),
            "bidStrategy": "CPC max",
        })

    if total_budget > 200:
        campaigns.append({
            "campaign": "Campagne Concurrents",
            "keywords": [f"[concurrent 1]", f"[concurrent 2]", f"alternative [concurrent]"],
            "budget": round(total_budget * 0.15),
            "bidStrategy": "CPC max amélioré",
        })

    return campaigns
