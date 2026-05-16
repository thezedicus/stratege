# 🚀 Stratège — Commandes de lancement (macOS, Python 3.9.6)

## Méthode 1 — Script automatique (recommandé)

```bash
# Depuis la racine du repo
bash start.sh
```

Le script :
- Crée le virtualenv Python 3.9.6
- Installe toutes les dépendances backend
- Lance uvicorn sur le port 8000
- Lance Next.js sur le port 3000

---

## Méthode 2 — Démarrage manuel (deux terminaux)

### Terminal 1 — Backend (FastAPI)

```bash
cd /chemin/vers/stratege/backend

# Créer le virtualenv avec Python 3.9.6
python3.9 -m venv .venv

# Activer
source .venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Copier le .env
cp .env.example .env   # puis éditer si besoin

# Lancer le serveur
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Le backend est disponible sur : http://localhost:8000  
Documentation Swagger : http://localhost:8000/docs

---

### Terminal 2 — Frontend (Next.js 14)

```bash
cd /chemin/vers/stratege/frontend

# Installer les dépendances Node (une seule fois)
npm install

# Créer le fichier .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Lancer le serveur de développement
npm run dev
```

Le frontend est disponible sur : http://localhost:3000

---

## Méthode 3 — Build de production

### Backend
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd frontend
npm run build    # compile Next.js
npm start        # démarre en mode production
```

---

## Variables d'environnement

### `backend/.env`
```env
ENVIRONMENT=development
DEBUG=true
# Optionnel — améliore l'analyse PageSpeed
PAGESPEED_API_KEY=votre_cle_google_pagespeed
```

### `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Dépendances exactes

### Python (backend/requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2
python-dotenv==1.0.0
python-multipart==0.0.6
```

### Node (frontend/package.json — packages clés)
```
next@14
react@18
react-dom@18
axios
recharts
lucide-react
jspdf
react-hot-toast
tailwindcss@3
typescript
```

---

## Vérification que tout tourne

```bash
# Backend OK
curl http://localhost:8000/api/health

# Frontend OK
open http://localhost:3000
```

---

## Problèmes courants

| Problème | Solution |
|---|---|
| `python3.9: command not found` | `brew install python@3.9` |
| `node: command not found` | `source ~/.nvm/nvm.sh && nvm use 20` |
| `Port 8000 already in use` | `lsof -ti:8000 \| xargs kill` |
| `Port 3000 already in use` | `lsof -ti:3000 \| xargs kill` |
| `ModuleNotFoundError` | `pip install -r requirements.txt` dans le venv actif |
| `npm ERR! ENOENT` | `cd frontend && npm install` |

---

## Structure du repo

```
stratege/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Dépendances Python
│   ├── .env.example               # Variables d'env template
│   └── app/
│       ├── config.py
│       ├── routers/
│       │   ├── analysis.py        # POST /api/analysis, GET /api/analysis/{id}
│       │   └── health.py          # GET /api/health
│       ├── models/
│       │   └── schemas.py         # Pydantic models
│       └── services/
│           ├── swot_service.py    # Analyse SWOT par secteur
│           ├── persona_service.py # Génération de personas
│           ├── marketing_service.py
│           ├── seo_service.py
│           ├── ads_service.py
│           ├── sales_service.py
│           ├── synthesis_service.py
│           └── pagespeed_service.py
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx           # Landing page
    │   │   ├── wizard/page.tsx    # Wizard 5 étapes
    │   │   └── dashboard/[id]/page.tsx  # Dashboard 7 onglets
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── AppShell.tsx   # Sidebar gauche + shell
    │   │   │   └── RightPanel.tsx # Panneau droit
    │   │   └── dashboard/tabs/    # SwotTab, PersonasTab, etc.
    │   └── lib/
    │       └── api.ts             # Axios client
    ├── tailwind.config.js
    ├── next.config.js
    └── package.json
```
