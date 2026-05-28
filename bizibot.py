"""
bizibot.py - IA conversationnelle locale BiziApp v5.4
Chatbot francais pour micro-entrepreneurs et dirigeants TPE/PME

Architecture :
  - Moteur de matching base sur mots-cles + TF-IDF simplifie
  - Base de connaissances locale (aucune API externe)
  - Contexte utilisateur injecte (secteur, objectif, analyse SWOT)
  - Reponses personnalisees selon le profil
  - Historique de conversation en session_state
"""

import re as _re

# ========================================================================
# BASE DE CONNAISSANCES - 16 sujets en francais
# ========================================================================

_KB = {
    "swot": {
        "patterns": ["swot", "forces", "faiblesses", "opportunites", "menaces",
                     "diagnostic", "atouts", "points forts", "points faibles"],
        "response": (
            "**Votre analyse SWOT** structure votre reflexion en 4 quadrants :\n\n"
            "**Forces** - ce que vous faites mieux que vos concurrents\n"
            "**Faiblesses** - ce que vous devez ameliorer en priorite\n"
            "**Opportunites** - les tendances de marche a saisir maintenant\n"
            "**Menaces** - les risques a anticiper\n\n"
            "**Conseil** : Concentrez-vous sur 2 forces a maximiser et 1 faiblesse "
            "critique a corriger. Ne cherchez pas a tout faire en meme temps."
        ),
        "followups": ["Comment ameliorer mes forces ?", "Que faire face aux menaces ?", "Comment saisir les opportunites ?"]
    },
    "acquisition": {
        "patterns": ["trouver des clients", "acquisition", "prospecter", "leads", "prospects",
                     "nouveaux clients", "comment trouver", "attirer", "generer des leads",
                     "premier client", "clientele", "comment vendre"],
        "response": (
            "**Trouver vos premiers clients** - les 3 etapes essentielles :\n\n"
            "**1. Definir votre cible precisement**\n"
            "Ne ciblez pas tout le monde. Choisissez un profil : secteur, taille, probleme precis.\n\n"
            "**2. Aller la ou ils sont**\n"
            "- B2B -> LinkedIn, salons professionnels, reseau personnel\n"
            "- B2C -> Instagram, Google (SEO local), bouche-a-oreille\n\n"
            "**3. Faire une offre irresistible**\n"
            "- Commencez par un service de test a prix reduit\n"
            "- Ou offrez un audit/diagnostic gratuit de 30 min\n\n"
            "**Action immediate** : Contactez 10 personnes de votre reseau aujourd'hui "
            "et expliquez ce que vous faites. C'est votre source de clients #1 au demarrage."
        ),
        "followups": ["Quel canal choisir en priorite ?", "Comment faire une offre de lancement ?", "Comment prospecter sur LinkedIn ?"]
    },
    "marketing": {
        "patterns": ["marketing", "communication", "visibilite", "reseaux sociaux", "publicite",
                     "contenu", "strategie marketing", "plan marketing", "facebook", "instagram",
                     "linkedin", "tiktok", "youtube", "email marketing", "newsletter"],
        "response": (
            "**Strategie marketing pour votre activite** :\n\n"
            "**Regle d or** : choisissez 1 seul canal et maitrisez-le pendant 90 jours.\n\n"
            "**Selon votre cible :**\n"
            "- Particuliers (B2C) -> Instagram, Facebook, TikTok, Google\n"
            "- Professionnels (B2B) -> LinkedIn, email, evenements\n"
            "- Local -> Google My Business, bouche-a-oreille, partenariats locaux\n\n"
            "**Budget limite ?** Commencez par le contenu gratuit avant d'investir en pub.\n\n"
            "**La formule gagnante** : 1 post/jour + 1 newsletter/semaine + 1 article SEO/mois "
            "= croissance organique solide en 6 mois."
        ),
        "followups": ["Quel contenu creer pour ma cible ?", "Comment faire de la pub avec un petit budget ?", "Comment construire ma newsletter ?"]
    },
    "seo": {
        "patterns": ["seo", "referencement", "google", "visibilite google", "mots-cles",
                     "apparaitre sur google", "classement google", "recherche organique",
                     "site web", "blog", "contenu seo"],
        "response": (
            "**Le SEO pour votre activite** - apparaitre sur Google sans payer :\n\n"
            "**Les 3 piliers du SEO :**\n"
            "1. **Contenu** - creez des articles qui repondent aux vraies questions de vos clients\n"
            "2. **Technique** - votre site doit etre rapide, securise (HTTPS) et mobile-friendly\n"
            "3. **Autorite** - obtenez des liens d'autres sites vers le votre\n\n"
            "**Pour commencer :**\n"
            "- Creez 1 article par semaine sur des mots-cles longue traine\n"
            "- Optimisez votre fiche Google Business si vous avez une activite locale\n"
            "- Assurez-vous que chaque page a un titre H1 et une meta description\n\n"
            "**Resultats** : le SEO prend 3-6 mois. Commencez maintenant, "
            "vous recolterez les fruits dans 6 mois."
        ),
        "followups": ["Comment trouver les bons mots-cles ?", "Comment optimiser ma page Google Business ?", "Combien d'articles dois-je ecrire ?"]
    },
    "prix": {
        "patterns": ["prix", "tarif", "tarification", "combien facturer", "devis",
                     "pricing", "grille tarifaire", "trop cher", "augmenter mes prix",
                     "positionnement prix", "comment fixer"],
        "response": (
            "**Comment fixer vos prix** - sans vous sous-vendre :\n\n"
            "**Les erreurs a eviter :**\n"
            "- Calculer uniquement vos couts (vous oubliez votre valeur)\n"
            "- Copier les prix des concurrents sans analyser votre positionnement\n"
            "- Baisser vos prix pour conclure - cela attire de mauvais clients\n\n"
            "**La methode en 3 etapes :**\n"
            "1. Calculez votre cout reel : temps x taux horaire + frais\n"
            "2. Etudiez le marche : fourchette basse, mediane, premium\n"
            "3. Positionnez-vous : entree de gamme, milieu de gamme, ou premium\n\n"
            "**Regle d or** : si plus de 80% de vos prospects acceptent votre prix "
            "sans negocier, vous etes trop bon marche.\n\n"
            "**Testez une augmentation de 20-30%** sur vos prochaines propositions "
            "et observez le taux d'acceptation."
        ),
        "followups": ["Comment justifier des prix plus eleves ?", "Comment creer des packages ?", "Comment negocier avec les clients ?"]
    },
    "business_plan": {
        "patterns": ["business plan", "plan affaires", "previsionnel", "projet", "lancer",
                     "creer entreprise", "auto-entrepreneur", "micro-entrepreneur",
                     "se lancer", "demarrer", "creation entreprise", "statut juridique"],
        "response": (
            "**Creer votre entreprise** - les etapes cles :\n\n"
            "**1. Validez votre idee (avant tout)**\n"
            "Parlez a 10 personnes de votre cible. Sont-elles pretes a payer ?\n\n"
            "**2. Choisissez votre statut**\n"
            "- Micro-entrepreneur : ideal pour demarrer, simple, CA limite\n"
            "- SASU/EURL : si vous anticipez un CA important ou des risques\n"
            "- Portage salarial : pour les consultants qui veulent tester\n\n"
            "**3. Les 5 elements de votre business plan :**\n"
            "- Offre et cible\n"
            "- Modele economique\n"
            "- Plan d'acquisition clients\n"
            "- Previsionnel financier sur 3 ans\n"
            "- Besoins en financement\n\n"
            "**Conseil** : N'attendez pas un business plan parfait pour demarrer. "
            "Testez d'abord, structurez ensuite."
        ),
        "followups": ["Quel statut juridique choisir ?", "Comment faire un previsionnel ?", "Comment se faire financer ?"]
    },
    "financement": {
        "patterns": ["financement", "credit", "pret", "banque", "subvention", "aide",
                     "bpifrance", "aide creation", "investisseur", "levee de fonds",
                     "budget", "tresorerie", "cash flow"],
        "response": (
            "**Les financements disponibles pour votre projet** :\n\n"
            "**Aides et subventions (a chercher en premier) :**\n"
            "- ACRE : exoneration de charges les premieres annees\n"
            "- ARCE : convertir vos allocations chomage en capital\n"
            "- Aides regionales : variables selon votre region\n"
            "- BPI France : prets d'honneur et garanties bancaires\n\n"
            "**Prets bancaires :**\n"
            "- Pret professionnel classique (necessite un business plan solide)\n"
            "- Microcredit professionnel (jusqu'a 12 000 EUR via l'ADIE)\n\n"
            "**Alternatives :**\n"
            "- Crowdfunding (Ulule, KissKissBankBank)\n"
            "- Love money (famille, amis)\n\n"
            "**Commencez par les aides** avant de solliciter des prets - "
            "c'est de l'argent que vous ne remboursez pas."
        ),
        "followups": ["Comment obtenir un pret bancaire ?", "Quelles aides pour les auto-entrepreneurs ?", "Comment faire un previsionnel ?"]
    },
    "fidelisation": {
        "patterns": ["fidelisation", "garder mes clients", "retention", "clients qui partent",
                     "programme fidelite", "satisfaction client", "nps", "avis clients",
                     "recurrence", "abonnement"],
        "response": (
            "**Fideliser vos clients** - votre levier de croissance le plus rentable :\n\n"
            "**Pourquoi c'est prioritaire :**\n"
            "Garder un client existant coute 5x moins cher qu'en acquerir un nouveau.\n\n"
            "**Les 4 leviers de fidelisation :**\n"
            "1. Qualite irreprochablee : sous-promettez, sur-livrez\n"
            "2. Suivi proactif : contactez vos clients sans attendre\n"
            "3. Programme de recompenses : offres exclusives, reductions\n"
            "4. Communaute : creez un espace d'echange entre vos clients\n\n"
            "**Mesurez votre fidelisation :**\n"
            "- NPS : De 0 a 10, recommanderiez-vous nos services ?\n"
            "- Taux de retention : % de clients qui restent\n"
            "- LTV : valeur totale d'un client sur toute sa duree de vie\n\n"
            "**Action immediate** : Appelez vos 5 meilleurs clients cette semaine "
            "pour leur demander comment vous pouvez mieux les servir."
        ),
        "followups": ["Comment calculer mon NPS ?", "Comment creer un programme de fidelite ?", "Comment reduire le churn ?"]
    },
    "concurrence": {
        "patterns": ["concurrents", "concurrence", "differenciation", "se differencier",
                     "avantage concurrentiel", "unique", "usp", "proposition de valeur",
                     "benchmark", "marche concurrentiel"],
        "response": (
            "**Face a la concurrence** - comment vous differencier vraiment :\n\n"
            "**Ne pas copier vos concurrents** : c'est la premiere regle.\n\n"
            "**Les 5 axes de differenciation :**\n"
            "1. La specialisation : etre le meilleur dans une niche precise\n"
            "2. L'experience client : service irreprochablee avant, pendant, apres\n"
            "3. La rapidite : livrer plus vite que tout le monde\n"
            "4. Le prix : le moins cher OU le plus premium (jamais le milieu)\n"
            "5. La relation : humaniser votre marque, creer du lien authentique\n\n"
            "**Trouvez votre USP :**\n"
            "Completez cette phrase : Je suis le seul a __ pour __ qui veulent __\n\n"
            "Votre USP doit tenir en 1 phrase et etre comprise en 5 secondes."
        ),
        "followups": ["Comment analyser mes concurrents ?", "Comment creer mon USP ?", "Comment me positionner sur un marche sature ?"]
    },
    "productivite": {
        "patterns": ["productivite", "organisation", "gestion du temps", "procrastination",
                     "automatisation", "outils", "efficacite", "priorites", "planning",
                     "agenda", "routine", "workflow", "deleguer"],
        "response": (
            "**Productivite pour entrepreneurs** - faire plus avec moins :\n\n"
            "**La regle 80/20 (Pareto) :**\n"
            "20% de vos actions generent 80% de vos resultats. Identifiez-les.\n\n"
            "**La methode en 3 blocs quotidiens :**\n"
            "1. Matin (focus) : travail profond sans interruptions (2-3h)\n"
            "2. Apres-midi (communication) : emails, appels, reunions\n"
            "3. Fin de journee (planification) : preparez le lendemain en 15 min\n\n"
            "**Outils gratuits incontournables :**\n"
            "- Notion : organisation, notes, projets\n"
            "- Trello : gestion de projet visuelle\n"
            "- Calendly : prise de RDV automatisee\n\n"
            "**Ce que vous devez deleguer en premier** : comptabilite, reseaux sociaux, "
            "service client recurrent."
        ),
        "followups": ["Quels outils utiliser pour automatiser ?", "Comment deleguer efficacement ?", "Comment gerer mes emails ?"]
    },
    "comptabilite": {
        "patterns": ["comptabilite", "charges", "impots", "urssaf", "tva", "benefice",
                     "chiffre affaires", "facturation", "tresorerie", "bilan",
                     "compte bancaire", "expert-comptable", "cotisations"],
        "response": (
            "**Gestion financiere** pour micro-entrepreneur :\n\n"
            "**Les bases indispensables :**\n"
            "- Compte bancaire dedie : n'utilisez jamais votre compte perso\n"
            "- Facturez des la livraison : delai paiement max 30 jours\n"
            "- Mettez de cote 25-30% de votre CA pour les charges et impots\n\n"
            "**En micro-entreprise :**\n"
            "- Cotisations URSSAF : 12.8% (vente) / 22% (services) de votre CA\n"
            "- TVA : exonere en dessous des seuils\n\n"
            "**Outils gratuits :**\n"
            "- Indy ou Pennylane : comptabilite simplifiee auto-entrepreneur\n"
            "- Shine : compte pro avec comptabilite integree\n\n"
            "**Conseil d or** : Consultez un expert-comptable au moins une fois par an."
        ),
        "followups": ["Comment gerer ma tresorerie ?", "Comment facturer mes clients ?", "Quand dois-je passer a la TVA ?"]
    },
    "salutation": {
        "patterns": ["bonjour", "salut", "bonsoir", "hello", "coucou", "hey"],
        "response": (
            "**Bonjour !** Je suis BizIBot, votre assistant strategique.\n\n"
            "Je suis la pour repondre a toutes vos questions sur votre activite : "
            "strategie, marketing, clients, prix, financement...\n\n"
            "**Par quoi puis-je vous aider aujourd'hui ?**"
        ),
        "followups": ["Comment trouver des clients ?", "Ma strategie marketing", "Comment fixer mes prix ?"]
    },
    "remerciement": {
        "patterns": ["merci", "super", "parfait", "excellent", "genial", "top", "cool",
                     "utile", "aide", "tres bien"],
        "response": (
            "Avec plaisir ! N'hesitez pas si vous avez d'autres questions. "
            "Je suis la pour vous aider a developper votre activite.\n\n"
            "**Que souhaitez-vous approfondir ?**"
        ),
        "followups": ["Autre question sur ma strategie", "Mes clients", "Mon marketing"]
    },
    "aide_generale": {
        "patterns": ["aide", "help", "comment", "quoi faire", "par ou commencer",
                     "que faire", "conseil", "besoin", "perdu"],
        "response": (
            "**Je suis BizIBot, votre assistant strategique**\n\n"
            "Voici ce sur quoi je peux vous aider :\n\n"
            "**Strategie et Croissance** -> Trouver des clients, acquisition, prospection\n"
            "**Marketing et Communication** -> Reseaux sociaux, SEO, email marketing\n"
            "**Finances et Gestion** -> Tarification, comptabilite, financement\n"
            "**Lancement et Structure** -> Business plan, statut juridique\n"
            "**Operationnel** -> Productivite, outils, automatisation\n\n"
            "Posez-moi une question precise et j'y reponds avec des conseils actionnables."
        ),
        "followups": ["Comment trouver mes premiers clients ?", "Comment fixer mes prix ?", "Par ou commencer ma strategie marketing ?"]
    },
}


# ========================================================================
# MOTEUR DE MATCHING - TF-IDF simplifie
# ========================================================================

def _normalize(text):
    """Normalise le texte (accents, casse, ponctuation)."""
    text = text.lower()
    for src, dst in [
        ("e", ["e", "e", "e", "e"]),
    ]:
        pass
    replacements = {
        "e": ["e", "e", "e", "e"],
        "a": ["a", "a"],
        "u": ["u", "u"],
        "o": ["o"],
        "i": ["i"],
        "c": ["c"],
    }
    # Simple remplacement accent
    accents = {
        "e": "eeeeeee",
        "a": "aaa",
        "u": "uuu",
        "o": "oo",
        "i": "ii",
        "c": "cc",
    }
    text = _re.sub(r"[eeeee]", "e", text)
    text = _re.sub(r"[aaa]", "a", text)
    text = _re.sub(r"[uuu]", "u", text)
    text = _re.sub(r"[oo]", "o", text)
    text = _re.sub(r"[ii]", "i", text)
    text = _re.sub(r"c", "c", text)
    text = _re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def _tokenize(text):
    """Tokenise et normalise."""
    text = text.lower()
    # Remplacer accents
    accent_map = [
        ("e", "eeee"),
        ("e", "eeee"),
        ("a", "aaa"),
        ("u", "uuu"),
        ("o", "oo"),
        ("i", "ii"),
        ("c", "cc"),
    ]
    for char, variants in [
        ("e", ["e", "e", "e"]),
        ("a", ["a", "a"]),
        ("u", ["u", "u"]),
        ("o", ["o"]),
        ("i", ["i"]),
        ("c", ["c"]),
    ]:
        pass
    # Remplacement simple via translate
    trans = str.maketrans(
        "eeeeeaauuooiic",
        "eeeeeeaauuooiic"
    )
    text = _re.sub(r"[^a-z0-9\s-]", " ", text)
    tokens = [t for t in text.split() if len(t) > 2]
    return tokens


def _score(tokens, patterns):
    """Score de pertinence."""
    score = 0.0
    ptokens = []
    for p in patterns:
        ptokens.extend(_re.sub(r"[^a-z0-9\s-]", " ", p.lower()).split())
    for ut in tokens:
        for pt in ptokens:
            if ut == pt:
                score += 2.0
            elif len(ut) > 3 and (ut in pt or pt in ut):
                score += 0.5
    return score


def match_intent(question):
    """Retourne le sujet le plus pertinent."""
    q_clean = _re.sub(r"[^a-z0-9\s-]", " ", question.lower())
    tokens = [t for t in q_clean.split() if len(t) > 2]
    if not tokens:
        return "aide_generale", 0.0
    best_topic = "aide_generale"
    best_score = 0.0
    for topic, data in _KB.items():
        s = _score(tokens, data["patterns"])
        if s > best_score:
            best_score = s
            best_topic = topic
    return best_topic, best_score


# ========================================================================
# GENERATEUR DE REPONSE
# ========================================================================

def generate_response(question, context=None):
    """
    Genere une reponse personnalisee.
    context = {"activity": str, "goal": str, "maturity": str,
               "monthly_budget": float, "user_name": str}
    """
    ctx = context or {}
    activity = ctx.get("activity", "service")
    goal = ctx.get("goal", "leads")
    maturity = ctx.get("maturity", "launched")
    budget = float(ctx.get("monthly_budget", 0))
    user_name = ctx.get("user_name", "")

    topic, score = match_intent(question)
    base = _KB.get(topic, _KB["aide_generale"])
    response = base["response"]
    followups = base.get("followups", [])

    ACT = {"ecommerce": "e-commerce", "saas": "SaaS", "service": "services",
           "consulting": "conseil", "content": "creation de contenu", "other": "votre activite"}
    GOAL = {"leads": "generer des leads", "sales": "augmenter les ventes",
            "awareness": "developper la notoriete", "traffic": "attirer du trafic",
            "retention": "fideliser vos clients", "launch": "lancer votre activite",
            "growth": "accelerer la croissance"}

    act_lbl = ACT.get(activity, "votre activite")
    goal_lbl = GOAL.get(goal, "vos objectifs")

    # Personnalisation contextuelle
    if score > 0 and topic not in ("salutation", "remerciement", "aide_generale"):
        greeting = f"{user_name}, " if user_name else ""
        ctx_note = (
            f"\n\n---\n*Contexte : {greeting}activite **{act_lbl}**, "
            f"objectif **{goal_lbl}**.*"
        )
        response = response + ctx_note

    # Conseil budget
    if topic in ("financement", "prix", "comptabilite") and budget > 0:
        if budget < 100:
            response += (
                f"\n\n*Budget {budget:.0f} EUR/mois : "
                "privilegiez les canaux 100% gratuits (SEO, reseaux organiques).*"
            )
        elif budget < 500:
            response += (
                f"\n\n*Budget {budget:.0f} EUR/mois : "
                "1 outil premium max + canaux organiques.*"
            )
        else:
            response += (
                f"\n\n*Budget {budget:.0f} EUR/mois : "
                "vous pouvez tester la publicite payante (Meta/Google Ads).*"
            )

    # Conseil maturite
    if topic == "business_plan":
        if maturity == "idea":
            response += "\n\n*Phase idee : validez avant d investir. 10 interviews clients avant tout.*"
        elif maturity == "launched":
            response += "\n\n*Vous etes deja lance : concentrez-vous sur l optimisation.*"

    return {
        "response": response,
        "topic": topic,
        "score": score,
        "followups": followups[:3],
    }


# ========================================================================
# GESTION HISTORIQUE
# ========================================================================

def init_chat_history(ss):
    """Initialise l'historique."""
    if "bizibot_history" not in ss:
        ss["bizibot_history"] = []


def add_message(ss, role, content):
    """Ajoute un message (max 40)."""
    ss["bizibot_history"].append({"role": role, "content": content})
    if len(ss["bizibot_history"]) > 40:
        ss["bizibot_history"] = ss["bizibot_history"][-40:]


def get_history(ss):
    """Retourne l'historique."""
    return ss.get("bizibot_history", [])


def clear_history(ss):
    """Efface l'historique."""
    ss["bizibot_history"] = []
