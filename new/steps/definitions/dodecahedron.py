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
                             color='blue', width=2)
        labels = [str(i+1) for i in range(8)]
        Renderer3D.draw_points(ax, self.cube_vertices, colors='blue',
                              sizes=120, labels=labels)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení krychle (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)
        fig = PlotlyRenderer3D.add_edges(fig, self.cube_vertices, self.cube_edges,
                                         color='blue', width=3)
        labels = [str(i+1) for i in range(8)]
        fig = PlotlyRenderer3D.add_points(fig, self.cube_vertices, colors='blue',
                                          sizes=12, labels=labels)
        return fig


class DodecaStep2_GoldenRectangles(Step):
    """Dvanáctistěn - Krok 2: Přidání 12 vrcholů pomocí zlatého řezu"""

    def __init__(self):
        super().__init__()
        # Vytvoř všech 20 vrcholů dvanáctistěnu
        dodeca_vertices = []
        # 8 vrcholů krychle
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    dodeca_vertices.append([i, j, k])
        # 12 vrcholů ze zlatých obdélníků
        for coords in [
            [0, 1/PHI, PHI], [0, 1/PHI, -PHI], [0, -1/PHI, PHI], [0, -1/PHI, -PHI],
            [1/PHI, PHI, 0], [1/PHI, -PHI, 0], [-1/PHI, PHI, 0], [-1/PHI, -PHI, 0],
            [PHI, 0, 1/PHI], [PHI, 0, -1/PHI], [-PHI, 0, 1/PHI], [-PHI, 0, -1/PHI]
        ]:
            dodeca_vertices.append(coords)
        self.dodeca_vertices = np.array(dodeca_vertices)

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

### Tři skupiny obdélníků:

🔴 **Rovina YZ (x=0):** 4 vrcholy
- (0, ±1/φ, ±φ)

🟢 **Rovina XZ (y=0):** 4 vrcholy
- (±1/φ, ±φ, 0)

🔵 **Rovina XY (z=0):** 4 vrcholy
- (±φ, 0, ±1/φ)

---

### Celkem:

- **Modrých** vrcholů (krychle): 8
- **Červených** vrcholů (obdélníky): 12
- **CELKEM:** 8 + 12 = **20 vrcholů** ✓

---

➡️ **Další krok spojí body do hotového dvanáctistěnu!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení všech vrcholů (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')
        
        for i, v in enumerate(self.dodeca_vertices):
            color = 'blue' if i < 8 else 'red'
            size = 100 if i < 8 else 120
            Renderer3D.draw_point(ax, v, color=color, size=size)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení všech vrcholů (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)
        
        for i, v in enumerate(self.dodeca_vertices):
            color = 'blue' if i < 8 else 'red'
            size = 10 if i < 8 else 12
            fig = PlotlyRenderer3D.add_point(fig, v, color=color, size=size, show_label=False)
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
