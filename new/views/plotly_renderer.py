"""
Pomocné funkce pro vykreslování 3D diagramů pomocí Plotly
Helper functions for rendering 3D diagrams with Plotly (interactive!)
"""
import numpy as np
import plotly.graph_objects as go
from typing import List, Tuple, Union, Optional
from config.settings import COLORS, SIZES


class PlotlyRenderer3D:
    """Helper třída pro vykreslování interaktivních 3D prvků pomocí Plotly"""

    @staticmethod
    def create_figure(axis_limits: Tuple[float, float] = (-2, 2)) -> go.Figure:
        """
        Vytvoří prázdný Plotly 3D figure s nastaveným layoutem

        Args:
            axis_limits: Limity os (min, max)

        Returns:
            Plotly Figure instance
        """
        fig = go.Figure()

        # Nastav layout pro 3D scénu
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    range=[axis_limits[0], axis_limits[1]],
                    title='X',
                    gridcolor='lightgray',
                    showbackground=True,
                    backgroundcolor='white'
                ),
                yaxis=dict(
                    range=[axis_limits[0], axis_limits[1]],
                    title='Y',
                    gridcolor='lightgray',
                    showbackground=True,
                    backgroundcolor='white'
                ),
                zaxis=dict(
                    range=[axis_limits[0], axis_limits[1]],
                    title='Z',
                    gridcolor='lightgray',
                    showbackground=True,
                    backgroundcolor='white'
                ),
                aspectmode='cube',  # Zajistí stejný poměr stran
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)  # Výchozí pozice kamery
                )
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=600,
            showlegend=False
        )

        return fig

    @staticmethod
    def add_point(fig: go.Figure,
                  point: Union[np.ndarray, List, Tuple],
                  color: str = None,
                  size: int = None,
                  label: str = '',
                  show_label: bool = True) -> go.Figure:
        """
        Přidá bod do Plotly figure

        Args:
            fig: Plotly Figure instance
            point: Souřadnice bodu [x, y, z]
            color: Barva bodu (CSS nebo hex)
            size: Velikost bodu
            label: Text popisku
            show_label: Zda zobrazit popisek

        Returns:
            Upravený Figure
        """
        if color is None:
            color = COLORS['selected_point']
        if size is None:
            size = SIZES['point_default'] // 10  # Plotly používá menší čísla

        point = np.array(point)

        # Přidej bod
        fig.add_trace(go.Scatter3d(
            x=[point[0]],
            y=[point[1]],
            z=[point[2]],
            mode='markers',
            marker=dict(
                size=size,
                color=color,
                line=dict(color='black', width=2)
            ),
            text=label if show_label else '',
            hovertext=f'{label}<br>({point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f})',
            hoverinfo='text',
            showlegend=False
        ))

        # Přidej textový popisek, pokud je zadán
        if label and show_label:
            fig.add_trace(go.Scatter3d(
                x=[point[0]],
                y=[point[1]],
                z=[point[2]],
                mode='text',
                text=[label],
                textposition='top center',
                textfont=dict(size=12, color='black'),
                hoverinfo='skip',
                showlegend=False
            ))

        return fig

    @staticmethod
    def add_points(fig: go.Figure,
                   points: np.ndarray,
                   colors: Union[str, List[str]] = None,
                   sizes: Union[int, List[int]] = None,
                   labels: Optional[List[str]] = None,
                   show_labels: bool = True) -> go.Figure:
        """
        Přidá více bodů najednou

        Args:
            fig: Plotly Figure instance
            points: Array bodů tvaru (N, 3)
            colors: Jedna barva nebo seznam barev
            sizes: Jedna velikost nebo seznam velikostí
            labels: Seznam popisků
            show_labels: Zda zobrazit popisky

        Returns:
            Upravený Figure
        """
        if colors is None:
            colors = COLORS['selected_point']
        if sizes is None:
            sizes = SIZES['point_default'] // 10

        # Pokud je colors nebo sizes jen jedna hodnota, vytvoř z ní seznam
        if isinstance(colors, str):
            colors = [colors] * len(points)
        if isinstance(sizes, int):
            sizes = [sizes] * len(points)

        for i, point in enumerate(points):
            label = labels[i] if labels and i < len(labels) else ''
            PlotlyRenderer3D.add_point(
                fig, point, colors[i], sizes[i], label, show_labels
            )

        return fig

    @staticmethod
    def add_edge(fig: go.Figure,
                 p1: Union[np.ndarray, List],
                 p2: Union[np.ndarray, List],
                 color: str = None,
                 width: int = None,
                 dash: str = 'solid') -> go.Figure:
        """
        Přidá hranu mezi dvěma body

        Args:
            fig: Plotly Figure instance
            p1: První bod [x, y, z]
            p2: Druhý bod [x, y, z]
            color: Barva hrany
            width: Tloušťka čáry
            dash: Styl čáry ('solid', 'dash', 'dot')

        Returns:
            Upravený Figure
        """
        if color is None:
            color = COLORS['solid_edge']
        if width is None:
            width = SIZES['edge_width']

        p1 = np.array(p1)
        p2 = np.array(p2)

        fig.add_trace(go.Scatter3d(
            x=[p1[0], p2[0]],
            y=[p1[1], p2[1]],
            z=[p1[2], p2[2]],
            mode='lines',
            line=dict(color=color, width=width, dash=dash),
            hoverinfo='skip',
            showlegend=False
        ))

        return fig

    @staticmethod
    def add_edges(fig: go.Figure,
                  vertices: np.ndarray,
                  edges: List[Tuple[int, int]],
                  color: str = None,
                  width: int = None,
                  dash: str = 'solid') -> go.Figure:
        """
        Přidá více hran najednou

        Args:
            fig: Plotly Figure instance
            vertices: Array vrcholů tvaru (N, 3)
            edges: Seznam dvojic (i, j) indexů vrcholů
            color: Barva hran
            width: Tloušťka čar
            dash: Styl čáry

        Returns:
            Upravený Figure
        """
        for i, j in edges:
            PlotlyRenderer3D.add_edge(
                fig, vertices[i], vertices[j], color, width, dash
            )

        return fig

    @staticmethod
    def add_axes_arrows(fig: go.Figure,
                       length: float = 2.0,
                       colors: Tuple[str, str, str] = ('red', 'green', 'blue')) -> go.Figure:
        """
        Přidá barevné osy souřadného systému

        Args:
            fig: Plotly Figure instance
            length: Délka os
            colors: Barvy pro X, Y, Z osy

        Returns:
            Upravený Figure
        """
        origin = [0, 0, 0]

        # X osa (červená)
        fig.add_trace(go.Scatter3d(
            x=[0, length], y=[0, 0], z=[0, 0],
            mode='lines',
            line=dict(color=colors[0], width=4),
            name='X',
            hoverinfo='name',
            showlegend=False
        ))

        # Y osa (zelená)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, length], z=[0, 0],
            mode='lines',
            line=dict(color=colors[1], width=4),
            name='Y',
            hoverinfo='name',
            showlegend=False
        ))

        # Z osa (modrá)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[0, length],
            mode='lines',
            line=dict(color=colors[2], width=4),
            name='Z',
            hoverinfo='name',
            showlegend=False
        ))

        return fig

    @staticmethod
    def add_title(fig: go.Figure, title: str) -> go.Figure:
        """
        Přidá titulek k figure

        Args:
            fig: Plotly Figure instance
            title: Text titulku

        Returns:
            Upravený Figure
        """
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=16, weight='bold')
            )
        )
        return fig

    @staticmethod
    def add_face(fig: go.Figure,
                 vertices: np.ndarray,
                 face_indices: List[int],
                 color: str = 'lightblue',
                 opacity: float = 0.3,
                 show_edges: bool = False) -> go.Figure:
        """
        Přidá jednu stěnu (plochu) do Plotly figure

        Args:
            fig: Plotly Figure instance
            vertices: Array všech vrcholů tvaru (N, 3)
            face_indices: Seznam indexů vrcholů tvořících stěnu
            color: Barva stěny
            opacity: Průhlednost (0.0 = průhledná, 1.0 = neprůhledná)
            show_edges: Zda zobrazit okraje stěny

        Returns:
            Upravený Figure
        """
        # Pro trojúhelník použij Mesh3d
        if len(face_indices) == 3:
            face_vertices = vertices[face_indices]
            fig.add_trace(go.Mesh3d(
                x=face_vertices[:, 0],
                y=face_vertices[:, 1],
                z=face_vertices[:, 2],
                i=[0],
                j=[1],
                k=[2],
                color=color,
                opacity=opacity,
                hoverinfo='skip',
                showlegend=False,
                flatshading=True
            ))
        # Pro čtyřúhelník rozděl na dva trojúhelníky
        elif len(face_indices) == 4:
            face_vertices = vertices[face_indices]
            fig.add_trace(go.Mesh3d(
                x=face_vertices[:, 0],
                y=face_vertices[:, 1],
                z=face_vertices[:, 2],
                i=[0, 0],
                j=[1, 2],
                k=[2, 3],
                color=color,
                opacity=opacity,
                hoverinfo='skip',
                showlegend=False,
                flatshading=True
            ))
        # Pro pětiúhelník rozděl na tři trojúhelníky
        elif len(face_indices) == 5:
            face_vertices = vertices[face_indices]
            fig.add_trace(go.Mesh3d(
                x=face_vertices[:, 0],
                y=face_vertices[:, 1],
                z=face_vertices[:, 2],
                i=[0, 0, 0],
                j=[1, 2, 3],
                k=[2, 3, 4],
                color=color,
                opacity=opacity,
                hoverinfo='skip',
                showlegend=False,
                flatshading=True
            ))

        return fig

    @staticmethod
    def add_faces(fig: go.Figure,
                  vertices: np.ndarray,
                  faces: List[List[int]],
                  color: str = 'lightblue',
                  opacity: float = 0.3) -> go.Figure:
        """
        Přidá více stěn najednou

        Args:
            fig: Plotly Figure instance
            vertices: Array vrcholů tvaru (N, 3)
            faces: Seznam stěn, kde každá stěna je seznam indexů vrcholů
            color: Barva stěn
            opacity: Průhlednost

        Returns:
            Upravený Figure
        """
        for face in faces:
            PlotlyRenderer3D.add_face(fig, vertices, face, color, opacity)

        return fig
