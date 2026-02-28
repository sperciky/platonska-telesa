#!/usr/bin/env python3
"""Debug pentagon geometry calculation"""

import math

def create_pentagon_vertices():
    """Create vertices of a regular pentagon in a plane"""

    # Edge length
    edge_len = 1.0

    # Origin at (0, 0, 0)
    origin = (0.0, 0.0, 0.0)

    # First edge goes to (1, 0, 0)
    e1 = (1.0, 0.0, 0.0)

    print("Regular Pentagon Vertices:")
    print(f"v0 (origin): {origin}")
    print(f"v1: {e1}")

    # Current position and direction
    current_pos = list(e1)
    current_dir = [1.0, 0.0, 0.0]  # Direction from origin to v1

    # Exterior angle for regular pentagon = 360/5 = 72°
    exterior_angle_deg = 72
    exterior_angle_rad = math.radians(exterior_angle_deg)

    vertices = [origin, e1]

    # Walk around the pentagon
    for i in range(3):  # Create v2, v3, v4
        # Rotate direction by 72° (counterclockwise in xy-plane)
        cos_a = math.cos(exterior_angle_rad)
        sin_a = math.sin(exterior_angle_rad)

        # 2D rotation in xy-plane
        new_dir_x = current_dir[0] * cos_a - current_dir[1] * sin_a
        new_dir_y = current_dir[0] * sin_a + current_dir[1] * cos_a
        current_dir = [new_dir_x, new_dir_y, 0.0]

        # Move by edge length
        current_pos = [
            current_pos[0] + edge_len * current_dir[0],
            current_pos[1] + edge_len * current_dir[1],
            current_pos[2] + edge_len * current_dir[2]
        ]

        vertices.append(tuple(current_pos))
        print(f"v{i+2}: ({current_pos[0]:.4f}, {current_pos[1]:.4f}, {current_pos[2]:.4f})")

    # Check if v4 connects back to origin
    print(f"\nCheck: Distance from v4 to origin:")
    v4 = vertices[4]
    dist = math.sqrt(v4[0]**2 + v4[1]**2 + v4[2]**2)
    print(f"  Distance: {dist:.4f} (should be ~{edge_len:.4f})")

    # Check interior angles
    print(f"\nInterior angles (should all be 108°):")

    # Angle at origin (between v4->v0->v1)
    # Vector from v0 to v1
    v01 = (e1[0], e1[1], e1[2])
    # Vector from v0 to v4
    v04 = (v4[0], v4[1], v4[2])

    # Dot product
    dot = v01[0]*v04[0] + v01[1]*v04[1] + v01[2]*v04[2]
    mag01 = math.sqrt(v01[0]**2 + v01[1]**2 + v01[2]**2)
    mag04 = math.sqrt(v04[0]**2 + v04[1]**2 + v04[2]**2)

    if mag01 > 0 and mag04 > 0:
        cos_angle = dot / (mag01 * mag04)
        # Clamp to [-1, 1] to avoid math domain errors
        cos_angle = max(-1.0, min(1.0, cos_angle))
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
        print(f"  Angle at v0 (origin): {angle_deg:.1f}°")

if __name__ == "__main__":
    create_pentagon_vertices()
