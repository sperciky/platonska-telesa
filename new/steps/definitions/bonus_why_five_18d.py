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

    def _get_platonic_solid_edges(self, n: int, count: int, planar: bool) -> list:
        """Get the actual edge directions for each Platonic solid configuration"""

        if planar or count * ((n - 2) * 180 / n) >= 360:
            # Planar: edges in xy-plane
            edges = []
            for i in range(count):
                angle = np.radians(i * 360 / count)
                edges.append(np.array([np.cos(angle), np.sin(angle), 0.0]))
            return edges

        # Valid 3D configurations - use actual Platonic solid geometry

        # Tetrahedron: 3 triangles
        if n == 3 and count == 3:
            # Tetrahedral angle: edges at ~109.47° to each other
            # Place first edge along x-axis, arrange others symmetrically
            sqrt2 = np.sqrt(2)
            sqrt6 = np.sqrt(6)
            edges = [
                np.array([1.0, 0.0, 0.0]),
                np.array([-1/3, 2*sqrt2/3, 0.0]),
                np.array([-1/3, -sqrt2/3, sqrt6/3])
            ]
            return edges

        # Octahedron: 4 triangles
        elif n == 3 and count == 4:
            # Square pyramid: edges at 90° in xy-plane
            edges = [
                np.array([1.0, 0.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
                np.array([-1.0, 0.0, 0.0]),
                np.array([0.0, -1.0, 0.0])
            ]
            return edges

        # Icosahedron: 5 triangles
        elif n == 3 and count == 5:
            # 5 edges in pentagonal cone
            phi = (1 + np.sqrt(5)) / 2  # Golden ratio
            # Elevation angle for icosahedron vertex
            theta = np.arctan(2)  # ~63.43°
            edges = []
            for i in range(5):
                angle = np.radians(i * 72)  # 360/5
                edges.append(np.array([
                    np.cos(theta) * np.cos(angle),
                    np.cos(theta) * np.sin(angle),
                    np.sin(theta)
                ]))
            return edges

        # Cube: 3 squares
        elif n == 4 and count == 3:
            # Three perpendicular edges
            edges = [
                np.array([1.0, 0.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
                np.array([0.0, 0.0, 1.0])
            ]
            return edges

        # Dodecahedron: 3 pentagons
        elif n == 5 and count == 3:
            # Three edges with dodecahedral angle
            phi = (1 + np.sqrt(5)) / 2
            # Normalize the three edge directions
            edges = [
                np.array([phi, 0.0, 1.0]),
                np.array([1.0, phi, 0.0]),
                np.array([0.0, 1.0, phi])
            ]
            edges = [e / np.linalg.norm(e) for e in edges]
            return edges

        # Fallback
        else:
            edges = []
            for i in range(count):
                angle = np.radians(i * 360 / count)
                edges.append(np.array([np.cos(angle), np.sin(angle), 0.2]))
            return edges

    def _create_regular_polygon_between_edges(self, e1: np.ndarray, e2: np.ndarray, n: int) -> list:
        """Create regular n-gon with origin as one vertex and e1, e2 as two edges"""
        origin = np.array([0.0, 0.0, 0.0])

        if n == 3:
            # Equilateral triangle
            return [origin, e1, e2]

        elif n == 4:
            # Square: fourth vertex at e1 + e2
            return [origin, e1, e1 + e2, e2]

        elif n == 5:
            # Regular pentagon
            # Calculate the other 2 vertices to make a regular pentagon
            # Use the fact that in a regular pentagon from one vertex,
            # the angle between consecutive sides is 108°

            # Edge length
            side_len = np.linalg.norm(e1)

            # Create orthonormal basis in the plane of the polygon
            u = e1 / np.linalg.norm(e1)

            # Find perpendicular direction in plane containing origin, e1, e2
            normal = np.cross(e1, e2)
            if np.linalg.norm(normal) < 1e-10:
                # Degenerate case
                return [origin, e1, e2]
            normal = normal / np.linalg.norm(normal)

            # v is perpendicular to u in the plane
            v = np.cross(normal, u)
            v = v / np.linalg.norm(v)

            # For regular pentagon with one vertex at origin:
            # angles from first edge are 0°, 72°, 144°, 216°, 288°
            # But we want vertices at 0, 108, 216, 324, which connects back
            # Actually for a pentagon fan from origin: 0, 108, 216, 324

            verts = [origin]
            for i in range(5):
                angle = np.radians(i * 72)  # Pentagon vertices at 72° intervals
                pt = side_len * (np.cos(angle) * u + np.sin(angle) * v)
                verts.append(pt)

            # Return the 5 vertices (origin + 4 outer)
            return verts[:5]

        elif n == 6:
            # Regular hexagon
            side_len = np.linalg.norm(e1)
            u = e1 / np.linalg.norm(e1)
            normal = np.cross(e1, e2)
            if np.linalg.norm(normal) < 1e-10:
                return [origin, e1, e2]
            normal = normal / np.linalg.norm(normal)
            v = np.cross(normal, u)
            v = v / np.linalg.norm(v)

            verts = [origin]
            for i in range(6):
                angle = np.radians(i * 60)
                pt = side_len * (np.cos(angle) * u + np.sin(angle) * v)
                verts.append(pt)

            return verts[:6]

        else:
            return [origin, e1, e2]

    def _create_vertex_3d(self, config: dict) -> list:
        """Create 3D visualization of faces meeting at a vertex"""
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

        # Get the actual Platonic solid edge directions
        edges = self._get_platonic_solid_edges(n, count, planar)

        # Create polygon faces between consecutive edges
        for i in range(count):
            e1 = edges[i]
            e2 = edges[(i + 1) % count]

            # Use helper to create regular polygon face
            verts = self._create_regular_polygon_between_edges(e1, e2, n)

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
