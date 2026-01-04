import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 14))
ax = fig.add_subplot(111, projection='3d')

# ========== VNĚJŠÍ DVACETISTĚN ==========
phi = (1 + np.sqrt(5)) / 2  # zlatý řez

vertices_icosahedron = np.array([
    # Obdélník v rovině YZ
    [ 0,  1,  phi],  # 0 = A
    [ 0,  1, -phi],  # 1 = B
    [ 0, -1,  phi],  # 2 = C
    [ 0, -1, -phi],  # 3 = D
    
    # Obdélník v rovině XZ
    [ 1,  phi,  0],  # 4 = E
    [ 1, -phi,  0],  # 5 = F
    [-1,  phi,  0],  # 6 = G
    [-1, -phi,  0],  # 7 = H
    
    # Obdélník v rovině XY
    [ phi,  0,  1],  # 8 = I
    [ phi,  0, -1],  # 9 = J
    [-phi,  0,  1],  # 10 = K
    [-phi,  0, -1]   # 11 = L
])

# Popisky A-L pro vrcholy dvacetistěnu
labels_icosahedron = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

# Stěny dvacetistěnu (20 trojúhelníků)
faces_icosahedron = np.array([
    # Horní čepice
    [0, 8, 4],
    [0, 4, 6],
    [0, 6, 10],
    [0, 10, 2],
    [0, 2, 8],
    
    # Horní pás
    [8, 2, 5],
    [2, 10, 7],
    [10, 6, 11],
    [6, 4, 1],
    [4, 8, 9],
    
    # Spodní pás
    [5, 2, 7],
    [7, 10, 11],
    [11, 6, 1],
    [1, 4, 9],
    [9, 8, 5],
    
    # Spodní čepice
    [3, 5, 7],
    [3, 7, 11],
    [3, 11, 1],
    [3, 1, 9],
    [3, 9, 5]
])

# Hrany dvacetistěnu
edges_icosahedron = set()
for face in faces_icosahedron:
    for i in range(3):
        edge = tuple(sorted([face[i], face[(i+1) % 3]]))
        edges_icosahedron.add(edge)
edges_icosahedron = list(edges_icosahedron)

print("="*60)
print("VNĚJŠÍ DVACETISTĚN")
print("="*60)
print(f"Počet vrcholů: {len(vertices_icosahedron)}")
print(f"Počet stěn: {len(faces_icosahedron)}")
print(f"Počet hran: {len(edges_icosahedron)}")

# ========== VEPSANÝ DVANÁCTISTĚN ==========

def triangle_center(v1, v2, v3):
    """Střed trojúhelníku"""
    return (v1 + v2 + v3) / 3

vertices_dodecahedron = []

print("\n" + "="*60)
print("VEPSANÝ DVANÁCTISTĚN")
print("="*60)

for i, face in enumerate(faces_icosahedron):
    v1 = vertices_icosahedron[face[0]]
    v2 = vertices_icosahedron[face[1]]
    v3 = vertices_icosahedron[face[2]]
    center = triangle_center(v1, v2, v3)
    vertices_dodecahedron.append(center)

vertices_dodecahedron = np.array(vertices_dodecahedron)

print(f"Počet vrcholů dvanáctistěnu: {len(vertices_dodecahedron)}")

# Najdi stěny dvanáctistěnu (12 pětiúhelníků)
def find_dodecahedron_faces(icosa_faces, icosa_vertices_count):
    vertex_to_faces = {}
    for face_idx, face in enumerate(icosa_faces):
        for vertex in face:
            if vertex not in vertex_to_faces:
                vertex_to_faces[vertex] = []
            vertex_to_faces[vertex].append(face_idx)
    
    dodeca_faces = []
    for vertex, face_indices in vertex_to_faces.items():
        if len(face_indices) == 5:
            dodeca_faces.append(face_indices)
    
    return dodeca_faces

faces_dodecahedron_unsorted = find_dodecahedron_faces(faces_icosahedron, len(vertices_icosahedron))

# Seřaď vrcholy pětiúhelníků
def sort_pentagon_vertices(pentagon_indices, vertices):
    center = np.mean([vertices[i] for i in pentagon_indices], axis=0)
    
    v0 = vertices[pentagon_indices[0]] - center
    v1 = vertices[pentagon_indices[1]] - center
    normal = np.cross(v0, v1)
    normal = normal / np.linalg.norm(normal)
    
    def angle_from_center(idx):
        v = vertices[idx] - center
        v_proj = v - np.dot(v, normal) * normal
        angle = np.arctan2(np.dot(np.cross(v0, v_proj), normal), np.dot(v0, v_proj))
        return angle
    
    sorted_indices = sorted(pentagon_indices, key=angle_from_center)
    return sorted_indices

faces_dodecahedron = []
for pentagon in faces_dodecahedron_unsorted:
    sorted_pentagon = sort_pentagon_vertices(pentagon, vertices_dodecahedron)
    faces_dodecahedron.append(sorted_pentagon)

# Hrany dvanáctistěnu
edges_dodecahedron = set()
for face in faces_dodecahedron:
    for i in range(len(face)):
        edge = tuple(sorted([face[i], face[(i+1) % len(face)]]))
        edges_dodecahedron.add(edge)
edges_dodecahedron = list(edges_dodecahedron)

print(f"Počet stěn dvanáctistěnu: {len(faces_dodecahedron)}")
print(f"Počet hran dvanáctistěnu: {len(edges_dodecahedron)}")

# ========== VYKRESLENÍ ==========

# 1. Stěny dvacetistěnu - PRŮHLEDNÉ ŽLUTÉ
ax.plot_trisurf(
    vertices_icosahedron[:, 0],
    vertices_icosahedron[:, 1],
    vertices_icosahedron[:, 2],
    triangles=faces_icosahedron,
    alpha=0.15,
    color='yellow',
    edgecolor='none'
)

# 2. Hrany dvacetistěnu - oranžové
for edge in edges_icosahedron:
    i, j = edge
    ax.plot(
        [vertices_icosahedron[i, 0], vertices_icosahedron[j, 0]],
        [vertices_icosahedron[i, 1], vertices_icosahedron[j, 1]],
        [vertices_icosahedron[i, 2], vertices_icosahedron[j, 2]],
        'orange', linewidth=2.5, alpha=0.7
    )

# 3. Dvanáctistěn - zelené hrany (BEZ ZMĚNY)
for edge in edges_dodecahedron:
    i, j = edge
    ax.plot(
        [vertices_dodecahedron[i, 0], vertices_dodecahedron[j, 0]],
        [vertices_dodecahedron[i, 1], vertices_dodecahedron[j, 1]],
        [vertices_dodecahedron[i, 2], vertices_dodecahedron[j, 2]],
        'g-', linewidth=3, alpha=0.8
    )

# 4. Vrcholy dvacetistěnu - oranžové s popisky A-L
ax.scatter(vertices_icosahedron[:, 0],
           vertices_icosahedron[:, 1],
           vertices_icosahedron[:, 2],
           c='orange', s=200, alpha=0.9, edgecolors='darkorange', linewidth=2, zorder=10)

for i, (vertex, label) in enumerate(zip(vertices_icosahedron, labels_icosahedron)):
    ax.text(vertex[0], vertex[1], vertex[2], f'  {label}', 
            fontsize=14, fontweight='bold', color='darkorange')

# 5. Vrcholy dvanáctistěnu - červené s popisky 0-19 (BEZ ZMĚNY)
ax.scatter(vertices_dodecahedron[:, 0],
           vertices_dodecahedron[:, 1],
           vertices_dodecahedron[:, 2],
           c='red', s=150, alpha=0.95, edgecolors='darkred', linewidth=2, zorder=8)

for i, vertex in enumerate(vertices_dodecahedron):
    ax.text(vertex[0], vertex[1], vertex[2], f' {i}', 
            fontsize=10, fontweight='bold', color='darkred')

# Nastavení
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)
ax.set_box_aspect([1, 1, 1])
ax.set_title('Dualita: Dvacetistěn (A-L) → Dvanáctistěn (0-19)', fontsize=18, fontweight='bold')
ax.view_init(elev=20, azim=45)

max_range = 2
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])
ax.set_zlim([-max_range, max_range])

plt.tight_layout()
plt.show()

# ========== SHRNUTÍ ==========
print("\n" + "="*60)
print("SHRNUTÍ")
print("="*60)
print("VNĚJŠÍ DVACETISTĚN:")
print(f"  - Vrcholy: A-L (12 vrcholů)")
print(f"  - Stěny: průhledné žluté (20 trojúhelníků)")
print(f"  - Hrany: oranžové (30 hran)")
print("\nVEPSANÝ DVANÁCTISTĚN:")
print(f"  - Vrcholy: 0-19 (20 vrcholů)")
print(f"  - Hrany: zelené (30 hran)")
print(f"  - Stěny: 12 pětiúhelníků")
print("\nDUALITA:")
print(f"  - Dvacetistěn: 12 vrcholů ↔ Dvanáctistěn: 12 stěn ✓")
print(f"  - Dvacetistěn: 20 stěn ↔ Dvanáctistěn: 20 vrcholů ✓")