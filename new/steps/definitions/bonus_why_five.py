"""
Bonusový krok - proč existuje pouze 5 Platónských těles
Bonus step - proof of why only 5 Platonic solids exist
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D


class BonusStep_WhyOnlyFive(Step):
    """Bonus: Proč existuje pouze 5 Platónských těles?"""

    def __init__(self):
        super().__init__()
        # Pro vizualizaci úhlů
        pass

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=17,
            category='Bonus',
            title='Bonus: Proč jich není více?',
            short_name='Proč jen 5?'
        )

    def get_description(self) -> str:
        return """
## Bonus: Proč existuje pouze 5 Platónských těles?

### Definice Platónských těles:

Platónské těleso musí splňovat:

1. **Těleso tvoří pravidelné mnohoúhelníky** (všechny strany a úhly stejné)
2. **Z každého vrcholu vychází stejný počet hran**
3. **V každém bodě se potkávají alespoň 3 stěny**
4. **Výsledné těleso musí být konvexní** → součet úhlů u vrcholu **< 360°**

---

### Důkaz: Proč jen 5 těles?

Díky těmto podmínkám můžeme pracovat pouze s **jedním bodem**.

---

### 1️⃣ Nejmenší mnohoúhelník: **Trojúhelník** (vnitřní úhel 60°)

Kolik trojúhelníků se může potkat v jednom vrcholu?

🔺 **3 trojúhelníky:** 3 × 60° = **180°** < 360° ✅ → **ČTYŘSTĚN** (tetraedr)

🔺 **4 trojúhelníky:** 4 × 60° = **240°** < 360° ✅ → **OSMISTĚN** (oktaedr)

🔺 **5 trojúhelníků:** 5 × 60° = **300°** < 360° ✅ → **DVACETISTĚN** (ikosaedr)

🔺 **6 trojúhelníků:** 6 × 60° = **360°** ❌ → rovinné, není konvexní

---

### 2️⃣ Následuje čtverec: **Čtverec** (vnitřní úhel 90°)

Kolik čtverců se může potkat v jednom vrcholu?

🟦 **3 čtverce:** 3 × 90° = **270°** < 360° ✅ → **KRYCHLE** (hexaedr)

🟦 **4 čtverce:** 4 × 90° = **360°** ❌ → rovinné, není konvexní

---

### 3️⃣ Další je pětiúhelník: **Pětiúhelník** (vnitřní úhel 108°)

Kolik pětiúhelníků se může potkat v jednom vrcholu?

🟫 **3 pětiúhelníky:** 3 × 108° = **324°** < 360° ✅ → **DVANÁCTISTĚN** (dodekaedr)

🟫 **4 pětiúhelníky:** 4 × 108° = **432°** > 360° ❌ → překročen limit!

---

### 4️⃣ Šestiúhelník a více: **Šestiúhelník** (vnitřní úhel 120°)

⬡ **3 šestiúhelníky:** 3 × 120° = **360°** ❌ → rovinné, není konvexní

Všechny další mnohoúhelníky (sedmiúhelník, osmiúhelník...) mají **větší úhel než 120°**,
takže by **přesáhly limit**, protože by pokračoval **šestiúhelník**, který má vnitřní úhel 120°.

A tři (120° krát 3 je 360°) by **leželi na rovině** a těleso by se z nich **nestát nemohlo**.

---

### ✨ Závěr: Pouze 5 Platónských těles!

| Těleso | Stěny | Vrcholy v jednom bodě | Součet úhlů |
|--------|-------|----------------------|-------------|
| Čtyřstěn | 3 trojúhelníky | 3 × 60° | 180° ✅ |
| Osmistěn | 4 trojúhelníky | 4 × 60° | 240° ✅ |
| Dvacetistěn | 5 trojúhelníků | 5 × 60° | 300° ✅ |
| Krychle | 3 čtverce | 3 × 90° | 270° ✅ |
| Dvanáctistěn | 3 pětiúhelníky | 3 × 108° | 324° ✅ |

**Více už jich být nemůže**, protože by **přesáhly limit 360°** nebo by **pokračoval šestiúhelník**,
který má vnitřní úhel 120° a tři (120° krát 3 je 360°) by **leželi na rovině**
a těleso by se z nich **nestát nemohlo**.

---

### 🎓 Matematická krása:

Toto je **úplný důkaz**! Nemusíme zkoušet všechny možnosti -
**matematika nám zaručuje**, že jiná Platónská tělesa **nemohou existovat**.

Proto staří Řekové považovali těchto 5 těles za **dokonalá** a **posvátná**!
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení vizualizace úhlů (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Simple text display
        ax.text(0, 0.5, 'Viz popis vpravo →',
                fontsize=20, ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('off')

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení vizualizace důkazu (Plotly - interaktivní)"""
        from plotly.subplots import make_subplots
        import math

        # Helper function to create polygon vertices around a central point
        def polygon_vertices(n_sides, angle_deg, radius=1.0, rotation_offset=0):
            """Generate vertices for a regular polygon"""
            vertices = []
            angle_rad = math.radians(angle_deg)
            for i in range(n_sides):
                angle = rotation_offset + i * angle_rad
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                vertices.append((x, y))
            vertices.append(vertices[0])  # Close the polygon
            return vertices

        def draw_polygons_at_vertex(fig, row, col, n_polygons, n_sides, color, title, total_angle):
            """Draw n_polygons regular polygons meeting at a vertex"""
            angle_per_polygon = 360.0 / n_sides  # Internal angle of regular polygon
            internal_angle = (n_sides - 2) * 180.0 / n_sides

            # Calculate the angle to rotate each polygon
            rotation_step = 2 * math.pi / n_polygons

            for i in range(n_polygons):
                rotation = i * rotation_step
                vertices = polygon_vertices(n_sides, 360/n_sides, radius=1.5, rotation_offset=rotation)

                xs = [v[0] for v in vertices]
                ys = [v[1] for v in vertices]

                # Fill color based on validity
                fillcolor = color if total_angle < 360 else 'lightcoral' if total_angle == 360 else 'red'

                fig.add_trace(go.Scatter(
                    x=xs, y=ys,
                    mode='lines',
                    fill='toself',
                    fillcolor=fillcolor,
                    opacity=0.3,
                    line=dict(color='darkgreen' if total_angle < 360 else 'darkred', width=2),
                    showlegend=False,
                    hoverinfo='text',
                    hovertext=f'{n_polygons} × {internal_angle:.0f}° = {total_angle:.0f}°'
                ), row=row, col=col)

            # Add central point
            fig.add_trace(go.Scatter(
                x=[0], y=[0],
                mode='markers',
                marker=dict(size=8, color='black'),
                showlegend=False,
                hoverinfo='skip'
            ), row=row, col=col)

            # Add title and angle sum
            status = '✅' if total_angle < 360 else '❌'
            fig.add_annotation(
                text=f'{title}<br>{total_angle:.0f}° {status}',
                x=0, y=-2.5,
                xref=f'x{col if row==1 else col+4}', yref=f'y{col if row==1 else col+4}',
                showarrow=False,
                font=dict(size=12, color='green' if total_angle < 360 else 'red')
            )

        # Create subplots
        fig = make_subplots(
            rows=3, cols=4,
            subplot_titles=('', '', '', '', '', '', '', '', '', '', '', ''),
            vertical_spacing=0.12,
            horizontal_spacing=0.08,
            specs=[[{'type': 'scatter'}] * 4 for _ in range(3)]
        )

        # Row 1: Triangles (60° each)
        draw_polygons_at_vertex(fig, 1, 1, 3, 3, 'lightgreen', '3 trojúhelníky', 180)
        draw_polygons_at_vertex(fig, 1, 2, 4, 3, 'lightgreen', '4 trojúhelníky', 240)
        draw_polygons_at_vertex(fig, 1, 3, 5, 3, 'lightgreen', '5 trojúhelníků', 300)
        draw_polygons_at_vertex(fig, 1, 4, 6, 3, 'lightcoral', '6 trojúhelníků', 360)

        # Row 2: Squares (90° each)
        draw_polygons_at_vertex(fig, 2, 1, 3, 4, 'lightblue', '3 čtverce', 270)
        draw_polygons_at_vertex(fig, 2, 2, 4, 4, 'lightcoral', '4 čtverce', 360)

        # Row 2: Pentagons (108° each)
        draw_polygons_at_vertex(fig, 2, 3, 3, 5, 'lightyellow', '3 pětiúhelníky', 324)
        draw_polygons_at_vertex(fig, 2, 4, 4, 5, 'red', '4 pětiúhelníky', 432)

        # Row 3: Hexagons (120° each)
        draw_polygons_at_vertex(fig, 3, 1, 3, 6, 'lightcoral', '3 šestiúhelníky', 360)

        # Add text explanations in remaining cells
        fig.add_annotation(
            text='<b>ČTYŘSTĚN</b><br>tetraedr',
            x=0, y=0, xref='x2', yref='y2',
            showarrow=False, font=dict(size=10, color='darkgreen')
        )
        fig.add_annotation(
            text='<b>OSMISTĚN</b><br>oktaedr',
            x=0, y=0, xref='x3', yref='y3',
            showarrow=False, font=dict(size=10, color='darkgreen')
        )
        fig.add_annotation(
            text='<b>DVACETISTĚN</b><br>ikosaedr',
            x=0, y=0, xref='x4', yref='y4',
            showarrow=False, font=dict(size=10, color='darkgreen')
        )

        fig.add_annotation(
            text='<b>KRYCHLE</b><br>hexaedr',
            x=0, y=0, xref='x5', yref='y5',
            showarrow=False, font=dict(size=10, color='darkgreen')
        )

        fig.add_annotation(
            text='<b>DVANÁCTISTĚN</b><br>dodekaedr',
            x=0, y=0, xref='x7', yref='y7',
            showarrow=False, font=dict(size=10, color='darkgreen')
        )

        # Update all axes
        for i in range(1, 13):
            fig.update_xaxes(
                showgrid=False, showticklabels=False, zeroline=False,
                range=[-3, 3], row=(i-1)//4 + 1, col=(i-1)%4 + 1
            )
            fig.update_yaxes(
                showgrid=False, showticklabels=False, zeroline=False,
                range=[-3, 3], scaleanchor=f'x{i}', scaleratio=1,
                row=(i-1)//4 + 1, col=(i-1)%4 + 1
            )

        fig.update_layout(
            title_text="Proč existuje pouze 5 Platónských těles?<br><sub>Součet úhlů u vrcholu musí být < 360°</sub>",
            title_x=0.5,
            height=900,
            showlegend=False,
            plot_bgcolor='white'
        )

        return fig
