"""
Kroky pro konstrukci dvacetistěnu
Icosahedron construction steps
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D
from config.settings import PHI


class IcosaStep1_Rectangle(Step):
    """Dvacetistěn - Krok 1: Obdélník se zlatým řezem"""

    def __init__(self):
        super().__init__()
        # Vrcholy dvacetistěnu
        self.icosa_vertices = np.array([
            [ 0,  1,  PHI], [ 0,  1, -PHI], [ 0, -1,  PHI], [ 0, -1, -PHI],
            [ 1,  PHI,  0], [ 1, -PHI,  0], [-1,  PHI,  0], [-1, -PHI,  0],
            [ PHI,  0,  1], [ PHI,  0, -1], [-PHI,  0,  1], [-PHI,  0, -1]
        ])
        # První obdélník (v rovině YZ)
        self.rect1 = self.icosa_vertices[:4]
        self.rect_edges = [(0,1), (1,3), (3,2), (2,0)]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=6,
            category='Dvacetistěn',
            title='Dvacetistěn - Krok 1: Obdélník se zlatým řezem',
            short_name='1. Obdélník se zlatým řezem'
        )

    def get_description(self) -> str:
        return f"""
## Dvacetistěn - Krok 1: Zlatý řez

### Co je zlatý řez?

**Zlatý řez** (φ) je speciální poměr: **φ ≈ {PHI:.3f}**

```
φ = (1 + √5) / 2 = 1.618...
```

---

### První obdélník v rovině YZ:

Obdélník má vrcholy v rovině **x = 0**:

```
Vrchol 1: (0,  1,  φ)
Vrchol 2: (0,  1, -φ)
Vrchol 3: (0, -1, -φ)
Vrchol 4: (0, -1,  φ)
```

---

### Rozměry obdélníku:

- **Kratší strana:** 2 (od -1 do +1 na ose Y)
- **Delší strana:** 2φ ≈ {2*PHI:.3f} (od -φ do +φ na ose Z)
- **Poměr:** 2φ / 2 = **φ** (zlatý řez!)

---

### Proč zlatý řez?

Zlatý řez má speciální vlastnost:
- φ² = φ + 1
- 1/φ = φ - 1

Díky těmto vlastnostem můžeme zkonstruovat dokonale pravidelný dvacetistěn!

---

➡️ **Další krok ukáže dva další obdélníky!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení prvního obdélníku (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli rovinu YZ
        y_plane = [-2, 2, 2, -2, -2]
        z_plane = [-2, -2, 2, 2, -2]
        x_plane = [0, 0, 0, 0, 0]
        ax.plot(x_plane, y_plane, z_plane, 'r--', alpha=0.2, linewidth=1)

        # Nakresli hrany obdélníku
        Renderer3D.draw_edges(
            ax, self.rect1, self.rect_edges,
            color='red', width=3
        )

        # Nakresli vrcholy
        labels = [str(i+1) for i in range(4)]
        Renderer3D.draw_points(
            ax, self.rect1,
            colors='red',
            sizes=150,
            labels=labels
        )

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení prvního obdélníku (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli hrany obdélníku
        fig = PlotlyRenderer3D.add_edges(
            fig, self.rect1, self.rect_edges,
            color='red', width=4
        )

        # Nakresli vrcholy
        labels = [str(i+1) for i in range(4)]
        fig = PlotlyRenderer3D.add_points(
            fig, self.rect1,
            colors='red',
            sizes=15,
            labels=labels
        )

        return fig


class IcosaStep2_ThreeRectangles(Step):
    """Dvacetistěn - Krok 2: Tři kolmé obdélníky"""

    def __init__(self):
        super().__init__()
        # Všechny vrcholy dvacetistěnu
        self.icosa_vertices = np.array([
            [ 0,  1,  PHI], [ 0,  1, -PHI], [ 0, -1,  PHI], [ 0, -1, -PHI],
            [ 1,  PHI,  0], [ 1, -PHI,  0], [-1,  PHI,  0], [-1, -PHI,  0],
            [ PHI,  0,  1], [ PHI,  0, -1], [-PHI,  0,  1], [-PHI,  0, -1]
        ])

        # Tři obdélníky
        self.rectangles = [
            (0, 1, 3, 2),    # YZ plane (červený)
            (4, 5, 7, 6),    # XZ plane (zelený)
            (8, 9, 11, 10)   # XY plane (modrý)
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=7,
            category='Dvacetistěn',
            title='Dvacetistěn - Krok 2: Tři kolmé obdélníky',
            short_name='2. Tři kolmé obdélníky'
        )

    def get_description(self) -> str:
        return f"""
## Dvacetistěn - Krok 2: Tři obdélníky

### Konstrukce pomocí zlatého řezu:

Vytvoříme **3 obdélníky** se zlatým řezem, **kolmé na sebe**:

---

### 🔴 ČERVENÝ obdélník (rovina YZ):
- **x = 0** (kolmý na osu X)
- Vrcholy: **(0, ±1, ±φ)**
- 4 vrcholy

### 🟢 ZELENÝ obdélník (rovina XZ):
- **y = 0** (kolmý na osu Y)
- Vrcholy: **(±1, ±φ, 0)**
- 4 vrcholy

### 🔵 MODRÝ obdélník (rovina XY):
- **z = 0** (kolmý na osu Z)
- Vrcholy: **(±φ, 0, ±1)**
- 4 vrcholy

---

### Rozměry každého obdélníku:

- **Kratší strana:** 2
- **Delší strana:** 2φ ≈ {2*PHI:.3f}
- **Poměr:** φ (zlatý řez!)

---

### Celkem vrcholů:

4 + 4 + 4 = **12 vrcholů dvacetistěnu** ✓

---

➡️ **Další krok spojí tyto vrcholy do hotového dvacetistěnu!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení tří obdélníků (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        colors_rect = ['red']*4 + ['green']*4 + ['blue']*4
        rect_colors = ['red', 'green', 'blue']

        # Nakresli obdélníky
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
                    self.icosa_vertices[edge[0]],
                    self.icosa_vertices[edge[1]],
                    color=color, width=2
                )

        # Nakresli vrcholy
        for v, color in zip(self.icosa_vertices, colors_rect):
            Renderer3D.draw_point(ax, v, color=color, size=100)

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení tří obdélníků (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        colors_rect = ['red']*4 + ['green']*4 + ['blue']*4
        rect_colors = ['red', 'green', 'blue']

        # Nakresli stěny obdélníků, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)

            for rect_idx, color in zip(self.rectangles, rect_colors):
                # Čtyřúhelník - použij indexy přímo
                face = [rect_idx[0], rect_idx[1], rect_idx[2], rect_idx[3]]
                fig = PlotlyRenderer3D.add_face(
                    fig, self.icosa_vertices, face,
                    color=color, opacity=opacity
                )

        # Nakresli hrany obdélníků
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
                    self.icosa_vertices[edge[0]],
                    self.icosa_vertices[edge[1]],
                    color=color, width=3
                )

        # Nakresli vrcholy
        for v, color in zip(self.icosa_vertices, colors_rect):
            fig = PlotlyRenderer3D.add_point(fig, v, color=color, size=10, show_label=False)

        return fig


class IcosaStep3_Complete(Step):
    """Dvacetistěn - Krok 3: Hotový dvacetistěn"""

    def __init__(self):
        super().__init__()
        # Vrcholy dvacetistěnu
        self.icosa_vertices = np.array([
            [ 0,  1,  PHI], [ 0,  1, -PHI], [ 0, -1,  PHI], [ 0, -1, -PHI],
            [ 1,  PHI,  0], [ 1, -PHI,  0], [-1,  PHI,  0], [-1, -PHI,  0],
            [ PHI,  0,  1], [ PHI,  0, -1], [-PHI,  0,  1], [-PHI,  0, -1]
        ])

        # Stěny dvacetistěnu (20 trojúhelníků)
        self.icosa_faces = [
            [0, 8, 4], [0, 4, 6], [0, 6, 10], [0, 10, 2], [0, 2, 8],
            [8, 2, 5], [2, 10, 7], [10, 6, 11], [6, 4, 1], [4, 8, 9],
            [5, 2, 7], [7, 10, 11], [11, 6, 1], [1, 4, 9], [9, 8, 5],
            [3, 5, 7], [3, 7, 11], [3, 11, 1], [3, 1, 9], [3, 9, 5]
        ]

        # Hrany (vypočítáme ze stěn)
        edges_set = set()
        for face in self.icosa_faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i+1)%3]]))
                edges_set.add(edge)
        self.icosa_edges = list(edges_set)

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=8,
            category='Dvacetistěn',
            title='Dvacetistěn - Krok 3: Hotový dvacetistěn',
            short_name='3. Hotový dvacetistěn'
        )

    def get_description(self) -> str:
        return """
## Dvacetistěn - Krok 3: Hotový dvacetistěn!

### Vlastnosti dvacetistěnu:

- **12 vrcholů** (ze tří zlatých obdélníků)
- **30 hran** (všechny stejně dlouhé)
- **20 trojúhelníkových stěn** (rovnostranné trojúhelníky)

---

### Délka hrany:

Díky zlatému řezu všechny hrany mají délku **2**!

Toto není náhoda - je to důsledek speciálních vlastností zlatého řezu:
- φ² = φ + 1
- Vrcholy jsou navrženy tak, aby vzdálenosti byly celá čísla

---

### Zajímavosti:

1. **Největší Platónské těleso** (nejvíce vrcholů, hran i stěn)
2. **Velmi blízké kouli** - nejlepší aproximace koule z Platónských těles
3. **20 trojúhelníkových stěn** - každá je rovnostranný trojúhelník
4. **Používá se v biologii** - některé viry mají tvar dvacetistěnu!
5. **Duální k dvanáctistěnu** - středy stěn jednoho tvoří vrcholy druhého

---

✨ **Gratuluji! Právě jsi zkonstruoval dvacetistěn!**

➡️ Pokračuj posledním Platónským tělesem - Dvanáctistěnem!
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení hotového dvacetistěnu (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany
        Renderer3D.draw_edges(
            ax, self.icosa_vertices, self.icosa_edges,
            color='blue', width=2
        )

        # Nakresli vrcholy
        labels = [chr(65+i) for i in range(12)]  # A-L
        Renderer3D.draw_points(
            ax, self.icosa_vertices,
            colors='red',
            sizes=120,
            labels=labels
        )

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení hotového dvacetistěnu (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěny, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)
            color = st.session_state.get('face_color', '#00CED1')
            fig = PlotlyRenderer3D.add_faces(
                fig, self.icosa_vertices, self.icosa_faces,
                color=color, opacity=opacity
            )

        # Nakresli hrany
        edge_width = st.session_state.get('edge_width', 3)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.icosa_vertices, self.icosa_edges,
            color='blue', width=edge_width
        )

        # Nakresli vrcholy
        vertex_size = st.session_state.get('vertex_size', 12)
        labels = [chr(65+i) for i in range(12)]  # A-L
        fig = PlotlyRenderer3D.add_points(
            fig, self.icosa_vertices,
            colors='red',
            sizes=vertex_size,
            labels=labels
        )

        return fig
