"""
Pomocné funkce pro vykreslování 3D diagramů
Helper functions for rendering 3D diagrams
"""
import numpy as np
from typing import List, Tuple, Union, Optional
from config.settings import COLORS, SIZES


class Renderer3D:
    """Helper třída pro vykreslování 3D prvků"""

    @staticmethod
    def draw_point(ax, point: Union[np.ndarray, List, Tuple],
                   color: str = None,
                   size: int = None,
                   label: str = '',
                   alpha: float = 0.9) -> None:
        """
        Nakreslí bod v 3D prostoru

        Args:
            ax: Matplotlib 3D axes
            point: Souřadnice bodu [x, y, z]
            color: Barva bodu
            size: Velikost bodu
            label: Text popisku
            alpha: Průhlednost
        """
        if color is None:
            color = COLORS['selected_point']
        if size is None:
            size = SIZES['point_default']

        point = np.array(point)
        ax.scatter([point[0]], [point[1]], [point[2]],
                   c=color, s=size, alpha=alpha,
                   edgecolors='black', linewidth=1.5)

        if label:
            ax.text(point[0], point[1], point[2],
                    f'  {label}',
                    fontsize=10,
                    fontweight='bold',
                    color='black')

    @staticmethod
    def draw_points(ax, points: np.ndarray,
                    colors: Union[str, List[str]] = None,
                    sizes: Union[int, List[int]] = None,
                    labels: Optional[List[str]] = None,
                    alpha: float = 0.9) -> None:
        """
        Nakreslí více bodů najednou

        Args:
            ax: Matplotlib 3D axes
            points: Array bodů tvaru (N, 3)
            colors: Jedna barva nebo seznam barev pro každý bod
            sizes: Jedna velikost nebo seznam velikostí
            labels: Seznam popisků (nebo None)
            alpha: Průhlednost
        """
        if colors is None:
            colors = COLORS['selected_point']
        if sizes is None:
            sizes = SIZES['point_default']

        # Pokud je colors nebo sizes jen jedna hodnota, vytvoř z ní seznam
        if isinstance(colors, str):
            colors = [colors] * len(points)
        if isinstance(sizes, int):
            sizes = [sizes] * len(points)

        for i, point in enumerate(points):
            label = labels[i] if labels and i < len(labels) else ''
            Renderer3D.draw_point(ax, point, colors[i], sizes[i], label, alpha)

    @staticmethod
    def draw_edge(ax, p1: Union[np.ndarray, List],
                  p2: Union[np.ndarray, List],
                  color: str = None,
                  width: int = None,
                  style: str = '-',
                  alpha: float = 0.8) -> None:
        """
        Nakreslí hranu mezi dvěma body

        Args:
            ax: Matplotlib 3D axes
            p1: První bod [x, y, z]
            p2: Druhý bod [x, y, z]
            color: Barva hrany
            width: Tloušťka čáry
            style: Styl čáry ('-', '--', ':', atd.)
            alpha: Průhlednost
        """
        if color is None:
            color = COLORS['solid_edge']
        if width is None:
            width = SIZES['edge_width']

        p1 = np.array(p1)
        p2 = np.array(p2)

        ax.plot([p1[0], p2[0]],
                [p1[1], p2[1]],
                [p1[2], p2[2]],
                color=color,
                linewidth=width,
                linestyle=style,
                alpha=alpha)

    @staticmethod
    def draw_edges(ax, vertices: np.ndarray,
                   edges: List[Tuple[int, int]],
                   color: str = None,
                   width: int = None,
                   style: str = '-',
                   alpha: float = 0.8) -> None:
        """
        Nakreslí více hran najednou

        Args:
            ax: Matplotlib 3D axes
            vertices: Array vrcholů tvaru (N, 3)
            edges: Seznam dvojic (i, j) indexů vrcholů
            color: Barva hran
            width: Tloušťka čar
            style: Styl čáry
            alpha: Průhlednost
        """
        for i, j in edges:
            Renderer3D.draw_edge(ax, vertices[i], vertices[j],
                                color, width, style, alpha)

    @staticmethod
    def draw_axes_arrows(ax, length: float = 2.0,
                        colors: Tuple[str, str, str] = ('red', 'green', 'blue')) -> None:
        """
        Nakreslí barevné osy souřadného systému

        Args:
            ax: Matplotlib 3D axes
            length: Délka os
            colors: Barvy pro X, Y, Z osy
        """
        origin = np.array([0, 0, 0])

        # X osa (červená)
        ax.plot([0, length], [0, 0], [0, 0],
                color=colors[0], linewidth=2, alpha=0.5, label='X')

        # Y osa (zelená)
        ax.plot([0, 0], [0, length], [0, 0],
                color=colors[1], linewidth=2, alpha=0.5, label='Y')

        # Z osa (modrá)
        ax.plot([0, 0], [0, 0], [0, length],
                color=colors[2], linewidth=2, alpha=0.5, label='Z')

    @staticmethod
    def draw_plane(ax, normal: str = 'z',
                   offset: float = 0.0,
                   limits: Tuple[float, float] = (-2, 2),
                   color: str = 'orange',
                   alpha: float = 0.1) -> None:
        """
        Nakreslí průhlednou rovinu

        Args:
            ax: Matplotlib 3D axes
            normal: Normála roviny ('x', 'y', nebo 'z')
            offset: Posunutí roviny od počátku
            limits: Hranice roviny
            color: Barva roviny
            alpha: Průhlednost
        """
        x = np.linspace(limits[0], limits[1], 2)
        y = np.linspace(limits[0], limits[1], 2)

        if normal.lower() == 'z':
            X, Y = np.meshgrid(x, y)
            Z = np.ones_like(X) * offset
        elif normal.lower() == 'y':
            X, Z = np.meshgrid(x, y)
            Y = np.ones_like(X) * offset
        else:  # x
            Y, Z = np.meshgrid(x, y)
            X = np.ones_like(Y) * offset

        ax.plot_surface(X, Y, Z, color=color, alpha=alpha)
