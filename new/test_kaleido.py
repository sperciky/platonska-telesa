#!/usr/bin/env python3
"""Quick test to check if Kaleido is working."""

import plotly.graph_objects as go

print("Creating simple figure...")
fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=[0, 1], y=[0, 1], z=[0, 1],
    mode='markers',
    marker=dict(size=10)
))

print("Calling fig.to_image() - this may take 30-60s on first run...")
print("(If this hangs for >2 minutes, Ctrl+C and we'll try a different approach)")

try:
    img_bytes = fig.to_image(format='png', width=400, height=400, scale=1)
    print(f"✓ Success! Generated {len(img_bytes)} bytes")
    print("\nKaleido is working. The issue might be:")
    print("  1. Complex figures taking too long at 900px")
    print("  2. Try smaller size: --size 500")
    print("  3. Try simpler step: --steps 1")
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nKaleido is not working. Solutions:")
    print("  1. pip uninstall kaleido")
    print("  2. pip install kaleido==0.2.1")
    print("  3. Restart terminal/IDE")
    print("  4. Check antivirus isn't blocking kaleido.exe")
