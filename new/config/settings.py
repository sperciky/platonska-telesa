"""
Konfigurační nastavení pro aplikaci Platónská tělesa
Configuration settings for Platonic Solids application
"""

# Streamlit page configuration
PAGE_CONFIG = {
    'page_title': 'Platónská tělesa - Interaktivní tutoriál',
    'page_icon': '📐',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Layout configuration
LAYOUT = {
    'diagram_column_ratio': 0.6,  # 60% width for diagram
    'description_column_ratio': 0.4,  # 40% width for description
}

# Matplotlib figure settings
FIGURE = {
    'figsize': (8, 7),  # Width, height in inches
    'dpi': 100,
    'facecolor': 'white',
}

# 3D plot settings
PLOT_3D = {
    'axis_limits': (-2, 2),
    'box_aspect': [1, 1, 1],
    'elevation': 20,
    'azimuth': 45,
}

# Visual styles
COLORS = {
    'selected_point': 'red',
    'unselected_point': 'lightgray',
    'cube_edge': 'gray',
    'solid_edge': 'blue',
    'strong_edge': 'red',

    # Color schemes for different solids
    'tetrahedron': '#FF6B6B',
    'octahedron': '#4ECDC4',
    'icosahedron': '#95E1D3',
    'dodecahedron': '#F38181',
}

SIZES = {
    'point_default': 100,
    'point_small': 60,
    'point_large': 150,
    'point_highlighted': 200,
    'edge_width': 2,
    'edge_width_thin': 1,
    'edge_width_thick': 3,
}

FONTS = {
    'title': 16,
    'subtitle': 14,
    'description': 11,
    'monospace': 'Consolas',
}

# Text settings
TEXT = {
    'box_style': 'round',
    'box_facecolor': 'wheat',
    'box_alpha': 0.9,
    'font_family': 'monospace',
}

# Golden ratio
PHI = (1 + 5**0.5) / 2

# Application metadata
APP_INFO = {
    'title': 'INTERAKTIVNÍ KONSTRUKCE PLATÓNSKÝCH TĚLES',
    'subtitle': 'Naučte se konstruovat všech 5 pravidelných mnohostěnů',
    'version': '2.0.0',
    'author': 'Matematický kroužek',
}
