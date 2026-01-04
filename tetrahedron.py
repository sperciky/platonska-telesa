import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Vytvoř 3D graf
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Definuj vrcholy čtyřstěnu (tetrahedron)
#phi = (1 + np.sqrt(5)) / 2  # zlatý řez
vertices = np.array([
    [1, 1, 1],
    [1, -1, -1],
    [-1, 1, -1],
    [-1, -1, 1]
])

# Definuj stěny (trojúhelníky) pomocí indexů vrcholů
faces = np.array([
    [0, 1, 2],
    [0, 1, 3],
    [0, 2, 3],
    [1, 2, 3]
])

# Nakresli těleso
ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2],
                triangles=faces, alpha=0.7, color='lightblue',
                edgecolor='navy', linewidth=1)

# Nakresli vrcholy
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2],
           c='red', s=100, marker='o')

# Nastav popisky a proporce
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])
ax.set_title('Čtyřstěn')

plt.show()