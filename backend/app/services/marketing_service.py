from app.models.schemas import AnalysisInput

PLATFORM_DATA: dict = {
    "ecommerce": [
        {"name": "Instagram Shopping",     "priority": "haute",   "reason": "Idéal pour les achats impulsifs et la découverte visuelle produit", "frequency": "1 post/jour + 5 stories"},
        {"name": "Pinterest",              "priority": "haute",   "reason": "Fort trafic d'intention d'achat, pins durables dans le temps",      "frequency": "5 épingles/jour"},
        {"name": "Facebook Ads",           "priority": "haute",   "reason": "Retargeting puissant et ciblage démographique précis",               "frequency": "2-3 campagnes actives"},
        {"name": "Google Shopping",        "priority": "moyenne", "reason": "Capture l'intention d'achat directe en phase de recherche",         "frequency": "Campagnes continues"},
        {"name": "TikTok",                 "priority": "moyenne", "reason": "Viralité produit, fort engagement Génération Z et Millennials",     "frequency": "3-5 vidéos/semaine"},
    ],
    "saas": [
        {"name": "LinkedIn",               "priority": "haute",   "reason": "Audience professionnelle B2B, décideurs et acheteurs",              "frequency": "5 posts/semaine"},
        {"name": "Google Ads",             "priority": "haute",   "reason": "Capture l'intention de recherche au moment clé du besoin",          "frequency": "Campagnes continues"},
        {"name": "Email Marketing",        "priority": "haute",   "reason": "Nurturing leads, séquences d'onboarding et rétention (ROI 42:1)",   "frequency": "1-2 emails/semaine"},
        {"name": "YouTube",                "priority": "moyenne", "reason": "Tutoriels, démos produit et SEO vidéo durable",                     "frequency": "1 vidéo/semaine"},
        {"name": "Webinaires",             "priority": "moyenne", "reason": "Conversion haute intention, démonstration valeur directe",          "frequency": "2/mois"},
    ],
    "service": [
        {"name": "LinkedIn",               "priority": "haute",   "reason": "Réseau de référence pour les services B2B et le personal branding", "frequency": "5 posts/semaine"},
        {"name": "Email Marketing",        "priority": "haute",   "reason": "Canal owned, meilleur ROI pour la fidélisation client",              "frequency": "1-2 emails/semaine"},
        {"name": "Google (SEO local)",     "priority": "haute",   "reason": "Capte les recherches directes de prestataires qualifiés",           "frequency": "2 articles/semaine"},
        {"name": "Instagram",              "priority": "moyenne", "reason": "Montre les coulisses et humanise le prestataire",                   "frequency": "4 posts/semaine"},
        {"name": "Podcasts / YouTube",     "priority": "moyenne", "reason": "Autorité sectorielle et contenu evergreen longue traîne",          "frequency": "1 épisode/semaine"},
    ],
    "website": [
        {"name": "Google My Business",     "priority": "haute",   "reason": "Visibilité locale gratuite et reviews clients essentielles",        "frequency": "1 post/semaine"},
        {"name": "Facebook",               "priority": "haute",   "reason": "Communauté locale, évènements et groupes de quartier",              "frequency": "4 posts/semaine"},
        {"name": "Instagram",              "priority": "moyenne", "reason": "Vitrine visuelle, hashtags locaux et collaborations",               "frequency": "3-4 posts/semaine"},
        {"name": "Email Newsletter",       "priority": "haute",   "reason": "Canal owned indépendant des algorithmes (ROI 42:1)",               "frequency": "1-2/semaine"},
        {"name": "Google Ads (local)",     "priority": "moyenne", "reason": "Ciblage géographique précis sur votre zone de chalandise",         "frequency": "Campagnes ciblées"},
    ],
    "consulting": [
        {"name": "LinkedIn",               "priority": "haute",   "reason": "Plateforme numéro 1 pour le personal branding B2B",                 "frequency": "5 posts/semaine"},
        {"name": "Email Marketing",        "priority": "haute",   "reason": "Nurturing prospects, newsletter d'expertise",                       "frequency": "1/semaine"},
        {"name": "Podcast / YouTube",      "priority": "haute",   "reason": "Contenu long format pour démontrer l'expertise",                   "frequency": "1 épisode/semaine"},
        {"name": "Google (SEO)",           "priority": "moyenne", "reason": "Articles de fond qui capturent les recherches intentionnelles",     "frequency": "2 articles/semaine"},
        {"name": "Webinaires",             "priority": "haute",   "reason": "Génération de leads qualifiés et démonstration de valeur",          "frequency": "1-2/mois"},
    ],
    "content": [
        {"name": "YouTube",                "priority": "haute",   "reason": "Plateforme vidéo avec meilleur ROI long terme et SEO intégré",      "frequency": "2-3 vidéos/semaine"},
        {"name": "Newsletter (Substack)",  "priority": "haute",   "reason": "Audience owned, monétisation directe, fidélisation forte",          "frequency": "1-2/semaine"},
        {"name": "Instagram / TikTok",     "priority": "haute",   "reason": "Découverte, viralité et croissance rapide d'audience",              "frequency": "1 post/jour"},
        {"name": "Podcast",                "priority": "moyenne", "reason": "Audience fidèle, partenariats et brand deals",                      "frequency": "1 épisode/semaine"},
        {"name": "Pinterest",              "priority": "moyenne", "reason": "Trafic evergreen vers blog et contenu long terme",                  "frequency": "5 pins/jour"},
    ],
    "default": [
        {"name": "Instagram",              "priority": "haute",   "reason": "Large audience, format visuel adapté à tous secteurs",              "frequency": "1 post/jour"},
        {"name": "Email Newsletter",       "priority": "haute",   "reason": "Canal owned avec meilleur ROI du marketing digital (42:1)",        "frequency": "1-2/semaine"},
        {"name": "Facebook",               "priority": "haute",   "reason": "Ciblage avancé, groupes communautaires et publicité accessible",   "frequency": "5 posts/semaine"},
        {"name": "LinkedIn",               "priority": "moyenne", "reason": "Réseautage professionnel et autorité sectorielle",                  "frequency": "3-4 posts/semaine"},
        {"name": "Google Ads",             "priority": "moyenne", "reason": "Capture l'intention de recherche directe",                         "frequency": "Campagnes ciblées"},
    ],
}

CONTENT_FORMATS: dict = {
    "awareness": ["Reel / TikTok viral",      "Infographie partageable",    "Article de blog SEO",      "Podcast épisode",         "Vidéo YouTube"],
    "sales":     ["Témoignage client vidéo",  "Démonstration produit",      "Comparatif / Avantages",   "Offre spéciale limitée",  "Tutoriel pratique"],
    "leads":     ["Lead magnet téléchargeable","Webinaire gratuit",          "Quiz interactif",          "Checklist PDF",           "Template gratuit"],
    "traffic":   ["Article SEO long-form",    "Guide complet (+3 000 mots)","Série de posts LinkedIn",  "FAQ enrichie",            "Thread Twitter/X"],
}

CONTENT_TOPICS: dict = {
    "ecommerce":   ["Coulisses de fabrication", "Unboxing et test produit", "Guide d'utilisation pas à pas", "Tendances saison", "Comparatif produits"],
    "saas":        ["Tutoriel fonctionnalité",  "Cas client chiffré (ROI)", "Tendances du secteur",          "Tips productivité",  "Webinaire live Q&A"],
    "service":     ["Étude de cas client",      "Méthode de travail",       "Avant/Après mission réelle",    "Conseils gratuits",  "Témoignage client"],
    "website":     ["Coulisses de l'activité",  "Présentation équipe",      "Actualités locales",            "Partenariats locaux","Évènement ou atelier"],
    "consulting":  ["Analyse de tendance",      "Erreur courante à éviter", "Framework propriétaire",        "Interview expert",   "Étude de cas anonymisée"],
    "content":     ["Coulisses de création",    "Chiffres du mois",         "Outil favori du moment",        "Mon parcours",       "Collab avec créateur"],
    "default":     ["Conseils pratiques",       "Coulisses de l'activité",  "Question à la communauté",      "Résultats partagés", "Ressource gratuite"],
}


def generate_marketing(data: AnalysisInput) -> dict:
    platforms = PLATFORM_DATA.get(data.activityType, PLATFORM_DATA["default"])

    # Budget allocation fixed percentages (always sums to 100%)
    ads_pct     = 0.50
    tools_pct   = 0.25
    content_pct = 0.15
    seo_pct     = 0.10

    ads     = round(data.monthlyBudget * ads_pct)
    tools   = round(data.monthlyBudget * tools_pct)
    content = round(data.monthlyBudget * content_pct)
    seo     = round(data.monthlyBudget * seo_pct)

    # Adjust seo to absorb rounding residuals
    seo = max(0, int(data.monthlyBudget) - ads - tools - content)

    budget_allocation = [
        {"category": "Publicité payante (Google/Meta)", "percentage": 50, "amount": ads},
        {"category": "Outils et logiciels",             "percentage": 25, "amount": tools},
        {"category": "Création de contenu",             "percentage": 15, "amount": content},
        {"category": "SEO et netlinking",               "percentage": 10, "amount": seo},
    ]

    formats = CONTENT_FORMATS.get(data.goal, CONTENT_FORMATS["awareness"])
    topics  = CONTENT_TOPICS.get(data.activityType, CONTENT_TOPICS["default"])
    platform_names = [p["name"].split()[0] for p in platforms[:4]]

    content_plan = []
    for week in range(1, 5):
        for i, platform in enumerate(platform_names[:3]):
            content_plan.append({
                "week":     week,
                "platform": platform,
                "format":   formats[i % len(formats)],
                "topic":    topics[(week * 3 + i) % len(topics)],
                "hashtags": _get_hashtags(data.activityType, data.goal),
            })

    editorial_calendar = [
        {"day": "Lun", "content": "Contenu éducatif / Conseil pratique",    "format": "Carrousel"},
        {"day": "Mar", "content": "Coulisses / Behind the scenes",           "format": "Reel"},
        {"day": "Mer", "content": "Témoignage ou résultat client",           "format": "Post image"},
        {"day": "Jeu", "content": "Astuce rapide / Tip actionnable",         "format": "Story"},
        {"day": "Ven", "content": "Offre ou promotion du week-end",          "format": "Post + Story"},
        {"day": "Sam", "content": "Engagement communauté / Sondage",        "format": "Sondage Stories"},
        {"day": "Dim", "content": "Inspiration / Citation motivante",        "format": "Citation visuelle"},
    ]

    rule8020 = {
        "focus": [
            "Email marketing — ROI moyen de 42:1, canal owned indépendant des algorithmes",
            f"Canal principal de votre audience : {platforms[0]['name']} ({platforms[0]['reason']})",
            "Contenu evergreen (guides, tutoriels) qui génère du trafic longtemps après publication",
            "Retargeting des visiteurs chauds ayant montré une intention claire",
            f"SEO sur {_get_top_keywords_count(data.budget)} mots-clés à fort potentiel et faible difficulté",
        ],
        "avoid": [
            "Être présent sur toutes les plateformes simultanément — dispersez votre énergie",
            "Créer du contenu sans stratégie ni calendrier de distribution défini",
            "Ignorer les données analytiques hebdomadaires (taux de rebond, CTR, conversions)",
            "Acheter des followers, des likes ou des avis factices — pénalisé par les algorithmes",
            "Dépenser en publicité payante sans avoir optimisé sa page de destination au préalable",
        ],
    }

    return {
        "contentPlan":       content_plan,
        "platforms":         platforms,
        "budgetAllocation":  budget_allocation,
        "rule8020":          rule8020,
        "editorialCalendar": editorial_calendar,
    }


def _get_hashtags(activity: str, goal: str) -> list:
    base = {
        "ecommerce":  ["ecommerce", "boutiqueenligne", "shopping"],
        "saas":       ["saas", "startup", "productivite"],
        "service":    ["freelance", "entrepreneur", "expertise"],
        "website":    ["siteweb", "creationsite", "webdesign"],
        "consulting": ["conseil", "strategy", "coaching"],
        "content":    ["contentcreator", "createur", "digital"],
        "default":    ["entrepreneur", "business", "croissance"],
    }
    goal_tags = {
        "awareness": ["notoriete", "branding", "visibilite"],
        "sales":     ["vente", "promotion", "offre"],
        "leads":     ["leadgeneration", "prospection", "growth"],
        "traffic":   ["seo", "trafic", "referencement"],
    }
    return base.get(activity, base["default"]) + goal_tags.get(goal, [])


def _get_top_keywords_count(budget: float) -> int:
    if budget < 50:    return 3
    if budget < 100:   return 5
    if budget < 300:   return 10
    if budget < 600:   return 20
    return 30
