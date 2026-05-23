# Stratège — Expert Virtuel en Stratégie Business

> Application web qui agit comme un expert freelance virtuel en stratégie business, marketing, vente et communication.

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-blue)
![License](https://img.shields.io/badge/license-MIT-purple)

## Fonctionnalités

- **Wizard de qualification** : Formulaire multi-étapes avec barre de progression
- **Diagnostic Stratégique** : Analyse SWOT automatisée selon le budget et secteur
- **Personas & Psychologie** : 5 personas détaillés (SONCAS, AIDA, SPIN) avec photos réelles
- **Stratégie de Vente** : Scripts SPIN, Challenger, SONCAS personnalisés
- **Marketing Digital** : Plan de contenu, calendrier éditorial, règle 80/20
- **SEO, SEA & GEO** : Audit on-page, mots-clés, campagnes Google Ads
- **Publicité Payante & Organique** : Media plan Facebook/Instagram/Google Ads
- **Rapport de Synthèse** : Actions prioritaires, estimation ROI, export PDF

## Stack Technique

| Couche | Technologie |
|--------|------------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS + Framer Motion |
| Charts | Recharts |
| Backend | Python FastAPI |
| BDD | PostgreSQL |
| Hébergement | Vercel (front) + Railway (back) |

## APIs Intégrées

- Google PageSpeed Insights
- Random User Generator (randomuser.me)
- OpenAI API (gpt-3.5-turbo avec fallback template)
- DummyJSON / Fake Store API
- Google Trends (pytrends)

## Démarrage rapide

### Prérequis
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Renseigner les variables d'environnement
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Renseigner les variables d'environnement
uvicorn main:app --reload
```

### Docker (tout-en-un)

```bash
cp .env.example .env
docker-compose up --build
```

## Variables d'environnement

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_KEY=sk-...  # optionnel
```

### Backend (`.env`)
```
DATABASE_URL=postgresql://user:password@localhost:5432/stratege
OPENAI_API_KEY=sk-...
PAGESPEED_API_KEY=...  # optionnel
SECRET_KEY=your-secret-key
```

## Déploiement

### Vercel (Frontend)
```bash
cd frontend
npx vercel --prod
```

### Railway (Backend)
Importer le repo dans [Railway](https://railway.app) et pointer vers le dossier `backend`.

## Structure du projet

```
stratege/
├── frontend/          # Next.js 14 App
│   └── src/
│       ├── app/       # App Router
│       ├── components/
│       ├── lib/
│       └── hooks/
├── backend/           # FastAPI
│   └── app/
│       ├── models/
│       ├── routers/
│       └── services/
└── docker-compose.yml
```

## Licence

MIT — Voir [LICENSE](LICENSE)


## Déploiement Streamlit Cloud

**URL GitHub à entrer dans Streamlit Cloud :**
```
https://github.com/thezedicus/stratege/blob/main/biziapp.py
```

> Le repo doit être connecté via GitHub OAuth dans Streamlit Cloud.
> Le champ "GitHub URL" doit pointer vers le fichier `.py` directement.
