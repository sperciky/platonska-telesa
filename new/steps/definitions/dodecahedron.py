"""
Kroky pro konstrukci dvanáctistěnu
Dodecahedron construction steps
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D
from config.settings import PHI


class DodecaStep1_Cube(Step):
    """Dvanáctistěn - Krok 1: Krychle (8 vrcholů)"""

    def __init__(self):
        super().__init__()
        # Vrcholy krychle
        self.cube_vertices = np.array([
            [-1, -1, -1], [-1, -1,  1], [-1,  1, -1], [-1,  1,  1],
            [ 1, -1, -1], [ 1, -1,  1], [ 1,  1, -1], [ 1,  1,  1]
        ])
        self.cube_edges = [
            (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
            (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=9,
            category='Dvanáctistěn',
            title='Dvanáctistěn - Krok 1: Krychle (8 vrcholů)',
            short_name='1. Krychle'
        )

    def get_description(self) -> str:
        return """
## Dvanáctistěn - Krok 1: Začneme krychlí

### Krychle má 8 vrcholů:

```
(±1, ±1, ±1)
```

---

### Dvanáctistěn má 20 vrcholů!

To znamená, že potřebujeme přidat **ještě 12 vrcholů** k těmto 8.

---

### Plán:

1. ✅ Začneme s 8 vrcholy krychle
2. ➡️ Přidáme 12 vrcholů (zlatý řez!)
3. ➡️ Spojíme do dvanáctistěnu

---

➡️ **Další krok ukáže, jak získat dalších 12 vrcholů!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení krychle (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        Renderer3D.draw_edges(ax, self.cube_vertices, self.cube_edges,
                             color='orange', width=2)
        labels = [str(i+1) for i in range(8)]
        Renderer3D.draw_points(ax, self.cube_vertices, colors='orange',
                              sizes=120, labels=labels)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení krychle (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)
        fig = PlotlyRenderer3D.add_edges(fig, self.cube_vertices, self.cube_edges,
                                         color='orange', width=3)
        labels = [str(i+1) for i in range(8)]
        fig = PlotlyRenderer3D.add_points(fig, self.cube_vertices, colors='orange',
                                          sizes=12, labels=labels)
        return fig


class DodecaStep2_GoldenRectangles(Step):
    """Dvanáctistěn - Krok 2: Přidání 12 vrcholů pomocí zlatého řezu"""

    def __init__(self):
        super().__init__()
        # Vytvoř všech 20 vrcholů dvanáctistěnu
        dodeca_vertices = []
        # 8 vrcholů krychle (indices 0-7)
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    dodeca_vertices.append([i, j, k])
        # 12 vrcholů ze zlatých obdélníků
        for coords in [
            [0, 1/PHI, PHI], [0, 1/PHI, -PHI], [0, -1/PHI, PHI], [0, -1/PHI, -PHI],  # 8-11: YZ (red)
            [1/PHI, PHI, 0], [1/PHI, -PHI, 0], [-1/PHI, PHI, 0], [-1/PHI, -PHI, 0],  # 12-15: XY (green)
            [PHI, 0, 1/PHI], [PHI, 0, -1/PHI], [-PHI, 0, 1/PHI], [-PHI, 0, -1/PHI]  # 16-19: ZX (blue)
        ]:
            dodeca_vertices.append(coords)
        self.dodeca_vertices = np.array(dodeca_vertices)

        # Hrany krychle (indices 0-7)
        self.cube_edges = [
            (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
            (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
        ]

        # Tři zlaté obdélníky
        self.rectangles = [
            (8, 9, 11, 10),    # YZ plane (červený)
            (12, 13, 15, 14),  # XY plane (zelený)
            (16, 17, 19, 18)   # ZX plane (modrý)
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=10,
            category='Dvanáctistěn',
            title='Dvanáctistěn - Krok 2: Přidání 12 vrcholů',
            short_name='2. Přidání 12 vrcholů'
        )

    def get_description(self) -> str:
        return f"""
## Dvanáctistěn - Krok 2: Zlaté obdélníky

### Princip: Opět zlatý řez!

Podobně jako u dvacetistěnu, použijeme **zlatý řez φ = {PHI:.3f}**

---

### Tři skupiny zlatých obdélníků:

🔴 **ČERVENÝ obdélník (rovina YZ, x=0):** 4 vrcholy
- (0, ±1/φ, ±φ)

🟢 **ZELENÝ obdélník (rovina XY, z=0):** 4 vrcholy
- (±1/φ, ±φ, 0)

🔵 **MODRÝ obdélník (rovina ZX, y=0):** 4 vrcholy
- (±φ, 0, ±1/φ)

🟠 **ORANŽOVÁ krychle:** 8 vrcholů
- (±1, ±1, ±1)

---

### Celkem:

- **Oranžových** vrcholů (krychle): 8
- **Červených** vrcholů: 4
- **Zelených** vrcholů: 4
- **Modrých** vrcholů: 4
- **CELKEM:** 8 + 4 + 4 + 4 = **20 vrcholů** ✓

---

➡️ **Další krok spojí body do hotového dvanáctistěnu!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení všech vrcholů (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany krychle (oranžová)
        Renderer3D.draw_edges(
            ax, self.dodeca_vertices, self.cube_edges,
            color='orange', width=2
        )

        # Nakresli obdélníky
        rect_colors = ['red', 'green', 'blue']
        for rect_idx, color in zip(self.rectangles, rect_colors):
            edges = [
                (rect_idx[0], rect_idx[1]),
                (rect_idx[1], rect_idx[2]),
                (rect_idx[2], rect_idx[3]),
                (rect_idx[3], rect_idx[0])
            ]
            for edge in edges:
                Renderer3D.draw_edge(
                    ax,
                    self.dodeca_vertices[edge[0]],
                    self.dodeca_vertices[edge[1]],
                    color=color, width=2
                )

        # Nakresli vrcholy
        colors_vertices = ['orange']*8 + ['red']*4 + ['green']*4 + ['blue']*4
        for v, color in zip(self.dodeca_vertices, colors_vertices):
            Renderer3D.draw_point(ax, v, color=color, size=100)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení všech vrcholů (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli hrany krychle (oranžová)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.dodeca_vertices, self.cube_edges,
            color='orange', width=3
        )

        # Nakresli obdélníky
        rect_colors = ['red', 'green', 'blue']
        for rect_idx, color in zip(self.rectangles, rect_colors):
            edges = [
                (rect_idx[0], rect_idx[1]),
                (rect_idx[1], rect_idx[2]),
                (rect_idx[2], rect_idx[3]),
                (rect_idx[3], rect_idx[0])
            ]
            for edge in edges:
                fig = PlotlyRenderer3D.add_edge(
                    fig,
                    self.dodeca_vertices[edge[0]],
                    self.dodeca_vertices[edge[1]],
                    color=color, width=3
                )

        # Nakresli vrcholy
        colors_vertices = ['orange']*8 + ['red']*4 + ['green']*4 + ['blue']*4
        for v, color in zip(self.dodeca_vertices, colors_vertices):
            fig = PlotlyRenderer3D.add_point(fig, v, color=color, size=10, show_label=False)
        return fig


class DodecaStep3_Complete(Step):
    """Dvanáctistěn - Krok 3: Hotový dvanáctistěn"""

    def __init__(self):
        super().__init__()
        # Všech 20 vrcholů
        dodeca_vertices = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    dodeca_vertices.append([i, j, k])
        for coords in [
            [0, 1/PHI, PHI], [0, 1/PHI, -PHI], [0, -1/PHI, PHI], [0, -1/PHI, -PHI],
            [1/PHI, PHI, 0], [1/PHI, -PHI, 0], [-1/PHI, PHI, 0], [-1/PHI, -PHI, 0],
            [PHI, 0, 1/PHI], [PHI, 0, -1/PHI], [-PHI, 0, 1/PHI], [-PHI, 0, -1/PHI]
        ]:
            dodeca_vertices.append(coords)
        self.dodeca_vertices = np.array(dodeca_vertices)
        
        # Najdi hrany (body ve vzdálenosti 2/φ)
        sample_edges = []
        for i in range(len(self.dodeca_vertices)):
            for j in range(i+1, len(self.dodeca_vertices)):
                dist = np.linalg.norm(self.dodeca_vertices[i] - self.dodeca_vertices[j])
                if 1.1 < dist < 1.3:
                    sample_edges.append((i, j))
        self.sample_edges = sample_edges[:30]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=11,
            category='Dvanáctistěn',
            title='Dvanáctistěn - Krok 3: Hotový dvanáctistěn',
            short_name='3. Hotový dvanáctistěn'
        )

    def get_description(self) -> str:
        return f"""
## Dvanáctistěn - Krok 3: Hotovo!

### Vlastnosti dvanáctistěnu:

- **20 vrcholů** (8 z krychle + 12 ze zlatých obdélníků)
- **30 hran** (všechny stejně dlouhé)
- **12 pětiúhelníkových stěn** (pravidelné pětiúhelníky)

---

### Délka hrany:

d = 2/φ ≈ {2/PHI:.3f}

---

### Zajímavosti:

1. **Jediné Platónské těleso s pětiúhelníkovými stěnami**
2. **Duální k dvacetistěnu** - středy 12 stěn dvanáctistěnu tvoří vrcholy dvacetistěnu
3. **Má nejvíce stěn ze všech těles kromě dvacetistěnu**
4. **Používá se v matematice** - pro studium symetrie a grup

---

✨ **Gratuluji! Zkonstruoval jsi všechna 5 Platónských těles!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení hotového dvanáctistěnu (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')
        
        Renderer3D.draw_edges(ax, self.dodeca_vertices, self.sample_edges,
                             color='green', width=2)
        
        for i, v in enumerate(self.dodeca_vertices):
            color = 'blue' if i < 8 else 'red'
            Renderer3D.draw_point(ax, v, color=color, size=100)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení hotového dvanáctistěnu (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)
        
        fig = PlotlyRenderer3D.add_edges(fig, self.dodeca_vertices, self.sample_edges,
                                         color='green', width=2)
        
        for i, v in enumerate(self.dodeca_vertices):
            color = 'blue' if i < 8 else 'red'
            fig = PlotlyRenderer3D.add_point(fig, v, color=color, size=10, show_label=False)
        return fig
