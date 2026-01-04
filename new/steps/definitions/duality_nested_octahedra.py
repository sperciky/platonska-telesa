"""
Vnořené osmistěny a krychle
Nested Octahedra and Cube
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D


class DualityNestedOctahedra(Step):
    """Dualita - Vnořené osmistěny"""

    def __init__(self):
        super().__init__()

        # VNĚJŠÍ OSMISTĚN (vrcholy 1-6, největší)
        scale = 2
        self.outer_octa_vertices = np.array([
            [ scale,  0,  0],  # 1: +X
            [-scale,  0,  0],  # 2: -X
            [ 0,  scale,  0],  # 3: +Y
            [ 0, -scale,  0],  # 4: -Y
            [ 0,  0,  scale],  # 5: +Z
            [ 0,  0, -scale]   # 6: -Z
        ])

        self.outer_octa_labels = ['1', '2', '3', '4', '5', '6']

        # Stěny vnějšího osmistěnu (8 trojúhelníků)
        self.outer_octa_faces = [
            [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
            [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
        ]

        # VEPSANÁ KRYCHLE (vrcholy K-R)
        # Vrcholy krychle jsou ve středech stěn vnějšího osmistěnu
        def triangle_center(v1, v2, v3):
            """Vypočítá těžiště trojúhelníku"""
            return (v1 + v2 + v3) / 3

        self.cube_vertices = []
        for face in self.outer_octa_faces:
            a, b, c = face
            center = triangle_center(
                self.outer_octa_vertices[a],
                self.outer_octa_vertices[b],
                self.outer_octa_vertices[c]
            )
            self.cube_vertices.append(center)

        self.cube_vertices = np.array(self.cube_vertices)
        self.cube_labels = ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

        # Hrany krychle - najdeme na základě sousedních stěn osmistěnu
        def find_cube_edges(faces):
            """Najde hrany krychle na základě sousedních stěn"""
            edges = []
            for i in range(len(faces)):
                for j in range(i + 1, len(faces)):
                    shared = len(set(faces[i]) & set(faces[j]))
                    if shared == 2:
                        edges.append((i, j))
            return edges

        self.cube_edges = find_cube_edges(self.outer_octa_faces)

        # VNITŘNÍ OSMISTĚN (vrcholy 7-12)
        # Vrcholy vnitřního osmistěnu jsou ve středech stěn krychle
        # Najdeme stěny krychle
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

        cube_faces = find_cube_faces_from_octahedron_faces(self.outer_octa_faces)

        def quad_center(v1, v2, v3, v4):
            """Vypočítá střed čtyřúhelníku"""
            return (v1 + v2 + v3 + v4) / 4

        self.inner_octa_vertices = []
        for face in cube_faces:
            centers = [self.cube_vertices[idx] for idx in face]
            center = quad_center(centers[0], centers[1], centers[2], centers[3])
            self.inner_octa_vertices.append(center)

        self.inner_octa_vertices = np.array(self.inner_octa_vertices)
        self.inner_octa_labels = ['7', '8', '9', '10', '11', '12']

        # Hrany vnitřního osmistěnu
        self.inner_octa_edges = []
        for i in range(len(cube_faces)):
            for j in range(i + 1, len(cube_faces)):
                shared = len(set(cube_faces[i]) & set(cube_faces[j]))
                if shared == 2:
                    self.inner_octa_edges.append((i, j))

        # Stěny vnitřního osmistěnu (8 trojúhelníků)
        self.inner_octa_faces = [
            [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
            [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=13,
            category='Dualita',
            title='Dualita: Vnořené osmistěny',
            short_name='Vnořené osmistěny'
        )

    def get_description(self) -> str:
        # Vypočítejme délky hran
        def edge_length(v1, v2):
            return np.linalg.norm(v2 - v1)

        outer_edge = edge_length(self.outer_octa_vertices[0], self.outer_octa_vertices[2])
        if len(self.cube_edges) > 0:
            i, j = self.cube_edges[0]
            cube_edge = edge_length(self.cube_vertices[i], self.cube_vertices[j])
        else:
            cube_edge = 0
        if len(self.inner_octa_edges) > 0:
            i, j = self.inner_octa_edges[0]
            inner_edge = edge_length(self.inner_octa_vertices[i], self.inner_octa_vertices[j])
        else:
            inner_edge = 0

        return f"""
## Dualita: Osmistěn → Krychle → Osmistěn

### Vnořená tělesa:

Tento diagram ukazuje **trojitou dualitu** - tři tělesa vnořená do sebe:

---

### 🟠 VNĚJŠÍ OSMISTĚN (1-6, oranžový):

- **6 vrcholů** na osách souřadnic
- **8 stěn** (trojúhelníkových)
- **12 hran**
- Délka hrany: **2√2 ≈ {outer_edge:.3f}**

---

### 🟢 VEPSANÁ KRYCHLE (K-R, zelená):

- **8 vrcholů** (ve středech stěn vnějšího osmistěnu!)
- **6 stěn** (čtvercových)
- **12 hran**
- Délka hrany: **2√(2/3) ≈ {cube_edge:.3f}**

---

### 🔵 VNITŘNÍ OSMISTĚN (7-12, modrý):

- **6 vrcholů** (ve středech stěn krychle!)
- **8 stěn** (trojúhelníkových)
- **12 hran**
- Délka hrany: **2√(2/9) ≈ {inner_edge:.3f}**

---

### Poměry délek hran:

- **Vnější osmistěn : Krychle** = √3 ≈ 1.732
- **Krychle : Vnitřní osmistěn** = √3 ≈ 1.732
- **Vnější osmistěn : Vnitřní osmistěn** = 3

---

### Zajímavosti:

1. **Každé těleso je duální k sousednímu**
2. **Poměr velikostí je vždy √3**
3. **Tento proces můžeme opakovat donekonečna!**
4. **Všechna tři tělesa mají 12 hran**

---

✨ **Tohle je krásný příklad matematické symetrie!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení vnořených osmistěnů (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany vnějšího osmistěnu (oranžová)
        edges_set = set()
        for face in self.outer_octa_faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i+1)%3]]))
                edges_set.add(edge)
        outer_edges = list(edges_set)
        Renderer3D.draw_edges(
            ax, self.outer_octa_vertices, outer_edges,
            color='orange', width=2
        )

        # Nakresli hrany krychle (zelená)
        Renderer3D.draw_edges(
            ax, self.cube_vertices, self.cube_edges,
            color='green', width=2.5
        )

        # Nakresli hrany vnitřního osmistěnu (modrá)
        Renderer3D.draw_edges(
            ax, self.inner_octa_vertices, self.inner_octa_edges,
            color='blue', width=2
        )

        # Nakresli vrcholy
        for v, label in zip(self.outer_octa_vertices, self.outer_octa_labels):
            Renderer3D.draw_point(ax, v, color='orange', size=150, label=label)

        for v, label in zip(self.cube_vertices, self.cube_labels):
            Renderer3D.draw_point(ax, v, color='lime', size=150, label=label)

        for v, label in zip(self.inner_octa_vertices, self.inner_octa_labels):
            Renderer3D.draw_point(ax, v, color='blue', size=150, label=label)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení vnořených osmistěnů (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2.5, 2.5))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěny, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)

            # Vnější osmistěn - žlutá průhledná
            fig = PlotlyRenderer3D.add_faces(
                fig, self.outer_octa_vertices, self.outer_octa_faces,
                color='#FFD700', opacity=opacity * 0.4  # Velmi průhledná
            )

            # Vnitřní osmistěn - azurová
            fig = PlotlyRenderer3D.add_faces(
                fig, self.inner_octa_vertices, self.inner_octa_faces,
                color='#00CED1', opacity=opacity
            )

        # Nakresli hrany vnějšího osmistěnu (oranžová)
        edge_width = st.session_state.get('edge_width', 3)
        edges_set = set()
        for face in self.outer_octa_faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i+1)%3]]))
                edges_set.add(edge)
        outer_edges = list(edges_set)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.outer_octa_vertices, outer_edges,
            color='orange', width=edge_width
        )

        # Nakresli hrany krychle (zelená)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.cube_vertices, self.cube_edges,
            color='green', width=edge_width
        )

        # Nakresli hrany vnitřního osmistěnu (modrá)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.inner_octa_vertices, self.inner_octa_edges,
            color='blue', width=edge_width
        )

        # Nakresli vrcholy
        vertex_size = st.session_state.get('vertex_size', 12)

        for v, label in zip(self.outer_octa_vertices, self.outer_octa_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='orange', size=vertex_size, label=label
            )

        for v, label in zip(self.cube_vertices, self.cube_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='lime', size=vertex_size, label=label
            )

        for v, label in zip(self.inner_octa_vertices, self.inner_octa_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='red', size=vertex_size, label=label
            )

        return fig
