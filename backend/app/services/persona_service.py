import copy

PERSONA_TEMPLATES: dict = {
    "ecommerce": [
        {
            "name": "Sophie Martin", "age": 32, "job": "Responsable marketing",
            "location": "Paris, France",
            "quote": "Je veux des produits de qualité livrés rapidement, sans mauvaise surprise.",
            "goals": ["Trouver des produits tendance rapidement", "Bénéficier d'un service client réactif", "Comparer facilement les offres"],
            "painPoints": ["Délais de livraison trop longs", "Retours produits compliqués", "Manque de confiance sur les nouveaux sites"],
            "channels": ["Instagram", "Pinterest", "Email"],
            "buyingTriggers": ["Promotion flash", "Avis clients positifs", "Livraison gratuite"],
            "soncas": {
                "Sécurité": "Rassurée par les avis certifiés, les retours faciles et le paiement sécurisé.",
                "Orgueil": "Fière d'acheter des marques qui reflètent ses valeurs.",
                "Nouveauté": "Attirée par les nouvelles collections et tendances.",
                "Confort": "Apprécie une navigation fluide et un checkout simplifié.",
                "Argent": "Sensible aux codes promo et à la livraison gratuite.",
                "Sympathie": "Fidèle aux marques qui lui parlent humainement.",
            },
            "aida": {
                "attention": "Publicité Instagram avec image lifestyle haute qualité et couleurs tendance.",
                "interest": "Présentation du produit en contexte d'usage avec témoignages clients.",
                "desire": "Offre limitée, stock limité ou édition exclusive pour créer l'urgence.",
                "action": "CTA 'Ajouter au panier' avec livraison gratuite mise en avant.",
            },
            "spin": {
                "situation": "Comment gérez-vous actuellement vos achats en ligne pour ce type de produit ?",
                "problem": "Êtes-vous déjà été déçue par la qualité ou les délais de livraison ?",
                "implication": "Ces déceptions vous font-elles perdre du temps et de l'argent à faire des retours ?",
                "need": "Si vous trouviez un site avec des retours simplifiés et une qualité garantie, cela changerait votre façon d'acheter ?",
            },
            "nudges": [
                "Social proof : '847 clients satisfaits cette semaine'",
                "Urgence : 'Il ne reste que 3 articles en stock'",
                "Ancrage prix : barrer l'ancien prix, afficher la réduction en %",
                "Réciprocité : offrir un guide gratuit avant l'achat",
                "Autorité : certifications et labels de qualité visibles",
                "FOMO : 'X personnes regardent ce produit en ce moment'",
            ],
        },
        {
            "name": "Thomas Dubois", "age": 28, "job": "Développeur freelance",
            "location": "Lyon, France",
            "quote": "Je compare tout avant d'acheter. Le meilleur rapport qualité/prix, c'est non-négociable.",
            "goals": ["Maximiser la valeur de chaque achat", "Recevoir des produits durables", "Processus d'achat simple et rapide"],
            "painPoints": ["Trop d'options à comparer", "Sites peu transparents sur les caractéristiques", "SAV inexistant"],
            "channels": ["YouTube", "Reddit", "Google"],
            "buyingTriggers": ["Tests comparatifs", "Garantie longue durée", "Prix transparent"],
            "soncas": {
                "Sécurité": "Cherche des garanties solides et des retours sans question.",
                "Orgueil": "Veut acheter malin et ne pas se faire avoir.",
                "Nouveauté": "Intéressé par les nouvelles technologies et innovations.",
                "Confort": "Veut une expérience d'achat rapide et efficace.",
                "Argent": "Très sensible au ROI et à la durabilité du produit.",
                "Sympathie": "Apprécie les marques transparentes et authentiques.",
            },
            "aida": {
                "attention": "Article comparatif ou vidéo YouTube qui ressort sur ses recherches.",
                "interest": "Fiche produit ultra-détaillée avec specs techniques et tableau comparatif.",
                "desire": "Témoignages d'experts et garantie satisfait ou remboursé 30 jours.",
                "action": "Option 'Acheter en 1 clic' avec paiement en plusieurs fois sans frais.",
            },
            "spin": {
                "situation": "Combien de temps passez-vous en moyenne à comparer avant d'acheter ?",
                "problem": "Avez-vous déjà regretté un achat à cause d'informations insuffisantes ?",
                "implication": "Ce temps de recherche vous fait-il parfois rater des bonnes affaires ?",
                "need": "Si vous aviez accès à toutes les infos en un seul endroit avec garantie, seriez-vous prêt à décider plus vite ?",
            },
            "nudges": [
                "Preuve sociale : nombre d'unités vendues",
                "Effet de dotation : essai gratuit 14 jours",
                "Comparaison : tableau versus concurrents",
                "Garantie : satisfaction 30 jours clairement affichée",
                "Transparence : composition, origine, certifications",
            ],
        },
    ],
    "saas": [
        {
            "name": "Claire Rousseau", "age": 38, "job": "Directrice d'une PME (15 salariés)",
            "location": "Bordeaux, France",
            "quote": "J'ai besoin d'outils qui fonctionnent vraiment et qui ne me font pas perdre du temps.",
            "goals": ["Automatiser les tâches répétitives", "Avoir une vue d'ensemble de l'activité", "Former facilement mon équipe"],
            "painPoints": ["Trop d'outils qui ne se parlent pas", "Formations longues et coûteuses", "Support technique peu réactif"],
            "channels": ["LinkedIn", "Email professionnel", "Bouche-à-oreille"],
            "buyingTriggers": ["Essai gratuit sans CB", "ROI démontrable", "Support inclus"],
            "soncas": {
                "Sécurité": "Veut un contrat clair, des données sécurisées (RGPD) et un SLA garanti.",
                "Orgueil": "Fière d'utiliser des outils modernes qui impressionnent ses clients.",
                "Nouveauté": "Ouverte aux nouvelles fonctionnalités si elles apportent une valeur réelle.",
                "Confort": "Veut une solution clé en main, pas de développement complexe.",
                "Argent": "Calcule le ROI : temps économisé × coût horaire vs abonnement.",
                "Sympathie": "Préfère des éditeurs à taille humaine, proches de leurs clients.",
            },
            "aida": {
                "attention": "Article LinkedIn avec statistique choc sur la productivité des PME.",
                "interest": "Cas client similaire avec ROI mesuré et témoignage vidéo.",
                "desire": "Démo personnalisée avec ses problématiques spécifiques.",
                "action": "Offre d'essai gratuit 14 jours sans carte bancaire, onboarding guidé.",
            },
            "spin": {
                "situation": "Quels outils utilisez-vous actuellement pour gérer vos processus métier ?",
                "problem": "Combien d'heures par semaine votre équipe passe-t-elle sur des tâches manuelles évitables ?",
                "implication": "Si ces heures étaient libérées, quel impact cela aurait sur votre croissance ?",
                "need": "Un outil qui automatise tout ça et s'intègre à vos existants, ça réglerait le problème ?",
            },
            "nudges": [
                "Trial sans friction : pas de CB pour commencer",
                "Cas clients du même secteur avec ROI chiffré",
                "Onboarding guidé en moins de 5 minutes",
                "Urgence : 'Offre de lancement à -40% jusqu'au [date]'",
                "Témoignages vidéo d'entrepreneurs reconnus",
            ],
        },
    ],
    "service": [
        {
            "name": "Isabelle Moreau", "age": 45, "job": "Cadre en reconversion",
            "location": "Nantes, France",
            "quote": "J'ai 20 ans d'expérience à valoriser. Il me faut juste le bon accompagnement.",
            "goals": ["Valoriser mon expertise en ligne", "Créer des revenus complémentaires stables", "Gagner en liberté et flexibilité"],
            "painPoints": ["Peur de la technologie et du marketing digital", "Syndrome de l'imposteur", "Manque de réseau dans le digital"],
            "channels": ["LinkedIn", "Email", "Podcasts"],
            "buyingTriggers": ["Accompagnement humain", "Résultats progressifs visibles", "Communauté de pairs"],
            "soncas": {
                "Sécurité": "Besoin d'un cadre rassurant et d'un accompagnement pas à pas.",
                "Orgueil": "Veut être reconnue pour son expertise de 20 ans.",
                "Nouveauté": "Ouverte au digital si expliqué simplement.",
                "Confort": "Interface claire, support téléphonique apprécié.",
                "Argent": "Prête à investir si ROI clair et délai réaliste.",
                "Sympathie": "Cherche une relation de confiance, pas une transaction.",
            },
            "aida": {
                "attention": "Post LinkedIn sur la reconversion réussie d'un profil similaire.",
                "interest": "Contenu éducatif sur comment monétiser son expertise.",
                "desire": "Programme structuré avec accompagnement humain et communauté.",
                "action": "Appel découverte gratuit de 30 minutes avec un expert.",
            },
            "spin": {
                "situation": "Vous avez 20 ans d'expérience. Comment valorisez-vous cette expertise aujourd'hui ?",
                "problem": "Qu'est-ce qui vous a empêché jusqu'ici de lancer votre activité en ligne ?",
                "implication": "Si vous attendez encore 1 an, qu'est-ce que vous risquez de perdre ?",
                "need": "Un programme qui vous prend par la main de A à Z, c'est ce qu'il vous faudrait ?",
            },
            "nudges": [
                "Autorité : 'Fondé par des experts avec 15 ans d'expérience'",
                "Preuve sociale : 'Rejoignez 2 400 reconvertis accompagnés'",
                "Urgence douce : 'Prochaine cohorte démarre le [date]'",
                "Réciprocité : webinaire gratuit de valeur avant toute vente",
            ],
        },
    ],
    "default": [
        {
            "name": "Marie Legrand", "age": 35, "job": "Entrepreneur indépendant",
            "location": "France",
            "quote": "Je cherche des solutions concrètes qui m'aident à avancer rapidement.",
            "goals": ["Gagner du temps sur les tâches répétitives", "Développer son activité de façon autonome", "Avoir des résultats mesurables"],
            "painPoints": ["Manque de temps et de ressources", "Trop d'options, pas assez de clarté", "Difficulté à mesurer le ROI"],
            "channels": ["Instagram", "LinkedIn", "Google"],
            "buyingTriggers": ["Résultats prouvés", "Simplicité d'utilisation", "Rapport qualité/prix"],
            "soncas": {
                "Sécurité": "Rassurée par les garanties, avis certifiés et politique de remboursement.",
                "Orgueil": "Veut des solutions qui font la différence et montrent son professionnalisme.",
                "Nouveauté": "Curieuse des nouvelles approches si elles sont pragmatiques.",
                "Confort": "Apprécie une prise en main intuitive et un support réactif.",
                "Argent": "Sensible au ROI démontrable et aux offres d'entrée de gamme.",
                "Sympathie": "Fidèle aux marques authentiques qui comprennent son quotidien.",
            },
            "aida": {
                "attention": "Contenu qui parle directement de son problème quotidien avec un chiffre impactant.",
                "interest": "Démonstration concrète du bénéfice avec avant/après ou cas d'usage.",
                "desire": "Témoignages de profils similaires et offre personnalisée.",
                "action": "CTA clair avec essai gratuit ou garantie satisfait ou remboursé.",
            },
            "spin": {
                "situation": "Comment gérez-vous actuellement ce défi au quotidien ?",
                "problem": "Quelles sont les principales difficultés avec votre solution actuelle ?",
                "implication": "Ces difficultés ont-elles un impact sur votre croissance ou rentabilité ?",
                "need": "Si vous pouviez résoudre ce problème facilement, comment cela changerait votre activité ?",
            },
            "nudges": [
                "Preuve sociale : nombre d'utilisateurs actifs",
                "Ancrage : comparer au coût de ne rien faire",
                "Urgence : offre limitée dans le temps",
                "Réciprocité : contenu gratuit de valeur avant l'achat",
                "Cohérence : micro-engagements progressifs",
                "Autorité : certifications, partenariats reconnus",
            ],
        },
    ],
}

EXTRA_PERSONAS = [
    {
        "name": "Lucas Bernard", "age": 24, "job": "Étudiant / Side-hustler",
        "location": "Toulouse, France",
        "quote": "Je veux lancer mon projet avec un budget minimal mais des résultats max.",
        "goals": ["Monétiser une passion", "Apprendre en faisant", "Atteindre l'indépendance financière"],
        "painPoints": ["Budget très limité", "Manque d'expérience business", "Temps fragmenté entre études et projet"],
        "channels": ["TikTok", "YouTube", "Discord"],
        "buyingTriggers": ["Offre freemium", "Communauté active", "Tutoriels inclus"],
        "soncas": {
            "Sécurité": "Rassurer sur le risque financier minimal.",
            "Orgueil": "Valoriser le fait de créer quelque chose de soi.",
            "Nouveauté": "Attirer avec les dernières tendances et outils.",
            "Confort": "Interface simple, pas de courbe d'apprentissage.",
            "Argent": "Très sensible au prix, cherche les plans gratuits.",
            "Sympathie": "Apprécie les communautés bienveillantes.",
        },
        "aida": {
            "attention": "TikTok ou Reel montrant le résultat en 30 secondes.",
            "interest": "Tutoriel étape par étape avec résultat concret.",
            "desire": "Success story d'un profil similaire (jeune, même budget).",
            "action": "Plan gratuit ou essai sans engagement.",
        },
        "spin": {
            "situation": "Tu travailles sur ton projet à côté de tes études. Comment tu t'organises ?",
            "problem": "C'est quoi le plus gros blocage qui t'empêche d'avancer ?",
            "implication": "Si tu ne règles pas ça maintenant, dans 6 mois tu seras où ?",
            "need": "Si je te montre comment faire ça gratuitement en 1 semaine, tu passes à l'action ?",
        },
        "nudges": [
            "Gamification : badges et niveaux de progression",
            "Communauté : forum d'entraide entre utilisateurs",
            "Quick win : résultat visible en moins de 15 minutes",
            "FOMO : 'X personnes ont lancé leur projet ce mois-ci'",
        ],
    },
    {
        "name": "Antoine Petit", "age": 52, "job": "Chef d'entreprise (TPE)",
        "location": "Marseille, France",
        "quote": "Je veux déléguer ce que je ne comprends pas et me concentrer sur mon cœur de métier.",
        "goals": ["Augmenter le CA sans augmenter la charge de travail", "Digitaliser son activité", "Trouver de nouveaux clients"],
        "painPoints": ["Pas de temps pour le marketing", "Méfiance envers les prestataires digitaux", "ROI difficile à mesurer"],
        "channels": ["Téléphone", "Email", "Google (recherche)"],
        "buyingTriggers": ["Références clients dans son secteur", "Contrat simple et transparent", "Résultats mesurables"],
        "soncas": {
            "Sécurité": "Contrat clair, pas de mauvaise surprise, résiliation possible.",
            "Orgueil": "Veut être le leader dans son domaine local.",
            "Nouveauté": "Peu attiré par la nouveauté, préfère le prouvé.",
            "Confort": "Délègue tout, ne veut pas être impliqué dans le technique.",
            "Argent": "Raisonne en CA généré vs coût de la prestation.",
            "Sympathie": "Préfère travailler avec des gens qu'il apprécie et qui le comprennent.",
        },
        "aida": {
            "attention": "Cas client dans son secteur avec CA généré mentionné.",
            "interest": "Présentation du processus, de ce qu'il n'a pas à faire.",
            "desire": "Audit gratuit de sa situation actuelle avec recommandations.",
            "action": "Rendez-vous téléphonique pour présenter une proposition sur mesure.",
        },
        "spin": {
            "situation": "Comment trouvez-vous vos nouveaux clients actuellement ?",
            "problem": "Êtes-vous satisfait du volume et de la qualité des prospects que vous générez ?",
            "implication": "Si vous n'optimisez pas votre acquisition maintenant, quel impact sur votre CA dans 2 ans ?",
            "need": "Un système clé en main qui génère des leads qualifiés pendant que vous vous concentrez sur votre métier, ça vous intéresse ?",
        },
        "nudges": [
            "Référence sectorielle : client connu dans son domaine",
            "Garantie résultats ou remboursé",
            "Simplicité : 'Vous n'avez rien à faire, on gère tout'",
            "Urgence douce : 'Calendrier presque complet, 1 place disponible'",
        ],
    },
    {
        "name": "Camille Dumont", "age": 29, "job": "Créatrice de contenu / Influenceuse micro",
        "location": "Bordeaux, France",
        "quote": "Mon audience me fait confiance. Je veux lui proposer uniquement ce qui vaut vraiment le coup.",
        "goals": ["Monétiser son audience de façon authentique", "Trouver des partenaires alignés avec ses valeurs", "Automatiser ses revenus"],
        "painPoints": ["Propositions de partenariats non alignés", "Revenus irréguliers et imprévisibles", "Peu de temps pour les négociations commerciales"],
        "channels": ["Instagram", "TikTok", "Newsletter"],
        "buyingTriggers": ["Alignement de valeurs", "Exclusivité ou accès privilégié", "Commission transparente"],
        "soncas": {
            "Sécurité": "Veut des partenariats stables et des revenus prévisibles.",
            "Orgueil": "Tient à son authenticité et à la qualité de ce qu'elle recommande.",
            "Nouveauté": "Intéressée par les nouveaux formats et tendances contenu.",
            "Confort": "Apprécie les outils simples et automatisés.",
            "Argent": "Veut des commissions justes et des paiements réguliers.",
            "Sympathie": "Préfère les marques qui la traitent comme un partenaire, pas un canal.",
        },
        "aida": {
            "attention": "Message personnalisé montrant qu'on a vraiment regardé son contenu.",
            "interest": "Proposition de valeur claire et chiffres de performance transparents.",
            "desire": "Produit ou service qu'elle utiliserait vraiment, avec liberté créative.",
            "action": "Offre d'essai exclusif avant la collaboration officielle.",
        },
        "spin": {
            "situation": "Comment sélectionnez-vous les produits que vous recommandez à votre audience ?",
            "problem": "Avez-vous déjà recommandé quelque chose qui a déçu votre audience ?",
            "implication": "Un mauvais partenariat peut éroder la confiance de vos abonnés — comment vous en prémunissez-vous ?",
            "need": "Si on vous propose un produit que vous adorez vraiment, avec liberté totale sur le contenu, vous seriez partante ?",
        },
        "nudges": [
            "Exclusivité : code promo dédié et suivi personnalisé",
            "Social proof : 'Vos pairs X et Y utilisent déjà notre produit'",
            "Autonomie : liberté créative totale sur le contenu",
            "Réciprocité : envoyer le produit gratuitement avant toute décision",
        ],
    },
    {
        "name": "Nadia Benali", "age": 41, "job": "Directrice achats (grande entreprise)",
        "location": "Paris, France",
        "quote": "Je cherche des solutions éprouvées qui minimisent les risques pour mon entreprise.",
        "goals": ["Réduire les coûts opérationnels", "Gagner en efficacité sur les process d'achat", "Satisfaire ses équipes avec de bons outils"],
        "painPoints": ["Processus de validation interne longs", "Risque de choix d'un mauvais fournisseur", "Justifier le ROI auprès de la direction"],
        "channels": ["LinkedIn", "Email professionnel", "Salons et événements B2B"],
        "buyingTriggers": ["Références d'entreprises similaires", "Démo sur mesure + POC", "Support dédié et SLA"],
        "soncas": {
            "Sécurité": "Processus d'achat rigoureux, certifications, conformité RGPD.",
            "Orgueil": "Veut être reconnue comme quelqu'un qui choisit les meilleures solutions.",
            "Nouveauté": "Intéressée si la nouveauté est prouvée et documentée.",
            "Confort": "Intégration fluide avec les systèmes existants.",
            "Argent": "Budget défini en amont, optimisation du TCO (Total Cost of Ownership).",
            "Sympathie": "Apprécie les commerciaux qui comprennent son métier.",
        },
        "aida": {
            "attention": "White paper ou étude de cas d'une entreprise du même secteur.",
            "interest": "Présentation ROI avec chiffres mesurables sur 12-24 mois.",
            "desire": "Proof of Concept (POC) de 30 jours avec métriques définies.",
            "action": "Appel avec le directeur technique et l'équipe commerciale simultanément.",
        },
        "spin": {
            "situation": "Comment gérez-vous actuellement ce process dans votre organisation ?",
            "problem": "Quels sont les principaux blocages qui ralentissent votre équipe ?",
            "implication": "Ces inefficacités représentent combien de temps et d'argent perdu par an ?",
            "need": "Si on pouvait réduire ce coût de 30% en 6 mois, ça justifierait une évaluation approfondie ?",
        },
        "nudges": [
            "Autorité : certifications ISO, labels de sécurité",
            "Preuve : liste de références dans son secteur",
            "Risque réduit : POC gratuit de 30 jours",
            "Engagement progressif : contrat modulable et résiliable",
        ],
    },
]


def _fetch_random_users(count: int) -> list:
    """
    Génère des données utilisateur synthétiques sans API externe.
    Utilise DiceBear Avatars (open-source, gratuit, sans clé) pour les photos.
    """
    FIRST_NAMES = ["Alex","Sophie","Marc","Julie","Thomas","Emma","Lucas","Léa",
                   "Nicolas","Chloé","Antoine","Manon","Romain","Inès","Baptiste","Camille"]
    LAST_NAMES  = ["Martin","Bernard","Dubois","Thomas","Robert","Richard","Petit","Durand",
                   "Leroy","Moreau","Simon","Laurent","Lefebvre","Michel","Garcia","David"]
    CITIES      = ["Paris","Lyon","Marseille","Bordeaux","Nantes","Toulouse","Strasbourg","Nice"]
    import random, hashlib
    users = []
    for i in range(count):
        first = FIRST_NAMES[i % len(FIRST_NAMES)]
        last  = LAST_NAMES[(i * 3) % len(LAST_NAMES)]
        city  = CITIES[i % len(CITIES)]
        seed  = hashlib.md5(f"{first}{last}{i}".encode()).hexdigest()[:10]
        # DiceBear open-source avatar API — no key, no rate limit, MIT license
        avatar_style = ["avataaars", "personas", "micah", "adventurer"][i % 4]
        photo_url = f"https://api.dicebear.com/7.x/{avatar_style}/svg?seed={seed}&backgroundColor=b6e3f4,c0aede,d1d4f9"
        users.append({
            "name":     {"first": first, "last": last},
            "location": {"city": city},
            "picture":  {"large": photo_url},
        })
    return users


async def generate_personas(activity_type: str, goal: str, maturity: str) -> list:
    class _D:
        pass
    data = _D()
    data.activityType = activity_type
    data.goal = goal
    data.maturity = maturity
    # Deep copy to prevent mutation of the module-level template cache
    template_key = data.activityType if data.activityType in PERSONA_TEMPLATES else "default"
    base_personas: list = copy.deepcopy(PERSONA_TEMPLATES[template_key])
    extra_personas: list = copy.deepcopy(EXTRA_PERSONAS)

    all_personas = base_personas + extra_personas
    all_personas = all_personas[:5]

    random_users = _fetch_random_users(len(all_personas))

    for i, persona in enumerate(all_personas):
        persona["id"] = f"persona-{i + 1}"
        if i < len(random_users):
            user = random_users[i]
            persona["photo"] = user["picture"]["large"]
        else:
            persona["photo"] = (
                f"https://api.dicebear.com/7.x/avataaars/svg?seed={persona['name'].replace(' ', '_')}"
            )

    return all_personas
