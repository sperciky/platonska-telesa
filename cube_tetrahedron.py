import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# ========== STŘEDNÍ KRYCHLE (začneme s ní) ==========
# Krychle se středem v [0,0,0] a hranou délky 2
vertices_middle_cube = np.array([
    [-1, -1, -1],  # K
    [ 1, -1, -1],  # L
    [ 1,  1, -1],  # M
    [-1,  1, -1],  # N
    [-1, -1,  1],  # O
    [ 1, -1,  1],  # P
    [ 1,  1,  1],  # Q
    [-1,  1,  1]   # R
])

labels_middle_cube = ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

edges_middle_cube = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # spodní čtverec
    (4, 5), (5, 6), (6, 7), (7, 4),  # horní čtverec
    (0, 4), (1, 5), (2, 6), (3, 7)   # svislé hrany
]

# Stěny střední krychle (každá stěna jako 4 vrcholy)
faces_middle_cube_quads = [
    [0, 1, 2, 3],  # spodní stěna (z=-1): K,L,M,N
    [4, 5, 6, 7],  # horní stěna (z=1): O,P,Q,R
    [0, 1, 5, 4],  # přední stěna (y=-1): K,L,P,O
    [2, 3, 7, 6],  # zadní stěna (y=1): M,N,R,Q
    [0, 3, 7, 4],  # levá stěna (x=-1): K,N,R,O
    [1, 2, 6, 5]   # pravá stěna (x=1): L,M,Q,P
]

# ========== VNITŘNÍ OSMISTĚN ==========
# Vrcholy osmistěnu = středy stěn krychle

def quad_center(v1, v2, v3, v4):
    """Vypočítá střed čtyřúhelníku"""
    return (v1 + v2 + v3 + v4) / 4

vertices_inner_octahedron = []

print("Vrcholy vnitřního osmistěnu (středy stěn krychle):")
for i, face in enumerate(faces_middle_cube_quads):
    centers = [vertices_middle_cube[idx] for idx in face]
    center = quad_center(centers[0], centers[1], centers[2], centers[3])
    vertices_inner_octahedron.append(center)
    print(f"Stěna {i} {face}: střed = {center}")

vertices_inner_octahedron = np.array(vertices_inner_octahedron)

labels_inner_octahedron = ['1', '2', '3', '4', '5', '6']

# Stěny vnitřního osmistěnu
# Index vrcholů: 0=spodní, 1=horní, 2=přední, 3=zadní, 4=levá, 5=pravá
faces_inner_octahedron = [
    (0, 2, 5),  # spodní-přední-pravá
    (0, 5, 3),  # spodní-pravá-zadní
    (0, 3, 4),  # spodní-zadní-levá
    (0, 4, 2),  # spodní-levá-přední
    (1, 5, 2),  # horní-pravá-přední
    (1, 3, 5),  # horní-zadní-pravá
    (1, 4, 3),  # horní-levá-zadní
    (1, 2, 4)   # horní-přední-levá
]

# ========== VNĚJŠÍ OSMISTĚN ==========
# Vrcholy vnějšího osmistěnu = středy stěn vnitřního osmistěnu

def triangle_center(v1, v2, v3):
    """Vypočítá těžiště trojúhelníku"""
    return (v1 + v2 + v3) / 3

vertices_outer_octahedron = []

print("\nVrcholy vnějšího osmistěnu (středy stěn vnitřního osmistěnu):")
for i, face in enumerate(faces_inner_octahedron):
    a, b, c = face
    center = triangle_center(
        vertices_inner_octahedron[a],
        vertices_inner_octahedron[b],
        vertices_inner_octahedron[c]
    )
    vertices_outer_octahedron.append(center)
    print(f"Stěna {i} {face}: střed = {center}")

vertices_outer_octahedron = np.array(vertices_outer_octahedron)

# Najdi hrany vnějšího osmistěnu
def find_octahedron_edges_from_faces(faces):
    """Najde hrany osmistěnu z jeho stěn"""
    edges = []
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            # Dvě stěny sdílejí hranu, pokud mají 2 společné vrcholy
            shared = len(set(faces[i]) & set(faces[j]))
            if shared == 2:
                edges.append((i, j))
    return edges

edges_outer_octahedron = find_octahedron_edges_from_faces(faces_inner_octahedron)

# ========== VYKRESLENÍ ==========

# 1. Střední krychle - zelené hrany
for edge in edges_middle_cube:
    i, j = edge
    ax.plot(
        [vertices_middle_cube[i, 0], vertices_middle_cube[j, 0]],
        [vertices_middle_cube[i, 1], vertices_middle_cube[j, 1]],
        [vertices_middle_cube[i, 2], vertices_middle_cube[j, 2]],
        'g-', linewidth=3
    )

# 2. Vnitřní osmistěn - modrý průhledný
ax.plot_trisurf(
    vertices_inner_octahedron[:, 0],
    vertices_inner_octahedron[:, 1],
    vertices_inner_octahedron[:, 2],
    triangles=faces_inner_octahedron,
    alpha=0.3,
    color='cyan',
    edgecolor='blue',
    linewidth=2
)

# 3. Vnější osmistěn - žlutý průhledný
for edge in edges_outer_octahedron:
    i, j = edge
    ax.plot(
        [vertices_outer_octahedron[i, 0], vertices_outer_octahedron[j, 0]],
        [vertices_outer_octahedron[i, 1], vertices_outer_octahedron[j, 1]],
        [vertices_outer_octahedron[i, 2], vertices_outer_octahedron[j, 2]],
        'orange', linewidth=2.5, alpha=0.6
    )

# ========== VRCHOLY S POPISKY ==========

# Vrcholy střední krychle - zelené s popisky K-R
ax.scatter(vertices_middle_cube[:, 0],
           vertices_middle_cube[:, 1],
           vertices_middle_cube[:, 2],
           c='lime', s=200, alpha=0.9, edgecolors='darkgreen', linewidth=2, zorder=5)

for vertex, label in zip(vertices_middle_cube, labels_middle_cube):
    ax.text(vertex[0], vertex[1], vertex[2], f'  {label}', 
            fontsize=14, fontweight='bold', color='darkgreen')

# Vrcholy vnitřního osmistěnu - červené s popisky 1-6
ax.scatter(vertices_inner_octahedron[:, 0],
           vertices_inner_octahedron[:, 1],
           vertices_inner_octahedron[:, 2],
           c='red', s=200, alpha=0.9, edgecolors='darkred', linewidth=2, zorder=6)

for vertex, label in zip(vertices_inner_octahedron, labels_inner_octahedron):
    ax.text(vertex[0], vertex[1], vertex[2], f'  {label}', 
            fontsize=14, fontweight='bold', color='red')

# Vrcholy vnějšího osmistěnu - oranžové
ax.scatter(vertices_outer_octahedron[:, 0],
           vertices_outer_octahedron[:, 1],
           vertices_outer_octahedron[:, 2],
           c='orange', s=150, alpha=0.8, edgecolors='darkorange', linewidth=2, zorder=4)

# Nastavení
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])
ax.set_title('Opačná dualita: Krychle (K-R) → Osmistěn (1-6) → Osmistěn', fontsize=16)
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()

# Kontrola výpis
print("\n=== KONTROLA ===")
print("\nStředy stěn krychle (vrcholy vnitřního osmistěnu):")
print("1 (spodní stěna):", vertices_inner_octahedron[0], "→ očekáváno: [0, 0, -1]")
print("2 (horní stěna):", vertices_inner_octahedron[1], "→ očekáváno: [0, 0, 1]")
print("3 (přední stěna):", vertices_inner_octahedron[2], "→ očekáváno: [0, -1, 0]")
print("4 (zadní stěna):", vertices_inner_octahedron[3], "→ očekáváno: [0, 1, 0]")
print("5 (levá stěna):", vertices_inner_octahedron[4], "→ očekáváno: [-1, 0, 0]")
print("6 (pravá stěna):", vertices_inner_octahedron[5], "→ očekáváno: [1, 0, 0]")