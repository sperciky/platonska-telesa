"""
Úvodní kroky prezentace
Introduction steps
"""
import numpy as np
from matplotlib.figure import Figure
import plotly.graph_objects as go
from steps.base_step import Step, StepMetadata
from config.settings import APP_INFO
from views.plotly_renderer import PlotlyRenderer3D


class IntroStep(Step):
    """Úvodní krok - představení tutoriálu"""

    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=0,
            category='Úvod',
            title='Vítejte v tutoriálu!',
            short_name='Úvod'
        )

    def get_description(self) -> str:
        return f"""
# {APP_INFO['title']}

## Co se naučíš:

1. **Čtyřstěn** (4 vrcholy, 6 hran, 4 stěny)
2. **Osmistěn** (6 vrcholů, 12 hran, 8 stěn)
3. **Dvacetistěn** (12 vrcholů, 30 hran, 20 stěn)
4. **Dvanáctistěn** (20 vrcholů, 30 hran, 12 stěn)
5. **Bonus:** Střed trojúhelníku

---

### Jak používat tento tutoriál:

- **Vlevo:** 3D interaktivní diagram
- **Vpravo:** Vysvětlení krok za krokem
- **Postranní panel:** Navigace mezi kroky

---

### Zajímavost:

Existuje pouze **5 pravidelných mnohostěnů**! Toto tvrzení dokázali už staří Řekové.

**Platónská tělesa** mají zvláštní vlastnosti:
- Všechny stěny jsou stejné pravidelné mnohoúhelníky
- V každém vrcholu se schází stejný počet stěn
- Mají dokonalou symetrii

---

👈 **Začni výběrem kroku v postranním panelu!**
"""

    def render_diagram(self, fig: Figure, ax) -> None:
        """Úvodní diagram - prázdné 3D osy (matplotlib - legacy)"""
        self.setup_axes(ax)
        ax.set_title(self.metadata.title, fontsize=16, fontweight='bold', pad=20)

        # Zobraz jen osy bez dat
        ax.grid(True, alpha=0.3)

    def render_plotly_diagram(self) -> go.Figure:
        """Úvodní diagram - prázdné 3D osy (Plotly - interaktivní)"""
        fig = PlotlyRenderer3D.create_figure(axis_limits=(-2, 2))
        fig = PlotlyRenderer3D.add_title(fig, self.metadata.title)

        # Prázdný diagram - zobrazí jen osy
        return fig
