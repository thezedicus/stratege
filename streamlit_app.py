# streamlit_app.py — Entry point for Streamlit Cloud
# Launches biziapp.py in the same Python namespace

import os
import sys

# Add current directory to path
_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

# Execute biziapp.py directly
_app = os.path.join(_dir, "biziapp.py")
with open(_app, "r", encoding="utf-8") as _f:
    _code = _f.read()

exec(compile(_code, _app, "exec"), {"__name__": "__main__", "__file__": _app})
