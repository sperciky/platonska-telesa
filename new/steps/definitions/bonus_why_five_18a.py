"""
Step 18a: Enhanced proof - Side-by-side comparison with angle meters
"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import streamlit as st
from steps.base_step import Step, StepMetadata


class BonusStep_WhyFive_18A(Step):
    """Step 18a: Side-by-side visualization with angle meters"""

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=18,
            category='Bonus',
            title='Důkaz úhlů (kruhové měřidlo)',
            short_name='Úhly - kruhy'
        )

    def get_description(self) -> str:
        return """
## Step 18a: Důkaz pomocí úhlů - Kruhové vizualizace

**Klíčová myšlenka:** Součet úhlů u vrcholu musí být **< 360°**, jinak nevznikne 3D těleso.

Tato vizualizace ukazuje:
- **Vlevo:** Jak se mnohoúhelníky potkávají ve vrcholu
- **Vpravo:** Kruhové měřidlo ukazující součet úhlů (max 360°)

✅ **Zelená** = Platné (<360°) → vznikne Platónské těleso
❌ **Červená** = Neplatné (≥360°) → vznikne rovina nebo nelze složit
"""

    def render_diagram(self, fig, ax) -> None:
        """Vykreslení (matplotlib - legacy, pouze placeholder)"""
        from matplotlib.figure import Figure
        self.setup_axes(ax)
        ax.set_title(self.get_metadata().title, fontsize=14, fontweight='bold')
        ax.text(0, 0, 'Viz interaktivní Plotly diagram →',
                fontsize=16, ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('off')

    def render_plotly_diagram(self) -> go.Figure:
        """Create side-by-side comparison: polygons + circular angle meter"""

        # Configuration for each case
        configs = [
            # Triangles (60° each)
            {'n_poly': 3, 'n_sides': 3, 'count': 3, 'name': 'ČTYŘSTĚN', 'latin': 'tetraedr'},
            {'n_poly': 3, 'n_sides': 3, 'count': 4, 'name': 'OSMISTĚN', 'latin': 'oktaedr'},
            {'n_poly': 3, 'n_sides': 3, 'count': 5, 'name': 'DVACETISTĚN', 'latin': 'ikosaedr'},
            {'n_poly': 3, 'n_sides': 3, 'count': 6, 'name': '❌ Rovina', 'latin': '6 trojúhelníků'},

            # Squares (90° each)
            {'n_poly': 4, 'n_sides': 4, 'count': 3, 'name': 'KRYCHLE', 'latin': 'hexaedr'},
            {'n_poly': 4, 'n_sides': 4, 'count': 4, 'name': '❌ Rovina', 'latin': '4 čtverce'},

            # Pentagons (108° each)
            {'n_poly': 5, 'n_sides': 5, 'count': 3, 'name': 'DVANÁCTISTĚN', 'latin': 'dodekaedr'},
            {'n_poly': 5, 'n_sides': 5, 'count': 4, 'name': '❌ Překročeno', 'latin': '4 pětiúhelníky'},

            # Hexagons (120° each)
            {'n_poly': 6, 'n_sides': 6, 'count': 3, 'name': '❌ Rovina', 'latin': '3 šestiúhelníky'},
        ]

        # Create figure with subplots: 9 rows, 2 columns (left: polygons, right: angle meter)
        fig = make_subplots(
            rows=9, cols=2,
            column_widths=[0.5, 0.5],
            vertical_spacing=0.04,
            horizontal_spacing=0.1,
            specs=[[{'type': 'scatter'}, {'type': 'scatter'}] for _ in range(9)]
        )

        for idx, cfg in enumerate(configs):
            row = idx + 1
            n_sides = cfg['n_poly']
            count = cfg['count']

            # Calculate angle
            internal_angle = (n_sides - 2) * 180.0 / n_sides
            total_angle = count * internal_angle
            is_valid = total_angle < 360

            # LEFT: Draw polygons meeting at vertex
            self._draw_polygons_at_vertex(fig, row, 1, count, n_sides, internal_angle, total_angle, is_valid)

            # RIGHT: Draw circular angle meter
            self._draw_angle_meter(fig, row, 2, count, internal_angle, total_angle, is_valid, cfg['name'], cfg['latin'])

        # Update all axes
        for i in range(1, 19):  # 9 rows × 2 cols = 18 subplots
            fig.update_xaxes(
                showgrid=False, showticklabels=False, zeroline=False,
                range=[-2, 2], row=(i-1)//2 + 1, col=(i-1)%2 + 1
            )
            fig.update_yaxes(
                showgrid=False, showticklabels=False, zeroline=False,
                range=[-2, 2], scaleanchor=f'x{i}', scaleratio=1,
                row=(i-1)//2 + 1, col=(i-1)%2 + 1
            )

        fig.update_layout(
            title_text="Důkaz: Proč pouze 5 Platónských těles?<br><sub>Levý sloupec: Mnohoúhelníky ve vrcholu | Pravý sloupec: Kruhové měřidlo úhlů</sub>",
            title_x=0.5,
            height=2000,
            showlegend=False,
            plot_bgcolor='white'
        )

        return fig

    def _draw_polygons_at_vertex(self, fig, row, col, count, n_sides, internal_angle, total_angle, is_valid):
        """Draw polygons meeting at a shared vertex"""
        angle_step = internal_angle * math.pi / 180.0

        for i in range(count):
            rotation = i * angle_step
            vertices = self._polygon_at_vertex(n_sides, edge_length=1.2, rotation_offset=rotation)

            xs = [v[0] for v in vertices]
            ys = [v[1] for v in vertices]

            fillcolor = 'lightgreen' if is_valid else 'lightcoral'
            linecolor = 'darkgreen' if is_valid else 'darkred'

            fig.add_trace(go.Scatter(
                x=xs, y=ys,
                mode='lines',
                fill='toself',
                fillcolor=fillcolor,
                opacity=0.4,
                line=dict(color=linecolor, width=2),
                showlegend=False,
                hoverinfo='text',
                hovertext=f'{count} × {internal_angle:.0f}° = {total_angle:.0f}°'
            ), row=row, col=col)

        # Add central vertex point
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            marker=dict(size=10, color='black', symbol='circle'),
            showlegend=False,
            hoverinfo='skip'
        ), row=row, col=col)

        # Add label
        subplot_idx = (row - 1) * 2 + col
        fig.add_annotation(
            text=f'{count} mnohoúhelníků<br>{total_angle:.0f}°',
            x=0, y=-1.7,
            xref=f'x{subplot_idx}', yref=f'y{subplot_idx}',
            showarrow=False,
            font=dict(size=10)
        )

    def _draw_angle_meter(self, fig, row, col, count, internal_angle, total_angle, is_valid, name, latin):
        """Draw circular angle meter (like a pie chart showing angle coverage)"""
        subplot_idx = (row - 1) * 2 + col

        # Draw full 360° circle outline
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = 1.3 * np.cos(theta)
        circle_y = 1.3 * np.sin(theta)

        fig.add_trace(go.Scatter(
            x=circle_x, y=circle_y,
            mode='lines',
            line=dict(color='gray', width=2, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ), row=row, col=col)

        # Draw filled arc for angle coverage
        angle_coverage = min(total_angle, 360) / 360.0 * 2 * np.pi
        arc_theta = np.linspace(0, angle_coverage, 50)
        arc_x = np.concatenate([[0], 1.3 * np.cos(arc_theta), [0]])
        arc_y = np.concatenate([[0], 1.3 * np.sin(arc_theta), [0]])

        fillcolor = 'lightgreen' if is_valid else 'lightcoral'

        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y,
            mode='lines',
            fill='toself',
            fillcolor=fillcolor,
            opacity=0.5,
            line=dict(color='green' if is_valid else 'red', width=2),
            showlegend=False,
            hoverinfo='text',
            hovertext=f'{total_angle:.0f}° / 360°'
        ), row=row, col=col)

        # If angle > 360, show overflow in red
        if total_angle > 360:
            overflow = total_angle - 360
            overflow_arc = overflow / 360.0 * 2 * np.pi
            overflow_theta = np.linspace(0, overflow_arc, 30)
            overflow_x = np.concatenate([[0], 1.5 * np.cos(overflow_theta), [0]])
            overflow_y = np.concatenate([[0], 1.5 * np.sin(overflow_theta), [0]])

            fig.add_trace(go.Scatter(
                x=overflow_x, y=overflow_y,
                mode='lines',
                fill='toself',
                fillcolor='red',
                opacity=0.3,
                line=dict(color='darkred', width=2),
                showlegend=False,
                hoverinfo='text',
                hovertext=f'Přetečení: +{overflow:.0f}°'
            ), row=row, col=col)

        # Add center point
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            marker=dict(size=8, color='black'),
            showlegend=False,
            hoverinfo='skip'
        ), row=row, col=col)

        # Add angle label in center
        status = '✅' if is_valid else '❌'
        fig.add_annotation(
            text=f'<b>{total_angle:.0f}°</b> {status}',
            x=0, y=0,
            xref=f'x{subplot_idx}', yref=f'y{subplot_idx}',
            showarrow=False,
            font=dict(size=12, color='green' if is_valid else 'red')
        )

        # Add Platonic solid name
        fig.add_annotation(
            text=f'<b>{name}</b><br><sub>{latin}</sub>',
            x=0, y=-1.7,
            xref=f'x{subplot_idx}', yref=f'y{subplot_idx}',
            showarrow=False,
            font=dict(size=10, color='green' if is_valid else 'red')
        )

    def _polygon_at_vertex(self, n_sides, edge_length=1.0, rotation_offset=0):
        """Generate vertices for a regular polygon with one vertex at origin"""
        vertices = [(0, 0)]

        internal_angle = (n_sides - 2) * 180.0 / n_sides
        external_angle = 180.0 - internal_angle

        current_angle = rotation_offset
        current_x, current_y = 0, 0

        for i in range(n_sides):
            next_x = current_x + edge_length * math.cos(current_angle)
            next_y = current_y + edge_length * math.sin(current_angle)
            vertices.append((next_x, next_y))

            current_angle += math.radians(external_angle)
            current_x, current_y = next_x, next_y

        return vertices
