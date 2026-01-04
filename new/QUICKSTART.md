# 🚀 Quick Start Guide

## Spuštění aplikace

### 1. Instalace (pouze jednou)

```bash
cd /home/user/platonska-telesa/new
pip3 install -r requirements.txt
```

### 2. Spuštění

```bash
streamlit run app.py
```

Aplikace se otevře na **http://localhost:8501**

---

## 🎯 Jak používat aplikaci

### Navigace:

1. **Postranní panel (vlevo):**
   - Klikni na jakýkoliv krok pro přechod
   - Kroky jsou organizovány podle kategorií

2. **Hlavní okno:**
   - **Levá strana:** Interaktivní 3D diagram
     - Můžeš diagram otáčet myší!
   - **Pravá strana:** Podrobné vysvětlení

3. **Navigační tlačítka:**
   - "⬅️ Předchozí" / "Další ➡️"
   - Nacházejí se nahoře i dole stránky

---

## ➕ Jak přidat nové kroky

### Příklad: Přidání kroku pro Osmistěn

#### 1. Vytvoř nový soubor `octahedron.py`

```bash
cd steps/definitions/
touch octahedron.py
```

#### 2. Napiš třídu kroku

```python
# steps/definitions/octahedron.py
import numpy as np
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D

class OctaStep1_Axes(Step):
    """Osmistěn - Krok 1: Vrcholy na osách"""

    def __init__(self):
        super().__init__()
        # Data pro tento krok
        self.vertices = np.array([
            [ 1,  0,  0],  # +X
            [-1,  0,  0],  # -X
            [ 0,  1,  0],  # +Y
            [ 0, -1,  0],  # -Y
            [ 0,  0,  1],  # +Z
            [ 0,  0, -1]   # -Z
        ])

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=4,  # Číslo kroku (pokračování po čtyřstěnu)
            category='Osmistěn',
            title='Osmistěn - Krok 1: Vrcholy na osách',
            short_name='1. Vrcholy na osách'
        )

    def get_description(self) -> str:
        return """
## Osmistěn - Krok 1: Vrcholy na osách

### 6 vrcholů na osách:

```
( 1,  0,  0) → +X (červený)
(-1,  0,  0) → -X (červený)
( 0,  1,  0) → +Y (zelený)
( 0, -1,  0) → -Y (zelený)
( 0,  0,  1) → +Z (modrý)
( 0,  0, -1) → -Z (modrý)
```

### Proč zrovna na osách?

Osmistěn má vrcholy **symetricky** umístěné...
"""

    def render_diagram(self, fig, ax):
        """Vykreslení diagramu"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Nakresli osy
        Renderer3D.draw_axes_arrows(ax, length=1.5)

        # Nakresli vrcholy
        labels = ['+X', '-X', '+Y', '-Y', '+Z', '-Z']
        colors = ['red', 'red', 'green', 'green', 'blue', 'blue']

        Renderer3D.draw_points(
            ax, self.vertices,
            colors=colors,
            sizes=150,
            labels=labels
        )
```

#### 3. Zaregistruj krok v `app.py`

```python
# app.py
from steps.definitions.octahedron import OctaStep1_Axes  # Přidej import

def register_all_steps():
    registry = get_registry()
    registry.clear()

    # Existující kroky
    registry.register(IntroStep())
    registry.register(TetraStep1_Cube())
    registry.register(TetraStep2_Selection())
    registry.register(TetraStep3_Complete())

    # NOVÝ KROK - přidej zde!
    registry.register(OctaStep1_Axes())
```

#### 4. Restartuj aplikaci

```bash
# Zastav běžící app (Ctrl+C) a spusť znovu:
streamlit run app.py
```

**Hotovo!** Nový krok se objeví v sidebaru pod kategorií "Osmistěn".

---

## 🎨 Dostupné pomocné funkce

### Renderer3D helper funkce:

```python
from views.renderer import Renderer3D

# Nakresli bod
Renderer3D.draw_point(ax, [1, 2, 3], color='red', size=150, label='A')

# Nakresli více bodů
points = np.array([[0,0,0], [1,1,1], [2,2,2]])
Renderer3D.draw_points(ax, points, colors='blue', sizes=100)

# Nakresli hranu
Renderer3D.draw_edge(ax, [0,0,0], [1,1,1], color='green', width=3)

# Nakresli více hran
vertices = np.array([[...], [...], ...])
edges = [(0,1), (1,2), (2,0)]  # Indexy vrcholů
Renderer3D.draw_edges(ax, vertices, edges, color='red')

# Nakresli osy souřadného systému
Renderer3D.draw_axes_arrows(ax, length=2.0)

# Nakresli rovinu
Renderer3D.draw_plane(ax, normal='z', offset=0, color='orange', alpha=0.2)
```

### Geometry helper třídy:

```python
from models.geometry import Point3D, Edge, GeometryHelper

# Vytvoř bod
p1 = Point3D(1, 2, 3)
p2 = Point3D(4, 5, 6)

# Vypočítej vzdálenost
distance = p1.distance_to(p2)

# Vypočítej střed bodů
points = [Point3D(0,0,0), Point3D(2,2,2)]
center = GeometryHelper.calculate_centroid(points)
```

---

## 🔧 Změna nastavení

Všechna nastavení jsou v `config/settings.py`:

```python
# Změň velikost diagramu
FIGURE = {
    'figsize': (10, 8),  # Větší
    'dpi': 150,          # Vyšší kvalita
}

# Změň barvy
COLORS = {
    'selected_point': 'orange',  # Místo červené
    'tetrahedron': '#FF6B6B',
}

# Změň limity os
PLOT_3D = {
    'axis_limits': (-3, 3),  # Větší rozsah
}
```

---

## 📊 Současný stav aplikace

✅ **Hotové kroky:**
- Krok 0: Úvod
- Krok 1-3: Čtyřstěn (kompletní)

🚧 **Zbývá přidat:**
- Kroky 4-5: Osmistěn
- Kroky 6-8: Dvacetistěn
- Kroky 9-12: Dvanáctistěn
- Krok 13: Bonus (střed trojúhelníku)

---

## 🐛 Časté problémy

### Aplikace se nespustí:

```bash
# Zkontroluj instalaci:
pip3 list | grep streamlit

# Reinstaluj:
pip3 install --upgrade streamlit
```

### Import error:

```bash
# Ujisti se, že jsi ve správné složce:
pwd  # Mělo by ukazovat: /home/user/platonska-telesa/new

# Spusť z kořenové složky new/:
streamlit run app.py
```

### Diagram se nevykresluje:

```python
# Zkontroluj, že používáš správný import:
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
```

---

## 💡 Tipy pro vývoj

1. **Hot reload:** Streamlit automaticky načte změny při uložení souboru
2. **Debug:** Použij `st.write(data)` pro výpis proměnných
3. **Testování:** Nejdřív otestuj krok v Pythonu, pak přidej do app
4. **Organizace:** Jeden soubor = jedna kategorie (tetrahedron.py, octahedron.py...)

---

**Hodně štěstí s vývojem! 🎓**
