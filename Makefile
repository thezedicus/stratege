.PHONY: install start backend frontend build clean help

## Afficher l'aide
help:
	@echo ""
	@echo "  \033[1mStratège — Commandes disponibles\033[0m"
	@echo ""
	@echo "  make install    Installer toutes les dépendances"
	@echo "  make start      Démarrer backend + frontend"
	@echo "  make backend    Démarrer le backend seul"
	@echo "  make frontend   Démarrer le frontend seul"
	@echo "  make build      Build de production Next.js"
	@echo "  make clean      Supprimer venv, node_modules, .next"
	@echo ""

## Installer toutes les dépendances
install:
	@echo "📦 Installation backend..."
	cd backend && python3.9 -m venv .venv && .venv/bin/pip install -q --upgrade pip && .venv/bin/pip install -q -r requirements.txt
	@echo "📦 Installation frontend..."
	cd frontend && npm install --silent
	@echo "✅ Dépendances installées"

## Démarrer les deux serveurs
start:
	@bash start.sh

## Backend seul
backend:
	@cd backend && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Frontend seul
frontend:
	@cd frontend && npm run dev

## Build production
build:
	@cd frontend && npm run build
	@echo "✅ Build Next.js terminé"

## Nettoyage
clean:
	@rm -rf backend/.venv frontend/node_modules frontend/.next
	@echo "✅ Nettoyage terminé"
