"""
Bonusový krok - proč existuje pouze 5 Platónských těles
Bonus step - proof of why only 5 Platonic solids exist
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
import streamlit as st
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D
from views.plotly_renderer import PlotlyRenderer3D


class BonusStep_WhyOnlyFive(Step):
    """Bonus: Proč existuje pouze 5 Platónských těles?"""

    def __init__(self):
        super().__init__()
        # Pro vizualizaci úhlů
        pass

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=17,
            category='Bonus',
            title='Bonus: Proč jich není více?',
            short_name='Proč jen 5?'
        )

    def get_description(self) -> str:
        return """
## Bonus: Proč existuje pouze 5 Platónských těles?

### Definice Platónských těles:

Platónské těleso musí splňovat:

1. **Těleso tvoří pravidelné mnohoúhelníky** (všechny strany a úhly stejné)
2. **Z každého vrcholu vychází stejný počet hran**
3. **V každém bodě se potkávají alespoň 3 stěny**
4. **Výsledné těleso musí být konvexní** → součet úhlů u vrcholu **< 360°**

---

### Důkaz: Proč jen 5 těles?

Díky těmto podmínkám můžeme pracovat pouze s **jedním bodem**.

---

### 1️⃣ Nejmenší mnohoúhelník: **Trojúhelník** (vnitřní úhel 60°)

Kolik trojúhelníků se může potkat v jednom vrcholu?

🔺 **3 trojúhelníky:** 3 × 60° = **180°** < 360° ✅ → **ČTYŘSTĚN** (tetraedr)

🔺 **4 trojúhelníky:** 4 × 60° = **240°** < 360° ✅ → **OSMISTĚN** (oktaedr)

🔺 **5 trojúhelníků:** 5 × 60° = **300°** < 360° ✅ → **DVACETISTĚN** (ikosaedr)

🔺 **6 trojúhelníků:** 6 × 60° = **360°** ❌ → rovinné, není konvexní

---

### 2️⃣ Následuje čtverec: **Čtverec** (vnitřní úhel 90°)

Kolik čtverců se může potkat v jednom vrcholu?

🟦 **3 čtverce:** 3 × 90° = **270°** < 360° ✅ → **KRYCHLE** (hexaedr)

🟦 **4 čtverce:** 4 × 90° = **360°** ❌ → rovinné, není konvexní

---

### 3️⃣ Další je pětiúhelník: **Pětiúhelník** (vnitřní úhel 108°)

Kolik pětiúhelníků se může potkat v jednom vrcholu?

🟫 **3 pětiúhelníky:** 3 × 108° = **324°** < 360° ✅ → **DVANÁCTISTĚN** (dodekaedr)

🟫 **4 pětiúhelníky:** 4 × 108° = **432°** > 360° ❌ → překročen limit!

---

### 4️⃣ Šestiúhelník a více: **Šestiúhelník** (vnitřní úhel 120°)

⬡ **3 šestiúhelníky:** 3 × 120° = **360°** ❌ → rovinné, není konvexní

Všechny další mnohoúhelníky (sedmiúhelník, osmiúhelník...) mají **větší úhel než 120°**,
takže by **přesáhly limit**, protože by pokračoval **šestiúhelník**, který má vnitřní úhel 120°.

A tři (120° krát 3 je 360°) by **leželi na rovině** a těleso by se z nich **nestát nemohlo**.

---

### ✨ Závěr: Pouze 5 Platónských těles!

| Těleso | Stěny | Vrcholy v jednom bodě | Součet úhlů |
|--------|-------|----------------------|-------------|
| Čtyřstěn | 3 trojúhelníky | 3 × 60° | 180° ✅ |
| Osmistěn | 4 trojúhelníky | 4 × 60° | 240° ✅ |
| Dvacetistěn | 5 trojúhelníků | 5 × 60° | 300° ✅ |
| Krychle | 3 čtverce | 3 × 90° | 270° ✅ |
| Dvanáctistěn | 3 pětiúhelníky | 3 × 108° | 324° ✅ |

**Více už jich být nemůže**, protože by **přesáhly limit 360°** nebo by **pokračoval šestiúhelník**,
který má vnitřní úhel 120° a tři (120° krát 3 je 360°) by **leželi na rovině**
a těleso by se z nich **nestát nemohlo**.

---

### 🎓 Matematická krása:

Toto je **úplný důkaz**! Nemusíme zkoušet všechny možnosti -
**matematika nám zaručuje**, že jiná Platónská tělesa **nemohou existovat**.

Proto staří Řekové považovali těchto 5 těles za **dokonalá** a **posvátná**!
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Vykreslení vizualizace úhlů (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=14, fontweight='bold')

        # Simple text display
        ax.text(0, 0.5, 'Viz popis vpravo →',
                fontsize=20, ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('off')

    def render_plotly_diagram(self) -> go.Figure:
        """Vykreslení vizualizace důkazu (Plotly - interaktivní)"""
        # Create a figure showing the angular constraints
        fig = go.Figure()

        # Data for visualization
        solids = [
            ('Čtyřstěn', 3, 60, 180, 'green'),
            ('Osmistěn', 4, 60, 240, 'green'),
            ('Dvacetistěn', 5, 60, 300, 'green'),
            ('Krychle', 3, 90, 270, 'blue'),
            ('Dvanáctistěn', 3, 108, 324, 'orange'),
        ]

        impossible = [
            ('6 trojúhelníků', 6, 60, 360, 'red'),
            ('4 čtverce', 4, 90, 360, 'red'),
            ('4 pětiúhelníky', 4, 108, 432, 'red'),
            ('3 šestiúhelníky', 3, 120, 360, 'red'),
        ]

        # Create bar chart
        names = [s[0] for s in solids] + [i[0] for i in impossible]
        angles = [s[3] for s in solids] + [i[3] for i in impossible]
        colors = [s[4] for s in solids] + [i[4] for i in impossible]

        fig.add_trace(go.Bar(
            x=names,
            y=angles,
            marker_color=colors,
            text=[f'{a}°' for a in angles],
            textposition='outside',
            hovertemplate='%{x}<br>Součet úhlů: %{y}°<extra></extra>'
        ))

        # Add 360° limit line
        fig.add_hline(y=360, line_dash="dash", line_color="red",
                     annotation_text="Limit 360° (rovinné)",
                     annotation_position="right")

        fig.update_layout(
            title="Součet úhlů u vrcholu - Proč jen 5 Platónských těles?",
            xaxis_title="Konfigurace",
            yaxis_title="Součet úhlů (°)",
            yaxis_range=[0, 450],
            height=600,
            showlegend=False,
            hovermode='x unified'
        )

        return fig
