"""
Step 18c: Enhanced proof - Vertical flow diagram showing logical progression
"""
import numpy as np
import plotly.graph_objects as go
import math
import streamlit as st
from steps.base_step import Step, StepMetadata


class BonusStep_WhyFive_18C(Step):
    """Step 18c: Flow diagram visualization"""

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=20,
            category='Bonus',
            title='Důkaz úhlů (vývojový diagram)',
            short_name='Úhly - diagram'
        )

    def get_description(self) -> str:
        return """
## Step 18c: Důkaz pomocí úhlů - Vývojový diagram

**Logický postup krok za krokem:**

Tento diagram ukazuje logickou cestu důkazu:
1. Začneme s definicí Platónského tělesa
2. Odvodíme podmínku úhlů
3. Procházíme pravidelné mnohoúhelníky
4. Pro každý testujeme možné počty ve vrcholu
5. Zjistíme, že existuje pouze 5 validních kombinací

Výsledek je **kompletní a vyčerpávající důkaz**!
"""

    def render_plotly_diagram(self) -> go.Figure:
        """Create vertical flow diagram showing the proof logic"""

        fig = go.Figure()

        # Define flow boxes (y coordinates from top to bottom)
        boxes = [
            # Level 0: Starting point
            {'y': 9.5, 'text': '<b>Start: Co je Platónské těleso?</b><br>Konvexní těleso ze stejných pravidelných mnohoúhelníků', 'color': '#6c757d', 'width': 6},

            # Level 1: Conditions
            {'y': 8.5, 'text': '<b>Podmínka 1:</b> Vrchol = ≥3 stěny', 'color': '#17a2b8', 'width': 3},
            {'y': 8.5, 'text': '<b>Podmínka 2:</b> Součet úhlů < 360°', 'color': '#17a2b8', 'width': 3, 'x_offset': 3},

            # Level 2: Angle formula
            {'y': 7.3, 'text': '<b>Vzorec vnitřního úhlu:</b><br>α = (n-2) × 180° / n<br>(n = počet stran)', 'color': '#ffc107', 'width': 6},

            # Level 3: Polygon examination header
            {'y': 6.3, 'text': '<b>Prozkoumání pravidelných mnohoúhelníků:</b>', 'color': '#6c757d', 'width': 6},

            # Level 4-8: Each polygon type
            # Triangles
            {'y': 5.3, 'text': '△ Trojúhelník: 60°', 'color': '#e7f3ff', 'width': 1.5},
            {'y': 5.3, 'text': '3× = 180° ✅<br>ČTYŘSTĚN', 'color': '#d4edda', 'width': 1.1, 'x_offset': 1.5},
            {'y': 5.3, 'text': '4× = 240° ✅<br>OSMISTĚN', 'color': '#d4edda', 'width': 1.1, 'x_offset': 2.6},
            {'y': 5.3, 'text': '5× = 300° ✅<br>DVACETISTĚN', 'color': '#d4edda', 'width': 1.1, 'x_offset': 3.7},
            {'y': 5.3, 'text': '6× = 360° ❌', 'color': '#f8d7da', 'width': 1.2, 'x_offset': 4.8},

            # Squares
            {'y': 4.3, 'text': '□ Čtverec: 90°', 'color': '#e7f3ff', 'width': 1.5},
            {'y': 4.3, 'text': '3× = 270° ✅<br>KRYCHLE', 'color': '#d4edda', 'width': 1.5, 'x_offset': 1.5},
            {'y': 4.3, 'text': '4× = 360° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 3.0},
            {'y': 4.3, 'text': '5× > 360° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 4.5},

            # Pentagons
            {'y': 3.3, 'text': '⬠ Pětiúhelník: 108°', 'color': '#e7f3ff', 'width': 1.5},
            {'y': 3.3, 'text': '3× = 324° ✅<br>DVANÁCTISTĚN', 'color': '#d4edda', 'width': 1.5, 'x_offset': 1.5},
            {'y': 3.3, 'text': '4× = 432° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 3.0},
            {'y': 3.3, 'text': '5× > 432° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 4.5},

            # Hexagons
            {'y': 2.3, 'text': '⬡ Šestiúhelník: 120°', 'color': '#e7f3ff', 'width': 1.5},
            {'y': 2.3, 'text': '3× = 360° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 1.5},
            {'y': 2.3, 'text': '4× = 480° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 3.0},
            {'y': 2.3, 'text': '5× > 480° ❌', 'color': '#f8d7da', 'width': 1.5, 'x_offset': 4.5},

            # Higher polygons
            {'y': 1.3, 'text': '⬢ Sedmiúhelník+: ≥128.57°', 'color': '#e7f3ff', 'width': 2.0},
            {'y': 1.3, 'text': '3× ≥ 385.7° ❌  Všechny překročeny!', 'color': '#f8d7da', 'width': 4.0, 'x_offset': 2.0},

            # Final conclusion
            {'y': 0.2, 'text': '<b>✅ ZÁVĚR: Pouze 5 Platónských těles!</b><br>Čtyřstěn • Osmistěn • Dvacetistěn • Krychle • Dvanáctistěn', 'color': '#28a745', 'width': 6},
        ]

        # Draw boxes
        for box in boxes:
            x_center = box.get('x_offset', 0) + box['width'] / 2
            fig.add_shape(
                type='rect',
                x0=box.get('x_offset', 0), y0=box['y'] - 0.4,
                x1=box.get('x_offset', 0) + box['width'], y1=box['y'] + 0.4,
                fillcolor=box['color'],
                line=dict(color='black', width=2),
                opacity=0.8
            )
            fig.add_annotation(
                x=x_center, y=box['y'],
                text=box['text'],
                showarrow=False,
                font=dict(size=10, color='white' if box['color'] in ['#6c757d', '#28a745'] else 'black'),
                align='center'
            )

        # Draw arrows connecting boxes
        arrows = [
            # From start to conditions
            {'x0': 3, 'y0': 9.1, 'x1': 1.5, 'y1': 8.9},
            {'x0': 3, 'y0': 9.1, 'x1': 4.5, 'y1': 8.9},
            # From conditions to formula
            {'x0': 1.5, 'y0': 8.1, 'x1': 3, 'y1': 7.7},
            {'x0': 4.5, 'y0': 8.1, 'x1': 3, 'y1': 7.7},
            # From formula to examination
            {'x0': 3, 'y0': 6.9, 'x1': 3, 'y1': 6.7},
            # From examination to polygons
            {'x0': 3, 'y0': 5.9, 'x1': 3, 'y1': 5.7},
            # From polygons to conclusion
            {'x0': 3, 'y0': 0.9, 'x1': 3, 'y1': 0.6},
        ]

        for arrow in arrows:
            fig.add_annotation(
                x=arrow['x1'], y=arrow['y1'],
                ax=arrow['x0'], ay=arrow['y0'],
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='black'
            )

        # Configure layout
        fig.update_xaxes(range=[-0.5, 6.5], showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(range=[-0.5, 10], showgrid=False, showticklabels=False, zeroline=False)

        fig.update_layout(
            title_text="Důkaz: Logický vývojový diagram<br><sub>Krok za krokem od definice k závěru</sub>",
            title_x=0.5,
            height=1200,
            plot_bgcolor='white',
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True)
        )

        return fig
