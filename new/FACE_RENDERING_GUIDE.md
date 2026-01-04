# Guide pro vykreslování stěn / Face Rendering Guide

## Přehled / Overview

Aplikace podporuje vykreslování stěn (ploch) 3D těles s nastavitelnou průhledností.
Uživatel může zapnout/vypnout stěny a řídit jejich průhlednost pomocí ovládacích prvků v postranním menu.

## Globální nastavení / Global Settings

V `st.session_state` jsou uloženy:
- `show_faces` (bool): Zapne/vypne vykreslování stěn
- `face_opacity` (float 0.0-1.0): Průhlednost stěn (0.0 = průhledné, 1.0 = neprůhledné)

Tyto hodnoty přetrvávají mezi kroky.

## Jak přidat stěny do kroku / How to Add Faces to a Step

### 1. Import Streamlit

```python
import streamlit as st
```

### 2. Definuj stěny v `__init__()`

```python
def __init__(self):
    super().__init__()

    # Vrcholy
    self.vertices = np.array([...])

    # Hrany
    self.edges = [...]

    # Stěny (seznamy indexů vrcholů)
    self.faces = [
        [0, 1, 2],      # Trojúhelník
        [3, 4, 5, 6],   # Čtyřúhelník
        [7, 8, 9, 10, 11]  # Pětiúhelník
    ]
```

### 3. Vykresli stěny v `render_plotly_diagram()`

```python
def render_plotly_diagram(self) -> go.Figure:
    fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))

    # Zkontroluj, zda jsou stěny zapnuté
    if st.session_state.get('show_faces', False):
        opacity = st.session_state.get('face_opacity', 0.3)

        # Vykresli stěny
        fig = PlotlyRenderer3D.add_faces(
            fig, self.vertices, self.faces,
            color='cyan',  # Barva stěn
            opacity=opacity
        )

    # ... zbytek vykreslování (hrany, vrcholy)

    return fig
```

## Podpora pro více objektů / Multiple Objects Support

Pro duální tělesa nebo více objektů v jednom kroku:

```python
def render_plotly_diagram(self) -> go.Figure:
    fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))

    if st.session_state.get('show_faces', False):
        opacity = st.session_state.get('face_opacity', 0.3)

        # Objekt 1 - Čtyřstěn (azurová barva)
        fig = PlotlyRenderer3D.add_faces(
            fig, self.tetra_vertices, self.tetra_faces,
            color='cyan', opacity=opacity
        )

        # Objekt 2 - Osmistěn (růžová barva)
        fig = PlotlyRenderer3D.add_faces(
            fig, self.octa_vertices, self.octa_faces,
            color='pink', opacity=opacity
        )

    # ... hrany a vrcholy pro oba objekty

    return fig
```

## Podporované typy stěn / Supported Face Types

- **Trojúhelníky** (3 vrcholy): Přímo vykresleny pomocí Mesh3d
- **Čtyřúhelníky** (4 vrcholy): Rozděleny na 2 trojúhelníky
- **Pětiúhelníky** (5 vrcholů): Rozděleny na 3 trojúhelníky

## API Reference

### PlotlyRenderer3D.add_face()

```python
PlotlyRenderer3D.add_face(
    fig: go.Figure,
    vertices: np.ndarray,      # Všechny vrcholy
    face_indices: List[int],   # Indexy vrcholů této stěny
    color: str = 'lightblue',  # Barva stěny
    opacity: float = 0.3,      # Průhlednost
    show_edges: bool = False   # Zobrazit okraje (zatím neimplementováno)
) -> go.Figure
```

### PlotlyRenderer3D.add_faces()

```python
PlotlyRenderer3D.add_faces(
    fig: go.Figure,
    vertices: np.ndarray,        # Všechny vrcholy
    faces: List[List[int]],      # Seznam stěn
    color: str = 'lightblue',    # Barva všech stěn
    opacity: float = 0.3         # Průhlednost
) -> go.Figure
```

## Příklad: Kompletní tetrahedron / Example: Complete Tetrahedron

Viz: `steps/definitions/tetrahedron.py` - třída `TetraStep3_Complete`

## Doporučené barvy pro stěny / Recommended Face Colors

- Čtyřstěn: `'cyan'`
- Osmistěn: `'lightgreen'`
- Dvacetistěn: `'lightyellow'`
- Dvanáctistěn: `'lightpink'`
- Krychle: `'lightgray'`

Pro duální tělesa použij kontrastní barvy (např. `'cyan'` a `'pink'`).
