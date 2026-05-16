from app.models.schemas import AnalysisInput

SECTOR_DATA = {
    "ecommerce": {
        "strengths_base": ["Marché mondial accessible 24h/24", "Faibles coûts opérationnels vs commerce physique", "Données clients exploitables en temps réel"],
        "weaknesses_base": ["Concurrence en ligne très intense", "Problèmes de confiance et retours clients", "Logistique et gestion des stocks complexes"],
        "opportunities_base": ["Croissance du m-commerce (+35% par an)", "Personnalisation IA des recommandations", "Marchés internationaux peu saturés"],
        "threats_base": ["Amazon et marketplaces dominants", "Évolutions réglementaires RGPD/e-commerce", "Coûts d'acquisition client en hausse"],
    },
    "saas": {
        "strengths_base": ["Revenus récurrents (MRR/ARR) prévisibles", "Scalabilité sans coûts marginaux élevés", "Déploiement immédiat, mises à jour centralisées"],
        "weaknesses_base": ["Coûts d'acquisition client (CAC) élevés", "Churn et fidélisation critiques", "Infrastructure cloud coûteuse au démarrage"],
        "opportunities_base": ["Transformation digitale des PME accélérée", "Intégrations API et écosystème partenaires", "Intelligence artificielle comme différenciateur"],
        "threats_base": ["Consolidation du marché SaaS", "Copie rapide des fonctionnalités par concurrents", "Dépendance aux plateformes (App Store, AWS)"],
    },
    "service": {
        "strengths_base": ["Faibles coûts fixes initiaux", "Forte marge potentielle sur expertise", "Relation client directe et personnalisée"],
        "weaknesses_base": ["Scalabilité limitée par le temps disponible", "Dépendance à la réputation et bouche-à-oreille", "Difficile à automatiser entièrement"],
        "opportunities_base": ["Digitalisation des services traditionnels", "Plateformes de mise en relation (Malt, Upwork)", "Productisation des services en offres packagées"],
        "threats_base": ["Plateformes low-cost concurrentes", "Automatisation IA des tâches répétitives", "Cyclicité économique impactant les budgets clients"],
    },
    "website": {
        "strengths_base": ["Présence digitale professionnelle 24/7", "Vitrine accessible mondialement", "Support commercial automatisé"],
        "weaknesses_base": ["Trafic organique long à construire", "Mise à jour et maintenance requises", "Conversion souvent faible sans optimisation"],
        "opportunities_base": ["SEO local très accessible pour PME", "Contenu evergreen générateur de leads passifs", "Intégration CRM et automatisation marketing"],
        "threats_base": ["Changements algorithmes Google fréquents", "Concurrence des réseaux sociaux pour l'attention", "Coûts publicitaires croissants"],
    },
    "consulting": {
        "strengths_base": ["Expertise à forte valeur ajoutée et différenciante", "Relation client longue durée et fidélisation naturelle", "Faibles coûts fixes, marges élevées"],
        "weaknesses_base": ["Dépendance directe au temps et à la disponibilité", "Difficile à scaler sans recrutement", "Image parfois perçue comme coûteuse par les PME"],
        "opportunities_base": ["Demande croissante en accompagnement stratégique post-Covid", "Digitalisation des missions en format remote", "Productisation en formations ou programmes en ligne"],
        "threats_base": ["Concurrence des cabinets low-cost et freelances", "IA automatisant les analyses et livrables standards", "Cycles économiques impactant les budgets conseil"],
    },
    "content": {
        "strengths_base": ["Création de valeur continue et actifs durables", "Audience owned indépendante des algorithmes (email, newsletter)", "Multiples sources de revenus (ads, sponsoring, formations)"],
        "weaknesses_base": ["Revenus irréguliers et dépendants de la plateforme", "Temps de construction long avant monétisation", "Burnout créatif et constance exigée"],
        "opportunities_base": ["Explosion du creator economy et des outils de monétisation", "Niches hyper-spécialisées peu couvertes et rentables", "Intelligence artificielle pour accélérer la production de contenu"],
        "threats_base": ["Saturation des plateformes et chute organique", "Changements d'algorithmes destructeurs d'audience", "Copie et plagiat du contenu par des concurrents"],
    },
    "application": {
        "strengths_base": ["Usage quotidien et fort potentiel d'engagement", "Notifications push pour réengagement direct", "Monétisation variée : freemium, abonnement, in-app"],
        "weaknesses_base": ["Coûts de développement et maintenance élevés", "Taux de désinstallation très élevé (70% à J+30)", "Dépendance aux stores Apple et Google"],
        "opportunities_base": ["6 milliards de smartphones utilisateurs potentiels", "PWA réduisant les barrières de distribution", "IA générative comme fonctionnalité différenciante"],
        "threats_base": ["Compétition féroce dans les stores (5M+ applications)", "Politiques App Store contraignantes et commissions 30%", "Coûts d'acquisition utilisateur mobile en forte hausse"],
    },
    "other": {
        "strengths_base": ["Agilité et liberté d'expérimentation", "Connaissance terrain et proximité client unique", "Capacité à pivoter rapidement selon le marché"],
        "weaknesses_base": ["Positionnement à clarifier pour se différencier", "Ressources et budget à optimiser en priorité", "Notoriété et crédibilité à construire"],
        "opportunities_base": ["Marchés de niche sous-exploités à forte rentabilité", "Outils digitaux low-cost pour tester et valider", "Partenariats stratégiques pour accélérer la croissance"],
        "threats_base": ["Acteurs établis avec avantage concurrentiel fort", "Évolution rapide des attentes clients et technologies", "Risque de sous-capitalisation en phase de croissance"],
    },
}

DEFAULT_DATA = {
    "strengths_base": ["Agilité et capacité d'adaptation rapide", "Connaissance client directe", "Innovation sans contraintes corporate"],
    "weaknesses_base": ["Ressources financières limitées", "Notoriété à construire", "Équipe réduite, charge de travail importante"],
    "opportunities_base": ["Niches de marché sous-exploitées", "Croissance des outils no-code et IA", "Communautés digitales engagées"],
    "threats_base": ["Acteurs établis avec avantage concurrentiel", "Évolution rapide des technologies", "Risque de copie par des concurrents plus grands"],
}


def _budget_score(budget: float) -> int:
    if budget < 100: return 20
    if budget < 300: return 45
    if budget < 600: return 65
    return 85


def _maturity_score(maturity: str) -> int:
    return {"idea": 20, "inprogress": 50, "launched": 80}.get(maturity, 40)


def generate_swot(data: AnalysisInput) -> dict:
    sector = SECTOR_DATA.get(data.activityType, DEFAULT_DATA)

    budget_add = []
    if data.budget < 100:
        budget_add.append("Budget contraint nécessitant une priorisation rigoureuse")
    elif data.budget > 600:
        budget_add.append("Budget suffisant pour tester plusieurs canaux d'acquisition")

    goal_opportunities = {
        "awareness": "Stratégies de contenu viral et collaborations influenceurs accessibles",
        "sales": "Tunnel de vente optimisé avec des outils gratuits ou freemium",
        "leads": "Lead magnets et landing pages à forte conversion",
        "traffic": "SEO organique et marketing de contenu à fort ROI",
    }

    budget_s = _budget_score(data.budget)
    maturity_s = _maturity_score(data.maturity)

    return {
        "strengths": sector["strengths_base"] + budget_add,
        "weaknesses": sector["weaknesses_base"],
        "opportunities": sector["opportunities_base"] + [goal_opportunities.get(data.goal, "")],
        "threats": sector["threats_base"],
        "score": {
            "innovation": min(90, 50 + (20 if data.activityType in ["saas", "application"] else 0)),
            "market": min(90, 40 + (10 if data.maturity == "launched" else 0)),
            "budget": budget_s,
            "maturity": maturity_s,
            "digital": min(90, 60 + (15 if data.activityType in ["saas", "ecommerce"] else 0)),
        },
    }
