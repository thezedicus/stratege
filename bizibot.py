"""
bizibot.py — IA conversationnelle locale BiziApp v5.4
Chatbot français pour micro-entrepreneurs et dirigeants TPE/PME

Architecture :
  - Moteur de matching basé sur mots-cles + TF-IDF simplifié
  - Base de connaissances locale (aucune API externe)
  - Contexte utilisateur injecté (secteur, objectif, analyse SWOT)
  - Réponses personnalisées selon le profil
  - Historique de conversation en session_state
"""

import re as _re
import math as _math

# ══════════════════════════════════════════════════════════════════════════
# BASE DE CONNAISSANCES — 80+ sujets couverts en français
# Format : { "topic": { "patterns": [...], "response": "...", "followups": [...] } }
# ══════════════════════════════════════════════════════════════════════════

_KB = {
    # ── SWOT ──────────────────────────────────────────────────────────────
    "swot": {
        "patterns": ["swot", "forces", "faiblesses", "opportunités", "menaces",
                     "analyse swot", "diagnostic", "atouts", "points forts", "points faibles"],
        "response": """**Votre analyse SWOT** structure votre réflexion en 4 quadrants :

**Forces** — ce que vous faites mieux que vos concurrents
**Faiblesses** — ce que vous devez améliorer en priorité
**Opportunités** — les tendances de marché à saisir maintenant
**Menaces** — les risques à anticiper

💡 **Conseil** : Concentrez-vous sur 2 forces à maximiser et 1 faiblesse critique à corriger. Ne cherchez pas à tout faire en même temps.""",
        "followups": ["Comment améliorer mes forces ?", "Que faire face aux menaces ?", "Comment saisir les opportunités ?"]
    },
    # ── ACQUISITION CLIENTS ───────────────────────────────────────────────
    "acquisition": {
        "patterns": ["trouver des clients", "acquisition", "prospecter", "leads", "prospects",
                     "nouveaux clients", "comment trouver", "attirer", "générer des leads",
                     "premier client", "clientèle", "comment vendre"],
        "response": """**Trouver vos premiers clients** — les 3 étapes essentielles :

**1. Définir votre cible précisément**
Ne ciblez pas "tout le monde". Choisissez un profil : secteur, taille, problème précis.

**2. Aller là où ils sont**
- B2B → LinkedIn, salons professionnels, réseau personnel
- B2C → Instagram, Google (SEO local), bouche-à-oreille

**3. Faire une offre irrésistible**
- Commencez par un service de test à prix réduit
- Ou offrez un audit/diagnostic gratuit de 30 min

💡 **Action immédiate** : Contactez 10 personnes de votre réseau aujourd'hui et expliquez ce que vous faites. C'est votre source de clients #1 au démarrage.""",
        "followups": ["Quel canal choisir en priorité ?", "Comment faire une offre de lancement ?", "Comment prospecter sur LinkedIn ?"]
    },
    # ── MARKETING ─────────────────────────────────────────────────────────
    "marketing": {
        "patterns": ["marketing", "communication", "visibilité", "réseaux sociaux", "publicité",
                     "contenu", "stratégie marketing", "plan marketing", "facebook", "instagram",
                     "linkedin", "tiktok", "youtube", "email marketing", "newsletter"],
        "response": """**Stratégie marketing pour votre activité** :

**Règle d'or** : choisissez 1 seul canal et maîtrisez-le pendant 90 jours.

**Selon votre cible :**
- **Particuliers (B2C)** → Instagram, Facebook, TikTok, Google
- **Professionnels (B2B)** → LinkedIn, email, événements
- **Local** → Google My Business, bouche-à-oreille, partenariats locaux

**Budget limité ?** Commencez par le contenu gratuit (posts, articles, vidéos) avant d'investir en pub.

💡 **La formule gagnante** : 1 post/jour sur 1 réseau + 1 newsletter/semaine + 1 article SEO/mois = croissance organique solide en 6 mois.""",
        "followups": ["Quel contenu créer pour ma cible ?", "Comment faire de la publicité avec un petit budget ?", "Comment construire ma newsletter ?"]
    },
    # ── SEO ───────────────────────────────────────────────────────────────
    "seo": {
        "patterns": ["seo", "référencement", "google", "visibilité google", "mots-clés",
                     "apparaître sur google", "classement google", "recherche organique",
                     "site web", "blog", "contenu seo"],
        "response": """**Le SEO pour votre activité** — apparaître sur Google sans payer :

**Les 3 piliers du SEO :**
1. **Contenu** — créez des articles qui répondent aux vraies questions de vos clients
2. **Technique** — votre site doit être rapide, sécurisé (HTTPS) et mobile-friendly
3. **Autorité** — obtenez des liens d'autres sites vers le vôtre

**Pour commencer :**
- Créez 1 article par semaine sur des mots-clés longue traîne
- Optimisez votre fiche Google Business si vous avez une activité locale
- Assurez-vous que chaque page a un titre H1 et une meta description

💡 **Résultats** : le SEO prend 3-6 mois. Commencez maintenant, vous récolterez les fruits dans 6 mois.""",
        "followups": ["Comment trouver les bons mots-clés ?", "Comment optimiser ma page Google Business ?", "Combien d'articles dois-je écrire ?"]
    },
    # ── PRIX / TARIFICATION ───────────────────────────────────────────────
    "prix": {
        "patterns": ["prix", "tarif", "tarification", "combien facturer", "devis", "tarifs",
                     "pricing", "grille tarifaire", "trop cher", "augmenter mes prix",
                     "positionnement prix", "comment fixer"],
        "response": """**Comment fixer vos prix** — sans vous sous-vendre :

**Les erreurs à éviter :**
- Calculer uniquement vos coûts (vous oubliez votre valeur)
- Copier les prix des concurrents sans analyser votre positionnement
- Baisser vos prix pour conclure — cela attire de mauvais clients

**La méthode en 3 étapes :**
1. **Calculez votre coût réel** : temps × taux horaire + frais
2. **Étudiez le marché** : fourchette basse, médiane, premium
3. **Positionnez-vous** : entrée de gamme, milieu de gamme, ou premium

**Règle d'or** : si plus de 80% de vos prospects acceptent votre prix sans négocier, vous êtes trop bon marché.

💡 **Testez une augmentation de 20-30%** sur vos prochaines propositions et observez le taux d'acceptation.""",
        "followups": ["Comment justifier des prix plus élevés ?", "Comment créer des packages ?", "Comment négocier avec les clients ?"]
    },
    # ── BUSINESS PLAN ─────────────────────────────────────────────────────
    "business_plan": {
        "patterns": ["business plan", "plan d affaires", "prévisionnel", "projet", "lancer",
                     "créer mon entreprise", "auto-entrepreneur", "micro-entrepreneur",
                     "se lancer", "démarrer", "création entreprise", "statut juridique"],
        "response": """**Créer votre entreprise** — les étapes clés :

**1. Validez votre idée (avant tout)**
Parlez à 10 personnes de votre cible. Sont-elles prêtes à payer ?

**2. Choisissez votre statut**
- **Micro-entrepreneur** : idéal pour démarrer, simple, CA limité
- **SASU/EURL** : si vous anticipez un CA important ou des risques
- **Portage salarial** : pour les consultants qui veulent tester sans créer de structure

**3. Les 5 éléments de votre business plan :**
- Offre et cible
- Modèle économique (comment vous gagnez de l'argent)
- Plan d'acquisition clients
- Prévisionnel financier sur 3 ans
- Besoins en financement

💡 **Conseil** : N'attendez pas un business plan parfait pour démarrer. Testez d'abord, structurez ensuite.""",
        "followups": ["Quel statut juridique choisir ?", "Comment faire un prévisionnel ?", "Comment se faire financer ?"]
    },
    # ── FINANCEMENT ───────────────────────────────────────────────────────
    "financement": {
        "patterns": ["financement", "crédit", "prêt", "banque", "subvention", "aide",
                     "bpifrance", "aide création", "investisseur", "levée de fonds",
                     "budget", "trésorerie", "cash flow"],
        "response": """**Les financements disponibles pour votre projet** :

**Aides et subventions (à chercher en premier) :**
- **ACRE** : exonération de charges les premières années
- **ARCE** : convertir vos allocations chômage en capital
- **Aides régionales** : variables selon votre région (cherchez sur votre portail régional)
- **BPI France** : prêts d'honneur et garanties bancaires

**Prêts bancaires :**
- Prêt professionnel classique (nécessite un business plan solide)
- Microcrédit professionnel (jusqu'à 12 000€ via l'ADIE)

**Alternatives :**
- Crowdfunding (Ulule, KissKissBankBank) pour les projets avec communauté
- Love money (famille, amis) pour les tout débuts
- Clients comme premiers financeurs (prépayez des abonnements)

💡 **Commencez par les aides** avant de solliciter des prêts — c'est de l'argent que vous ne remboursez pas.""",
        "followups": ["Comment obtenir un prêt bancaire ?", "Quelles aides pour les auto-entrepreneurs ?", "Comment faire un prévisionnel pour la banque ?"]
    },
    # ── FIDÉLISATION ──────────────────────────────────────────────────────
    "fidelisation": {
        "patterns": ["fidélisation", "garder mes clients", "rétention", "churns", "clients qui partent",
                     "programme fidélité", "satisfaction client", "nps", "avis clients",
                     "récurrence", "abonnement"],
        "response": """**Fidéliser vos clients** — votre levier de croissance le plus rentable :

**Pourquoi c'est prioritaire :**
Garder un client existant coûte 5x moins cher qu'en acquérir un nouveau.

**Les 4 leviers de fidélisation :**
1. **Qualité irréprochable** : sous-promettez, sur-livrez
2. **Suivi proactif** : contactez vos clients sans attendre qu'ils vous contactent
3. **Programme de récompenses** : offres exclusives, accès prioritaire, réductions
4. **Communauté** : créez un espace d'échange entre vos clients (groupe privé, événements)

**Mesurez votre fidélisation :**
- NPS (Net Promoter Score) : "De 0 à 10, recommanderiez-vous nos services ?"
- Taux de rétention : % de clients qui restent d'une période à l'autre
- LTV : valeur totale d'un client sur toute sa durée de vie

💡 **Action immédiate** : Appelez vos 5 meilleurs clients cette semaine pour leur demander comment vous pouvez mieux les servir.""",
        "followups": ["Comment calculer mon NPS ?", "Comment créer un programme de fidélité ?", "Comment réduire le churn ?"]
    },
    # ── CONCURRENCE ───────────────────────────────────────────────────────
    "concurrence": {
        "patterns": ["concurrents", "concurrence", "différenciation", "se différencier",
                     "avantage concurrentiel", "unique", "usp", "proposition de valeur",
                     "benchmark", "comparaison", "marché concurrentiel"],
        "response": """**Face à la concurrence** — comment vous différencier vraiment :

**Ne pas copier vos concurrents** : c'est la première règle.

**Les 5 axes de différenciation :**
1. **La spécialisation** : être le meilleur dans une niche précise
2. **L'expérience client** : service irréprochable avant, pendant, après
3. **La rapidité** : livrer plus vite que tout le monde
4. **Le prix** : le moins cher OU le plus premium (jamais le milieu)
5. **La relation** : humaniser votre marque, créer du lien authentique

**Trouvez votre USP (Unique Selling Proposition) :**
Complétez cette phrase : "Je suis le seul à _______ pour _______ qui veulent _______"

💡 **Exemple** : "Je suis la seule à créer des sites web express en 5 jours pour des coachs qui veulent se lancer vite sans se ruiner."

Votre USP doit tenir en 1 phrase et être comprise en 5 secondes.""",
        "followups": ["Comment analyser mes concurrents ?", "Comment créer mon USP ?", "Comment me positionner sur un marché saturé ?"]
    },
    # ── RÉSEAUX SOCIAUX ───────────────────────────────────────────────────
    "reseaux_sociaux": {
        "patterns": ["réseaux sociaux", "instagram", "linkedin", "facebook", "tiktok",
                     "youtube", "twitter", "x", "pinterest", "snapchat", "social media",
                     "community manager", "contenu", "posts", "stories", "reels"],
        "response": """**Stratégie réseaux sociaux** pour votre activité :

**Choisissez 1 réseau principal** selon votre cible :
- **Instagram / TikTok** : cibles jeunes, produits visuels, B2C lifestyle
- **LinkedIn** : B2B, conseil, services professionnels, recrutement
- **Facebook** : cibles 35-55 ans, communautés locales, groupes de niche
- **YouTube / Pinterest** : contenu éducatif, recherche d'inspiration

**La règle des 3 types de contenu :**
- 60% de valeur (conseils, tutoriels, astuces)
- 30% de coulisses (comment vous travaillez, votre équipe)
- 10% de vente (offres, témoignages, promo)

**Fréquence réaliste :**
- 3-5 posts/semaine sur votre réseau principal
- Régularité > quantité : mieux vaut 3 posts/semaine pendant 6 mois que 10 posts/semaine pendant 3 semaines

💡 **Outil gratuit** : Canva pour créer vos visuels en 5 minutes sans designer.""",
        "followups": ["Comment créer du contenu rapidement ?", "Comment augmenter mon engagement ?", "Comment convertir mes abonnés en clients ?"]
    },
    # ── PRODUCTIVITÉ / ORGANISATION ───────────────────────────────────────
    "productivite": {
        "patterns": ["productivité", "organisation", "gestion du temps", "procrastination",
                     "automatisation", "outils", "efficacité", "priorités", "planning",
                     "agenda", "routine", "workflow", "déléguer"],
        "response": """**Productivité pour entrepreneurs** — faire plus avec moins :

**La règle 80/20 (Pareto) :**
20% de vos actions génèrent 80% de vos résultats. Identifiez-les et concentrez-vous dessus.

**La méthode en 3 blocs quotidiens :**
1. **Matin (focus)** : travail profond sans interruptions (2-3h)
2. **Après-midi (communication)** : emails, appels, réunions
3. **Fin de journée (planification)** : préparez le lendemain en 15 min

**Outils gratuits incontournables :**
- **Notion** : organisation, notes, projets
- **Trello** : gestion de projet visuelle
- **Calendly** : prise de RDV automatisée
- **Zapier** (limité gratuit) : automatisations

💡 **Ce que vous devez déléguer en premier** : comptabilité, réseaux sociaux, service client récurrent. Votre temps vaut trop cher pour des tâches à faible valeur ajoutée.""",
        "followups": ["Quels outils utiliser pour automatiser ?", "Comment déléguer efficacement ?", "Comment gérer mes emails sans perdre de temps ?"]
    },
    # ── COMPTABILITÉ / GESTION FINANCIÈRE ────────────────────────────────
    "comptabilite": {
        "patterns": ["comptabilité", "charges", "impôts", "urssaf", "tva", "bénéfice",
                     "chiffre d affaires", "facturation", "devis", "trésorerie", "bilan",
                     "compte bancaire", "expert-comptable", "cotisations"],
        "response": """**Gestion financière** pour micro-entrepreneur :

**Les bases indispensables :**
- **Compte bancaire dédié** : n'utilisez jamais votre compte perso pour l'activité
- **Facturez dès la livraison** : ne laissez jamais de délai de paiement >30 jours
- **Mettez de côté les charges** : 25-30% de votre CA pour les cotisations et impôts

**En micro-entreprise :**
- Cotisations URSSAF : 12,8% (vente) / 22% (services) de votre CA
- Impôts : inclus dans le versement libératoire OU déclaration classique
- TVA : exonéré en dessous des seuils (91 500€ vente / 36 800€ services)

**Outils gratuits :**
- **Indy** ou **Pennylane** : comptabilité simplifiée auto-entrepreneur
- **Shine** : compte pro avec comptabilité intégrée (6€/mois)

💡 **Conseil d'or** : Consultez un expert-comptable au moins une fois par an. Une heure de conseil vous fera économiser des milliers d'euros.""",
        "followups": ["Comment gérer ma trésorerie ?", "Comment facturer mes clients ?", "Quand dois-je passer à la TVA ?"]
    },
    # ── EMAIL MARKETING ───────────────────────────────────────────────────
    "email_marketing": {
        "patterns": ["email", "newsletter", "emailing", "liste email", "mailing list",
                     "mailchimp", "brevo", "campagne email", "séquence email",
                     "automation email", "taux d ouverture"],
        "response": """**Email marketing** — votre actif le plus rentable :

**Pourquoi l'email > les réseaux sociaux :**
- Vos abonnés sont à vous (pas soumis aux algorithmes)
- Taux d'ouverture moyen : 20-25% vs 3-5% sur les réseaux
- ROI moyen : 42€ pour 1€ investi

**Construire votre liste :**
- Lead magnet gratuit (guide PDF, checklist, audit offert)
- Formulaire sur votre site
- Pop-up de sortie (avant que le visiteur quitte)

**La séquence de bienvenue (automatique) :**
1. Email J0 : Votre cadeau + qui vous êtes
2. Email J2 : Votre histoire + pourquoi vous faites ce métier
3. Email J4 : Votre méthode / approche unique
4. Email J7 : Témoignage client + appel à l'action

**Outils gratuits :** Brevo (ex-Sendinblue), Mailchimp, Systeme.io

💡 **Fréquence idéale** : 1 email/semaine. Ni trop (vous épuisez), ni trop peu (vous oubliez).""",
        "followups": ["Comment créer un lead magnet ?", "Quel outil email choisir ?", "Comment améliorer mon taux d'ouverture ?"]
    },
    # ── SALARIES / RECRUTEMENT ────────────────────────────────────────────
    "recrutement": {
        "patterns": ["recruter", "salarié", "embaucher", "recrutement", "contrat",
                     "cdd", "cdi", "alternance", "stage", "freelance", "sous-traitance",
                     "prestataire", "équipe", "premier employé"],
        "response": """**Recruter votre premier collaborateur** :

**Avant de recruter un salarié, explorez d'abord :**
- **Freelance** : idéal pour les missions ponctuelles (Malt, Fiverr, LinkedIn)
- **Alternant** : 0€ de charges dans certains cas (aide gouvernementale)
- **Stagiaire** : gratification minimale (~600€/mois pour 6 mois)
- **Portage salarial** : le freelance est salarié d'une société tierce, vous payez une facture

**Si vous recrutez un salarié :**
- CDI : +50% de coût en plus du salaire brut (charges patronales)
- CDD : même coût, mais durée limitée et renouvellement limité
- Aide à l'embauche : renseignez-vous sur les aides actuelles (France Travail, PMSM)

**Ce que vous devez déléguer en premier :**
1. Tâches administratives
2. Réseaux sociaux / contenu
3. Service client récurrent

💡 **Règle** : Recrutez quand vous refusez des clients faute de temps, pas avant.""",
        "followups": ["Comment trouver un bon freelance ?", "Quel contrat choisir ?", "Comment intégrer un nouveau collaborateur ?"]
    },
    # ── DÉVELOPPEMENT PERSONNEL ───────────────────────────────────────────
    "developpement_perso": {
        "patterns": ["motivation", "confiance", "peur", "doute", "syndrome imposteur",
                     "burnout", "stress", "mental", "bien-être", "développement personnel",
                     "mindset", "resilience", "objectifs"],
        "response": """**Le mindset de l'entrepreneur** — ce que personne ne vous dit :

**Le syndrome de l'imposteur est universel :**
95% des entrepreneurs le vivent. Même les plus grands. Ce n'est pas un signe d'incompétence, c'est un signe que vous sortez de votre zone de confort.

**Les vraies difficultés du premier an :**
- Solitude décisionnelle
- Irrégularité des revenus
- Doute permanent
- Jugement des proches

**Comment traverser ces moments :**
1. Entourez-vous d'autres entrepreneurs (réseaux, meetups, Slack)
2. Célébrez les petites victoires
3. Mesurez vos progrès (pas juste le CA)
4. Acceptez l'erreur comme outil d'apprentissage

**La vérité** : les entrepreneurs qui réussissent ne sont pas ceux qui doutent le moins, mais ceux qui agissent malgré le doute.

💡 **Action** : Rejoignez un groupe d'entrepreneurs en ligne (Facebook, Slack, Discord). La communauté est votre meilleur antidote à la solitude entrepreneuriale.""",
        "followups": ["Comment dépasser le syndrome de l'imposteur ?", "Comment gérer le stress entrepreneurial ?", "Comment fixer mes objectifs ?"]
    },
    # ── INSTAGRAM ─────────────────────────────────────────────────────────
    "instagram": {
        "patterns": ["instagram", "insta", "reels", "stories instagram", "feed instagram",
                     "bio instagram", "croître sur instagram", "abonnés instagram"],
        "response": """**Instagram pour votre activité** — la stratégie qui fonctionne en 2025 :

**Ce qui marche vraiment :**
- **Reels** : portée organique 3-5x supérieure aux photos
- **Stories quotidiennes** : maintenir le lien avec votre communauté
- **Carousel** (plusieurs images) : excellent pour l'éducation et les conseils

**Votre bio parfaite :**
Ligne 1 : Qui vous servez
Ligne 2 : Ce que vous leur apportez
Ligne 3 : Preuve sociale ou CTA
Lien : vers votre site ou un lien multipage (Linktree)

**Fréquence recommandée :**
- 3-5 Reels/semaine
- Stories quotidiennes (5-10/jour)
- 2-3 posts carousel/mois

💡 **Secret** : les 50 premiers commentaires dans l'heure suivant la publication = l'algorithme booste votre post. Engagez votre communauté rapidement après publication.""",
        "followups": ["Comment créer un Reel qui fonctionne ?", "Comment trouver des idées de contenu ?", "Comment passer de 0 à 1000 abonnés ?"]
    },
    # ── LINKEDIN ──────────────────────────────────────────────────────────
    "linkedin": {
        "patterns": ["linkedin", "profil linkedin", "posts linkedin", "réseau professionnel",
                     "b2b linkedin", "prospection linkedin", "ssi linkedin"],
        "response": """**LinkedIn pour trouver des clients B2B** — la méthode en 2025 :

**Votre profil doit convertir :**
- Photo professionnelle (pas de selfie)
- Titre : pas votre poste, mais la valeur que vous apportez
- À propos : racontez votre histoire + résultats clients + CTA

**La stratégie de contenu qui fonctionne :**
- 3 posts/semaine : 1 conseil, 1 témoignage/cas client, 1 backstage
- Commentez 10 posts de votre cible chaque jour (visibilité gratuite)
- Publiez aux meilleures heures : mardi-jeudi, 8h-10h ou 17h-19h

**Prospection directe (DM) :**
1. Demandez la connexion sans message (acceptation +60%)
2. Attendez 2-3 jours
3. Envoyez un message personnalisé (pas un copier-coller)
4. Apportez de la valeur avant de vendre

💡 **Outil gratuit** : LinkedIn SSI (Social Selling Index) pour mesurer votre influence. Tapez "LinkedIn SSI" dans Google.""",
        "followups": ["Comment écrire un post LinkedIn viral ?", "Comment prospecter sans être intrusif ?", "Comment optimiser mon profil LinkedIn ?"]
    },
    # ── GÉNÉRALISTE ───────────────────────────────────────────────────────
    "aide_generale": {
        "patterns": ["aide", "help", "comment", "quoi faire", "par où commencer",
                     "que faire", "conseil", "besoin d aide", "perdu", "je ne sais pas"],
        "response": """**Je suis BizIBot, votre assistant stratégique** 

Voici ce sur quoi je peux vous aider :

**Stratégie & Croissance**
→ Trouver des clients, acquisition, prospection

**Marketing & Communication**
→ Réseaux sociaux, SEO, email marketing, contenu

**Finances & Gestion**
→ Tarification, comptabilité, financement, trésorerie

**Lancement & Structure**
→ Business plan, statut juridique, business model

**Opérationnel**
→ Productivité, recrutement, outils, automatisation

Posez-moi une question précise et j'y réponds avec des conseils actionnables adaptés à votre situation.""",
        "followups": ["Comment trouver mes premiers clients ?", "Comment fixer mes prix ?", "Par où commencer ma stratégie marketing ?"]
    },
    # ── SALUTATION ────────────────────────────────────────────────────────
    "salutation": {
        "patterns": ["bonjour", "salut", "bonsoir", "hello", "coucou", "hey", "hi"],
        "response": "**Bonjour !** Je suis BizIBot, votre assistant stratégique.

Je suis là pour répondre à toutes vos questions sur votre activité : stratégie, marketing, clients, prix, financement...

**Par quoi puis-je vous aider aujourd'hui ?**",
        "followups": ["Comment trouver des clients ?", "Ma stratégie marketing", "Comment fixer mes prix ?"]
    },
    # ── REMERCIEMENT ──────────────────────────────────────────────────────
    "remerciement": {
        "patterns": ["merci", "super", "parfait", "excellent", "génial", "top", "cool",
                     "c est utile", "ça aide", "très bien"],
        "response": "Avec plaisir ! 😊 N'hésitez pas si vous avez d'autres questions. Je suis là pour vous aider à développer votre activité.

**Que souhaitez-vous approfondir ?**",
        "followups": ["Autre question sur ma stratégie", "Mes clients", "Mon marketing"]
    },
}

# ══════════════════════════════════════════════════════════════════════════
# MOTEUR DE MATCHING — TF-IDF simplifié
# ══════════════════════════════════════════════════════════════════════════

def _tokenize(text: str) -> list:
    """Normalise et découpe le texte en tokens."""
    text = text.lower()
    text = _re.sub(r"[éèêë]", "e", text)
    text = _re.sub(r"[àâä]", "a", text)
    text = _re.sub(r"[ùûü]", "u", text)
    text = _re.sub(r"[ôö]", "o", text)
    text = _re.sub(r"[îï]", "i", text)
    text = _re.sub(r"[ç]", "c", text)
    text = _re.sub(r"[^a-z0-9\s]", " ", text)
    return [t for t in text.split() if len(t) > 2]


def _score_topic(user_tokens: list, patterns: list) -> float:
    """Score de pertinence d'un sujet pour une question donnée."""
    score = 0.0
    all_pattern_tokens = []
    for p in patterns:
        all_pattern_tokens.extend(_tokenize(p))
    for ut in user_tokens:
        for pt in all_pattern_tokens:
            if ut == pt:
                score += 2.0
            elif ut in pt or pt in ut:
                score += 0.8
    return score


def match_intent(question: str) -> tuple:
    """Retourne le sujet le plus pertinent et son score."""
    tokens = _tokenize(question)
    if not tokens:
        return "aide_generale", 0.0
    best_topic = "aide_generale"
    best_score = 0.0
    for topic, data in _KB.items():
        score = _score_topic(tokens, data["patterns"])
        if score > best_score:
            best_score = score
            best_topic = topic
    return best_topic, best_score


# ══════════════════════════════════════════════════════════════════════════
# RÉPONSE CONTEXTUELLE — enrichie avec les données de l'analyse
# ══════════════════════════════════════════════════════════════════════════

def generate_response(
    question: str,
    context: dict | None = None,
) -> dict:
    """
    Génère une réponse personnalisée.

    context = {
        "activity": "ecommerce",
        "goal": "leads",
        "maturity": "launched",
        "monthly_budget": 200.0,
        "user_name": "Marie",
        "swot": {...},
        "synthesis": {...},
    }
    """
    ctx = context or {}
    activity   = ctx.get("activity", "service")
    goal       = ctx.get("goal", "leads")
    maturity   = ctx.get("maturity", "launched")
    budget     = ctx.get("monthly_budget", 0.0)
    user_name  = ctx.get("user_name", "")

    topic, score = match_intent(question)
    base = _KB.get(topic, _KB["aide_generale"])
    response = base["response"]
    followups = base.get("followups", [])

    # ── Personnalisation contextuelle ──────────────────────────────────────
    _ACT_LABELS = {
        "ecommerce":  "e-commerce",
        "saas":       "SaaS/tech",
        "service":    "services",
        "consulting": "conseil",
        "content":    "création de contenu",
        "other":      "votre activité",
    }
    _GOAL_LABELS = {
        "leads":      "générer des leads",
        "sales":      "augmenter les ventes",
        "awareness":  "développer la notoriété",
        "traffic":    "attirer du trafic",
        "retention":  "fidéliser vos clients",
        "launch":     "lancer votre activité",
        "growth":     "accélérer la croissance",
    }
    act_lbl  = _ACT_LABELS.get(activity, "votre activité")
    goal_lbl = _GOAL_LABELS.get(goal, "vos objectifs")

    # Ajout d'un contexte personnalisé en intro
    greeting = f"**{user_name}**, " if user_name else ""
    if score > 0 and topic not in ("salutation", "remerciement", "aide_generale"):
        context_note = f"

---
*💼 Contexte : {greeting}votre activité en **{act_lbl}** avec l'objectif de **{goal_lbl}**.*"
        response = response + context_note

    # Ajout d'un conseil spécifique budget si question financière
    if topic in ("financement", "prix", "comptabilite") and budget > 0:
        if budget < 100:
            response += f"

💰 *Avec votre budget de {budget:.0f}€/mois : privilégiez les canaux 100% gratuits (SEO, réseaux organiques, bouche-à-oreille).*"
        elif budget < 500:
            response += f"

💰 *Avec votre budget de {budget:.0f}€/mois : 1 outil premium max + canaux organiques.*"
        else:
            response += f"

💰 *Avec votre budget de {budget:.0f}€/mois : vous pouvez tester la publicité payante (Meta/Google Ads).*"

    # Ajout d'un conseil maturité si question sur lancement
    if topic == "business_plan":
        if maturity == "idea":
            response += "

🌱 *Vous êtes en phase idée — validez avant d'investir. 10 interviews clients avant tout.*"
        elif maturity == "launched":
            response += "

🚀 *Vous êtes déjà lancé — concentrez-vous sur l'optimisation, pas la création.*"

    return {
        "response":  response,
        "topic":     topic,
        "score":     score,
        "followups": followups[:3],
        "sources":   ["Base BiziApp", "Données sectorielles France 2025"],
    }


# ══════════════════════════════════════════════════════════════════════════
# HISTORIQUE DE CONVERSATION
# ══════════════════════════════════════════════════════════════════════════

def init_chat_history(session_state) -> None:
    """Initialise l'historique si absent."""
    if "bizibot_history" not in session_state:
        session_state["bizibot_history"] = []
    if "bizibot_initialized" not in session_state:
        session_state["bizibot_initialized"] = False


def add_message(session_state, role: str, content: str) -> None:
    """Ajoute un message à l'historique (max 50 messages)."""
    session_state["bizibot_history"].append({
        "role": role,
        "content": content,
    })
    if len(session_state["bizibot_history"]) > 50:
        session_state["bizibot_history"] = session_state["bizibot_history"][-50:]


def get_history(session_state) -> list:
    """Retourne l'historique complet."""
    return session_state.get("bizibot_history", [])


def clear_history(session_state) -> None:
    """Efface l'historique."""
    session_state["bizibot_history"] = []
    session_state["bizibot_initialized"] = False
