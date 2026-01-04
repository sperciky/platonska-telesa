
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(1, 1, 1, c='red', s=100, marker='o')
plt.show()
KeyboardInterrupt

#ax.plot_trisurf(x, y, z, triangles=faces, alpha=0.8, color='cyan')
