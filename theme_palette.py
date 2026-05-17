"""
theme_palette.py
================
Palette de couleurs centralisée pour le backend Stratège.
Source de vérité unique côté Python — doit rester synchronisée avec
frontend/src/styles/tokens.css.

Utile pour :
  - exports PDF via ReportLab (rapports de synthèse stratégique)
  - graphiques Matplotlib / Plotly côté API
  - email transactionnels (templating)
  - tout générateur d'images / médias backend

Usage :
    from app.services.theme_palette import PALETTE, hex_to_rgb

    color = PALETTE["ambre"]               # → "#D97706"
    r, g, b = hex_to_rgb(PALETTE["sauge"]) # → (4, 120, 87)
"""

from __future__ import annotations
from typing import Tuple, Dict


# ─────────────────────────────────────────────────────────────────────────────
# PALETTE — copie miroir des tokens CSS (tokens.css)
# ─────────────────────────────────────────────────────────────────────────────
PALETTE: Dict[str, str] = {
    # Neutres
    "ivoire":        "#FAF8F4",
    "brume":         "#F2EFE8",
    "craie":         "#E7E2D6",
    "encre":         "#1A1A1A",
    "encre_soft":    "#4A4A4A",
    "encre_mute":    "#8A8A8A",

    # Graphite (dominante)
    "graphite":      "#0F172A",
    "graphite_soft": "#1E293B",
    "graphite_mute": "#475569",

    # Ambre (accent chaud)
    "ambre":         "#D97706",
    "ambre_soft":    "#FBBF24",
    "ambre_pale":    "#FEF3C7",

    # Sauge (accent froid)
    "sauge":         "#047857",
    "sauge_soft":    "#10B981",
    "sauge_pale":    "#D1FAE5",

    # États
    "danger":        "#B91C1C",
    "danger_pale":   "#FEE2E2",
    "warn":          "#C2410C",
    "warn_pale":     "#FFEDD5",
    "info":          "#1D4ED8",
    "info_pale":     "#DBEAFE",
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """'#FAF8F4' → (250, 248, 244)"""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Couleur hex invalide : {hex_color}")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def hex_to_rgb_norm(hex_color: str) -> Tuple[float, float, float]:
    """'#FAF8F4' → (0.98, 0.97, 0.96) — utile pour ReportLab."""
    r, g, b = hex_to_rgb(hex_color)
    return (r / 255, g / 255, b / 255)


def reportlab_color(name: str):
    """
    Retourne un objet reportlab.lib.colors.Color pour la palette.
    Import paresseux pour ne pas forcer la dépendance reportlab partout.

    Usage:
        from app.services.theme_palette import reportlab_color
        c = reportlab_color("ambre")
        canvas.setFillColor(c)
    """
    try:
        from reportlab.lib.colors import Color
    except ImportError as exc:
        raise ImportError(
            "reportlab n'est pas installé. `pip install reportlab` pour utiliser cette fonction."
        ) from exc

    if name not in PALETTE:
        raise KeyError(f"Couleur '{name}' inconnue. Disponibles : {list(PALETTE.keys())}")
    r, g, b = hex_to_rgb_norm(PALETTE[name])
    return Color(r, g, b)


def plotly_template() -> Dict:
    """
    Template Plotly minimal aligné sur la charte Stratège.
    Usage:
        import plotly.graph_objects as go
        from app.services.theme_palette import plotly_template
        fig = go.Figure()
        fig.update_layout(template=plotly_template())
    """
    return {
        "layout": {
            "paper_bgcolor": PALETTE["ivoire"],
            "plot_bgcolor":  PALETTE["ivoire"],
            "font": {
                "family": "Geist, -apple-system, sans-serif",
                "color":  PALETTE["encre"],
                "size":   13,
            },
            "title": {
                "font": {
                    "family": "Fraunces, serif",
                    "color":  PALETTE["encre"],
                    "size":   20,
                },
            },
            "colorway": [
                PALETTE["graphite"],
                PALETTE["ambre"],
                PALETTE["sauge"],
                PALETTE["info"],
                PALETTE["warn"],
                PALETTE["graphite_mute"],
                PALETTE["ambre_soft"],
                PALETTE["sauge_soft"],
            ],
            "xaxis": {
                "gridcolor":  PALETTE["craie"],
                "linecolor":  PALETTE["encre_mute"],
                "tickcolor":  PALETTE["encre_mute"],
                "zerolinecolor": PALETTE["craie"],
            },
            "yaxis": {
                "gridcolor":  PALETTE["craie"],
                "linecolor":  PALETTE["encre_mute"],
                "tickcolor":  PALETTE["encre_mute"],
                "zerolinecolor": PALETTE["craie"],
            },
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# Mapping sémantique (lisibilité dans le code applicatif)
# ─────────────────────────────────────────────────────────────────────────────
SEMANTIC = {
    "primary":         PALETTE["graphite"],
    "primary_hover":   PALETTE["graphite_soft"],
    "accent":          PALETTE["ambre"],
    "accent_hover":    PALETTE["ambre_soft"],
    "success":         PALETTE["sauge"],
    "error":           PALETTE["danger"],
    "warning":         PALETTE["warn"],
    "info":            PALETTE["info"],
    "background":      PALETTE["ivoire"],
    "surface":         PALETTE["brume"],
    "border":          PALETTE["craie"],
    "text_primary":    PALETTE["encre"],
    "text_secondary":  PALETTE["encre_soft"],
    "text_muted":      PALETTE["encre_mute"],
}


if __name__ == "__main__":
    # Petit smoke-test
    print("Palette Stratège :")
    for name, hexcode in PALETTE.items():
        print(f"  {name:18s} {hexcode}  rgb{hex_to_rgb(hexcode)}")
