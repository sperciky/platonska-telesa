"""
Step 18b: Enhanced proof - Interactive table with visual indicators
"""
import numpy as np
import plotly.graph_objects as go
import math
import streamlit as st
from steps.base_step import Step, StepMetadata


class BonusStep_WhyFive_18B(Step):
    """Step 18b: Table-based visualization with angle calculations"""

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=18,
            category='Bonus',
            title='18b: Důkaz úhlů (tabulka)',
            short_name='Úhly - tabulka'
        )

    def get_description(self) -> str:
        return """
## Step 18b: Důkaz pomocí úhlů - Tabulková vizualizace

**Systematický přístup:** Prozkoumáme všechny možnosti kombinací.

Pro každý pravidelný mnohoúhelník zjistíme:
1. **Vnitřní úhel** = (n-2) × 180° / n
2. **Počet ve vrcholu** (minimálně 3)
3. **Součet úhlů** = počet × vnitřní úhel
4. **Validita:** < 360° = ✅ | = 360° = ❌ (rovina) | > 360° = ❌ (nelze)

Výsledek: **Pouze 5 validních kombinací = 5 Platónských těles!**
"""

    def render_plotly_diagram(self) -> go.Figure:
        """Create comprehensive table showing all polygon-count combinations"""

        # Define data for the table
        data = [
            # Polygon | Internal angle | Count | Sum | Status | Platonic solid
            ['△ Trojúhelník', '60°', '3', '180°', '✅', '<b>ČTYŘSTĚN</b> (tetraedr)'],
            ['△ Trojúhelník', '60°', '4', '240°', '✅', '<b>OSMISTĚN</b> (oktaedr)'],
            ['△ Trojúhelník', '60°', '5', '300°', '✅', '<b>DVACETISTĚN</b> (ikosaedr)'],
            ['△ Trojúhelník', '60°', '6', '360°', '❌', 'Rovina (nelze)'],
            ['', '', '', '', '', ''],
            ['□ Čtverec', '90°', '3', '270°', '✅', '<b>KRYCHLE</b> (hexaedr)'],
            ['□ Čtverec', '90°', '4', '360°', '❌', 'Rovina (nelze)'],
            ['', '', '', '', '', ''],
            ['⬠ Pětiúhelník', '108°', '3', '324°', '✅', '<b>DVANÁCTISTĚN</b> (dodekaedr)'],
            ['⬠ Pětiúhelník', '108°', '4', '432°', '❌', 'Překročeno (nelze)'],
            ['', '', '', '', '', ''],
            ['⬡ Šestiúhelník', '120°', '3', '360°', '❌', 'Rovina (nelze)'],
            ['⬡ Šestiúhelník', '120°', '4', '480°', '❌', 'Překročeno (nelze)'],
            ['', '', '', '', '', ''],
            ['⬢ Sedmiúhelník+', '≥128.57°', '3', '≥385.7°', '❌', 'Vždy překročeno'],
        ]

        # Calculate totals
        total_angle_values = [180, 240, 300, 360, None, 270, 360, None, 324, 432, None, 360, 480, None, 385.7]

        # Color cells based on validity
        cell_colors = []
        for i, row in enumerate(data):
            if row[0] == '':  # Empty separator row
                cell_colors.append(['white'] * 6)
            elif row[4] == '✅':
                cell_colors.append(['#d4edda', '#d4edda', '#d4edda', '#d4edda', '#28a745', '#d4edda'])
            else:
                cell_colors.append(['#f8d7da', '#f8d7da', '#f8d7da', '#f8d7da', '#dc3545', '#f8d7da'])

        # Create table
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=[
                    '<b>Mnohoúhelník</b>',
                    '<b>Vnitřní úhel</b>',
                    '<b>Počet ve vrcholu</b>',
                    '<b>Součet úhlů</b>',
                    '<b>Status</b>',
                    '<b>Platónské těleso</b>'
                ],
                fill_color='#6c757d',
                font=dict(color='white', size=14),
                align='center',
                height=40
            ),
            cells=dict(
                values=list(zip(*data)),  # Transpose for column-wise data
                fill_color=list(zip(*cell_colors)),
                font=dict(color='black', size=12),
                align=['left', 'center', 'center', 'center', 'center', 'left'],
                height=35
            )
        )])

        # Add annotations explaining the logic
        fig.add_annotation(
            text=(
                '<b>Matematický důkaz:</b><br>'
                '1. Vrchol musí spojovat ≥3 stěny (jinak není těleso)<br>'
                '2. Součet úhlů musí být <360° (jinak to není konvexní 3D těleso)<br>'
                '3. Procházíme všechny pravidelné mnohoúhelníky:<br>'
                '   • Trojúhelník (60°): 3,4,5 možné → 3 Platónská tělesa ✅<br>'
                '   • Čtverec (90°): pouze 3 možné → 1 Platónské těleso ✅<br>'
                '   • Pětiúhelník (108°): pouze 3 možné → 1 Platónské těleso ✅<br>'
                '   • Šestiúhelník+ (≥120°): žádné možné → 0 Platónských těles ❌<br><br>'
                '<b>Celkem: 5 Platónských těles!</b>'
            ),
            xref='paper', yref='paper',
            x=0.5, y=-0.15,
            showarrow=False,
            font=dict(size=13),
            align='left',
            bgcolor='#f8f9fa',
            bordercolor='#6c757d',
            borderwidth=2
        )

        fig.update_layout(
            title_text="Důkaz: Systematické prozkoumání všech možností<br><sub>Pouze 5 kombinací splňuje podmínky → 5 Platónských těles</sub>",
            title_x=0.5,
            height=900,
            margin=dict(t=100, b=200)
        )

        return fig
