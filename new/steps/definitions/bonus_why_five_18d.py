"""
Step 21 (18d): Důkaz pomocí úhlů - 3D vizualizace vrcholu
Bonus step showing 3D visualization of faces meeting at a vertex
"""
from typing import List, Tuple
import numpy as np
import plotly.graph_objects as go
from matplotlib.figure import Figure

from steps.base_step import Step, StepMetadata


class BonusStep_WhyFive_18D(Step):
    """Step 21 (18d): 3D vizualizace - Jak se stýkají stěny ve vrcholu"""

    def __init__(self):
        super().__init__()
        self.dodec_faces_cache = None

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

        configs = [
            {"n": 3, "count": 3, "name": "3 trojúhelníky", "solid": "Tetraedr", "valid": True},
            {"n": 3, "count": 4, "name": "4 trojúhelníky", "solid": "Oktaedr", "valid": True},
            {"n": 3, "count": 5, "name": "5 trojúhelníků", "solid": "Ikosaedr", "valid": True},
            {"n": 4, "count": 3, "name": "3 čtverce", "solid": "Krychle", "valid": True},
            {"n": 5, "count": 3, "name": "3 pětiúhelníky", "solid": "Dodekaedr", "valid": True},
            {"n": 3, "count": 6, "name": "6 trojúhelníků", "solid": "Rovina", "valid": False, "planar": True},
            {"n": 4, "count": 4, "name": "4 čtverce", "solid": "Rovina", "valid": False, "planar": True},
            {"n": 6, "count": 3, "name": "3 šestiúhelníky", "solid": "Rovina", "valid": False, "planar": True},
            {"n": 3, "count": 7, "name": "7 trojúhelníků", "solid": "Nemožné!", "valid": False, "planar": False},
            {"n": 5, "count": 4, "name": "4 pětiúhelníky", "solid": "Nemožné!", "valid": False, "planar": False},
        ]

        # Use 5 rows x 2 columns for more square-like spaces
        rows, cols = 5, 2
        fig = make_subplots(
            rows=rows, cols=cols,
            specs=[[{'type': 'scene'}] * cols] * rows,
            subplot_titles=[f"{c['name']}<br>{c['solid']}" for c in configs],
            vertical_spacing=0.08,
            horizontal_spacing=0.08
        )

        for idx, config in enumerate(configs):
            row, col = idx // cols + 1, idx % cols + 1
            traces = self._create_vertex_3d(config)
            for trace in traces:
                fig.add_trace(trace, row=row, col=col)

            scene_name = 'scene' if idx == 0 else f'scene{idx + 1}'

            # Use larger range for hexagons and pentagons to avoid clipping
            n = config['n']
            if n >= 5:  # Pentagons and hexagons need more space
                axis_range = [-2.5, 2.5]
            else:  # Triangles and squares fit in smaller range
                axis_range = [-1.5, 1.5]

            fig.update_layout(**{
                scene_name: dict(
                    xaxis=dict(range=axis_range, showticklabels=False, title=''),
                    yaxis=dict(range=axis_range, showticklabels=False, title=''),
                    zaxis=dict(range=axis_range, showticklabels=False, title=''),
                    aspectmode='cube',
                    aspectratio=dict(x=1, y=1, z=1),  # Force equal proportions
                    camera=dict(eye=dict(x=1.3, y=1.3, z=1.2), up=dict(x=0, y=0, z=1)),
                    bgcolor='white'
                )
            })

        fig.update_layout(
            title=dict(text="3D Vizualizace: Jak se stěny potkávají ve vrcholu",
                      font=dict(size=20, color='#2c3e50'), x=0.5, xanchor='center'),
            showlegend=False, height=1800,  # Taller for 5 rows
            margin=dict(t=80, l=10, r=10, b=10), paper_bgcolor='#f8f9fa'
        )
        return fig

    def _generate_dodecahedron(self) -> Tuple[List[np.ndarray], List[List[int]]]:
        """Generate dodecahedron vertices and find pentagon faces"""
        phi = (1 + np.sqrt(5)) / 2
        vertices = []

        # 8 vertices at (±1, ±1, ±1)
        for i in [1, -1]:
            for j in [1, -1]:
                for k in [1, -1]:
                    vertices.append(np.array([i, j, k], dtype=float))

        # 4 vertices at (0, ±φ, ±1/φ)
        for i in [1, -1]:
            for j in [1, -1]:
                vertices.append(np.array([0, i*phi, j/phi], dtype=float))

        # 4 vertices at (±1/φ, 0, ±φ)
        for i in [1, -1]:
            for j in [1, -1]:
                vertices.append(np.array([i/phi, 0, j*phi], dtype=float))

        # 4 vertices at (±φ, ±1/φ, 0)
        for i in [1, -1]:
            for j in [1, -1]:
                vertices.append(np.array([i*phi, j/phi, 0], dtype=float))

        # Build adjacency list
        edge_dist = 2 / phi  # Edge length of dodecahedron
        adj = {i: [] for i in range(len(vertices))}
        for i in range(len(vertices)):
            for j in range(i+1, len(vertices)):
                dist = np.linalg.norm(vertices[i] - vertices[j])
                if abs(dist - edge_dist) < 0.01:
                    adj[i].append(j)
                    adj[j].append(i)

        # Find all pentagon faces using exhaustive search
        faces = self._find_all_pentagon_faces_exhaustive(vertices, adj)

        return vertices, faces

    def _find_all_pentagon_faces_exhaustive(self, vertices: List[np.ndarray], adj: dict) -> List[List[int]]:
        """Find all pentagon faces using exhaustive DFS search"""
        faces = []
        visited_faces = set()

        def dfs_find_cycle(path, target_len):
            """DFS to find cycles of target length"""
            if len(path) == target_len:
                # Check if it closes
                if path[0] in adj[path[-1]]:
                    return [path[:]]
                return []

            current = path[-1]
            prev = path[-2] if len(path) > 1 else None
            found_cycles = []

            for neighbor in adj[current]:
                if neighbor == prev:  # Don't go back
                    continue
                if neighbor in path[:-1]:  # Don't revisit (except to close)
                    continue

                path.append(neighbor)
                found_cycles.extend(dfs_find_cycle(path, target_len))
                path.pop()

            return found_cycles

        # Try starting from each vertex and edge
        for start in range(len(vertices)):
            for second in adj[start]:
                if start < second:  # Avoid duplicates
                    cycles = dfs_find_cycle([start, second], 5)

                    for cycle in cycles:
                        face_set = frozenset(cycle)
                        if face_set not in visited_faces:
                            # Verify it's a valid pentagon
                            if self._is_valid_pentagon([vertices[i] for i in cycle]):
                                faces.append(cycle)
                                visited_faces.add(face_set)

        return faces

    def _build_face_cycle(self, start: int, second: int, adj: dict, target_length: int, vertices: List[np.ndarray] = None) -> List[int]:
        """Build a face cycle starting from start->second using geometric selection"""
        face = [start, second]
        current = second
        prev = start

        for step in range(target_length - 2):
            # Find next vertex in the cycle
            candidates = [v for v in adj[current] if v != prev and v not in face]

            if not candidates:
                return None

            if len(candidates) == 1:
                next_v = candidates[0]
            elif vertices is not None:
                # Use geometric criterion: pick the one that continues the face
                # in a consistent rotational direction
                v_prev = vertices[prev]
                v_curr = vertices[current]

                # Vector from prev to current
                edge_prev = v_curr - v_prev

                # For each candidate, compute the cross product to determine rotation
                best_candidate = None
                best_angle = -1

                for cand in candidates:
                    v_cand = vertices[cand]
                    edge_next = v_cand - v_curr

                    # Cross product gives normal to the plane
                    cross = np.cross(edge_prev, edge_next)

                    # Dot product with current normal estimate
                    if step == 0:
                        # First step: just pick based on angle
                        angle = np.dot(edge_prev, edge_next) / (np.linalg.norm(edge_prev) * np.linalg.norm(edge_next) + 1e-10)
                    else:
                        # Later steps: maintain consistent normal direction
                        if len(face) >= 3:
                            v0, v1, v2 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
                            face_normal = np.cross(v1 - v0, v2 - v0)
                            face_normal = face_normal / (np.linalg.norm(face_normal) + 1e-10)
                            angle = np.dot(cross, face_normal)
                        else:
                            angle = np.linalg.norm(cross)

                    if angle > best_angle:
                        best_angle = angle
                        best_candidate = cand

                next_v = best_candidate if best_candidate is not None else candidates[0]
            else:
                next_v = candidates[0]

            face.append(next_v)
            prev = current
            current = next_v

        # Check if it closes (last vertex connects to start)
        if start in adj[current]:
            return face
        return None

    def _is_valid_pentagon(self, verts: List[np.ndarray]) -> bool:
        """Check if 5 vertices form a valid regular pentagon"""
        if len(verts) != 5:
            return False

        # Check all edges have similar length
        edge_lengths = []
        for i in range(5):
            edge_len = np.linalg.norm(verts[i] - verts[(i+1) % 5])
            edge_lengths.append(edge_len)

        avg_len = np.mean(edge_lengths)
        if any(abs(l - avg_len) > 0.1 for l in edge_lengths):
            return False

        # Check planarity
        p0, p1, p2, p3 = verts[0], verts[1], verts[2], verts[3]
        normal = np.cross(p1 - p0, p2 - p0)
        normal = normal / (np.linalg.norm(normal) + 1e-10)

        # All vertices should be in the same plane
        for v in verts:
            dist_to_plane = abs(np.dot(v - p0, normal))
            if dist_to_plane > 0.1:
                return False

        return True

    def _get_dodecahedron_faces_at_vertex(self, vertex_idx: int) -> List[List[np.ndarray]]:
        """Get the 3 pentagon faces containing the specified vertex"""
        if self.dodec_faces_cache is None:
            vertices, faces = self._generate_dodecahedron()
            self.dodec_faces_cache = (vertices, faces)
        else:
            vertices, faces = self.dodec_faces_cache

        # Find faces containing vertex_idx
        vertex_faces = []
        for face_indices in faces:
            if vertex_idx in face_indices:
                # Convert indices to actual vertices
                face_verts = [vertices[i] for i in face_indices]
                vertex_faces.append(face_verts)

        return vertex_faces[:3]  # Should be exactly 3 for dodecahedron

    def _create_vertex_3d(self, config: dict) -> list:
        """Create 3D visualization with equal edge lengths"""
        n = config['n']
        count = config['count']
        valid = config.get('valid', True)
        planar = config.get('planar', False)

        interior_angle = (n - 2) * 180 / n
        total_angle = count * interior_angle

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

        # Special handling for dodecahedron (3 pentagons)
        if n == 5 and count == 3 and valid:
            # Get actual dodecahedron faces
            vertices, faces_indices = self._generate_dodecahedron()

            # Find vertex (1, 1, 1)
            center_idx = None
            center = np.array([1.0, 1.0, 1.0])
            for i, v in enumerate(vertices):
                if np.linalg.norm(v - center) < 0.01:
                    center_idx = i
                    break

            # Get 3 faces containing this vertex
            vertex_faces_verts = []
            for face_idx in faces_indices:
                if center_idx in face_idx:
                    face_verts = [vertices[i] for i in face_idx]
                    vertex_faces_verts.append(face_verts)

            # Shift and scale faces so center is at origin
            edge_length = 1.0
            actual_edge_len = np.linalg.norm(vertices[faces_indices[0][0]] - vertices[faces_indices[0][1]])

            for face_verts in vertex_faces_verts[:3]:  # Take first 3 faces
                # Shift to origin
                shifted_verts = [(v - center) * (edge_length / actual_edge_len) for v in face_verts]

                # Create mesh
                x_coords = [v[0] for v in shifted_verts]
                y_coords = [v[1] for v in shifted_verts]
                z_coords = [v[2] for v in shifted_verts]

                # Triangulate from first vertex
                i_indices, j_indices, k_indices = [], [], []
                for vtx_idx in range(1, len(shifted_verts) - 1):
                    i_indices.append(0)
                    j_indices.append(vtx_idx)
                    k_indices.append(vtx_idx + 1)

                traces.append(go.Mesh3d(
                    x=x_coords, y=y_coords, z=z_coords,
                    i=i_indices, j=j_indices, k=k_indices,
                    color=color, opacity=0.75, flatshading=False, hoverinfo='skip'
                ))

                # Edges
                for vtx_idx in range(len(shifted_verts)):
                    v1, v2 = shifted_verts[vtx_idx], shifted_verts[(vtx_idx + 1) % len(shifted_verts)]
                    traces.append(go.Scatter3d(
                        x=[v1[0], v2[0]], y=[v1[1], v2[1]], z=[v1[2], v2[2]],
                        mode='lines', line=dict(color=edge_color, width=4),
                        hoverinfo='skip', showlegend=False
                    ))

        else:
            # Original logic for other shapes
            edges = self._get_edges_from_origin(n, count, planar)

            # For impossible configurations (total_angle > 360), show overlapping faces
            if not valid and not planar and total_angle > 360:
                # Calculate how many faces fit without exceeding 360°
                max_faces_fit = int(360 / interior_angle)
                excess_angle = total_angle - 360

                # Create faces between consecutive edges
                for i in range(count):
                    e1 = edges[i]
                    e2 = edges[(i + 1) % count]

                    verts = self._create_face(e1, e2, n)

                    # Determine color and opacity based on whether this face fits
                    if i < max_faces_fit:
                        # Faces that fit: normal color with transparency
                        face_color = 'rgba(241, 196, 15, 0.6)'  # Yellow/orange
                        face_edge_color = 'rgb(243, 156, 18)'
                        face_opacity = 0.6
                    else:
                        # Overlapping faces: bright red with high transparency
                        face_color = 'rgba(231, 76, 60, 0.4)'  # Red, more transparent
                        face_edge_color = 'rgb(192, 57, 43)'
                        face_opacity = 0.4

                    # Create mesh
                    x_coords = [v[0] for v in verts]
                    y_coords = [v[1] for v in verts]
                    z_coords = [v[2] for v in verts]

                    # Triangulate from origin
                    i_indices, j_indices, k_indices = [], [], []
                    for vtx_idx in range(1, len(verts) - 1):
                        i_indices.append(0)
                        j_indices.append(vtx_idx)
                        k_indices.append(vtx_idx + 1)

                    traces.append(go.Mesh3d(
                        x=x_coords, y=y_coords, z=z_coords,
                        i=i_indices, j=j_indices, k=k_indices,
                        color=face_color, opacity=face_opacity, flatshading=False, hoverinfo='skip'
                    ))

                    # Edges
                    for vtx_idx in range(len(verts)):
                        v1, v2 = verts[vtx_idx], verts[(vtx_idx + 1) % len(verts)]
                        traces.append(go.Scatter3d(
                            x=[v1[0], v2[0]], y=[v1[1], v2[1]], z=[v1[2], v2[2]],
                            mode='lines', line=dict(color=face_edge_color, width=3),
                            hoverinfo='skip', showlegend=False
                        ))

                # Add annotation showing total angle and excess
                # Position text above the configuration
                traces.append(go.Scatter3d(
                    x=[0], y=[0], z=[1.8],
                    mode='text',
                    text=f'{count}×{interior_angle:.0f}° = {total_angle:.0f}°',
                    textfont=dict(size=14, color='red', family='Arial Black'),
                    hoverinfo='skip', showlegend=False
                ))

                traces.append(go.Scatter3d(
                    x=[0], y=[0], z=[1.5],
                    mode='text',
                    text=f'Přebytek: {excess_angle:.0f}°',
                    textfont=dict(size=12, color='darkred'),
                    hoverinfo='skip', showlegend=False
                ))

                # Add circular diagram showing angular excess
                # Draw a circle representing 360° and show the excess
                circle_radius = 0.4
                circle_z = -1.2

                # Draw 360° circle (green arc)
                theta_360 = np.linspace(0, 2 * np.pi, 100)
                circle_x = circle_radius * np.cos(theta_360)
                circle_y = circle_radius * np.sin(theta_360)
                circle_z_arr = np.full_like(theta_360, circle_z)

                traces.append(go.Scatter3d(
                    x=circle_x, y=circle_y, z=circle_z_arr,
                    mode='lines',
                    line=dict(color='green', width=4),
                    hoverinfo='skip', showlegend=False
                ))

                # Draw excess arc (red arc extending beyond 360°)
                if excess_angle > 0:
                    excess_radians = np.radians(excess_angle)
                    theta_excess = np.linspace(0, excess_radians, 50)
                    excess_x = circle_radius * np.cos(theta_excess)
                    excess_y = circle_radius * np.sin(theta_excess)
                    excess_z = np.full_like(theta_excess, circle_z)

                    traces.append(go.Scatter3d(
                        x=excess_x, y=excess_y, z=excess_z,
                        mode='lines',
                        line=dict(color='red', width=6),
                        hoverinfo='skip', showlegend=False
                    ))

                # Label for diagram
                traces.append(go.Scatter3d(
                    x=[0], y=[0], z=[circle_z - 0.3],
                    mode='text',
                    text='360°',
                    textfont=dict(size=10, color='green'),
                    hoverinfo='skip', showlegend=False
                ))

            else:
                # Normal rendering for valid and planar configurations
                for i in range(count):
                    e1 = edges[i]
                    e2 = edges[(i + 1) % count]

                    verts = self._create_face(e1, e2, n)

                    # Create mesh
                    x_coords = [v[0] for v in verts]
                    y_coords = [v[1] for v in verts]
                    z_coords = [v[2] for v in verts]

                    # Triangulate from origin
                    i_indices, j_indices, k_indices = [], [], []
                    for vtx_idx in range(1, len(verts) - 1):
                        i_indices.append(0)
                        j_indices.append(vtx_idx)
                        k_indices.append(vtx_idx + 1)

                    traces.append(go.Mesh3d(
                        x=x_coords, y=y_coords, z=z_coords,
                        i=i_indices, j=j_indices, k=k_indices,
                        color=color, opacity=0.75, flatshading=False, hoverinfo='skip'
                    ))

                    # Edges
                    for vtx_idx in range(len(verts)):
                        v1, v2 = verts[vtx_idx], verts[(vtx_idx + 1) % len(verts)]
                        traces.append(go.Scatter3d(
                            x=[v1[0], v2[0]], y=[v1[1], v2[1]], z=[v1[2], v2[2]],
                            mode='lines', line=dict(color=edge_color, width=4),
                            hoverinfo='skip', showlegend=False
                        ))

        # Central vertex
        traces.append(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers+text',
            marker=dict(size=12, color='darkblue'),
            text=f'{total_angle:.0f}°',
            textposition='top center',
            textfont=dict(size=10, color='black'),
            hoverinfo='skip', showlegend=False
        ))

        return traces

    def _get_edges_from_origin(self, n: int, count: int, planar: bool) -> List[np.ndarray]:
        """Get edge directions from origin that form faces with equal edge lengths"""
        interior_angle = (n - 2) * 180 / n
        total_angle = count * interior_angle

        edge_length = 1.0
        edges = []

        if planar or total_angle >= 360:
            # Planar: edges in xy-plane
            for i in range(count):
                angle = np.radians(i * 360 / count)
                edges.append(edge_length * np.array([np.cos(angle), np.sin(angle), 0.0]))
            return edges

        # 3D cases with equal edge lengths
        if n == 3:  # Triangles
            # For equilateral triangles: edges at specific elevation
            # cos(elev) = 1/√3 for equilateral faces
            elev = np.arccos(1.0 / np.sqrt(3))  # ≈ 54.74°
            for i in range(count):
                azim = np.radians(i * 360 / count)
                edges.append(edge_length * np.array([
                    np.cos(elev) * np.cos(azim),
                    np.cos(elev) * np.sin(azim),
                    np.sin(elev)
                ]))
            return edges

        elif n == 4:  # Squares
            # For cube: perpendicular edges
            if count == 3:
                edges = [
                    edge_length * np.array([1.0, 0.0, 0.0]),
                    edge_length * np.array([0.0, 1.0, 0.0]),
                    edge_length * np.array([0.0, 0.0, 1.0])
                ]
                return edges
            else:
                for i in range(count):
                    angle = np.radians(i * 360 / count)
                    edges.append(edge_length * np.array([np.cos(angle), np.sin(angle), 0.0]))
                return edges

        elif n == 5:  # Pentagons (impossible cases)
            for i in range(count):
                angle = np.radians(i * 360 / count)
                edges.append(edge_length * np.array([np.cos(angle), np.sin(angle), 0.0]))
            return edges

        elif n == 6:  # Hexagons
            for i in range(count):
                angle = np.radians(i * 360 / count)
                edges.append(edge_length * np.array([np.cos(angle), np.sin(angle), 0.0]))
            return edges

        # Default fallback
        for i in range(count):
            angle = np.radians(i * 360 / count)
            edges.append(edge_length * np.array([np.cos(angle), np.sin(angle), 0.3]))
        return edges

    def _create_face(self, e1: np.ndarray, e2: np.ndarray, n: int) -> List[np.ndarray]:
        """Create a face with n vertices: origin + (n-1) outer vertices"""
        origin = np.array([0.0, 0.0, 0.0])
        edge_len = np.linalg.norm(e1)

        if n == 3:
            # Triangle: origin + 2 edges
            return [origin, e1, e2]

        elif n == 4:
            # Square: origin + e1 + (e1+e2) + e2
            return [origin, e1, e1 + e2, e2]

        elif n == 5:
            # Pentagon with origin as one vertex
            # Vertices: origin, e1, v2, v3, e2 (where v2, v3 are intermediate)

            # Create orthonormal basis in the face plane
            u = e1 / np.linalg.norm(e1)
            normal = np.cross(e1, e2)
            if np.linalg.norm(normal) < 1e-10:
                return [origin, e1, e2]
            normal = normal / np.linalg.norm(normal)
            v = np.cross(normal, u)
            v = v / np.linalg.norm(v)

            # For a regular pentagon with one vertex at origin,
            # interior angle at origin = 108°
            # We need 5 vertices: origin, e1, v2, v3, e2
            # Angles from e1: 0°, 108°, 216°, 324° (back to near origin)
            verts = [origin]

            # v1 = e1 (angle 0°)
            verts.append(e1)

            # v2 at 108° from e1
            angle2 = np.radians(108)
            v2 = edge_len * (np.cos(angle2) * u + np.sin(angle2) * v)
            verts.append(v2)

            # v3 at 216° from e1
            angle3 = np.radians(216)
            v3 = edge_len * (np.cos(angle3) * u + np.sin(angle3) * v)
            verts.append(v3)

            # v4 = e2 (should be at ~288° from e1 for regular pentagon)
            verts.append(e2)

            return verts

        elif n == 6:
            # Hexagon with origin as one vertex
            # For regular hexagon: vertices at origin, e1, v2, v3, v4, e2
            # Consecutive edges turn by exterior angle = 60° (since interior = 120°)

            u = e1 / np.linalg.norm(e1)
            normal = np.cross(e1, e2)
            if np.linalg.norm(normal) < 1e-10:
                return [origin, e1, e2]
            normal = normal / np.linalg.norm(normal)
            v = np.cross(normal, u)
            v = v / np.linalg.norm(v)

            # Start at origin, go to e1, then turn 60° at each step
            verts = [origin, e1]
            current_pos = e1.copy()
            current_dir = e1 / edge_len  # Direction from origin to e1

            # Create 4 intermediate vertices (total 6: origin, e1, v2, v3, v4, e2)
            for i in range(4):
                # Turn by exterior angle 60°
                angle = np.radians((i+1) * 60)
                new_dir = np.cos(angle) * u + np.sin(angle) * v
                current_pos = current_pos + edge_len * new_dir

                # Last vertex should be e2, not computed
                if i < 3:
                    verts.append(current_pos)

            verts.append(e2)
            return verts

        return [origin, e1, e2]
