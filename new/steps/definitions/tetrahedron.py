"""
Kroky pro konstrukci čtyřstěnu
Tetrahedron construction steps
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D
from config.settings import PHI


class TetraStep1_Cube(Step):
    """Čtyřstěn - Krok 1: Krychle"""

    def __init__(self):
        super().__init__()
        # Vrcholy krychle
        self.cube_vertices = np.array([
            [-1, -1, -1],  # 0
            [-1, -1,  1],  # 1
            [-1,  1, -1],  # 2
            [-1,  1,  1],  # 3
            [ 1, -1, -1],  # 4
            [ 1, -1,  1],  # 5
            [ 1,  1, -1],  # 6
            [ 1,  1,  1]   # 7
        ])

        # Hrany krychle
        self.cube_edges = [
            (0, 1), (0, 2), (0, 4),
            (1, 3), (1, 5),
            (2, 3), (2, 6),
            (3, 7),
            (4, 5), (4, 6),
            (5, 7), (6, 7)
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=1,
            category='Čtyřstěn',
            title='Čtyřstěn - Krok 1: Krychle',
            short_name='1. Krychle'
        )

    def get_description(self) -> str:
        return """
## Čtyřstěn - Krok 1: Začneme krychlí

### Krychle má 8 vrcholů:

Souřadnice všech vrcholů jsou **±1** v každé ose:

```
Vrchol 0: (-1, -1, -1)
Vrchol 1: (-1, -1,  1)
Vrchol 2: (-1,  1, -1)
Vrchol 3: (-1,  1,  1)
Vrchol 4: ( 1, -1, -1)
Vrchol 5: ( 1, -1,  1)
Vrchol 6: ( 1,  1, -1)
Vrchol 7: ( 1,  1,  1)
```

---

### Co budeme dělat:

Z těchto **8 vrcholů** vybereme **4 vrcholy** tak, aby:

1. ✅ Žádné dva vrcholy **nesdílely hranu** krychle
2. ✅ Všechny vzdálenosti mezi vybranými vrcholy byly **stejné**

---

### Proč krychle?

Krychle je skvělý výchozí bod, protože:
- Má jasně definované vrcholy
- Je symetrická
- Lze v ní najít čtyřstěn!

---

➡️ **Pokračuj na další krok a uvidíš, jak vybrat správné vrcholy!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení krychle (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany krychle
        Renderer3D.draw_edges(
            ax, self.cube_vertices, self.cube_edges,
            color='orange', width=2
        )

        # Nakresli vrcholy
        labels = [str(i) for i in range(8)]
        Renderer3D.draw_points(
            ax, self.cube_vertices,
            colors='orange',
            sizes=120,
            labels=labels
        )

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení krychle (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli hrany krychle
        fig = PlotlyRenderer3D.add_edges(
            fig, self.cube_vertices, self.cube_edges,
            color='orange', width=3
        )

        # Nakresli vrcholy
        labels = [str(i) for i in range(8)]
        fig = PlotlyRenderer3D.add_points(
            fig, self.cube_vertices,
            colors='orange',
            sizes=12,
            labels=labels
        )

        return fig


class TetraStep2_Selection(Step):
    """Čtyřstěn - Krok 2: Výběr vrcholů"""

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

        # Vybrané vrcholy pro čtyřstěn
        self.tetra_indices = [7, 4, 2, 1]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=2,
            category='Čtyřstěn',
            title='Čtyřstěn - Krok 2: Výběr vrcholů',
            short_name='2. Výběr vrcholů'
        )

    def get_description(self) -> str:
        return """
## Čtyřstěn - Krok 2: Jak vybrat správné vrcholy?

### Pravidlo: Součin souřadnic = 1

Vybereme vrcholy, jejichž souřadnice mají **součin = 1**:

```
Vrchol 7: ( 1,  1,  1) → 1 × 1 × 1 = 1 ✓
Vrchol 4: ( 1, -1, -1) → 1 × (-1) × (-1) = 1 ✓
Vrchol 2: (-1,  1, -1) → (-1) × 1 × (-1) = 1 ✓
Vrchol 1: (-1, -1,  1) → (-1) × (-1) × 1 = 1 ✓
```

---

### Proč zrovna tyto?

**Důležitá vlastnost:**
- Žádné dva vybrané vrcholy **nesdílejí hranu** krychle!
- Jsou **maximálně vzdálené** od sebe
- Tvoří dokonalou symetrii

---

### Kontrola:

Zkus se podívat na diagram vlevo a ověř si, že:
1. Červené body (7, 4, 2, 1) nejsou přímo spojené hranou krychle
2. Šedé body jsou ostatní vrcholy krychle

---

➡️ **Další krok ukáže hotový čtyřstěn!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení krychle s označenými vrcholy (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany krychle
        Renderer3D.draw_edges(
            ax, self.cube_vertices, self.cube_edges,
            color='lightgray', width=1, style='--', alpha=0.3
        )

        # Nakresli vrcholy - vybrané červeně, ostatní šedě
        for i, v in enumerate(self.cube_vertices):
            if i in self.tetra_indices:
                Renderer3D.draw_point(ax, v, color='red', size=150, label=str(i))
            else:
                Renderer3D.draw_point(ax, v, color='lightgray', size=60, label=str(i))

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení krychle s označenými vrcholy (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli hrany krychle
        fig = PlotlyRenderer3D.add_edges(
            fig, self.cube_vertices, self.cube_edges,
            color='lightgray', width=2, dash='dash'
        )

        # Nakresli vrcholy - vybrané červeně, ostatní šedě
        for i, v in enumerate(self.cube_vertices):
            if i in self.tetra_indices:
                fig = PlotlyRenderer3D.add_point(fig, v, color='red', size=15, label=str(i))
            else:
                fig = PlotlyRenderer3D.add_point(fig, v, color='lightgray', size=6, label=str(i))

        return fig


class TetraStep3_Complete(Step):
    """Čtyřstěn - Krok 3: Hotový čtyřstěn"""

    def __init__(self):
        super().__init__()
        # Vrcholy čtyřstěnu
        self.tetra_vertices = np.array([
            [ 1,  1,  1],  # Vrchol 7
            [ 1, -1, -1],  # Vrchol 4
            [-1,  1, -1],  # Vrchol 2
            [-1, -1,  1]   # Vrchol 1
        ])

        # Hrany čtyřstěnu (všechny možné dvojice)
        self.tetra_edges = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3), (2, 3)
        ]

        # Stěny čtyřstěnu (4 trojúhelníky)
        self.tetra_faces = [
            [0, 1, 2],  # Stěna ABC
            [0, 1, 3],  # Stěna ABD
            [0, 2, 3],  # Stěna ACD
            [1, 2, 3]   # Stěna BCD
        ]

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=3,
            category='Čtyřstěn',
            title='Čtyřstěn - Krok 3: Hotovo!',
            short_name='3. Hotový čtyřstěn'
        )

    def get_description(self) -> str:
        edge_length = np.linalg.norm(self.tetra_vertices[0] - self.tetra_vertices[1])

        return f"""
## Čtyřstěn - Krok 3: Hotový čtyřstěn!

### Vlastnosti čtyřstěnu:

- **4 vrcholy** (A, B, C, D)
- **6 hran** (každý vrchol spojen s každým)
- **4 trojúhelníkové stěny** (rovnostranné trojúhelníky)

---

### Výpočet délky hrany:

Vezměme například hranu AB:

```
A = (1, 1, 1)
B = (1, -1, -1)

d = √[(1-1)² + (1-(-1))² + (1-(-1))²]
d = √[0 + 4 + 4]
d = √8 = 2√2 ≈ {edge_length:.3f}
```

---

### Ověření pravidelnosti:

✅ **Všechny hrany mají stejnou délku!**

Můžeš si ověřit, že vzdálenost mezi **jakýmikoliv dvěma** vrcholy je vždy **2√2**.

---

### Zajímavost:

Čtyřstěn je:
- **Nejjednodušší** Platónské těleso
- Má **nejméně** vrcholů, hran i stěn
- Každá stěna je **rovnostranný trojúhelník**

---

✨ **Gratuluji! Právě jsi zkonstruoval čtyřstěn!**

➡️ Pokračuj dalším tělesem - Osmistěnem!
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení hotového čtyřstěnu (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli hrany čtyřstěnu
        Renderer3D.draw_edges(
            ax, self.tetra_vertices, self.tetra_edges,
            color='blue', width=3, alpha=0.8
        )

        # Nakresli vrcholy
        labels = ['A', 'B', 'C', 'D']
        Renderer3D.draw_points(
            ax, self.tetra_vertices,
            colors='red',
            sizes=150,
            labels=labels
        )

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení hotového čtyřstěnu (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Nakresli stěny, pokud je to zapnuté
        if st.session_state.get('show_faces', False):
            opacity = st.session_state.get('face_opacity', 0.5)
            color = st.session_state.get('face_color', '#00CED1')
            fig = PlotlyRenderer3D.add_faces(
                fig, self.tetra_vertices, self.tetra_faces,
                color=color, opacity=opacity
            )

        # Nakresli hrany čtyřstěnu
        edge_width = st.session_state.get('edge_width', 4)
        fig = PlotlyRenderer3D.add_edges(
            fig, self.tetra_vertices, self.tetra_edges,
            color='blue', width=edge_width
        )

        # Nakresli vrcholy
        vertex_size = st.session_state.get('vertex_size', 15)
        labels = ['A', 'B', 'C', 'D']
        fig = PlotlyRenderer3D.add_points(
            fig, self.tetra_vertices,
            colors='red',
            sizes=vertex_size,
            labels=labels
        )

        return fig
