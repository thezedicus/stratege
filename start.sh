#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Stratège — Script de démarrage local (macOS / Python 3.9.6 + Node 20+)
# Usage : bash start.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"
FRONTEND_DIR="$REPO_ROOT/frontend"

# ── Couleurs ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'

log()  { echo -e "${BLUE}[Stratège]${NC} $1"; }
ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }

# ── Python ────────────────────────────────────────────────────────────────────
PYTHON=$(python3.9 -c "import sys; print(sys.executable)" 2>/dev/null || python3 -c "import sys; print(sys.executable)")
PY_VER=$($PYTHON --version 2>&1)
log "Python : $PY_VER ($PYTHON)"

# ── Environnement virtuel backend ─────────────────────────────────────────────
if [ ! -d "$BACKEND_DIR/.venv" ]; then
  log "Création du virtualenv backend..."
  $PYTHON -m venv "$BACKEND_DIR/.venv"
  ok "Virtualenv créé"
fi

log "Activation du virtualenv..."
source "$BACKEND_DIR/.venv/bin/activate"

log "Installation des dépendances backend..."
pip install --quiet --upgrade pip
pip install --quiet -r "$BACKEND_DIR/requirements.txt"
ok "Dépendances backend installées"

# ── .env backend ──────────────────────────────────────────────────────────────
if [ ! -f "$BACKEND_DIR/.env" ]; then
  warn ".env manquant → copie depuis .env.example"
  cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env" 2>/dev/null || cat > "$BACKEND_DIR/.env" <<'EOF'
ENVIRONMENT=development
DEBUG=true
# PAGESPEED_API_KEY=votre_cle_google
EOF
fi

# ── Node / npm ────────────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  log "Node non trouvé — chargement nvm..."
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
fi
NODE_VER=$(node --version 2>/dev/null || echo "non trouvé")
log "Node : $NODE_VER"

# ── Dépendances frontend ──────────────────────────────────────────────────────
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
  log "Installation npm frontend..."
  cd "$FRONTEND_DIR" && npm install --silent
  cd "$REPO_ROOT"
  ok "Dépendances frontend installées"
fi

# ── .env frontend ─────────────────────────────────────────────────────────────
if [ ! -f "$FRONTEND_DIR/.env.local" ]; then
  echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > "$FRONTEND_DIR/.env.local"
  ok ".env.local frontend créé"
fi

# ── Démarrage ─────────────────────────────────────────────────────────────────
log "Démarrage du backend FastAPI sur http://localhost:8000 ..."
cd "$BACKEND_DIR"
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd "$REPO_ROOT"

sleep 2
log "Démarrage du frontend Next.js sur http://localhost:3000 ..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!
cd "$REPO_ROOT"

ok "Stratège est disponible sur http://localhost:3000"
echo ""
echo "  Backend  → http://localhost:8000"
echo "  Frontend → http://localhost:3000"
echo "  API Docs → http://localhost:8000/docs"
echo ""
echo "  Ctrl+C pour arrêter les deux serveurs"

# ── Arrêt propre ──────────────────────────────────────────────────────────────
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Serveurs arrêtés.'" SIGINT SIGTERM
wait
