"""
Step 21 (18d): Důkaz pomocí úhlů - 3D vizualizace vrcholu
Bonus step showing 3D visualization of faces meeting at a vertex
"""
from typing import Dict, Any
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
- **Červená:** Nemožná konfigurace (>360°) → stěny by se musely překrývat

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

        # Create subplots in a grid
        from plotly.subplots import make_subplots

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

    def _rotation_matrix_z(self, angle_deg):
        """Rotation matrix around z-axis"""
        angle = np.radians(angle_deg)
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])

    def _create_vertex_3d(self, config: dict) -> list:
        """Create 3D visualization of faces meeting at a vertex

        Geometry: 'count' edges meet at origin, forming 'count' n-sided faces
        """
        n = config['n']  # Number of sides of polygon
        count = config['count']  # Number of polygons meeting at vertex
        valid = config.get('valid', True)
        planar = config.get('planar', False)

        # Calculate interior angle
        interior_angle = (n - 2) * 180 / n
        total_angle = count * interior_angle

        # Choose color based on validity
        if valid:
            color = 'rgba(46, 204, 113, 0.7)'  # Green
            edge_color = 'rgb(39, 174, 96)'
        elif planar:
            color = 'rgba(241, 196, 15, 0.7)'  # Yellow/Orange
            edge_color = 'rgb(243, 156, 18)'
        else:
            color = 'rgba(231, 76, 60, 0.7)'  # Red
            edge_color = 'rgb(192, 57, 43)'

        traces = []
        origin = np.array([0.0, 0.0, 0.0])

        # Step 1: Create 'count' edges emanating from origin
        # These are arranged symmetrically in azimuth
        edges = []
        angular_spacing = 360.0 / count

        # Elevation: how much edges tilt up from xy-plane
        if planar or total_angle >= 360:
            elevation = 0  # Flat
        else:
            deficit = 360 - total_angle
            # More deficit = sharper vertex = higher elevation
            elevation = min(60, deficit / count * 1.2)  # degrees, capped at 60°

        for i in range(count):
            azimuth = np.radians(i * angular_spacing)
            elev = np.radians(elevation)

            edge_end = np.array([
                np.cos(elev) * np.cos(azimuth),
                np.cos(elev) * np.sin(azimuth),
                np.sin(elev)
            ])
            edges.append(edge_end)

        # Step 2: Create polygon faces
        # Each face connects 'count' edges in a specific pattern
        # For triangles (n=3): face = [origin, edge_i, edge_i+1]
        # For squares (n=4): face = [origin, edge_i, edge_i+edge_i+1, edge_i+1]
        # For pentagons (n=5): more complex

        for i in range(count):
            e1 = edges[i]
            e2 = edges[(i + 1) % count]

            if n == 3:
                # Triangle: origin + 2 consecutive edges
                verts = [origin.copy(), e1.copy(), e2.copy()]

            elif n == 4:
                # Square: origin + edge1 + (edge1+edge2) + edge2
                # The "far corner" is the sum of the two edge vectors
                far_corner = e1 + e2
                verts = [origin.copy(), e1.copy(), far_corner.copy(), e2.copy()]

            elif n == 5:
                # Pentagon: origin + edge1 + 2 intermediate + edge2
                # Create a regular pentagon in the plane defined by origin, e1, e2
                # Define local coordinate system
                v1 = e1 / np.linalg.norm(e1)  # unit vector along e1
                # v2 in the plane, perpendicular to v1
                temp = e2 - np.dot(e2, v1) * v1
                v2 = temp / np.linalg.norm(temp) if np.linalg.norm(temp) > 1e-10 else np.array([0, 0, 1])

                # Pentagon vertices in polar coordinates (centered at origin)
                # Interior angle of pentagon = 108°
                # At the origin, we want angle = 108° between adjacent sides
                angle_at_origin = interior_angle
                angular_step = angle_at_origin / (n - 1)  # Divide the angle

                pentagon_verts = [origin.copy()]
                for j in range(n):
                    if j == 0:
                        pentagon_verts.append(e1.copy())
                    elif j == n - 1:
                        pentagon_verts.append(e2.copy())
                    else:
                        # Intermediate vertex
                        angle = j * angular_step
                        # Rotate e1 by 'angle' in the plane
                        cos_a = np.cos(np.radians(angle))
                        sin_a = np.sin(np.radians(angle))
                        # Also scale outward to form regular pentagon
                        scale = 1.0 / np.cos(np.radians(angular_step / 2))
                        pt = scale * (cos_a * v1 + sin_a * v2)
                        pentagon_verts.append(pt)

                verts = pentagon_verts[:-1]  # Remove duplicate of origin

            elif n == 6:
                # Hexagon: similar to pentagon
                v1 = e1 / np.linalg.norm(e1)
                temp = e2 - np.dot(e2, v1) * v1
                v2 = temp / np.linalg.norm(temp) if np.linalg.norm(temp) > 1e-10 else np.array([0, 0, 1])

                angle_at_origin = interior_angle
                angular_step = angle_at_origin / (n - 1)

                hexagon_verts = [origin.copy()]
                for j in range(n):
                    if j == 0:
                        hexagon_verts.append(e1.copy())
                    elif j == n - 1:
                        hexagon_verts.append(e2.copy())
                    else:
                        angle = j * angular_step
                        cos_a = np.cos(np.radians(angle))
                        sin_a = np.sin(np.radians(angle))
                        scale = 1.0 / np.cos(np.radians(angular_step / 2))
                        pt = scale * (cos_a * v1 + sin_a * v2)
                        hexagon_verts.append(pt)

                verts = hexagon_verts[:-1]

            else:
                # Default: just triangle
                verts = [origin.copy(), e1.copy(), e2.copy()]

            # Create mesh
            x_coords = [v[0] for v in verts]
            y_coords = [v[1] for v in verts]
            z_coords = [v[2] for v in verts]

            # Triangulate
            i_indices = []
            j_indices = []
            k_indices = []
            for vtx_idx in range(1, len(verts) - 1):
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
            for vtx_idx in range(len(verts)):
                v1 = verts[vtx_idx]
                v2 = verts[(vtx_idx + 1) % len(verts)]

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
