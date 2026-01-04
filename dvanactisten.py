import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# ========== DVACETISTĚN (ICOSAHEDRON) ==========
phi = (1 + np.sqrt(5)) / 2  # zlatý řez ≈ 1.618

# Vrcholy: 3 obdélníky se zlatým řezem, kolmé na sebe
vertices_icosahedron = np.array([
    # Obdélník v rovině YZ
    [ 0,  1,  phi],  # 0
    [ 0,  1, -phi],  # 1
    [ 0, -1,  phi],  # 2
    [ 0, -1, -phi],  # 3
    
    # Obdélník v rovině XZ
    [ 1,  phi,  0],  # 4
    [ 1, -phi,  0],  # 5
    [-1,  phi,  0],  # 6
    [-1, -phi,  0],  # 7
    
    # Obdélník v rovině XY
    [ phi,  0,  1],  # 8
    [ phi,  0, -1],  # 9
    [-phi,  0,  1],  # 10
    [-phi,  0, -1]   # 11
])

# SPRÁVNÉ STĚNY dvacetistěnu (20 rovnostranných trojúhelníků)
# Každý vrchol má kolem sebe 5 trojúhelníků
faces_icosahedron = np.array([
    # Horní čepice (5 trojúhelníků kolem vrcholu 0)
    [0, 8, 4],
    [0, 4, 6],
    [0, 6, 10],
    [0, 10, 2],
    [0, 2, 8],
    
    # Horní pás (5 trojúhelníků)
    [8, 2, 5],
    [2, 10, 7],
    [10, 6, 11],
    [6, 4, 1],
    [4, 8, 9],
    
    # Spodní pás (5 trojúhelníků)
    [5, 2, 7],
    [7, 10, 11],
    [11, 6, 1],
    [1, 4, 9],
    [9, 8, 5],
    
    # Spodní čepice (5 trojúhelníků kolem vrcholu 3)
    [3, 5, 7],
    [3, 7, 11],
    [3, 11, 1],
    [3, 1, 9],
    [3, 9, 5]
])

print(f"Počet vrcholů: {len(vertices_icosahedron)}")
print(f"Počet stěn: {len(faces_icosahedron)}")

# Spočítej hrany
edges_icosahedron = set()
for face in faces_icosahedron:
    for i in range(3):
        edge = tuple(sorted([face[i], face[(i+1) % 3]]))
        edges_icosahedron.add(edge)

edges_icosahedron = list(edges_icosahedron)
print(f"Počet hran: {len(edges_icosahedron)}")

# Kontrola Eulerovy formule
V = len(vertices_icosahedron)
E = len(edges_icosahedron)
F = len(faces_icosahedron)
print(f"\nEulerova formule: V - E + F = {V} - {E} + {F} = {V - E + F}")

# Kontrola délek hran - všechny by měly být stejné
print("\n=== KONTROLA DÉLEK HRAN ===")
edge_lengths = []
for edge in edges_icosahedron[:5]:  # zkontroluj prvních 5 hran
    i, j = edge
    length = np.linalg.norm(vertices_icosahedron[i] - vertices_icosahedron[j])
    edge_lengths.append(length)
    print(f"Hrana {i}-{j}: délka = {length:.6f}")

print(f"Průměrná délka hrany: {np.mean(edge_lengths):.6f}")
print(f"Rozdíl min-max: {np.max(edge_lengths) - np.min(edge_lengths):.10f}")

# ========== VYKRESLENÍ ==========

# 1. Stěny - průhledné modré
ax.plot_trisurf(
    vertices_icosahedron[:, 0],
    vertices_icosahedron[:, 1],
    vertices_icosahedron[:, 2],
    triangles=faces_icosahedron,
    alpha=0.3,
    color='cyan',
    edgecolor='none',
    linewidth=0
)

# 2. Hrany - modré
for edge in edges_icosahedron:
    i, j = edge
    ax.plot(
        [vertices_icosahedron[i, 0], vertices_icosahedron[j, 0]],
        [vertices_icosahedron[i, 1], vertices_icosahedron[j, 1]],
        [vertices_icosahedron[i, 2], vertices_icosahedron[j, 2]],
        'b-', linewidth=2.5, alpha=0.8
    )

# 3. Vrcholy s popisky
ax.scatter(vertices_icosahedron[:, 0],
           vertices_icosahedron[:, 1],
           vertices_icosahedron[:, 2],
           c='red', s=200, alpha=0.95, edgecolors='darkred', linewidth=2, zorder=10)

for i, vertex in enumerate(vertices_icosahedron):
    ax.text(vertex[0], vertex[1], vertex[2], f' {i}', 
            fontsize=12, fontweight='bold', color='darkred')

# Nastavení
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)
ax.set_box_aspect([1, 1, 1])
ax.set_title('Dvacetistěn - 20 rovnostranných trojúhelníků', fontsize=16, fontweight='bold')
ax.view_init(elev=20, azim=45)

max_range = 2
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])
ax.set_zlim([-max_range, max_range])

plt.tight_layout()
plt.show()

# Výpis struktury
print("\n=== STRUKTURA DVACETISTĚNU ===")
print("Vrcholy jsou uspořádány ve 3 obdélnících se zlatým řezem:")
print("  Obdélník YZ: vrcholy 0, 1, 2, 3")
print("  Obdélník XZ: vrcholy 4, 5, 6, 7")
print("  Obdélník XY: vrcholy 8, 9, 10, 11")
print("\nKaždý vrchol má přesně 5 sousedů (stupeň = 5)")
print("Každá stěna je rovnostranný trojúhelník")
print("Těleso je konvexní")