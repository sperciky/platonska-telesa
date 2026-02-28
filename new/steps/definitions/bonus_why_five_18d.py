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

    def _create_vertex_3d(self, config: dict) -> list:
        """Create 3D visualization of faces meeting at a vertex"""
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

        # Vertex at origin
        vertex = np.array([0, 0, 0])

        # For planar configurations, faces lie in xy-plane
        # For 3D configurations, faces are tilted up from xy-plane
        if planar or total_angle >= 360:
            # Flat or impossible - arrange in plane
            angle_step = 360 / count
            tilt_angle = 0  # Flat
        else:
            # Valid 3D - calculate tilt to form cone
            angle_step = 360 / count
            # The cone angle depends on the deficit angle
            deficit = 360 - total_angle
            # Convert to radians for tilt calculation
            tilt_angle = deficit / count * 0.8  # Heuristic for visual clarity

        # Create each face
        for i in range(count):
            # Rotation angle around z-axis
            rotation_angle = i * angle_step

            # Create regular n-gon in local coordinates
            polygon_points = []
            for j in range(n):
                angle = j * (360 / n)
                x = np.cos(np.radians(angle)) * 0.8
                y = np.sin(np.radians(angle)) * 0.8
                polygon_points.append([x, y, 0])

            # Transform to position
            transformed_points = []
            for point in polygon_points:
                # Tilt up from xy-plane
                x, y, z = point
                if not planar and total_angle < 360:
                    # Rotate around x-axis to tilt
                    tilt_rad = np.radians(tilt_angle)
                    y_new = y * np.cos(tilt_rad) - z * np.sin(tilt_rad)
                    z_new = y * np.sin(tilt_rad) + z * np.cos(tilt_rad)
                    y, z = y_new, z_new

                # Rotate around z-axis
                rot_rad = np.radians(rotation_angle)
                x_new = x * np.cos(rot_rad) - y * np.sin(rot_rad)
                y_new = x * np.sin(rot_rad) + y * np.cos(rot_rad)

                transformed_points.append([x_new, y_new, z])

            # Add vertex (origin) to close the pyramid face
            face_points = [vertex] + transformed_points

            # Create mesh for the face
            x_coords = [p[0] for p in face_points]
            y_coords = [p[1] for p in face_points]
            z_coords = [p[2] for p in face_points]

            # Create triangular faces for the mesh
            if n == 3:
                # Triangle - simple
                i_indices = [0, 1, 2]
                j_indices = [1, 2, 0]
                k_indices = [2, 0, 1]
            else:
                # Polygon - fan triangulation from vertex
                i_indices = []
                j_indices = []
                k_indices = []
                for idx in range(n):
                    i_indices.append(0)  # Vertex
                    j_indices.append(idx + 1)
                    k_indices.append((idx + 1) % n + 1)

            # Add face mesh
            traces.append(go.Mesh3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                i=i_indices,
                j=j_indices,
                k=k_indices,
                color=color,
                opacity=0.8,
                flatshading=True,
                hoverinfo='skip'
            ))

            # Add edges
            for idx in range(len(transformed_points)):
                p1 = transformed_points[idx]
                p2 = transformed_points[(idx + 1) % len(transformed_points)]

                # Edge from vertex to polygon point
                traces.append(go.Scatter3d(
                    x=[vertex[0], p1[0]],
                    y=[vertex[1], p1[1]],
                    z=[vertex[2], p1[2]],
                    mode='lines',
                    line=dict(color=edge_color, width=3),
                    hoverinfo='skip',
                    showlegend=False
                ))

                # Edge around polygon
                traces.append(go.Scatter3d(
                    x=[p1[0], p2[0]],
                    y=[p1[1], p2[1]],
                    z=[p1[2], p2[2]],
                    mode='lines',
                    line=dict(color=edge_color, width=2),
                    hoverinfo='skip',
                    showlegend=False
                ))

        # Add central vertex marker
        traces.append(go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode='markers',
            marker=dict(size=8, color='black'),
            hoverinfo='text',
            text=f'{total_angle:.1f}°',
            showlegend=False
        ))

        return traces
