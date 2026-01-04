"""
Dualita: Dvacetistěn a Dvanáctistěn
Duality: Icosahedron and Dodecahedron
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D
from config.settings import PHI


class DualityIcosahedronDodecahedron(Step):
    """Dualita - Dvacetistěn a Dvanáctistěn"""

    def __init__(self):
        super().__init__()

        # VNĚJŠÍ DVACETISTĚN (vrcholy A-L)
        self.icosa_vertices = np.array([
            # Obdélník v rovině YZ
            [ 0,  1,  PHI],  # 0 = A
            [ 0,  1, -PHI],  # 1 = B
            [ 0, -1,  PHI],  # 2 = C
            [ 0, -1, -PHI],  # 3 = D

            # Obdélník v rovině XZ
            [ 1,  PHI,  0],  # 4 = E
            [ 1, -PHI,  0],  # 5 = F
            [-1,  PHI,  0],  # 6 = G
            [-1, -PHI,  0],  # 7 = H

            # Obdélník v rovině XY
            [ PHI,  0,  1],  # 8 = I
            [ PHI,  0, -1],  # 9 = J
            [-PHI,  0,  1],  # 10 = K
            [-PHI,  0, -1]   # 11 = L
        ])

        self.icosa_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

        # Stěny dvacetistěnu (20 trojúhelníků)
        self.icosa_faces = [
            # Horní čepice
            [0, 8, 4], [0, 4, 6], [0, 6, 10], [0, 10, 2], [0, 2, 8],

            # Horní pás
            [8, 2, 5], [2, 10, 7], [10, 6, 11], [6, 4, 1], [4, 8, 9],

            # Spodní pás
            [5, 2, 7], [7, 10, 11], [11, 6, 1], [1, 4, 9], [9, 8, 5],

            # Spodní čepice
            [3, 5, 7], [3, 7, 11], [3, 11, 1], [3, 1, 9], [3, 9, 5]
        ]

        # Hrany dvacetistěnu
        edges_set = set()
        for face in self.icosa_faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i+1)%3]]))
                edges_set.add(edge)
        self.icosa_edges = list(edges_set)

        # VEPSANÝ DVANÁCTISTĚN (vrcholy 0-19)
        # Vrcholy dvanáctistěnu jsou ve středech stěn dvacetistěnu
        def triangle_center(v1, v2, v3):
            """Střed trojúhelníku"""
            return (v1 + v2 + v3) / 3

        self.dodeca_vertices = []
        for face in self.icosa_faces:
            v1 = self.icosa_vertices[face[0]]
            v2 = self.icosa_vertices[face[1]]
            v3 = self.icosa_vertices[face[2]]
            center = triangle_center(v1, v2, v3)
            self.dodeca_vertices.append(center)

        self.dodeca_vertices = np.array(self.dodeca_vertices)

        # Najdi stěny dvanáctistěnu (12 pětiúhelníků)
        def find_dodecahedron_faces(icosa_faces, icosa_vertices_count):
            """Najde pětiúhelníkové stěny dvanáctistěnu"""
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

        faces_dodeca_unsorted = find_dodecahedron_faces(self.icosa_faces, len(self.icosa_vertices))

        # Seřaď vrcholy pětiúhelníků
        def sort_pentagon_vertices(pentagon_indices, vertices):
            """Seřadí vrcholy pětiúhelníku proti směru hodinových ručiček"""
            center = np.mean([vertices[i] for i in pentagon_indices], axis=0)

            v0 = vertices[pentagon_indices[0]] - center
            v1 = vertices[pentagon_indices[1]] - center
            normal = np.cross(v0, v1)
            if np.linalg.norm(normal) > 0:
                normal = normal / np.linalg.norm(normal)
            else:
                normal = np.array([0, 0, 1])

            def angle_from_center(idx):
                v = vertices[idx] - center
                v_proj = v - np.dot(v, normal) * normal
                angle = np.arctan2(np.dot(np.cross(v0, v_proj), normal), np.dot(v0, v_proj))
                return angle

            sorted_indices = sorted(pentagon_indices, key=angle_from_center)
            return sorted_indices

        self.dodeca_faces = []
        for pentagon in faces_dodeca_unsorted:
            sorted_pentagon = sort_pentagon_vertices(pentagon, self.dodeca_vertices)
            self.dodeca_faces.append(sorted_pentagon)

        # Hrany dvanáctistěnu
        edges_dodeca_set = set()
        for face in self.dodeca_faces:
            for i in range(len(face)):
                edge = tuple(sorted([face[i], face[(i+1) % len(face)]]))
                edges_dodeca_set.add(edge)
        self.dodeca_edges = list(edges_dodeca_set)

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=14,
            category='Dualita',
            title='Dualita: Dvacetistěn ↔ Dvanáctistěn',
            short_name='Dvacetistěn ↔ Dvanáctistěn'
        )

    def get_description(self) -> str:
        return """
## Dualita: Dvacetistěn a Dvanáctistěn

### Nejsložitější dualita!

Dvacetistěn a dvanáctistěn tvoří **duální pár** - nejvíce komplexní ze všech Platónských těles.

---

### 🟠 DVACETISTĚN (A-L, oranžový):

- **12 vrcholů** (ze zlatých obdélníků)
- **20 stěn** (rovnostranné trojúhelníky)
- **30 hran**
- Vrcholy: Tři zlaté obdélníky

---

### 🔴 DVANÁCTISTĚN (0-19, červený):

- **20 vrcholů** (ve středech stěn dvacetistěnu!)
- **12 stěn** (pravidelné pětiúhelníky)
- **30 hran**
- Jediné těleso s pětiúhelníkovými stěnami

---

### Jak to funguje?

1. ✅ Vezmi dvacetistěn (12 vrcholů, 20 stěn)
2. ✅ Najdi středy všech 20 trojúhelníkových stěn
3. ✅ Tyto středy jsou vrcholy dvanáctistěnu! (20 vrcholů)
4. ✅ 12 pětiúhelníkových stěn odpovídá 12 vrcholům dvacetistěnu

---

### Dualita:

- Dvacetistěn: 12 vrcholů ↔ Dvanáctistěn: 12 stěn ✓
- Dvacetistěn: 20 stěn ↔ Dvanáctistěn: 20 vrcholů ✓
- Dvacetistěn: 30 hran ↔ Dvanáctistěn: 30 hran ✓

---

### Zajímavosti:

1. **Oba obsahují zlatý řez φ** ve svých souřadnicích
2. **Nejvíce vrcholů a stěn** ze všech Platónských těles
3. **Používají se v biologii** - viry a organické molekuly
4. **Krásný příklad přírodní symetrie**

---

✨ **Gratuluji! Prozkoumal jsi všechny duality Platónských těles!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení dvacetistěnu a dvanáctistěnu (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany dvacetistěnu (oranžová)
        Renderer3D.draw_edges(
            ax, self.icosa_vertices, self.icosa_edges,
            color='orange', width=2
        )

        # Nakresli hrany dvanáctistěnu (zelená)
        Renderer3D.draw_edges(
            ax, self.dodeca_vertices, self.dodeca_edges,
            color='green', width=2.5
        )

        # Nakresli vrcholy dvacetistěnu (oranžová)
        for v, label in zip(self.icosa_vertices, self.icosa_labels):
            Renderer3D.draw_point(ax, v, color='orange', size=150, label=label)

        # Nakresli vrcholy dvanáctistěnu (červená)
        for i, v in enumerate(self.dodeca_vertices):
            Renderer3D.draw_point(ax, v, color='red', size=120, label=str(i))

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení dvacetistěnu a dvanáctistěnu (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěny, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)

            # Dvacetistěn - žlutá velmi průhledná
            fig = PlotlyRenderer3D.add_faces(
                fig, self.icosa_vertices, self.icosa_faces,
                color='#FFD700', opacity=opacity * 0.3
            )

            # Dvanáctistěn - zelená
            fig = PlotlyRenderer3D.add_faces(
                fig, self.dodeca_vertices, self.dodeca_faces,
                color='#00FF00', opacity=opacity
            )

        # Nakresli hrany dvacetistěnu (oranžová)
        edge_width = st.session_state.get('edge_width', 3)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.icosa_vertices, self.icosa_edges,
            color='orange', width=edge_width
        )

        # Nakresli hrany dvanáctistěnu (zelená)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.dodeca_vertices, self.dodeca_edges,
            color='green', width=edge_width
        )

        # Nakresli vrcholy dvacetistěnu (oranžová)
        vertex_size = st.session_state.get('vertex_size', 12)
        for v, label in zip(self.icosa_vertices, self.icosa_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='orange', size=vertex_size, label=label
            )

        # Nakresli vrcholy dvanáctistěnu (červená)
        for i, v in enumerate(self.dodeca_vertices):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='red', size=vertex_size * 0.8, label=str(i)
            )

        return fig
