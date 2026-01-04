"""
Dualita: Čtyřstěn duální sám k sobě
Duality: Tetrahedron dual to itself
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D


class DualityTetrahedronSelf(Step):
    """Dualita - Čtyřstěn duální sám k sobě"""

    def __init__(self):
        super().__init__()

        # STŘEDNÍ ČTYŘSTĚN (výchozí)
        self.middle_tetra = np.array([
            [ 1,  1,  1],   # B
            [ 1, -1, -1],   # C
            [-1,  1, -1],   # D
            [-1, -1,  1]    # E
        ])

        self.middle_labels = ['B', 'C', 'D', 'E']

        # Stěny středního čtyřstěnu
        self.middle_faces = [
            [0, 1, 2],  # BCD
            [0, 1, 3],  # BCE
            [0, 2, 3],  # BDE
            [1, 2, 3]   # CDE
        ]

        # VNITŘNÍ ČTYŘSTĚN (duální ke střednímu - směrem dovnitř)
        # Vrcholy = středy stěn středního čtyřstěnu
        def triangle_center(v1, v2, v3):
            """Vypočítá střed (těžiště) trojúhelníku"""
            return (v1 + v2 + v3) / 3

        self.inner_tetra = []
        for face in self.middle_faces:
            v1 = self.middle_tetra[face[0]]
            v2 = self.middle_tetra[face[1]]
            v3 = self.middle_tetra[face[2]]
            center = triangle_center(v1, v2, v3)
            self.inner_tetra.append(center)

        self.inner_tetra = np.array(self.inner_tetra)
        self.inner_labels = ['F', 'G', 'H', 'I']

        # Stěny vnitřního čtyřstěnu
        self.inner_faces = [
            [0, 1, 2],  # FGH
            [0, 1, 3],  # FGI
            [0, 2, 3],  # FHI
            [1, 2, 3]   # GHI
        ]

        # VNĚJŠÍ ČTYŘSTĚN (duální ke střednímu - směrem ven)
        # Chceme, aby středy stěn vnějšího byly vrcholy středního
        # Matematika: S = suma vrcholů středního
        # Vnější vrchol i = S - 3 * střední vrchol i
        S = np.sum(self.middle_tetra, axis=0)

        self.outer_tetra = np.array([
            S - 3*self.middle_tetra[0],  # W = S - 3*B
            S - 3*self.middle_tetra[1],  # X = S - 3*C
            S - 3*self.middle_tetra[2],  # Y = S - 3*D
            S - 3*self.middle_tetra[3]   # Z = S - 3*E
        ])

        self.outer_labels = ['W', 'X', 'Y', 'Z']

        # Stěny vnějšího čtyřstěnu
        self.outer_faces = [
            [1, 2, 3],  # XYZ (naproti W, střed = B)
            [0, 2, 3],  # WYZ (naproti X, střed = C)
            [0, 1, 3],  # WXZ (naproti Y, střed = D)
            [0, 1, 2]   # WXY (naproti Z, střed = E)
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=15,
            category='Dualita',
            title='Dualita: Čtyřstěn ↔ Čtyřstěn',
            short_name='Čtyřstěn ↔ Čtyřstěn'
        )

    def get_description(self) -> str:
        # Vypočítej délky hran
        outer_edge = np.linalg.norm(self.outer_tetra[0] - self.outer_tetra[1])
        middle_edge = np.linalg.norm(self.middle_tetra[0] - self.middle_tetra[1])
        inner_edge = np.linalg.norm(self.inner_tetra[0] - self.inner_tetra[1])

        return f"""
## Dualita: Čtyřstěn duální sám k sobě!

### Unikátní vlastnost:

**Čtyřstěn je jediné Platónské těleso, které je duální SAMO K SOBĚ!**

Všechna ostatní tělesa mají různé duály:
- Krychle ↔ Osmistěn
- Dvacetistěn ↔ Dvanáctistěn
- **Čtyřstěn ↔ Čtyřstěn** ✨

---

### Trojitá dualita:

Tento diagram ukazuje **tři čtyřstěny vnořené do sebe**:

---

### 🔵 VNĚJŠÍ ČTYŘSTĚN (W-Z, modrý):

- **4 vrcholy**: W, X, Y, Z
- **4 stěny** (trojúhelníkové)
- **6 hran**
- Délka hrany: **{outer_edge:.3f}**
- **Středy stěn = vrcholy středního čtyřstěnu**

---

### 🟠 STŘEDNÍ ČTYŘSTĚN (B-E, oranžový):

- **4 vrcholy**: B, C, D, E
- **4 stěny** (trojúhelníkové)
- **6 hran**
- Délka hrany: **{middle_edge:.3f}**
- **Středy stěn = vrcholy vnitřního čtyřstěnu**

---

### 🔴 VNITŘNÍ ČTYŘSTĚN (F-I, červený):

- **4 vrcholy**: F, G, H, I (ve středech stěn středního)
- **4 stěny** (trojúhelníkové)
- **6 hran**
- Délka hrany: **{inner_edge:.3f}**

---

### Matematický vzorec:

Pro střední čtyřstěn s vrcholy **B, C, D, E**:

**Vnitřní čtyřstěn:**
- Vrcholy = středy stěn středního

**Vnější čtyřstěn:**
```
S = B + C + D + E  (suma vrcholů)

W = S - 3*B
X = S - 3*C
Y = S - 3*D
Z = S - 3*E
```

---

### Poměry délek hran:

- **Vnější : Střední** = {outer_edge/middle_edge:.3f}
- **Střední : Vnitřní** = {middle_edge/inner_edge:.3f}
- **Vnější : Vnitřní** = {outer_edge/inner_edge:.3f}

---

### Proč je čtyřstěn duální sám k sobě?

1. **Stejný počet vrcholů a stěn** (4 = 4)
2. **Symetrie** - každá stěna je rovnostranný trojúhelník
3. **Duální čtyřstěn má stejný tvar** - jen otočený a zmenšený
4. **Geometrická harmonie** - dokonalá symetrie

---

✨ **Čtyřstěn je nejjednodušší a nejsymetričtější Platónské těleso!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení trojité duality čtyřstěnů (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Vnější čtyřstěn - modré hrany
        outer_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in outer_edges:
            i, j = edge
            Renderer3D.draw_edge(ax, self.outer_tetra[i], self.outer_tetra[j],
                               color='blue', width=2)

        # Střední čtyřstěn - oranžové hrany
        middle_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in middle_edges:
            i, j = edge
            Renderer3D.draw_edge(ax, self.middle_tetra[i], self.middle_tetra[j],
                               color='orange', width=2.5)

        # Vnitřní čtyřstěn - červené hrany
        inner_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in inner_edges:
            i, j = edge
            Renderer3D.draw_edge(ax, self.inner_tetra[i], self.inner_tetra[j],
                               color='red', width=3)

        # Vrcholy
        for v, label in zip(self.outer_tetra, self.outer_labels):
            Renderer3D.draw_point(ax, v, color='blue', size=120, label=label)

        for v, label in zip(self.middle_tetra, self.middle_labels):
            Renderer3D.draw_point(ax, v, color='orange', size=150, label=label)

        for v, label in zip(self.inner_tetra, self.inner_labels):
            Renderer3D.draw_point(ax, v, color='red', size=120, label=label)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení trojité duality čtyřstěnů (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-4, 4))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěny, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)

            # Vnější čtyřstěn - velmi průhledné modré
            fig = PlotlyRenderer3D.add_faces(
                fig, self.outer_tetra, self.outer_faces,
                color='#4169E1', opacity=opacity * 0.2
            )

            # Střední čtyřstěn - oranžové průhledné
            fig = PlotlyRenderer3D.add_faces(
                fig, self.middle_tetra, self.middle_faces,
                color='orange', opacity=opacity * 0.5
            )

            # Vnitřní čtyřstěn - červené
            fig = PlotlyRenderer3D.add_faces(
                fig, self.inner_tetra, self.inner_faces,
                color='red', opacity=opacity
            )

        # Nakresli hrany
        edge_width = st.session_state.get('edge_width', 3)

        # Vnější čtyřstěn - modré hrany
        outer_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in outer_edges:
            i, j = edge
            fig = PlotlyRenderer3D.add_edge(
                fig, self.outer_tetra[i], self.outer_tetra[j],
                color='blue', width=edge_width
            )

        # Střední čtyřstěn - oranžové hrany
        middle_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in middle_edges:
            i, j = edge
            fig = PlotlyRenderer3D.add_edge(
                fig, self.middle_tetra[i], self.middle_tetra[j],
                color='orange', width=edge_width
            )

        # Vnitřní čtyřstěn - červené hrany
        inner_edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in inner_edges:
            i, j = edge
            fig = PlotlyRenderer3D.add_edge(
                fig, self.inner_tetra[i], self.inner_tetra[j],
                color='red', width=edge_width
            )

        # Nakresli vrcholy
        vertex_size = st.session_state.get('vertex_size', 12)

        # Vnější - modré
        for v, label in zip(self.outer_tetra, self.outer_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='blue', size=vertex_size, label=label
            )

        # Střední - oranžové
        for v, label in zip(self.middle_tetra, self.middle_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='orange', size=vertex_size * 1.2, label=label
            )

        # Vnitřní - červené
        for v, label in zip(self.inner_tetra, self.inner_labels):
            fig = PlotlyRenderer3D.add_point(
                fig, v, color='red', size=vertex_size, label=label
            )

        return fig
