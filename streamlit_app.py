# streamlit_app.py — Point d'entrée pour Streamlit Cloud
# Lance biziapp.py directement dans le même namespace

import os, sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_app_file  = os.path.join(_this_dir, "biziapp.py")

with open(_app_file, "r", encoding="utf-8") as _f:
    exec(compile(_f.read(), _app_file, "exec"), {"__name__": "__main__", "__file__": _app_file})
