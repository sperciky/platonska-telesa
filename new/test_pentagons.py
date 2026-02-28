#!/usr/bin/env python3
"""Test script to visualize 4 pentagons configuration"""

import sys
import numpy as np
import plotly.graph_objects as go

# Add steps to path
sys.path.insert(0, 'steps/definitions')
from bonus_why_five_18d import BonusWhyFive18d

# Create instance
viz = BonusWhyFive18d()

# Configuration for 4 pentagons (impossible)
config = {
    'n': 5,           # Pentagon
    'count': 4,       # 4 pentagons
    'valid': False,   # Invalid configuration
    'planar': False   # Not planar (>360°)
}

# Generate traces
traces = viz._create_vertex_3d(config)

# Create figure
fig = go.Figure(data=traces)

# Update layout
fig.update_layout(
    title="4 Pentagons (Impossible Configuration)",
    scene=dict(
        xaxis=dict(visible=True, range=[-2, 2]),
        yaxis=dict(visible=True, range=[-2, 2]),
        zaxis=dict(visible=True, range=[-2, 2]),
        aspectmode='cube'
    ),
    width=800,
    height=800,
    showlegend=False
)

# Save to HTML
output_file = '/tmp/test_pentagons.html'
fig.write_html(output_file)
print(f"✓ Saved to: {output_file}")
print("\nConfiguration:")
print(f"  - Shape: Pentagon (5 sides)")
print(f"  - Count: 4")
print(f"  - Interior angle: 108°")
print(f"  - Total angle: 4 × 108° = 432°")
print(f"  - Excess: 432° - 360° = 72°")
print(f"\nExpected:")
print(f"  - 3 yellow pentagons (0-108°, 108-216°, 216-324°)")
print(f"  - 1 red pentagon overlapping (324-432° wraps to 0°)")
