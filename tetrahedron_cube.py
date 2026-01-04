import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# ========== VNĚJŠÍ OSMISTĚN (největší) ==========
scale = 2
vertices_outer_octahedron = np.array([
    [ scale,  0,  0],  # 1: +X
    [-scale,  0,  0],  # 2: -X
    [ 0,  scale,  0],  # 3: +Y
    [ 0, -scale,  0],  # 4: -Y
    [ 0,  0,  scale],  # 5: +Z
    [ 0,  0, -scale]   # 6: -Z
])

labels_outer_octahedron = ['1', '2', '3', '4', '5', '6']

# Stěny vnějšího osmistěnu
faces_outer_octahedron = [
    (0, 2, 4),  # stěna 0: +X, +Y, +Z
    (0, 4, 3),  # stěna 1: +X, +Z, -Y
    (0, 3, 5),  # stěna 2: +X, -Y, -Z
    (0, 5, 2),  # stěna 3: +X, -Z, +Y
    (1, 4, 2),  # stěna 4: -X, +Z, +Y
    (1, 3, 4),  # stěna 5: -X, -Y, +Z
    (1, 5, 3),  # stěna 6: -X, -Z, -Y
    (1, 2, 5)   # stěna 7: -X, +Y, -Z
]

# ========== VEPSANÁ KRYCHLE ==========
def triangle_center(v1, v2, v3):
    """Vypočítá těžiště trojúhelníku"""
    return (v1 + v2 + v3) / 3

vertices_middle_cube = []

print("Vrcholy vepsané krychle (středy stěn vnějšího osmistěnu):")
for i, face in enumerate(faces_outer_octahedron):
    a, b, c = face
    center = triangle_center(
        vertices_outer_octahedron[a],
        vertices_outer_octahedron[b],
        vertices_outer_octahedron[c]
    )
    vertices_middle_cube.append(center)
    print(f"Stěna {i} {face}: střed = {center}")

vertices_middle_cube = np.array(vertices_middle_cube)

labels_middle_cube = ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

# Najdi hrany vepsané krychle
def find_cube_edges(faces):
    """Najde hrany krychle na základě sousedních stěn"""
    edges = []
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            shared = len(set(faces[i]) & set(faces[j]))
            if shared == 2:
                edges.append((i, j))
    return edges

edges_middle_cube = find_cube_edges(faces_outer_octahedron)

# ========== VNITŘNÍ OSMISTĚN ==========
def find_cube_faces_from_octahedron_faces(oct_faces):
    """Najde stěny krychle"""
    vertex_to_faces = {}
    for face_idx, face in enumerate(oct_faces):
        for vertex in face:
            if vertex not in vertex_to_faces:
                vertex_to_faces[vertex] = []
            vertex_to_faces[vertex].append(face_idx)
    
    cube_faces = []
    for vertex, face_indices in vertex_to_faces.items():
        if len(face_indices) == 4:
            cube_faces.append(face_indices)
    
    return cube_faces

faces_middle_cube = find_cube_faces_from_octahedron_faces(faces_outer_octahedron)

def quad_center(v1, v2, v3, v4):
    """Vypočítá střed čtyřúhelníku"""
    return (v1 + v2 + v3 + v4) / 4

vertices_inner_octahedron = []

print("\nVrcholy vnitřního osmistěnu (středy stěn krychle):")
for i, face in enumerate(faces_middle_cube):
    centers = [vertices_middle_cube[idx] for idx in face]
    center = quad_center(centers[0], centers[1], centers[2], centers[3])
    vertices_inner_octahedron.append(center)
    print(f"Stěna {i} {face}: střed = {center}")

vertices_inner_octahedron = np.array(vertices_inner_octahedron)

labels_inner_octahedron = ['7', '8', '9', '10', '11', '12']

# OPRAVA: Správné hrany vnitřního osmistěnu
# Osmistěn má 12 hran - každý vrchol je spojený s 4 dalšími
# Najdeme je ze stěn krychle - dvě stěny krychle sdílejí hranu
edges_inner_octahedron = []

for i in range(len(faces_middle_cube)):
    for j in range(i + 1, len(faces_middle_cube)):
        # Zjisti, kolik vrcholů krychle sdílejí dvě stěny
        shared = len(set(faces_middle_cube[i]) & set(faces_middle_cube[j]))
        if shared == 2:  # Sdílejí hranu krychle
            edges_inner_octahedron.append((i, j))

print(f"\nPočet hran vnitřního osmistěnu: {len(edges_inner_octahedron)}")
print("Hrany vnitřního osmistěnu:", edges_inner_octahedron)

# Alternativně: Stěny vnitřního osmistěnu (pro vykreslení pomocí plot_trisurf)
# Musíme určit, které 3 vrcholy tvoří trojúhelníkové stěny
# Osmistěn má stejnou strukturu jako vnější, jen je zmenšený a otočený

# ========== VYKRESLENÍ ==========

# 1. Vnější osmistěn - žlutý průhledný
ax.plot_trisurf(
    vertices_outer_octahedron[:, 0],
    vertices_outer_octahedron[:, 1],
    vertices_outer_octahedron[:, 2],
    triangles=faces_outer_octahedron,
    alpha=0.2,
    color='yellow',
    edgecolor='orange',
    linewidth=2
)

# 2. Vepsaná krychle - zelené hrany
for edge in edges_middle_cube:
    i, j = edge
    ax.plot(
        [vertices_middle_cube[i, 0], vertices_middle_cube[j, 0]],
        [vertices_middle_cube[i, 1], vertices_middle_cube[j, 1]],
        [vertices_middle_cube[i, 2], vertices_middle_cube[j, 2]],
        'g-', linewidth=3
    )

# 3. Vnitřní osmistěn - OPRAVENÉ HRANY - pouze hrany, ne plochy
for edge in edges_inner_octahedron:
    i, j = edge
    ax.plot(
        [vertices_inner_octahedron[i, 0], vertices_inner_octahedron[j, 0]],
        [vertices_inner_octahedron[i, 1], vertices_inner_octahedron[j, 1]],
        [vertices_inner_octahedron[i, 2], vertices_inner_octahedron[j, 2]],
        'b-', linewidth=2.5, color='blue'
    )

# ========== VRCHOLY S POPISKY ==========

# Vrcholy vnějšího osmistěnu - oranžové s popisky 1-6
ax.scatter(vertices_outer_octahedron[:, 0],
           vertices_outer_octahedron[:, 1],
           vertices_outer_octahedron[:, 2],
           c='orange', s=200, alpha=0.9, edgecolors='darkorange', linewidth=2, zorder=5)

for vertex, label in zip(vertices_outer_octahedron, labels_outer_octahedron):
    ax.text(vertex[0], vertex[1], vertex[2], f'  {label}', 
            fontsize=14, fontweight='bold', color='darkorange')

# Vrcholy vepsané krychle - zelené s popisky K-R
ax.scatter(vertices_middle_cube[:, 0],
           vertices_middle_cube[:, 1],
           vertices_middle_cube[:, 2],
           c='lime', s=200, alpha=0.9, edgecolors='darkgreen', linewidth=2, zorder=6)

for vertex, label in zip(vertices_middle_cube, labels_middle_cube):
    ax.text(vertex[0], vertex[1], vertex[2], f'  {label}', 
            fontsize=12, fontweight='bold', color='darkgreen')

# Vrcholy vnitřního osmistěnu - červené s popisky 7-12
ax.scatter(vertices_inner_octahedron[:, 0],
           vertices_inner_octahedron[:, 1],
           vertices_inner_octahedron[:, 2],
           c='red', s=200, alpha=0.9, edgecolors='darkred', linewidth=2, zorder=7)

for vertex, label in zip(vertices_inner_octahedron, labels_inner_octahedron):
    ax.text(vertex[0], vertex[1], vertex[2], f'  {label}', 
            fontsize=12, fontweight='bold', color='red')

# Nastavení
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])
ax.set_title('Dualita: Osmistěn (1-6) → Krychle (K-R) → Osmistěn (7-12)', fontsize=16)
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()