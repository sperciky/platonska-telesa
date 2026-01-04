"""
Dualita: Krychle a Osmistěn
Duality: Cube and Octahedron
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D


class DualityCubeOctahedron(Step):
    """Dualita - Krychle a Osmistěn"""

    def __init__(self):
        super().__init__()

        # STŘEDNÍ KRYCHLE (vrcholy K-R)
        # Vytvoříme krychli s vrcholy v bodech (±1, ±1, ±1)
        self.cube_vertices = np.array([
            [-1, -1, -1],  # K
            [-1, -1,  1],  # L
            [-1,  1, -1],  # M
            [-1,  1,  1],  # N
            [ 1, -1, -1],  # O
            [ 1, -1,  1],  # P
            [ 1,  1, -1],  # Q
            [ 1,  1,  1]   # R
        ])

        self.cube_labels = ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

        # Hrany krychle
        self.cube_edges = [
            (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
            (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
        ]

        # VNITŘNÍ OSMISTĚN (vrcholy 1-6)
        # Vrcholy osmistěnu jsou ve středech stěn krychle
        # Vypočítáme je jako středy stěn krychle
        cube_faces = [
            [0, 1, 3, 2],  # -X stěna
            [4, 5, 7, 6],  # +X stěna
            [0, 1, 5, 4],  # -Y stěna
            [2, 3, 7, 6],  # +Y stěna
            [0, 2, 6, 4],  # -Z stěna
            [1, 3, 7, 5]   # +Z stěna
        ]

        self.octa_vertices = []
        for face in cube_faces:
            face_vertices = self.cube_vertices[face]
            center = np.mean(face_vertices, axis=0)
            self.octa_vertices.append(center)

        self.octa_vertices = np.array(self.octa_vertices)
        self.octa_labels = ['1', '2', '3', '4', '5', '6']

        # Stěny osmistěnu (8 trojúhelníků)
        self.octa_faces = [
            [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
            [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
        ]

        # Hrany osmistěnu
        edges_set = set()
        for face in self.octa_faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i+1)%3]]))
                edges_set.add(edge)
        self.octa_edges = list(edges_set)

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=12,
            category='Dualita',
            title='Dualita: Krychle ↔ Osmistěn',
            short_name='Krychle ↔ Osmistěn'
        )

    def get_description(self) -> str:
        return """
## Dualita: Krychle a Osmistěn

### Co je dualita?

**Dualita** je speciální vztah mezi dvěma Platónskými tělesy:
- **Vrcholy** jednoho tělesa odpovídají **stěnám** druhého
- **Stěny** jednoho odpovídají **vrcholům** druhého

---

### Krychle ↔ Osmistěn:

🟢 **KRYCHLE (K-R, zelená):**
- **8 vrcholů** v bodech (±1, ±1, ±1)
- **6 stěn** (čtvercových)
- **12 hran**

🔵 **OSMISTĚN (1-6, modrý):**
- **6 vrcholů** (ve středech stěn krychle!)
- **8 stěn** (trojúhelníkových)
- **12 hran**

---

### Jak to funguje?

1. ✅ Vezmi krychli (8 vrcholů, 6 stěn)
2. ✅ Najdi středy všech 6 stěn krychle
3. ✅ Tyto středy jsou vrcholy osmistěnu! (6 vrcholů)
4. ✅ Osm trojúhelníkových stěn osmistěnu odpovídá 8 vrcholům krychle

---

### Zajímavost:

Krychle a osmistěn jsou **duální tělesa**:
- Krychle: 8 vrcholů ↔ Osmistěn: 8 stěn ✓
- Krychle: 6 stěn ↔ Osmistěn: 6 vrcholů ✓
- Krychle: 12 hran ↔ Osmistěn: 12 hran ✓

---

➡️ **Další krok ukáže vnořené osmistěny!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení krychle a osmistěnu (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany krychle (zelená)
        Renderer3D.draw_edges(
            ax, self.cube_vertices, self.cube_edges,
            color='green', width=2
        )

        # Nakresli hrany osmistěnu (modrá)
        Renderer3D.draw_edges(
            ax, self.octa_vertices, self.octa_edges,
            color='blue', width=2
        )

        # Nakresli vrcholy krychle (zelená)
        for v, label in zip(self.cube_vertices, self.cube_labels):
            Renderer3D.draw_point(ax, v, color='lime', size=120, label=label)

        # Nakresli vrcholy osmistěnu (modrá)
        for v, label in zip(self.octa_vertices, self.octa_labels):
            Renderer3D.draw_point(ax, v, color='blue', size=120, label=label)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení krychle a osmistěnu (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěny osmistěnu, pokud je to zapnuté (modrá)
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)
            fig = PlotlyRenderer3D.add_faces(
                fig, self.octa_vertices, self.octa_faces,
                color='blue', opacity=opacity
            )

        # Nakresli hrany krychle (zelená)
        edge_width = st.session_state.get('edge_width', 3)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.cube_vertices, self.cube_edges,
            color='green', width=edge_width
        )

        # Nakresli hrany osmistěnu (modrá)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.octa_vertices, self.octa_edges,
            color='blue', width=edge_width
        )

        # Nakresli vrcholy krychle (zelená)
        vertex_size = st.session_state.get('vertex_size', 12)
        for v, label in zip(self.cube_vertices, self.cube_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='lime', size=vertex_size, label=label
            )

        # Nakresli vrcholy osmistěnu (modrá)
        for v, label in zip(self.octa_vertices, self.octa_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='blue', size=vertex_size, label=label
            )

        return fig
