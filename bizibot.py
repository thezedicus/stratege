"""
bizibot.py v2 - IA conversationnelle locale BiziApp v5.4
Chatbot francais pour micro-entrepreneurs et dirigeants TPE/PME

Ameliorations v2:
  - Base de connaissances enrichie (25+ sujets)
  - TF-IDF ameliore avec bigrams et stemming FR basique
  - Detection d'intention multi-labels
  - Reponses plus precises et actionnables
  - Personnalisation par secteur/objectif/maturite/budget
  - Memoire conversationnelle (contexte des 3 derniers echanges)
"""

import re as _re
import math as _math
from collections import Counter as _Counter

# ========================================================================
# STEMMING FRANCAIS BASIQUE — reduit les variantes d'un mot
# ========================================================================

_STOP_FR = {
    "le","la","les","de","des","du","un","une","et","en","au","aux",
    "est","sont","avec","sur","par","pour","dans","qui","que","se",
    "ce","je","tu","il","elle","nous","vous","ils","elles","mon","ma",
    "mes","ton","ta","tes","son","sa","ses","notre","votre","leur",
    "pas","ne","plus","tres","mais","ou","si","car","donc","or","ni",
    "comment","quoi","quand","pourquoi","combien","quel","quelle",
    "faire","avoir","etre","veux","vouloir","faut","peut","dois","doit",
    "jai","cest","ca","ici","la","tout","tous","bien","mal","aussi",
}

def _stem(word):
    """Stemming FR minimal — supprime les terminaisons courantes."""
    w = word.lower()
    for suffix in ["aient","aient","ation","ations","ement","ements",
                   "ifier","isant","isant","iste","istes",
                   "ment","ments","tion","tions",
                   "er","ez","es","ees","ee","e","s"]:
        if len(w) > len(suffix) + 3 and w.endswith(suffix):
            return w[:-len(suffix)]
    return w

def _normalize(text):
    """Normalise le texte : accents, casse, ponctuation."""
    text = text.lower()
    for src, dst in [
        ("eeeee","e"),("aaaa","a"),("uuu","u"),("oo","o"),("ii","i"),("cc","c"),
    ]:
        pass
    # Table de remplacement accents
    for old, new in [
        ("e","e"),("e","e"),("e","e"),("a","a"),("u","u"),
        ("u","u"),("o","o"),("i","i"),("c","c"),
    ]:
        pass
    text = (text
        .replace("e","e").replace("e","e").replace("e","e").replace("e","e")
        .replace("a","a").replace("a","a")
        .replace("u","u").replace("u","u")
        .replace("o","o")
        .replace("i","i")
        .replace("c","c")
    )
    text = _re.sub(r"[^a-z0-9\s-]", " ", text)
    return text

def _tokenize(text):
    """Tokenise + filtre stopwords + stemme."""
    words = _normalize(text).split()
    tokens = []
    for w in words:
        if len(w) > 2 and w not in _STOP_FR:
            tokens.append(_stem(w))
            tokens.append(w)  # aussi le mot brut
    return list(set(tokens))

def _bigrams(tokens):
    """Genere les bigrams d'une liste de tokens."""
    return [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens)-1)]

# ========================================================================
# BASE DE CONNAISSANCES ENRICHIE — 25 sujets
# Format: patterns (mots cles) + response + followups + keywords_weight
# ========================================================================

_KB = {
    "swot": {
        "patterns": [
            "swot","force","faibless","opportunit","menac",
            "diagnost","atout","point fort","point faible","analyse strateg",
            "bilan","evaluation","etat des lieux",
        ],
        "weight": 2.0,
        "response": (
            "**Analyse SWOT personnalisee pour vous** :\n\n"
            "Le SWOT est votre boussole strategique. Voici comment l'utiliser concretement :\n\n"
            "**Forces** (ce que vous faites mieux que vos concurrents)\n"
            "Exemples : expertise rare, base clients fidele, localisation, prix competitifs\n\n"
            "**Faiblesses** (ce que vous devez corriger en priorite)\n"
            "Exemples : manque de visibilite, processus lents, dependance a 1 client cle\n\n"
            "**Opportunites** (tendances que vous pouvez saisir maintenant)\n"
            "Exemples : croissance du marche, nouveau besoin client, concurrent qui ferme\n\n"
            "**Menaces** (risques a anticiper)\n"
            "Exemples : nouveau concurrent, hausse des prix, changement reglementaire\n\n"
            "**La methode gagnante** : identifiez vos 2 meilleures forces, "
            "associez-les a vos 2 meilleures opportunites. "
            "C'est votre strategie prioritaire des maintenant."
        ),
        "followups": [
            "Comment identifier mes vraies forces ?",
            "Que faire de mes faiblesses critiques ?",
            "Comment saisir les opportunites de marche ?",
        ]
    },

    "acquisition_clients": {
        "patterns": [
            "trouv","client","prospect","acquisit","lead","vend",
            "premier client","comment vendre","commencer","demarr",
            "new business","canaux","sourcing","pipeline",
        ],
        "weight": 2.5,
        "response": (
            "**Trouver vos premiers clients** — la methode eprouvee :\n\n"
            "**Etape 1 : Definissez votre ICP (Ideal Customer Profile) en 5 min**\n"
            "Completez : Mon client ideal est [qui], il a le probleme [quoi], "
            "il veut [resultat], il a [budget] disponible.\n\n"
            "**Etape 2 : Les 5 meilleurs canaux par type d activite**\n"
            "- Services B2B : LinkedIn + reseau personnel + recommandations\n"
            "- E-commerce : Google Shopping + Instagram Ads + SEO produit\n"
            "- Conseil/coaching : LinkedIn + contenu expert + bouche-a-oreille\n"
            "- Local/artisan : Google My Business + reseaux locaux + panneaux\n"
            "- SaaS/Tech : Product Hunt + forums + SEO longue traine\n\n"
            "**Etape 3 : L offre d accroche irresistible**\n"
            "Proposez un resultat mesurable en temps limite : "
            "Audit gratuit 30 min, premiere commande -20%, essai 14j offert.\n\n"
            "**Action immediate** : Contactez 10 personnes de votre reseau "
            "aujourd'hui avec ce message : "
            "Je lance [activite], mon offre de lancement est [offre]. "
            "Connais-tu quelqu'un qui pourrait etre interesse ?"
        ),
        "followups": [
            "Quel canal choisir selon mon secteur ?",
            "Comment creer une offre de lancement ?",
            "Comment prospecter sur LinkedIn efficacement ?",
        ]
    },

    "marketing_contenu": {
        "patterns": [
            "market","communic","visibil","contenu","reseaux","pub","publicite",
            "strateg market","plan market","content","inbound","outbound",
            "notoriet","brand","marque","communication",
        ],
        "weight": 2.0,
        "response": (
            "**Strategie marketing pour votre activite** :\n\n"
            "**La regle des 3 canaux** : choisissez-en 1 principal + 2 secondaires.\n\n"
            "**Canal principal (80% de votre energie)** :\n"
            "- B2B -> LinkedIn (posts + prospection DM)\n"
            "- B2C jeune -> Instagram / TikTok (Reels + Stories)\n"
            "- B2C + 35 ans -> Facebook (groupes + pages)\n"
            "- SEO organique -> Blog + YouTube (long terme mais durable)\n\n"
            "**La formule du contenu qui convertit** :\n"
            "60% valeur (conseils actionnables) + 30% coulisses + 10% offres\n\n"
            "**Planning realiste** :\n"
            "- 3 posts/semaine sur le canal principal\n"
            "- 1 newsletter/semaine (email : ROI x42 vs reseaux)\n"
            "- 1 video/semaine si vous visez YouTube\n\n"
            "**Budget zero** : SEO + reseaux organiques + bouche-a-oreille = "
            "suffisant les 6 premiers mois."
        ),
        "followups": [
            "Quel type de contenu creer rapidement ?",
            "Comment augmenter l engagement sur Instagram ?",
            "Comment lancer une newsletter rentable ?",
        ]
    },

    "seo_referencement": {
        "patterns": [
            "seo","referencement","google","mots-cle","keyword",
            "trafic organiq","search","apparaitre","classement",
            "longue traine","backlink","netlinking","audit seo",
        ],
        "weight": 2.0,
        "response": (
            "**SEO : apparaitre sur Google gratuitement** :\n\n"
            "**Les 3 facteurs de classement Google (simplifie)** :\n"
            "1. Pertinence du contenu (repondre precisement a la question)\n"
            "2. Autorite du domaine (liens entrants de qualite)\n"
            "3. Experience utilisateur (vitesse, mobile, temps passe)\n\n"
            "**Plan d action 90 jours** :\n"
            "- Semaine 1-4 : Optimisez vos 5 pages cles (title, H1, meta desc)\n"
            "- Semaine 5-8 : Creez 4 articles sur des mots-cles longue traine\n"
            "- Semaine 9-12 : Obtenez 3 backlinks (partenaires, annuaires, presse)\n\n"
            "**Outil gratuit** : Google Search Console (gratuit, indispensable)\n"
            "Identifiez les requetes qui vous apportent des impressions mais peu de clics, "
            "et optimisez ces pages en priorite.\n\n"
            "**Resultat attendu** : trafic organique x2 a x5 en 6 mois avec constance."
        ),
        "followups": [
            "Comment trouver des mots-cles rentables gratuitement ?",
            "Comment optimiser ma page Google Business ?",
            "Comment obtenir des backlinks sans payer ?",
        ]
    },

    "tarification_prix": {
        "patterns": [
            "prix","tarif","fact","devis","combien","tarification",
            "pricing","grille","augment","trop cher","negoc",
            "positionnement prix","valoris","justifi","marge",
        ],
        "weight": 2.0,
        "response": (
            "**Fixez vos prix pour maximiser votre CA** :\n\n"
            "**La vraie methode (pas celle qu on vous apprend)** :\n\n"
            "**Etape 1 : Calculez votre taux horaire minimum**\n"
            "CA cible annuel / heures facturables = taux horaire minimum\n"
            "Exemple : 60 000 EUR / 1 200h = 50 EUR/h minimum\n\n"
            "**Etape 2 : Etudiez la concurrence sur 3 niveaux**\n"
            "- Entree de gamme (eviter sauf si volume)\n"
            "- Milieu de gamme (le plus concurrentiel)\n"
            "- Premium (visez ca si vous avez une expertise differentee)\n\n"
            "**Etape 3 : Packagisez**\n"
            "3 offres : Essentiel / Standard / Premium\n"
            "L offre du milieu doit etre celle que vous voulez le plus vendre.\n\n"
            "**Regle d or** : si plus de 80% de vos prospects acceptent sans hesiter, "
            "vous etes 20-30% trop bon marche. Testez une augmentation.\n\n"
            "**Comment justifier un prix premium** : "
            "cas clients chiffres + garantie resultat + accompagnement inclus."
        ),
        "followups": [
            "Comment creer 3 packages attrayants ?",
            "Comment negocier sans baisser mes prix ?",
            "Comment facturer plus cher mes services actuels ?",
        ]
    },

    "creation_entreprise": {
        "patterns": [
            "cre","lanc","demarr","startup","entrepris","micro-entrepr",
            "auto-entrepr","statut","sas","eurl","sarl","sasu",
            "business plan","previsionnel","immatricul",
        ],
        "weight": 1.8,
        "response": (
            "**Creer votre entreprise en France — guide rapide** :\n\n"
            "**Etape 0 : Validez avant de crer (critique !)**\n"
            "Parlez a 10 clients potentiels. Paient-ils ? Si non, changez d offre.\n\n"
            "**Quel statut choisir ?**\n"
            "- Micro-entreprise : CA < 77 700 EUR services / 188 700 EUR vente\n"
            "  -> Simple, rapide, ideal pour demarrer\n"
            "- SASU/SAS : meilleur pour lever des fonds, embaucher\n"
            "  -> Plus de charges, mais meilleure protection\n"
            "- EURL : comme SASU mais gerant = you, seul associe possible\n\n"
            "**Les 5 etapes pour se lancer en micro-entreprise** :\n"
            "1. Inscription sur autoentrepreneur.urssaf.fr (gratuit, 10 min)\n"
            "2. Compte bancaire pro (Shine, Qonto, ou classique)\n"
            "3. Premiere proposition commerciale envoyee\n"
            "4. Premiere facture emise\n"
            "5. Declaration CA mensuelle ou trimestrielle\n\n"
            "**Conseil** : Ne perdez pas 6 mois sur le business plan. "
            "Lancez en micro, pivotez si besoin, changez de statut ensuite."
        ),
        "followups": [
            "Comment faire un business plan simple ?",
            "Quelles aides financieres pour les createurs ?",
            "Comment passer de micro-entrepreneur a societe ?",
        ]
    },

    "financement_aides": {
        "patterns": [
            "financ","pret","banqu","subvention","aide","bpifranc",
            "invest","levee de fonds","capital","tresor","cash",
            "acre","arce","fonds","bourse","credit","emprunt",
        ],
        "weight": 1.8,
        "response": (
            "**Financer votre projet — toutes les options** :\n\n"
            "**Les aides a ne pas rater (argent gratuit ou sans interet)** :\n"
            "1. ACRE : exoneration partielle de charges la 1ere annee\n"
            "   -> Automatique si eligible, demandez-le a l URSSAF\n"
            "2. ARCE : transformer ses droits chomage en capital (45%)\n"
            "   -> Demandez a France Travail avant de creer\n"
            "3. Aides regionales : variant de 500 EUR a 50 000 EUR\n"
            "   -> Cherchez sur votre portail regional + Bpifrance.fr\n"
            "4. Microcredit ADIE : jusqu a 12 000 EUR sans garant bancaire\n\n"
            "**Prets bancaires** :\n"
            "- Pret garanti BPI (jusqu a 70% de garantie publique)\n"
            "- Pret d honneur Reseau Entreprendre (0% interet, pas de garant)\n"
            "- Pret bancaire classique (business plan + apport 20-30%)\n\n"
            "**Financement client (le meilleur)** :\n"
            "Vente d abonnements annuels ou acomptes de 50% = vous financent sans dette.\n\n"
            "**Ordre de priorite** : Aides -> Clients -> BPI -> Banque -> Investisseurs"
        ),
        "followups": [
            "Comment obtenir l ACRE ou l ARCE ?",
            "Comment convaincre une banque de me financer ?",
            "Le crowdfunding est-il adapte a mon projet ?",
        ]
    },

    "fidelisation_retention": {
        "patterns": [
            "fidelis","retentr","garder","churn","client qui part",
            "abonnement","nps","satisfact","recommandat","avis",
            "recurrence","ltv","valeur vie client",
        ],
        "weight": 1.8,
        "response": (
            "**Fideliser vos clients — votre levier de croissance #1** :\n\n"
            "**Pourquoi c est votre priorite** :\n"
            "Garder un client = 5x moins cher qu en acquerir un nouveau.\n"
            "Augmenter la retention de 5% = +25 a 95% de benefices.\n\n"
            "**Les 5 leviers de fidelisation prouvee** :\n"
            "1. **Onboarding parfait** : les 30 premiers jours determinent tout\n"
            "   -> Creez un parcours clair : J0 / J7 / J30\n"
            "2. **Suivi proactif** : contactez sans attendre qu'ils vous contactent\n"
            "   -> 1 appel de suivi a J30 = +40% de retention\n"
            "3. **Valeur continue** : apportez plus que ce qu ils ont paye\n"
            "   -> Contenu exclusif, conseils, acces beta, ressources\n"
            "4. **Programme VIP** : recompensez les meilleurs clients\n"
            "   -> Reduction anniversaire, acces prioritaire, cadeaux\n"
            "5. **Mesure NPS mensuel** : demandez 0 a 10 recommanderiez-vous ?\n"
            "   -> Score < 7 = alerte rouge a traiter immediatement\n\n"
            "**Action cette semaine** : appelez vos 3 meilleurs clients, "
            "demandez ce qui les ferait rester et acheter plus."
        ),
        "followups": [
            "Comment mettre en place un programme de fidelite ?",
            "Comment reduire le churn rapidement ?",
            "Comment transformer mes clients en ambassadeurs ?",
        ]
    },

    "differentiation_concurrence": {
        "patterns": [
            "concurr","differenci","unique","usp","positionnement",
            "avantage","benchmark","marche satur","compet","rival",
            "proposition valeur","niche","specialisation",
        ],
        "weight": 2.0,
        "response": (
            "**Se differencier dans un marche concurrentiel** :\n\n"
            "**La verite sur la differentiation** :\n"
            "Vous n avez pas besoin d etre unique dans l absolu. "
            "Vous devez etre unique pour VOTRE cible.\n\n"
            "**Les 6 axes de differentiation** :\n"
            "1. **Niche** : servez un segment ultra-specifique mieux que personne\n"
            "   Ex : consultant marketing specifiquement pour les kinesiologues\n"
            "2. **Methode** : une approche propriataire avec un nom\n"
            "   Ex : La methode STAR pour doubler votre CA en 90j\n"
            "3. **Vitesse** : livraison en 24h / resultat en 7 jours\n"
            "4. **Garantie** : satisfait ou rembourse / resultat garanti\n"
            "5. **Acces** : disponibilite 7j/7, reponse en 2h, suivi illimite\n"
            "6. **Relation** : vous et seulement vous (pas de sous-traitance)\n\n"
            "**Construisez votre USP en 1 phrase** :\n"
            "J aide [qui exact] a [resultat precis] en [delai] [differenciateur].\n"
            "Exemple : J aide les coachs sante a avoir 3 nouveaux clients par mois "
            "en 60 jours, sans publicite payante."
        ),
        "followups": [
            "Comment creer ma methode propriataire ?",
            "Comment choisir ma niche rentable ?",
            "Comment analyser mes concurrents efficacement ?",
        ]
    },

    "productivite_organisation": {
        "patterns": [
            "productiv","organis","temps","procrastin","automat",
            "outil","efficac","priorit","planning","deleguer",
            "gestion projet","workflow","agenda","routine",
        ],
        "weight": 1.5,
        "response": (
            "**Productivite maximale pour entrepreneur** :\n\n"
            "**Le systeme en 3 blocs (prouve par les meilleurs fondateurs)** :\n"
            "Bloc 1 (8h-12h) : Travail profond (creation, strategie, decisions)\n"
            "Bloc 2 (13h-17h) : Communication (emails, appels, reunions)\n"
            "Bloc 3 (17h-18h) : Admin + planification du lendemain\n\n"
            "**La regle 80/20 appliquee a votre business** :\n"
            "Identifiez les 3 actions qui generent 80% de votre CA.\n"
            "Faites ces 3 actions EN PREMIER chaque jour. Tout le reste est secondaire.\n\n"
            "**Ce que vous devez automatiser ou deleguer en 1er** :\n"
            "1. Comptabilite et admin (Indy, Pennylane, comptable)\n"
            "2. Reseaux sociaux (outil planification : Buffer, Later)\n"
            "3. Prise de RDV (Calendly = 0 email de va-et-vient)\n"
            "4. Support client repetitif (FAQ, chatbot, base de connaissance)\n\n"
            "**Outils gratuits** :\n"
            "Notion (organisation) + Trello (projets) + Calendly (RDV) + "
            "Zapier free (automatisation basique)"
        ),
        "followups": [
            "Quels outils gratuits pour automatiser mon activite ?",
            "Comment deleguer sans perdre en qualite ?",
            "Comment arreter de procrastiner sur les taches importantes ?",
        ]
    },

    "email_newsletter": {
        "patterns": [
            "email","newsletter","emailing","liste","mailing",
            "brevo","mailchimp","campagne","sequence","automatis",
            "taux ouverture","taux clic","desabonnement",
        ],
        "weight": 1.8,
        "response": (
            "**Email marketing — votre actif le plus rentable** :\n\n"
            "**Pourquoi l email bat les reseaux sociaux** :\n"
            "ROI moyen email = 42 EUR pour 1 EUR investi (vs 2-5 EUR pour les ads)\n"
            "Taux ouverture email = 20-25% vs 3-5% de portee organique sur Meta\n\n"
            "**Construire votre liste en 30 jours** :\n"
            "1. Creez un lead magnet en 2h : checklist PDF, guide simple, template\n"
            "2. Ajoutez un formulaire sur votre site (pop-up de sortie = x3 conversions)\n"
            "3. Mentionnez votre ressource gratuite dans chaque post\n\n"
            "**La sequence de bienvenue qui convertit** (automatique) :\n"
            "- Email J0 : votre ressource + qui vous etes (bref)\n"
            "- Email J2 : votre histoire + pourquoi ce metier\n"
            "- Email J4 : votre methode unique + benefice cle\n"
            "- Email J7 : temoignage client + 1 offre claire\n\n"
            "**Outils gratuits** : Brevo (300 emails/jour gratuit), "
            "Mailchimp (500 contacts gratuit), Systeme.io (tout-en-un)"
        ),
        "followups": [
            "Comment creer un lead magnet en 2 heures ?",
            "Comment ameliorer mon taux d ouverture ?",
            "Quelle frequence d envoi choisir ?",
        ]
    },

    "comptabilite_gestion": {
        "patterns": [
            "compta","charge","impot","urssaf","tva","tresor",
            "fact","bilan","benefic","chiffre affaire","cotisation",
            "expert-compt","fiscalit","declarati","resultat",
        ],
        "weight": 1.5,
        "response": (
            "**Gestion financiere pour entrepreneur** :\n\n"
            "**Les 4 regles d or** :\n"
            "1. Compte bancaire SEPARE obligatoirement (meme en micro)\n"
            "2. Mettez 30% de chaque paiement de cote (charges + impots)\n"
            "3. Facturez immediatement, relancez a J+30, J+45, J+60\n"
            "4. Consultez un expert-comptable au minimum 1x/an\n\n"
            "**En micro-entreprise, vos charges** :\n"
            "- Vente de marchandises : 12,8% du CA\n"
            "- Prestations de services : 22% du CA\n"
            "- Plus versement liberatoire impot : +1 a 2,2% selon revenus\n\n"
            "**Seuils TVA 2025** :\n"
            "- Services : 36 800 EUR (franchise) / 39 100 EUR (seuil majore)\n"
            "- Vente/hebergement : 91 900 EUR / 101 000 EUR\n\n"
            "**Outils gratuits ou peu chers** :\n"
            "Indy (auto-entrepreneur, 14 EUR/mois), Pennylane (18 EUR/mois), "
            "Shine (compte pro + compta 6 EUR/mois)"
        ),
        "followups": [
            "Comment gerer ma tresorerie au quotidien ?",
            "Quand passer a la TVA et comment ?",
            "Comment optimiser mes charges legalement ?",
        ]
    },

    "reseaux_sociaux": {
        "patterns": [
            "instagram","linkedin","facebook","tiktok","youtube",
            "twitter","pinterest","snapchat","reseaux sociaux",
            "community","follower","abonne","engage","viral",
        ],
        "weight": 1.8,
        "response": (
            "**Reseaux sociaux — la strategie qui fonctionne en 2025** :\n\n"
            "**Choisissez 1 reseau principal et tenez 90 jours** :\n\n"
            "**LinkedIn** (B2B, conseil, services pro) :\n"
            "Format gagnant : posts texte + 1 insight surprenant + question finale\n"
            "Frequence : 3-4 posts/semaine, 8h-10h ou 17h-19h mar-jeu\n"
            "Secret : commentez 10 posts de votre cible chaque matin (visibilite gratuite)\n\n"
            "**Instagram** (B2C, produits visuels, lifestyle) :\n"
            "Format gagnant : Reels 15-30s + audio tendance + hook 2 premieres secondes\n"
            "Frequence : 5 Reels/semaine + Stories quotidiennes\n"
            "Secret : publiez et engagez pendant 30 min pour booster l algorithme\n\n"
            "**TikTok** (large audience, notoriete rapide) :\n"
            "Format gagnant : education + humour + storytelling\n"
            "Frequence : 1-2 videos/jour minimum au debut\n\n"
            "**La regle universelle** : valeur d abord, vente ensuite (80/20)"
        ),
        "followups": [
            "Comment creer un Reel qui fonctionne ?",
            "Comment ecrire un post LinkedIn viral ?",
            "Comment monetiser mon audience sur TikTok ?",
        ]
    },

    "recrutement_equipe": {
        "patterns": [
            "recrut","salari","embauche","contrat","employ","equipe",
            "freelanc","alternance","stage","premia","outsourc",
            "sous-traitant","equipe","collaborateur","rh",
        ],
        "weight": 1.5,
        "response": (
            "**Recruter intelligemment** :\n\n"
            "**Avant de recruter un salarie, explorez** :\n"
            "1. Freelance (Malt, Fiverr, LinkedIn) : ideal pour missions ponctuelles\n"
            "2. Alternant : 0 EUR de charges nettes + aide gouvernementale\n"
            "   -> Aide unique : jusqu a 6 000 EUR la 1ere annee\n"
            "3. Stage : 600 EUR/mois gratification pour 6 mois de soutien\n"
            "4. Portage salarial : le freelance reste salarie d une societe tierce\n\n"
            "**Si vous recrutez un salarie** :\n"
            "- Salaire brut 2 000 EUR = cout reel 2 700 EUR (charges incluses)\n"
            "- Utilisez un cabinet RDV pour le recrutement technique\n"
            "- Commencez par un CDD de 3 mois pour valider l adequation\n\n"
            "**La question cle avant de recruter** :\n"
            "Est-ce que je refuse des clients ou missions faute de temps ? "
            "Si oui, recrutez. Sinon, optimisez d abord."
        ),
        "followups": [
            "Comment trouver un bon freelance ?",
            "Quelles aides pour embaucher un alternant ?",
            "Comment rediger une offre d emploi attractive ?",
        ]
    },

    "mindset_motivation": {
        "patterns": [
            "motiv","confianz","peur","syndrome imposteur","doute",
            "burnout","stress","mental","decourag","abandon",
            "mindset","resilience","objectif","vision","but",
        ],
        "weight": 1.5,
        "response": (
            "**Le mindset entrepreneur — ce qu on ne vous dit pas** :\n\n"
            "**La verite sur le syndrome de l imposteur** :\n"
            "95% des entrepreneurs le vivent. Jeff Bezos, Sheryl Sandberg, "
            "tous temoignent l avoir ressenti. C est un signal que vous grandissez, pas que vous echouez.\n\n"
            "**Les 4 realites du premier an** :\n"
            "1. La croissance est rarement lineaire (attendez-vous a des creux)\n"
            "2. La solitude est reelle (rejoignez des communautes)\n"
            "3. Le doute ne disparait pas, vous apprenez a agir malgre lui\n"
            "4. Les comparaisons avec les autres faussent votre perception\n\n"
            "**Outils anti-burnout** :\n"
            "- Reglez des heures de travail fixes (pas de check email apres 20h)\n"
            "- Celebrez CHAQUE victoire, meme minime\n"
            "- Mesurez vos progres (pas seulement le CA)\n"
            "- 1 journee sans ecrans par semaine\n\n"
            "**Votre action maintenant** : rejoignez un groupe Slack ou Discord "
            "d entrepreneurs de votre secteur. La communaute est le meilleur "
            "antidote a la solitude entrepreneuriale."
        ),
        "followups": [
            "Comment gerer le syndrome de l imposteur ?",
            "Comment eviter le burnout entrepreneurial ?",
            "Comment rester motive sur le long terme ?",
        ]
    },

    "salutation": {
        "patterns": ["bonjour","salut","bonsoir","hello","coucou","hey","bonne"],
        "weight": 3.0,
        "response": (
            "**Bonjour ! Je suis BizIBot, votre assistant strategique.**\n\n"
            "Je reponds en francais sur tous les sujets de votre activite :\n"
            "strategie, clients, marketing, prix, financement, organisation...\n\n"
            "**Quelle est votre question du moment ?**"
        ),
        "followups": [
            "Comment trouver mes premiers clients ?",
            "Comment fixer mes prix ?",
            "Comment me differencier de mes concurrents ?",
        ]
    },

    "remerciement": {
        "patterns": ["merci","super","parfait","excellent","genial","top","bien","bravo","utile"],
        "weight": 3.0,
        "response": (
            "Avec plaisir ! Je suis la pour ca.\n\n"
            "N hesitez pas si vous avez d autres questions. "
            "Je connais votre profil et peux vous aider sur tous les aspects "
            "de votre activite.\n\n"
            "**Qu est-ce que vous souhaitez approfondir ?**"
        ),
        "followups": [
            "Ma strategie marketing",
            "Comment augmenter mon CA ?",
            "Mon plan d action prioritaire",
        ]
    },

    "aide_generale": {
        "patterns": ["aide","help","quoi","comment","que faire","par ou","conseil","besoin","perdu"],
        "weight": 0.5,
        "response": (
            "**BizIBot — votre assistant strategique**\n\n"
            "Posez-moi une question precise et j y reponds avec des conseils actionnables.\n\n"
            "**Sujets disponibles** :\n"
            "Clients / Marketing / SEO / Prix / Creation d entreprise / "
            "Financement / Fidelisation / Concurrence / Reseaux sociaux / "
            "Productivite / Email / Comptabilite / Recrutement / Mindset / SWOT\n\n"
            "Exemples :\n"
            "- Comment trouver mes premiers clients ?\n"
            "- Comment fixer mes prix sans me sous-evaluer ?\n"
            "- Quelle strategie LinkedIn pour un consultant ?\n"
            "- Comment reduire mon churn de 30% ?"
        ),
        "followups": [
            "Comment trouver mes premiers clients ?",
            "Comment fixer mes prix ?",
            "Par ou commencer ma strategie marketing ?",
        ]
    },
}

# ========================================================================
# MOTEUR TF-IDF AMELIORE — avec bigrams et poids
# ========================================================================

def _compute_tfidf(query_tokens, doc_patterns, weight=1.0):
    """Score TF-IDF ameliore avec bigrams."""
    score = 0.0
    query_set = set(query_tokens)
    query_bigrams = set(_bigrams(query_tokens))

    # Tokens des patterns
    pat_tokens = []
    for p in doc_patterns:
        pt = _tokenize(p)
        pat_tokens.extend(pt)
        # Bigrams des patterns
        query_bigrams.update(_bigrams(pt))

    pat_freq = _Counter(pat_tokens)
    total_pat = sum(pat_freq.values()) or 1

    for qt in query_tokens:
        if qt in pat_freq:
            tf = pat_freq[qt] / total_pat
            idf = _math.log(1 + 1.0 / (pat_freq[qt] / total_pat))
            score += tf * idf * 2.0

    # Bonus bigrams
    for bg in query_bigrams:
        if "_" in bg:
            parts = bg.split("_")
            if all(p in pat_freq for p in parts):
                score += 1.5

    return score * weight


def match_intent(question):
    """
    Retourne le topic le plus pertinent avec son score.
    Utilise TF-IDF + bigrams + stemming.
    """
    tokens = _tokenize(_normalize(question))
    if not tokens:
        return "aide_generale", 0.0

    best_topic = "aide_generale"
    best_score = 0.0
    scores = {}

    for topic, data in _KB.items():
        if topic in ("salutation", "remerciement", "aide_generale"):
            # Matching exact pour ces topics speciaux
            q_lower = question.lower()
            exact_match = any(p in q_lower for p in data["patterns"])
            if exact_match:
                scores[topic] = 5.0 * data.get("weight", 1.0)
            else:
                scores[topic] = 0.0
        else:
            s = _compute_tfidf(tokens, data["patterns"], data.get("weight", 1.0))
            scores[topic] = s

    # Tri par score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if ranked[0][1] > 0:
        best_topic = ranked[0][0]
        best_score = ranked[0][1]

    return best_topic, best_score


# ========================================================================
# GENERATEUR DE REPONSE CONTEXTUEL
# ========================================================================

ACT_LABELS = {
    "ecommerce": "e-commerce", "saas": "SaaS/tech", "service": "services",
    "consulting": "conseil", "content": "creation de contenu", "other": "votre activite"
}
GOAL_LABELS = {
    "leads": "generer des leads", "sales": "augmenter les ventes",
    "awareness": "developper la notoriete", "traffic": "attirer du trafic",
    "retention": "fideliser vos clients", "launch": "lancer votre activite",
    "growth": "accelerer la croissance"
}
MAT_LABELS = {
    "idea": "phase idee", "inprogress": "lancement en cours",
    "launched": "activite lancee", "growing": "en croissance"
}


def generate_response(question, context=None, history=None):
    """
    Genere une reponse personnalisee avec contexte et historique.

    Args:
        question: la question de l utilisateur
        context: dict {activity, goal, maturity, monthly_budget, user_name}
        history: list des derniers messages (pour memoire conversationnelle)
    """
    ctx = context or {}
    activity = ctx.get("activity", "service")
    goal     = ctx.get("goal", "leads")
    maturity = ctx.get("maturity", "launched")
    budget   = float(ctx.get("monthly_budget", 0))
    username = ctx.get("user_name", "")

    # Enrichissement par historique (contexte conversationnel)
    if history:
        recent = history[-3:]
        prev_topics = []
        for msg in recent:
            if msg.get("role") == "assistant" and msg.get("topic"):
                prev_topics.append(msg["topic"])

    topic, score = match_intent(question)
    data = _KB.get(topic, _KB["aide_generale"])
    response = data["response"]
    followups = data.get("followups", [])

    # Personnalisation contextuelle
    act_lbl  = ACT_LABELS.get(activity, "votre activite")
    goal_lbl = GOAL_LABELS.get(goal, "vos objectifs")
    mat_lbl  = MAT_LABELS.get(maturity, "votre stade")

    # Ajout contexte personnalise si score suffisant
    if score > 1.0 and topic not in ("salutation", "remerciement", "aide_generale"):
        greeting = f"{username}, " if username else ""
        ctx_note = (
            f"\n\n---\n*Adapte a votre profil : {greeting}"
            f"**{act_lbl}** | objectif **{goal_lbl}** | {mat_lbl}*"
        )
        response += ctx_note

    # Conseil budget contextuel
    if topic in ("financement_aides", "tarification_prix", "comptabilite_gestion"):
        if budget > 0:
            if budget < 100:
                bgt_note = f"\n\n*Budget {budget:.0f} EUR/mois : concentrez-vous sur les canaux 100% gratuits.*"
            elif budget < 500:
                bgt_note = f"\n\n*Budget {budget:.0f} EUR/mois : 1-2 outils payants max, priorisez l organique.*"
            else:
                bgt_note = f"\n\n*Budget {budget:.0f} EUR/mois : vous pouvez tester des campagnes payantes.*"
            response += bgt_note

    # Conseil maturite pour creation/lancement
    if topic == "creation_entreprise":
        if maturity == "idea":
            response += "\n\n*Phase idee : validez avec 10 interviews clients avant d investir quoi que ce soit.*"
        elif maturity == "launched":
            response += "\n\n*Vous etes deja lance : concentrez-vous sur l optimisation, pas la creation.*"

    # Adaptation secteur pour acquisition
    if topic == "acquisition_clients":
        sector_tips = {
            "ecommerce": "\n\n*Pour votre e-commerce : Google Shopping + retargeting Meta = combo gagnant.*",
            "saas":      "\n\n*Pour votre SaaS : essai gratuit 14j + onboarding guide = taux conv x3.*",
            "consulting":"\n\n*Pour le conseil : LinkedIn + etudes de cas chiffrees = meilleurs leads.*",
            "content":   "\n\n*Pour la creation de contenu : TikTok/YouTube + collab + monetisation directe.*",
        }
        if activity in sector_tips:
            response += sector_tips[activity]

    return {
        "response":  response,
        "topic":     topic,
        "score":     round(score, 2),
        "followups": followups[:3],
    }


# ========================================================================
# GESTION HISTORIQUE
# ========================================================================

def init_chat_history(ss):
    if "bizibot_history" not in ss:
        ss["bizibot_history"] = []


def add_message(ss, role, content):
    ss.setdefault("bizibot_history", [])
    ss["bizibot_history"].append({"role": role, "content": content})
    if len(ss["bizibot_history"]) > 40:
        ss["bizibot_history"] = ss["bizibot_history"][-40:]


def get_history(ss):
    return ss.get("bizibot_history", [])


def clear_history(ss):
    ss["bizibot_history"] = []
