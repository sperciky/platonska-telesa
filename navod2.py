import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button

# =============================================================================
# POMOCNÉ FUNKCE
# =============================================================================

def plot_point(ax, point, color='red', size=100, label=''):
    """Nakreslí jeden bod"""
    ax.scatter([point[0]], [point[1]], [point[2]], 
               c=color, s=size, alpha=0.9, edgecolors='black', linewidth=2)
    if label:
        ax.text(point[0], point[1], point[2], f'  {label}', 
                fontsize=12, fontweight='bold', color='black')

def plot_edge(ax, p1, p2, color='blue', width=2, style='-'):
    """Nakreslí hranu mezi dvěma body"""
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
            color=color, linewidth=width, linestyle=style, alpha=0.8)

# =============================================================================
# PŘÍPRAVA DAT
# =============================================================================

phi = (1 + np.sqrt(5)) / 2

# Data pro všechny kroky
cube_vertices = np.array([
    [-1, -1, -1],  # 0
    [-1, -1,  1],  # 1
    [-1,  1, -1],  # 2
    [-1,  1,  1],  # 3
    [ 1, -1, -1],  # 4
    [ 1, -1,  1],  # 5
    [ 1,  1, -1],  # 6
    [ 1,  1,  1]   # 7
])

cube_edges = [
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), 
    (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
]

# OPRAVA: Správné vrcholy čtyřstěnu (žádné dva nejsou sousedé)
# Vrcholy: (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)
tetra_indices = [7, 4, 2, 1]
tetra_vertices = cube_vertices[tetra_indices]
tetra_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]

octa_vertices = np.array([
    [ 1,  0,  0], [-1,  0,  0], [ 0,  1,  0], 
    [ 0, -1,  0], [ 0,  0,  1], [ 0,  0, -1]
])

icosa_vertices = np.array([
    [ 0,  1,  phi], [ 0,  1, -phi], [ 0, -1,  phi], [ 0, -1, -phi],
    [ 1,  phi,  0], [ 1, -phi,  0], [-1,  phi,  0], [-1, -phi,  0],
    [ phi,  0,  1], [ phi,  0, -1], [-phi,  0,  1], [-phi,  0, -1]
])

rect1 = icosa_vertices[:4]

dodeca_vertices = []
for i in [-1, 1]:
    for j in [-1, 1]:
        for k in [-1, 1]:
            dodeca_vertices.append([i, j, k])

for coords in [
    [0, 1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, phi], [0, -1/phi, -phi],
    [1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, phi, 0], [-1/phi, -phi, 0],
    [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi]
]:
    dodeca_vertices.append(coords)

dodeca_vertices = np.array(dodeca_vertices)

# =============================================================================
# FUNKCE PRO KRESLENÍ JEDNOTLIVÝCH KROKŮ
# =============================================================================

def draw_step_0(ax):
    """Krok 0: Úvodní obrazovka"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('KONSTRUKCE PLATÓNSKÝCH TĚLES\n\nPoužij tlačítka Další/Předchozí', 
                 fontsize=16, fontweight='bold')
    
    text = """Naučíš se:

1. Čtyřstěn (4 vrcholy)
2. Osmistěn (6 vrcholů)
3. Dvacetistěn (12 vrcholů)
4. Dvanáctistěn (20 vrcholů)
5. Střed trojúhelníku

Použij tlačítka dole pro navigaci →"""
    
    ax.text2D(0.5, 0.5, text, transform=ax.transAxes, fontsize=14,
              verticalalignment='center', horizontalalignment='center',
              bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

def draw_step_1(ax):
    """Čtyřstěn - Krok 1: Krychle"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('ČTYŘSTĚN - Krok 1: Krychle', fontsize=14, fontweight='bold')
    
    for edge in cube_edges:
        plot_edge(ax, cube_vertices[edge[0]], cube_vertices[edge[1]], 
                  color='gray', width=1, style='--')
    
    for i, v in enumerate(cube_vertices):
        plot_point(ax, v, color='lightgray', size=80, label=str(i))
    
    text = """Krychle má 8 vrcholů:
(±1, ±1, ±1)

Vrchol 0: (-1,-1,-1)
Vrchol 1: (-1,-1, 1)
Vrchol 2: (-1, 1,-1)
...
Vrchol 7: ( 1, 1, 1)

Z nich vybereme 4 vrcholy."""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=10,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_2(ax):
    """Čtyřstěn - Krok 2: Výběr vrcholů"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('ČTYŘSTĚN - Krok 2: Výběr 4 vrcholů', fontsize=14, fontweight='bold')
    
    for edge in cube_edges:
        plot_edge(ax, cube_vertices[edge[0]], cube_vertices[edge[1]], 
                  color='lightgray', width=1, style='--')
    
    for i, v in enumerate(cube_vertices):
        if i in tetra_indices:
            plot_point(ax, v, color='red', size=150, label=str(i))
        else:
            plot_point(ax, v, color='lightgray', size=60, label=str(i))
    
    text = """Pravidlo: Součin souřadnic = 1

Vrchol 7: ( 1, 1, 1) → 1×1×1 = 1 ✓
Vrchol 4: ( 1,-1,-1) → 1×(-1)×(-1) = 1 ✓
Vrchol 2: (-1, 1,-1) → (-1)×1×(-1) = 1 ✓
Vrchol 1: (-1,-1, 1) → (-1)×(-1)×1 = 1 ✓

Žádné dva nejsou sousedé!"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=9,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_3(ax):
    """Čtyřstěn - Krok 3: Hotovo"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('ČTYŘSTĚN - Krok 3: Hotový čtyřstěn', fontsize=14, fontweight='bold')
    
    for edge in tetra_edges:
        plot_edge(ax, tetra_vertices[edge[0]], tetra_vertices[edge[1]], 
                  color='blue', width=3)
    
    labels_tetra = ['A (1,1,1)', 'B (1,-1,-1)', 'C (-1,1,-1)', 'D (-1,-1,1)']
    for i, (v, label) in enumerate(zip(tetra_vertices, labels_tetra)):
        plot_point(ax, v, color='red', size=150, label=label[0])
    
    edge_length = np.linalg.norm(tetra_vertices[0] - tetra_vertices[1])
    
    text = f"""Čtyřstěn:
- 4 vrcholy
- 6 hran
- 4 trojúhelníkové stěny

Délka hrany:
d = √[(1-1)² + (1-(-1))² + (1-(-1))²]
d = √[0 + 4 + 4]
d = √8 = 2√2 ≈ {edge_length:.3f}

Všechny hrany stejně dlouhé ✓"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=10,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_4(ax):
    """Osmistěn - Krok 1: Osy"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('OSMISTĚN - Krok 1: Vrcholy na osách', fontsize=14, fontweight='bold')
    
    ax.plot([-2, 2], [0, 0], [0, 0], 'r-', linewidth=2, alpha=0.3)
    ax.plot([0, 0], [-2, 2], [0, 0], 'g-', linewidth=2, alpha=0.3)
    ax.plot([0, 0], [0, 0], [-2, 2], 'b-', linewidth=2, alpha=0.3)
    
    labels = ['+X', '-X', '+Y', '-Y', '+Z', '-Z']
    colors = ['red', 'red', 'green', 'green', 'blue', 'blue']
    
    for v, label, color in zip(octa_vertices, labels, colors):
        plot_point(ax, v, color=color, size=150, label=label)
    
    text = """6 vrcholů na osách:
( 1,  0,  0) +X
(-1,  0,  0) -X
( 0,  1,  0) +Y
( 0, -1,  0) -Y
( 0,  0,  1) +Z
( 0,  0, -1) -Z"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=11,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_5(ax):
    """Osmistěn - Krok 2: Hotovo"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('OSMISTĚN - Krok 2: Hotový osmistěn', fontsize=14, fontweight='bold')
    
    octa_faces = [
        (0,2,4), (0,4,3), (0,3,5), (0,5,2),
        (1,4,2), (1,3,4), (1,5,3), (1,2,5)
    ]
    
    for face in octa_faces:
        for i in range(3):
            plot_edge(ax, octa_vertices[face[i]], octa_vertices[face[(i+1)%3]], 
                      color='blue', width=2)
    
    for i, v in enumerate(octa_vertices):
        plot_point(ax, v, color='red', size=150, label=str(i+1))
    
    edge_length = np.linalg.norm(octa_vertices[0] - octa_vertices[2])
    
    text = f"""Osmistěn:
- 6 vrcholů
- 12 hran
- 8 trojúhelníkových stěn

Délka hrany:
d = √[(1-0)² + (0-1)² + (0-0)²]
d = √2 ≈ {edge_length:.3f}"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=11,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_6(ax):
    """Dvacetistěn - Krok 1: První obdélník"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVACETISTĚN - Krok 1: Obdélník se zlatým řezem', fontsize=14, fontweight='bold')
    
    y_plane = [-2, 2, 2, -2, -2]
    z_plane = [-2, -2, 2, 2, -2]
    x_plane = [0, 0, 0, 0, 0]
    ax.plot(x_plane, y_plane, z_plane, 'r--', alpha=0.3, linewidth=1)
    
    rect_edges = [(0,1), (1,3), (3,2), (2,0)]
    for edge in rect_edges:
        plot_edge(ax, rect1[edge[0]], rect1[edge[1]], color='red', width=3)
    
    for i, v in enumerate(rect1):
        plot_point(ax, v, color='red', size=150, label=str(i+1))
    
    text = f"""Zlatý řez: φ = {phi:.3f}

Obdélník v rovině YZ:
Kratší: 2
Delší: 2φ ≈ {2*phi:.3f}

Poměr: φ

Vrcholy:
(0, ±1, ±φ)"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=11,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_7(ax):
    """Dvacetistěn - Krok 2: Tři obdélníky"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVACETISTĚN - Krok 2: Tři kolmé obdélníky', fontsize=14, fontweight='bold')
    
    colors_rect = ['red']*4 + ['green']*4 + ['blue']*4
    
    rectangles = [
        [(0,1,3,2)],
        [(4,5,7,6)],
        [(8,9,11,10)]
    ]
    rect_colors = ['red', 'green', 'blue']
    
    for rect_faces, color in zip(rectangles, rect_colors):
        for face in rect_faces:
            for i in range(4):
                v1 = icosa_vertices[face[i]]
                v2 = icosa_vertices[face[(i+1)%4]]
                plot_edge(ax, v1, v2, color=color, width=2)
    
    for v, color in zip(icosa_vertices, colors_rect):
        plot_point(ax, v, color=color, size=100)
    
    text = f"""Tři obdélníky:
φ = {phi:.3f}

Červený (YZ): (0, ±1, ±φ)
Zelený (XZ): (±1, ±φ, 0)
Modrý (XY): (±φ, 0, ±1)

Celkem: 12 vrcholů"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=10,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_8(ax):
    """Dvacetistěn - Krok 3: Hotovo"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVACETISTĚN - Krok 3: Hotový dvacetistěn', fontsize=14, fontweight='bold')
    
    icosa_faces = np.array([
        [0, 8, 4], [0, 4, 6], [0, 6, 10], [0, 10, 2], [0, 2, 8],
        [8, 2, 5], [2, 10, 7], [10, 6, 11], [6, 4, 1], [4, 8, 9],
        [5, 2, 7], [7, 10, 11], [11, 6, 1], [1, 4, 9], [9, 8, 5],
        [3, 5, 7], [3, 7, 11], [3, 11, 1], [3, 1, 9], [3, 9, 5]
    ])
    
    edges_set = set()
    for face in icosa_faces:
        for i in range(3):
            edge = tuple(sorted([face[i], face[(i+1)%3]]))
            edges_set.add(edge)
    
    for edge in edges_set:
        plot_edge(ax, icosa_vertices[edge[0]], icosa_vertices[edge[1]], 
                  color='blue', width=2)
    
    for i, v in enumerate(icosa_vertices):
        plot_point(ax, v, color='red', size=120, label=chr(65+i))
    
    text = f"""Dvacetistěn:
- 12 vrcholů
- 30 hran
- 20 trojúhelníků

Délka hrany = 2
(díky zlatému řezu!)"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=11,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_9(ax):
    """Dvanáctistěn - Krok 1: Krychle"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVANÁCTISTĚN - Krok 1: Krychle (8 vrcholů)', fontsize=14, fontweight='bold')
    
    for edge in cube_edges:
        plot_edge(ax, cube_vertices[edge[0]], cube_vertices[edge[1]], 
                  color='blue', width=2)
    
    for i, v in enumerate(cube_vertices):
        plot_point(ax, v, color='blue', size=120, label=str(i+1))
    
    text = """Krychle: 8 vrcholů
(±1, ±1, ±1)

Dvanáctistěn má 20 vrcholů,
takže potřebujeme přidat
ještě 12!"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=11,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_10(ax):
    """Dvanáctistěn - Krok 2: Přidání vrcholů - VYLEPŠENÉ VYSVĚTLENÍ"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVANÁCTISTĚN - Krok 2: Jak získat dalších 12 vrcholů?', 
                 fontsize=14, fontweight='bold')
    
    # Nakresli krychli světle
    for edge in cube_edges:
        plot_edge(ax, cube_vertices[edge[0]], cube_vertices[edge[1]], 
                  color='lightblue', width=1, style='--')
    
    for v in cube_vertices:
        plot_point(ax, v, color='lightblue', size=80)
    
    # Zvýrazni JEDEN obdélník jako příklad
    example_rect = np.array([
        [0,  1/phi,  phi],
        [0,  1/phi, -phi],
        [0, -1/phi,  phi],
        [0, -1/phi, -phi]
    ])
    
    # Nakresli rovinu YZ
    y_plane = [-2, 2, 2, -2, -2]
    z_plane = [-2, -2, 2, 2, -2]
    x_plane = [0, 0, 0, 0, 0]
    ax.plot(x_plane, y_plane, z_plane, 'orange', alpha=0.2, linewidth=2, 
            linestyle='--')
    
    # Nakresli obdélník ČERVENĚ
    rect_edges_example = [(0,1), (1,3), (3,2), (2,0)]
    for edge in rect_edges_example:
        plot_edge(ax, example_rect[edge[0]], example_rect[edge[1]], 
                  color='red', width=4)
    
    # Zvýrazni vrcholy obdélníku
    for i, v in enumerate(example_rect):
        plot_point(ax, v, color='red', size=180, label=f'{i+8}')
    
    # Nakresli MĚŘENÍ obdélníku
    mid_short = (example_rect[0] + example_rect[2]) / 2
    ax.text(mid_short[0]-0.3, mid_short[1], mid_short[2], 
            f'2/φ\n≈{2/phi:.2f}', fontsize=10, color='red', 
            fontweight='bold', ha='right')
    
    mid_long = (example_rect[0] + example_rect[1]) / 2
    ax.text(mid_long[0], mid_long[1]+0.2, mid_long[2]+0.3, 
            f'2φ\n≈{2*phi:.2f}', fontsize=10, color='red', 
            fontweight='bold', ha='center')
    
    text = f"""PRINCIP: Obdélníky se zlatým řezem!

Zlatý řez: φ = {phi:.3f}, 1/φ = {1/phi:.3f}

PŘÍKLAD (červený obdélník v rovině YZ):
- Rovina: x = 0 (kolmá na osu X)
- Kratší strana: od -1/φ do +1/φ → délka 2/φ
- Delší strana: od -φ do +φ → délka 2φ
- Poměr: 2φ / (2/φ) = φ² = φ ✓

4 vrcholy: (0, ±1/φ, ±φ)

CELKEM 3 takové obdélníky:
1) Rovina YZ (x=0): (0, ±1/φ, ±φ)    → 4 vrcholy
2) Rovina XZ (y=0): (±1/φ, ±φ, 0)    → 4 vrcholy  
3) Rovina XY (z=0): (±φ, 0, ±1/φ)    → 4 vrcholy

CELKEM: 4 + 4 + 4 = 12 nových vrcholů!
Spolu s krychlí: 8 + 12 = 20 vrcholů"""
    
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=9,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.9), family='monospace')

def draw_step_11(ax):
    """Dvanáctistěn - Krok 2b: Všechny tři obdélníky"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVANÁCTISTĚN - Krok 2b: Tři kolmé obdélníky', 
                 fontsize=14, fontweight='bold')
    
    # Nakresli krychli velmi světle
    for edge in cube_edges:
        plot_edge(ax, cube_vertices[edge[0]], cube_vertices[edge[1]], 
                  color='lightgray', width=0.5, style=':')
    
    for v in cube_vertices:
        plot_point(ax, v, color='lightgray', size=40)
    
    # TŘI OBDÉLNÍKY
    rect1_YZ = np.array([
        [0,  1/phi,  phi], [0,  1/phi, -phi],
        [0, -1/phi,  phi], [0, -1/phi, -phi]
    ])
    
    rect2_XZ = np.array([
        [ 1/phi,  phi, 0], [ 1/phi, -phi, 0],
        [-1/phi,  phi, 0], [-1/phi, -phi, 0]
    ])
    
    rect3_XY = np.array([
        [ phi, 0,  1/phi], [ phi, 0, -1/phi],
        [-phi, 0,  1/phi], [-phi, 0, -1/phi]
    ])
    
    # Nakresli obdélníky
    rect_edges_pattern = [(0,1), (1,3), (3,2), (2,0)]
    
    # Červený obdélník (YZ)
    for edge in rect_edges_pattern:
        plot_edge(ax, rect1_YZ[edge[0]], rect1_YZ[edge[1]], 
                  color='red', width=3)
    for i, v in enumerate(rect1_YZ):
        plot_point(ax, v, color='red', size=120)
    
    # Zelený obdélník (XZ)
    for edge in rect_edges_pattern:
        plot_edge(ax, rect2_XZ[edge[0]], rect2_XZ[edge[1]], 
                  color='green', width=3)
    for i, v in enumerate(rect2_XZ):
        plot_point(ax, v, color='green', size=120)
    
    # Modrý obdélník (XY)
    for edge in rect_edges_pattern:
        plot_edge(ax, rect3_XY[edge[0]], rect3_XY[edge[1]], 
                  color='blue', width=3)
    for i, v in enumerate(rect3_XY):
        plot_point(ax, v, color='blue', size=120)
    
    text = f"""Tři obdélníky kolmé na sebe:
φ = {phi:.3f}, 1/φ = {1/phi:.3f}

🔴 ČERVENÝ (rovina YZ, x=0):
   (0, ±1/φ, ±φ) → 4 vrcholy
   
🟢 ZELENÝ (rovina XZ, y=0):
   (±1/φ, ±φ, 0) → 4 vrcholy
   
🔵 MODRÝ (rovina XY, z=0):
   (±φ, 0, ±1/φ) → 4 vrcholy

Každý obdélník má:
- Kratší stranu: 2/φ ≈ {2/phi:.2f}
- Delší stranu: 2φ ≈ {2*phi:.2f}  
- Poměr stran: φ (zlatý řez!)

CELKEM: 4+4+4 = 12 vrcholů"""
    
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=9,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='lightyellow', alpha=0.9), family='monospace')



def draw_step_12(ax):
    """Dvanáctistěn - Krok 3: Hotovo"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('DVANÁCTISTĚN - Krok 3: Hotový dvanáctistěn', fontsize=14, fontweight='bold')
    
    sample_edges = []
    for i in range(len(dodeca_vertices)):
        for j in range(i+1, len(dodeca_vertices)):
            dist = np.linalg.norm(dodeca_vertices[i] - dodeca_vertices[j])
            if 1.1 < dist < 1.3:
                sample_edges.append((i, j))
    
    for edge in sample_edges[:30]:
        plot_edge(ax, dodeca_vertices[edge[0]], dodeca_vertices[edge[1]], 
                  color='green', width=2)
    
    for i, v in enumerate(dodeca_vertices):
        if i < 8:
            plot_point(ax, v, color='blue', size=100)
        else:
            plot_point(ax, v, color='red', size=100)
    
    text = f"""Dvanáctistěn:
- 20 vrcholů
- 30 hran
- 12 pětiúhelníků

Délka hrany:
d = 2/φ ≈ {2/phi:.3f}"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=11,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

def draw_step_13(ax):
    """Bonus: Střed trojúhelníku"""
    ax.clear()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title('BONUS: Střed trojúhelníku (těžiště)', fontsize=14, fontweight='bold')
    
    A = icosa_vertices[0]
    B = icosa_vertices[8]
    C = icosa_vertices[4]
    center = (A + B + C) / 3
    
    plot_edge(ax, A, B, color='blue', width=3)
    plot_edge(ax, B, C, color='blue', width=3)
    plot_edge(ax, C, A, color='blue', width=3)
    
    plot_point(ax, A, color='red', size=150, label='A')
    plot_point(ax, B, color='red', size=150, label='B')
    plot_point(ax, C, color='red', size=150, label='C')
    plot_point(ax, center, color='green', size=200, label='T')
    
    plot_edge(ax, A, center, color='green', width=2, style='--')
    plot_edge(ax, B, center, color='green', width=2, style='--')
    plot_edge(ax, C, center, color='green', width=2, style='--')
    
    text = f"""Střed trojúhelníku:
T = (A + B + C) / 3

A = ({A[0]:.1f}, {A[1]:.1f}, {A[2]:.1f})
B = ({B[0]:.1f}, {B[1]:.1f}, {B[2]:.1f})
C = ({C[0]:.1f}, {C[1]:.1f}, {C[2]:.1f})

T = ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})"""
    ax.text2D(0.02, 0.98, text, transform=ax.transAxes, fontsize=10,
              verticalalignment='top', bbox=dict(boxstyle='round', 
              facecolor='wheat', alpha=0.8), family='monospace')

# =============================================================================
# HLAVNÍ TŘÍDA PRO NAVIGACI
# =============================================================================

class StepNavigator:
    def __init__(self):
        self.current_step = 0
        self.total_steps = 14
        
        self.steps = [
            draw_step_0,   # 0: Úvod
            draw_step_1,   # 1: Čtyřstěn - krychle
            draw_step_2,   # 2: Čtyřstěn - výběr
            draw_step_3,   # 3: Čtyřstěn - hotovo
            draw_step_4,   # 4: Osmistěn - osy
            draw_step_5,   # 5: Osmistěn - hotovo
            draw_step_6,   # 6: Dvacetistěn - obdélník
            draw_step_7,   # 7: Dvacetistěn - 3 obdélníky
            draw_step_8,   # 8: Dvacetistěn - hotovo
            draw_step_9,   # 9: Dvanáctistěn - krychle
            draw_step_10,  # 10: Dvanáctistěn - +12
            draw_step_11,  # 11: Dvanáctistěn - vylepsene vysvetleni
            draw_step_12,  # 12: Dvanáctistěn - hotovo
            draw_step_13   # 13: Bonus - střed
        ]
        
        # Vytvoř figure a osu
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Přidej tlačítka
        ax_prev = plt.axes([0.3, 0.02, 0.15, 0.05])
        ax_next = plt.axes([0.55, 0.02, 0.15, 0.05])
        
        self.btn_prev = Button(ax_prev, 'Předchozí')
        self.btn_next = Button(ax_next, 'Další')
        
        self.btn_prev.on_clicked(self.prev_step)
        self.btn_next.on_clicked(self.next_step)
        
        # Přidej informaci o kroku
        self.step_text = self.fig.text(0.5, 0.95, '', ha='center', 
                                       fontsize=12, fontweight='bold')
        
        # Nakresli první krok
        self.update()
        
    def next_step(self, event):
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update()
    
    def prev_step(self, event):
        if self.current_step > 0:
            self.current_step -= 1
            self.update()
    
    def update(self):
        # Nakresli aktuální krok
        self.steps[self.current_step](self.ax)
        
        # Aktualizuj text s číslem kroku
        self.step_text.set_text(f'Krok {self.current_step} / {self.total_steps - 1}')
        
        # Překresli
        self.fig.canvas.draw()

# =============================================================================
# SPUŠTĚNÍ
# =============================================================================

print("="*70)
print("INTERAKTIVNÍ KONSTRUKCE PLATÓNSKÝCH TĚLES")
print("="*70)
print("\nPoužij tlačítka 'Další' a 'Předchozí' pro navigaci mezi kroky.")
print("Celkem je 13 kroků (0-12).")
print("\nZavři okno pro ukončení.")
print("\n" + "="*70)
print("KONTROLA VRCHOLŮ ČTYŘSTĚNU:")
print("="*70)
print(f"Vybrané vrcholy: {tetra_indices}")
print("Souřadnice:")
for i, idx in enumerate(tetra_indices):
    v = cube_vertices[idx]
    product = v[0] * v[1] * v[2]
    print(f"  Vrchol {idx}: {v} → součin = {product:.0f}")

# Kontrola, že žádné dva nejsou sousedé
print("\nKontrola hran (žádné dva vybrané vrcholy nesmí sdílet hranu):")
for i, idx1 in enumerate(tetra_indices):
    for idx2 in tetra_indices[i+1:]:
        if (idx1, idx2) in cube_edges or (idx2, idx1) in cube_edges:
            print(f"  CHYBA: Vrcholy {idx1} a {idx2} sdílejí hranu!")
        else:
            print(f"  OK: Vrcholy {idx1} a {idx2} nesdílejí hranu ✓")

navigator = StepNavigator()
plt.show()