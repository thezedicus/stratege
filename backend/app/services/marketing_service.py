from app.models.schemas import AnalysisInput

PLATFORM_DATA = {
    "ecommerce": [
        {"name": "Instagram Shopping", "priority": "haute", "reason": "Idéal pour les achats impulsifs et la découverte visuelle produit", "frequency": "1 post/jour + 5 stories"},
        {"name": "Pinterest", "priority": "haute", "reason": "Fort trafic d'intention d'achat, pins durables dans le temps", "frequency": "5 épingles/jour"},
        {"name": "Facebook Ads", "priority": "haute", "reason": "Retargeting puissant et ciblage démographique précis", "frequency": "2-3 campagnes actives"},
        {"name": "Google Shopping", "priority": "moyenne", "reason": "Capture l'intention d'achat directe en phase de recherche", "frequency": "Campagnes continues"},
        {"name": "TikTok", "priority": "moyenne", "reason": "Viralité produit, génération Z et millennials", "frequency": "3-5 vidéos/semaine"},
    ],
    "saas": [
        {"name": "LinkedIn", "priority": "haute", "reason": "Audience professionnelle B2B, décideurs et acheteurs", "frequency": "5 posts/semaine"},
        {"name": "Google Ads", "priority": "haute", "reason": "Capture l'intention de recherche au moment clé", "frequency": "Campagnes continues"},
        {"name": "Email Marketing", "priority": "haute", "reason": "Nurturing leads, séquences d'onboarding et rétention", "frequency": "1-2 emails/semaine"},
        {"name": "YouTube", "priority": "moyenne", "reason": "Tutoriels, démos produit et SEO vidéo durable", "frequency": "1 vidéo/semaine"},
        {"name": "Webinaires", "priority": "moyenne", "reason": "Conversion haute intention, démonstration valeur directe", "frequency": "2/mois"},
    ],
    "default": [
        {"name": "Instagram", "priority": "haute", "reason": "Large audience, format visuel adapté à tous secteurs", "frequency": "1 post/jour"},
        {"name": "Facebook", "priority": "haute", "reason": "Ciblage avancé, groupes communautaires et publicité", "frequency": "5 posts/semaine"},
        {"name": "LinkedIn", "priority": "moyenne", "reason": "Réseautage professionnel et autorité sectorielle", "frequency": "3-4 posts/semaine"},
        {"name": "Google Ads", "priority": "moyenne", "reason": "Capture l'intention de recherche directe", "frequency": "Campagnes ciblées"},
        {"name": "Email Newsletter", "priority": "haute", "reason": "Canal owned, ROI le plus élevé du marketing digital (42:1)", "frequency": "1-2/semaine"},
    ],
}

CONTENT_FORMATS = {
    "awareness": ["Reel / TikTok", "Infographie", "Article de blog", "Podcast", "Vidéo YouTube"],
    "sales": ["Témoignage client", "Démonstration produit", "Comparatif", "Offre spéciale", "Tutoriel"],
    "leads": ["Lead magnet", "Webinaire", "Quiz interactif", "Checklist PDF", "Template gratuit"],
    "traffic": ["Article SEO long-form", "Guide complet", "Série de posts", "Thread Twitter/X", "FAQ"],
}

CONTENT_TOPICS = {
    "ecommerce": ["Coulisses de fabrication", "Unboxing et test produit", "Guide d'utilisation", "Tendances saison", "Comparatif concurrence"],
    "saas": ["Tutoriel fonctionnalité", "Cas client avec ROI", "Tendances du secteur", "Tips productivité", "Webinaire live"],
    "service": ["Étude de cas client", "Méthode de travail", "Avant/Après mission", "Conseils gratuits", "Témoignage client"],
    "default": ["Conseils pratiques", "Coulisses de l'activité", "Question à la communauté", "Partage de résultats", "Ressource gratuite"],
}


def generate_marketing(data: AnalysisInput) -> dict:
    platforms = PLATFORM_DATA.get(data.activityType, PLATFORM_DATA["default"])

    ads = round(data.monthlyBudget * 0.50)
    tools = round(data.monthlyBudget * 0.25)
    content = round(data.monthlyBudget * 0.15)
    seo_budget = data.monthlyBudget - ads - tools - content

    budget_allocation = [
        {"category": "Publicité payante (Google/Meta)", "percentage": 50, "amount": ads},
        {"category": "Outils et logiciels", "percentage": 25, "amount": tools},
        {"category": "Création de contenu", "percentage": 15, "amount": content},
        {"category": "SEO et netlinking", "percentage": 10, "amount": seo_budget},
    ]

    formats = CONTENT_FORMATS.get(data.goal, CONTENT_FORMATS["awareness"])
    topics = CONTENT_TOPICS.get(data.activityType, CONTENT_TOPICS["default"])

    content_plan = []
    platform_names = [p["name"].split()[0] for p in platforms[:4]]

    for week in range(1, 5):
        for i, platform in enumerate(platform_names[:3]):
            content_plan.append({
                "week": week,
                "platform": platform,
                "format": formats[i % len(formats)],
                "topic": topics[(week * 3 + i) % len(topics)],
                "hashtags": _get_hashtags(data.activityType, data.goal),
            })

    editorial_calendar = [
        {"day": "Lun", "content": "Contenu éducatif / Conseil", "format": "Carrousel"},
        {"day": "Mar", "content": "Coulisses / Behind the scenes", "format": "Reel"},
        {"day": "Mer", "content": "Partage de résultats client", "format": "Post image"},
        {"day": "Jeu", "content": "Tip pratique / Astuce", "format": "Story"},
        {"day": "Ven", "content": "Offre / Promotion du WE", "format": "Post + Story"},
        {"day": "Sam", "content": "Engagement communauté", "format": "Sondage"},
        {"day": "Dim", "content": "Inspiration / Motivation", "format": "Citation"},
    ]

    rule_8020 = {
        "focus": [
            "Email marketing (ROI 42:1 en moyenne)",
            f"Le canal principal de votre audience cible : {platforms[0]['name']}",
            "Contenu evergreen qui génère du trafic sur le long terme",
            "Retargeting des visiteurs chauds (intention d'achat prouvée)",
            f"SEO sur les {_get_top_keywords_count(data.budget)} mots-clés à fort potentiel",
        ],
        "avoid": [
            "Être présent sur toutes les plateformes à la fois",
            "Créer du contenu sans stratégie de distribution",
            "Ignorer les données analytiques hebdomadaires",
            "Acheter des followers ou des likes",
        ],
    }

    return {
        "contentPlan": content_plan,
        "platforms": platforms,
        "budgetAllocation": budget_allocation,
        "rule8020": rule_8020,
        "editorialCalendar": editorial_calendar,
    }


def _get_hashtags(activity: str, goal: str) -> list:
    base = {
        "ecommerce": ["ecommerce", "boutiquenligne", "shopping"],
        "saas": ["saas", "startup", "productivite"],
        "service": ["freelance", "entrepreneur", "business"],
        "default": ["entrepreneur", "business", "croissance"],
    }
    goal_tags = {
        "awareness": ["marque", "notoriete", "visibilite"],
        "sales": ["vente", "promotion", "offre"],
        "leads": ["leadgeneration", "prospecton", "growth"],
        "traffic": ["seo", "trafic", "content"],
    }
    return base.get(activity, base["default"]) + goal_tags.get(goal, [])


def _get_top_keywords_count(budget: float) -> int:
    if budget < 100: return 5
    if budget < 300: return 10
    if budget < 600: return 20
    return 30
