import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Vrcholy krychle
vertices = [
    (0, 0, 0, 'A'),
    (2, 0, 0, 'B'),
    (2, 2, 0, 'C'),
    (0, 2, 0, 'D'),
    (0, 0, 2, 'E'),
    (2, 0, 2, 'F'),
    (2, 2, 2, 'G'),
    (0, 2, 2, 'H')
]

# Vrcholy osmistěnu
vertices_octahedron = [
    (1, 1, 0, '0'),
    (0, 1, 1, '1'),
    (1, 0, 1, '2'),
    (1, 1, 2, '3'), 
    (2, 1, 1, '4'),
    (1, 2, 1, '5'),
]

def draw_point_with_label(x, y, z, label):
    ax.scatter(x, y, z, c='red', s=100)
    ax.text(x+0.05, y+0.05, z+0.05, label, fontsize=12)

# Nakresli body krychle
for x, y, z, label in vertices:
    draw_point_with_label(x, y, z, label)

# Nakresli body osmistěnu
for x, y, z, label in vertices_octahedron:
    draw_point_with_label(x, y, z, label)

# Hrany krychle
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

for edge in edges:
    i, j = edge
    ax.plot(
        [vertices[i][0], vertices[j][0]],
        [vertices[i][1], vertices[j][1]],
        [vertices[i][2], vertices[j][2]],
        'k-', linewidth=2
    )

# STĚNY OSMISTĚNU (trojúhelníky)
# Každá stěna je definovaná třemi vrcholy
faces_octahedron = [
    (0, 1, 2),  # spodní polovina
    (0, 2, 4),
    (0, 4, 5),
    (0, 5, 1),
    (3, 1, 5),  # horní polovina
    (3, 5, 4),
    (3, 4, 2),
    (3, 2, 1)
]

# Připrav data pro plot_trisurf
# Potřebujeme pole pouze se souřadnicemi (bez popisků)
oct_coords = np.array([[x, y, z] for x, y, z, label in vertices_octahedron])

# Nakresli vybarvené stěny osmistěnu
ax.plot_trisurf(
    oct_coords[:, 0],  # X souřadnice
    oct_coords[:, 1],  # Y souřadnice
    oct_coords[:, 2],  # Z souřadnice
    triangles=faces_octahedron,
    alpha=0.3,         # průhlednost (0-1)
    color='cyan',      # barva
    edgecolor='blue',  # barva hran
    linewidth=1
)

# Nastavení os
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])

plt.show()