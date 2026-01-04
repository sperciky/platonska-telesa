"""
Bonusový krok - střed trojúhelníku
Bonus step - triangle centroid
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D
from config.settings import PHI


class BonusStep_TriangleCenter(Step):
    """Bonus: Střed trojúhelníku (těžiště)"""

    def __init__(self):
        super().__init__()
        # Vrcholy trojúhelníku z dvacetistěnu
        icosa_vertices = np.array([
            [ 0,  1,  PHI], [ 0,  1, -PHI], [ 0, -1,  PHI], [ 0, -1, -PHI],
            [ 1,  PHI,  0], [ 1, -PHI,  0], [-1,  PHI,  0], [-1, -PHI,  0],
            [ PHI,  0,  1], [ PHI,  0, -1], [-PHI,  0,  1], [-PHI,  0, -1]
        ])
        
        self.A = icosa_vertices[0]
        self.B = icosa_vertices[8]
        self.C = icosa_vertices[4]
        self.center = (self.A + self.B + self.C) / 3

        self.triangle_edges = [(0, 1), (1, 2), (2, 0)]
        self.triangle_vertices = np.array([self.A, self.B, self.C])

        # Stěna trojúhelníku (1 trojúhelník)
        self.triangle_face = [[0, 1, 2]]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=16,
            category='Bonus',
            title='Bonus: Střed trojúhelníku (těžiště)',
            short_name='Střed trojúhelníku'
        )

    def get_description(self) -> str:
        return f"""
## Bonus: Jak najít střed trojúhelníku?

### Vzorec pro těžiště:

Střed (těžiště) trojúhelníku **T** se spočítá jako **průměr** souřadnic vrcholů:

```
T = (A + B + C) / 3
```

---

### Příklad:

```
A = ({self.A[0]:.2f}, {self.A[1]:.2f}, {self.A[2]:.2f})
B = ({self.B[0]:.2f}, {self.B[1]:.2f}, {self.B[2]:.2f})
C = ({self.C[0]:.2f}, {self.C[1]:.2f}, {self.C[2]:.2f})

T = (A + B + C) / 3
T = ({self.center[0]:.2f}, {self.center[1]:.2f}, {self.center[2]:.2f})
```

---

### Co je těžiště?

- **Střed hmotnosti** trojúhelníku
- Bod, kde se **protínají těžnice** (čáry z vrcholů na středy protějších stran)
- **Vyvážený bod** - kdyby byl trojúhelník z kartonu, držel by se v rovnováze

---

### Vlastnosti těžiště:

1. ✅ Vždy leží **uvnitř** trojúhelníku
2. ✅ Dělí těžnice v poměru **2:1** od vrcholu
3. ✅ Je to **průměr** všech tří vrcholů

---

### Použití:

Těžiště se používá:
- V **počítačové grafice** (střed objektů)
- Ve **fyzice** (rovnováha těles)
- V **geometrii** (konstrukce a důkazy)

---

✨ **Gratuluji! Dokončil jsi celý tutoriál Platónských těles!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení trojúhelníku s těžištěm (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli trojúhelník
        Renderer3D.draw_edges(ax, self.triangle_vertices, self.triangle_edges,
                             color='blue', width=3)

        # Nakresli vrcholy
        labels = ['A', 'B', 'C']
        Renderer3D.draw_points(ax, self.triangle_vertices, colors='red',
                              sizes=150, labels=labels)

        # Nakresli těžiště
        Renderer3D.draw_point(ax, self.center, color='green', size=200, label='T')

        # Nakresli čáry z vrcholů do těžiště
        for v in self.triangle_vertices:
            Renderer3D.draw_edge(ax, v, self.center, color='green', width=2, style='--')

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení trojúhelníku s těžištěm (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěnu trojúhelníku, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)
            color = st.session_state.get('face_color', '#00CED1')
            fig = PlotlyRenderer3D.add_faces(
                fig, self.triangle_vertices, self.triangle_face,
                color=color, opacity=opacity
            )

        # Nakresli hrany trojúhelníku
        edge_width = st.session_state.get('edge_width', 4)
        fig = PlotlyRenderer3D.add_edges(fig, self.triangle_vertices, self.triangle_edges,
                                         color='blue', width=edge_width)

        # Nakresli vrcholy trojúhelníku
        vertex_size = st.session_state.get('vertex_size', 15)
        labels = ['A', 'B', 'C']
        fig = PlotlyRenderer3D.add_points(fig, self.triangle_vertices, colors='red',
                                          sizes=vertex_size, labels=labels)

        # Nakresli těžiště (o něco větší než vrcholy)
        fig = PlotlyRenderer3D.add_point(fig, self.center, color='green',
                                        size=vertex_size * 1.3, label='T')

        # Nakresli čáry z vrcholů do těžiště (tenčí než hrany)
        for v in self.triangle_vertices:
            fig = PlotlyRenderer3D.add_edge(fig, v, self.center, color='green',
                                            width=edge_width * 0.5, dash='dash')

        return fig
