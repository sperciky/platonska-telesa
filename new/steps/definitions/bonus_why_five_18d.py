"""
Step 21 (18d): Důkaz pomocí úhlů - 3D vizualizace vrcholu
Bonus step showing 3D visualization of faces meeting at a vertex
"""
from typing import List
import numpy as np
import plotly.graph_objects as go
from matplotlib.figure import Figure

from steps.base_step import Step, StepMetadata


class BonusStep_WhyFive_18D(Step):
    """Step 21 (18d): 3D vizualizace - Jak se stýkají stěny ve vrcholu"""

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=21,
            category="bonus",
            title="18d. Úhly - 3D vrchol",
            short_name="18d. Úhly - 3D vrchol"
        )

    def get_description(self) -> str:
        return """
## Step 18d: Důkaz pomocí úhlů - 3D Vizualizace vrcholu

**Prostorové pochopení:** Jak se stěny skutečně potkávají ve vrcholu?

Tato 3D vizualizace ukazuje:
- **Zelená:** Validní konfigurace (<360°) → stěny tvoří 3D "kužel"
- **Žlutá/Oranžová:** Rovinná konfigurace (=360°) → stěny leží v rovině
- **Červená:** Nemožná konfigurace (>360°) → stěny se překrývají!

Klíčové poznatky:
1. **3 trojúhelníky** (180°) → tvoří "ostrou" špičku tetraedru
2. **6 trojúhelníků** (360°) → ploché, jako šestiúhelník na rovině
3. **3 čtverce** (270°) → tvoří roh krychle (90° volného prostoru)
4. **4 čtverce** (360°) → ploché, jako na šachovnici
5. **3 pětiúhelníky** (324°) → mírně zakřivené, dodekaedr
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení (matplotlib - legacy, pouze placeholder)"""
        self.setup_axes(ax)
        ax.set_title(self.get_metadata().title, fontsize=14, fontweight='bold')
        ax.text(0, 0, 'Viz interaktivní 3D Plotly vizualizace →',
                fontsize=16, ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('off')

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení 3D vizualizace vrcholů (Plotly - interaktivní)"""
        from plotly.subplots import make_subplots

        # Configuration for different vertex arrangements
        configs = [
            # Valid configurations (green)
            {"n": 3, "count": 3, "name": "3 trojúhelníky", "solid": "Tetraedr", "valid": True},
            {"n": 3, "count": 4, "name": "4 trojúhelníky", "solid": "Oktaedr", "valid": True},
            {"n": 3, "count": 5, "name": "5 trojúhelníků", "solid": "Ikosaedr", "valid": True},
            {"n": 4, "count": 3, "name": "3 čtverce", "solid": "Krychle", "valid": True},
            {"n": 5, "count": 3, "name": "3 pětiúhelníky", "solid": "Dodekaedr", "valid": True},

            # Planar configurations (yellow/orange)
            {"n": 3, "count": 6, "name": "6 trojúhelníků", "solid": "Rovina", "valid": False, "planar": True},
            {"n": 4, "count": 4, "name": "4 čtverce", "solid": "Rovina", "valid": False, "planar": True},
            {"n": 6, "count": 3, "name": "3 šestiúhelníky", "solid": "Rovina", "valid": False, "planar": True},

            # Impossible configurations (red)
            {"n": 3, "count": 7, "name": "7 trojúhelníků", "solid": "Nemožné!", "valid": False, "planar": False},
            {"n": 5, "count": 4, "name": "4 pětiúhelníky", "solid": "Nemožné!", "valid": False, "planar": False},
        ]

        rows = 2
        cols = 5

        fig = make_subplots(
            rows=rows, cols=cols,
            specs=[[{'type': 'scene'}] * cols] * rows,
            subplot_titles=[f"{c['name']}<br>{c['solid']}" for c in configs],
            vertical_spacing=0.05,
            horizontal_spacing=0.02
        )

        # Generate each configuration
        for idx, config in enumerate(configs):
            row = idx // cols + 1
            col = idx % cols + 1

            traces = self._create_vertex_3d(config)

            for trace in traces:
                fig.add_trace(trace, row=row, col=col)

            # Configure the 3D scene
            scene_name = 'scene' if idx == 0 else f'scene{idx + 1}'
            fig.update_layout(**{
                scene_name: dict(
                    xaxis=dict(range=[-1.5, 1.5], showticklabels=False, title=''),
                    yaxis=dict(range=[-1.5, 1.5], showticklabels=False, title=''),
                    zaxis=dict(range=[-0.5, 1.5], showticklabels=False, title=''),
                    aspectmode='cube',
                    camera=dict(
                        eye=dict(x=1.3, y=1.3, z=1.2),
                        up=dict(x=0, y=0, z=1)
                    ),
                    bgcolor='white'
                )
            })

        fig.update_layout(
            title=dict(
                text="3D Vizualizace: Jak se stěny potkávají ve vrcholu",
                font=dict(size=24, color='#2c3e50'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            height=800,
            margin=dict(t=120, l=10, r=10, b=10),
            paper_bgcolor='#f8f9fa',
        )

        return fig

    def _create_regular_ngon(self, n: int, edge_length: float) -> List[np.ndarray]:
        """
        Create a regular n-sided polygon with one vertex at origin.
        All edges have the specified length.
        Returns vertices in local coordinates (before rotation/tilt).
        """
        origin = np.array([0.0, 0.0, 0.0])

        if n == 3:
            # Equilateral triangle: one vertex at origin, one along +x axis
            # Third vertex at 60° to make equilateral
            verts = [
                origin,
                np.array([edge_length, 0.0, 0.0]),
                np.array([edge_length * np.cos(np.radians(60)),
                         edge_length * np.sin(np.radians(60)),
                         0.0])
            ]
            return verts

        elif n == 4:
            # Square: one vertex at origin
            verts = [
                origin,
                np.array([edge_length, 0.0, 0.0]),
                np.array([edge_length, edge_length, 0.0]),
                np.array([0.0, edge_length, 0.0])
            ]
            return verts

        elif n == 5:
            # Regular pentagon: one vertex at origin
            # Interior angle = 108°
            verts = [origin]
            verts.append(np.array([edge_length, 0.0, 0.0]))

            # Remaining vertices at 108° intervals
            angle = 108  # degrees
            for i in range(1, n - 1):
                current_angle = np.radians(i * angle)
                verts.append(np.array([
                    edge_length * np.cos(current_angle),
                    edge_length * np.sin(current_angle),
                    0.0
                ]))

            return verts

        elif n == 6:
            # Regular hexagon: one vertex at origin
            # Interior angle = 120°
            verts = [origin]
            angle = 120  # degrees

            for i in range(n - 1):
                current_angle = np.radians(i * angle)
                verts.append(np.array([
                    edge_length * np.cos(current_angle),
                    edge_length * np.sin(current_angle),
                    0.0
                ]))

            return verts

        else:
            # Generic
            verts = [origin]
            interior_angle = (n - 2) * 180 / n

            for i in range(n - 1):
                angle_rad = np.radians(i * interior_angle)
                verts.append(np.array([
                    edge_length * np.cos(angle_rad),
                    edge_length * np.sin(angle_rad),
                    0.0
                ]))

            return verts

    def _create_vertex_3d(self, config: dict) -> list:
        """Create 3D visualization of faces meeting at a vertex with EQUAL edge lengths"""
        n = config['n']
        count = config['count']
        valid = config.get('valid', True)
        planar = config.get('planar', False)

        interior_angle = (n - 2) * 180 / n
        total_angle = count * interior_angle

        # Colors
        if valid:
            color = 'rgba(46, 204, 113, 0.7)'
            edge_color = 'rgb(39, 174, 96)'
        elif planar:
            color = 'rgba(241, 196, 15, 0.7)'
            edge_color = 'rgb(243, 156, 18)'
        else:
            color = 'rgba(231, 76, 60, 0.7)'
            edge_color = 'rgb(192, 57, 43)'

        traces = []
        origin = np.array([0.0, 0.0, 0.0])
        edge_length = 1.0  # All edges will have this length

        # Create faces with regular polygons
        angular_spacing = 360.0 / count

        for i in range(count):
            # Rotation angle for this face
            rotation = np.radians(i * angular_spacing)

            # Create a regular n-gon in local coordinates
            polygon_verts = self._create_regular_ngon(n, edge_length)

            # Calculate tilt based on configuration
            if planar or total_angle == 360:
                # Flat in xy-plane
                tilt_angle = 0
            elif total_angle < 360:
                # Tilt up - valid 3D
                deficit = 360 - total_angle
                tilt_angle = min(70, deficit / count * 1.5)
            else:
                # Tilt down/overlap - impossible
                excess = total_angle - 360
                tilt_angle = -min(30, excess / count * 0.8)

            # Transform vertices: rotate around z, then tilt
            transformed_verts = []
            for v in polygon_verts:
                # Rotate around z-axis
                x = v[0] * np.cos(rotation) - v[1] * np.sin(rotation)
                y = v[0] * np.sin(rotation) + v[1] * np.cos(rotation)
                z = v[2]

                # Tilt (rotate around y-axis after z-rotation)
                tilt_rad = np.radians(tilt_angle)
                x_new = x * np.cos(tilt_rad) - z * np.sin(tilt_rad)
                z_new = x * np.sin(tilt_rad) + z * np.cos(tilt_rad)

                transformed_verts.append(np.array([x_new, y, z_new]))

            # Create mesh
            x_coords = [v[0] for v in transformed_verts]
            y_coords = [v[1] for v in transformed_verts]
            z_coords = [v[2] for v in transformed_verts]

            # Triangulate from origin (vertex 0)
            i_indices = []
            j_indices = []
            k_indices = []
            for vtx_idx in range(1, len(transformed_verts) - 1):
                i_indices.append(0)
                j_indices.append(vtx_idx)
                k_indices.append(vtx_idx + 1)

            traces.append(go.Mesh3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                i=i_indices,
                j=j_indices,
                k=k_indices,
                color=color,
                opacity=0.75,
                flatshading=False,
                hoverinfo='skip'
            ))

            # Add edges
            for vtx_idx in range(len(transformed_verts)):
                v1 = transformed_verts[vtx_idx]
                v2 = transformed_verts[(vtx_idx + 1) % len(transformed_verts)]

                traces.append(go.Scatter3d(
                    x=[v1[0], v2[0]],
                    y=[v1[1], v2[1]],
                    z=[v1[2], v2[2]],
                    mode='lines',
                    line=dict(color=edge_color, width=4),
                    hoverinfo='skip',
                    showlegend=False
                ))

        # Add central vertex marker
        traces.append(go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode='markers+text',
            marker=dict(size=12, color='darkblue'),
            text=f'{total_angle:.0f}°',
            textposition='top center',
            textfont=dict(size=10, color='black'),
            hoverinfo='skip',
            showlegend=False
        ))

        return traces
