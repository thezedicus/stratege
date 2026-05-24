# streamlit_app.py — Point d'entree Streamlit Cloud
# Streamlit Cloud detecte automatiquement ce fichier
# Importe biziapp.py directement sans exec() pour compatibilite maximale

import os
import sys

# S'assurer que le repertoire courant est dans le path
_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

# Import direct — Streamlit Cloud peut detecter st.set_page_config()
import biziapp  # noqa: F401
