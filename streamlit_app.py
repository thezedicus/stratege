# Point d'entrée Streamlit Cloud — redirige vers biziapp.py
# Streamlit Cloud cherche ce fichier par défaut

import runpy
import os
import sys

# Exécute biziapp.py dans le même répertoire
_dir = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(_dir, "biziapp.py"), run_name="__main__")
