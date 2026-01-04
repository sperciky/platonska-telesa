"""
Bonusový krok - střed trojúhelníku
Bonus step - triangle centroid
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
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

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=12,
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

        # Nakresli trojúhelník
        fig = PlotlyRenderer3D.add_edges(fig, self.triangle_vertices, self.triangle_edges,
                                         color='blue', width=4)

        # Nakresli vrcholy
        labels = ['A', 'B', 'C']
        fig = PlotlyRenderer3D.add_points(fig, self.triangle_vertices, colors='red',
                                          sizes=15, labels=labels)

        # Nakresli těžiště
        fig = PlotlyRenderer3D.add_point(fig, self.center, color='green', size=20, label='T')

        # Nakresli čáry z vrcholů do těžiště
        for v in self.triangle_vertices:
            fig = PlotlyRenderer3D.add_edge(fig, v, self.center, color='green', 
                                            width=2, dash='dash')

        return fig
