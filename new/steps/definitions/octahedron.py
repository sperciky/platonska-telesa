"""
Kroky pro konstrukci osmistěnu
Octahedron construction steps
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D


class OctaStep1_Axes(Step):
    """Osmistěn - Krok 1: Vrcholy na osách"""

    def __init__(self):
        super().__init__()
        # Vrcholy osmistěnu na osách
        self.octa_vertices = np.array([
            [ 1,  0,  0],  # +X
            [-1,  0,  0],  # -X
            [ 0,  1,  0],  # +Y
            [ 0, -1,  0],  # -Y
            [ 0,  0,  1],  # +Z
            [ 0,  0, -1]   # -Z
        ])

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=4,
            category='Osmistěn',
            title='Osmistěn - Krok 1: Vrcholy na osách',
            short_name='1. Vrcholy na osách'
        )

    def get_description(self) -> str:
        return """
## Osmistěn - Krok 1: Vrcholy na osách souřadnic

### 6 vrcholů umístěných symetricky:

```
( 1,  0,  0) → +X (červený)
(-1,  0,  0) → -X (červený)
( 0,  1,  0) → +Y (zelený)
( 0, -1,  0) → -Y (zelený)
( 0,  0,  1) → +Z (modrý)
( 0,  0, -1) → -Z (modrý)
```

---

### Proč zrovna na osách?

Osmistěn má **dokonalou symetrii**:
- Každý vrchol leží na jedné z os souřadného systému
- Vzdálenost od počátku je vždy **1**
- Vrcholy tvoří **3 páry protilehlých bodů**

---

### Konstrukce:

1. ✅ Umísti bod na **+X** osu: (1, 0, 0)
2. ✅ Umísti bod na **-X** osu: (-1, 0, 0)
3. ✅ To samé pro osy Y a Z

---

➡️ **Další krok ukáže, jak tyto body spojit do osmistěnu!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení vrcholů na osách (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli osy
        ax.plot([-2, 2], [0, 0], [0, 0], 'r-', linewidth=2, alpha=0.3)
        ax.plot([0, 0], [-2, 2], [0, 0], 'g-', linewidth=2, alpha=0.3)
        ax.plot([0, 0], [0, 0], [-2, 2], 'b-', linewidth=2, alpha=0.3)

        # Nakresli vrcholy
        labels = ['+X', '-X', '+Y', '-Y', '+Z', '-Z']
        colors = ['red', 'red', 'green', 'green', 'blue', 'blue']

        for v, label, color in zip(self.octa_vertices, labels, colors):
            Renderer3D.draw_point(ax, v, color=color, size=150, label=label)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení vrcholů na osách (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli barevné osy
        fig = PlotlyRenderer3D.add_axes_arrows(fig, length=1.5)

        # Nakresli vrcholy
        labels = ['+X', '-X', '+Y', '-Y', '+Z', '-Z']
        colors = ['red', 'red', 'green', 'green', 'blue', 'blue']

        for v, label, color in zip(self.octa_vertices, labels, colors):
            fig = PlotlyRenderer3D.add_point(fig, v, color=color, size=15, label=label)

        return fig


class OctaStep2_Complete(Step):
    """Osmistěn - Krok 2: Hotový osmistěn"""

    def __init__(self):
        super().__init__()
        # Vrcholy osmistěnu
        self.octa_vertices = np.array([
            [ 1,  0,  0], [-1,  0,  0], [ 0,  1,  0],
            [ 0, -1,  0], [ 0,  0,  1], [ 0,  0, -1]
        ])

        # Stěny osmistěnu (trojúhelníky)
        self.octa_faces = [
            (0, 2, 4), (0, 4, 3), (0, 3, 5), (0, 5, 2),
            (1, 4, 2), (1, 3, 4), (1, 5, 3), (1, 2, 5)
        ]

        # Hrany (vypočítáme ze stěn)
        self.octa_edges = set()
        for face in self.octa_faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i+1)%3]]))
                self.octa_edges.add(edge)
        self.octa_edges = list(self.octa_edges)

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=5,
            category='Osmistěn',
            title='Osmistěn - Krok 2: Hotový osmistěn',
            short_name='2. Hotový osmistěn'
        )

    def get_description(self) -> str:
        edge_length = np.linalg.norm(self.octa_vertices[0] - self.octa_vertices[2])

        return f"""
## Osmistěn - Krok 2: Hotový osmistěn!

### Vlastnosti osmistěnu:

- **6 vrcholů** (na osách souřadného systému)
- **12 hran** (všechny stejně dlouhé)
- **8 trojúhelníkových stěn** (rovnostranné trojúhelníky)

---

### Výpočet délky hrany:

Vezměme hranu mezi vrcholy na osách +X a +Y:

```
+X = (1, 0, 0)
+Y = (0, 1, 0)

d = √[(1-0)² + (0-1)² + (0-0)²]
d = √[1 + 1 + 0]
d = √2 ≈ {edge_length:.3f}
```

---

### Ověření pravidelnosti:

✅ **Všechny hrany mají délku √2**

Každá hrana spojuje dva sousední vrcholy na různých osách.

---

### Zajímavost:

Osmistěn je **duální** k hranu! To znamená:
- Středy stěn osmistěnu tvoří vrcholy hrany
- Středy stěn hrany tvoří vrcholy osmistěnu
- Mají opačný poměr vrcholů a stěn

---

✨ **Gratuluji! Právě jsi zkonstruoval osmistěn!**

➡️ Pokračuj dalším tělesem - Dvacetistěnem!
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení hotového osmistěnu (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany
        Renderer3D.draw_edges(
            ax, self.octa_vertices, self.octa_edges,
            color='blue', width=2
        )

        # Nakresli vrcholy
        labels = [str(i+1) for i in range(6)]
        Renderer3D.draw_points(
            ax, self.octa_vertices,
            colors='red',
            sizes=150,
            labels=labels
        )

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení hotového osmistěnu (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli hrany
        fig = PlotlyRenderer3D.add_edges(
            fig, self.octa_vertices, self.octa_edges,
            color='blue', width=4
        )

        # Nakresli vrcholy
        labels = [str(i+1) for i in range(6)]
        fig = PlotlyRenderer3D.add_points(
            fig, self.octa_vertices,
            colors='red',
            sizes=15,
            labels=labels
        )

        return fig
