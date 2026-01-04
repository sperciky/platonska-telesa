"""
Základní třída pro kroky prezentace
Base class for presentation steps using Template Method pattern
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import plotly.graph_objects as go


@dataclass
class StepMetadata:
    """Metadata o kroku"""
    number: int
    category: str  # 'intro', 'tetrahedron', 'octahedron', atd.
    title: str
    short_name: str  # Pro sidebar


class Step(ABC):
    """
    Abstraktní základní třída pro jeden krok prezentace

    Každý krok musí implementovat:
    - get_metadata(): metadata o kroku
    - get_description(): popisný text v češtině
    - render_diagram(): vykreslení matplotlib diagramu (legacy)
    - render_plotly_diagram(): vykreslení interaktivního Plotly diagramu
    """

    def __init__(self):
        self._metadata: Optional[StepMetadata] = None

    @property
    def metadata(self) -> StepMetadata:
        """Vrátí metadata kroku (lazy loading)"""
        if self._metadata is None:
            self._metadata = self.get_metadata()
        return self._metadata

    @abstractmethod
    def get_metadata(self) -> StepMetadata:
        """
        Vrátí metadata o kroku

        Returns:
            StepMetadata s informacemi o kroku
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Vrátí popisný text v češtině

        Returns:
            Český text s popisem kroku (může obsahovat markdown)
        """
        pass

    @abstractmethod
    def render_diagram(self, fig: Figure, ax) -> None:
        """
        Vykreslí 3D diagram pro tento krok (matplotlib - legacy)

        Args:
            fig: Matplotlib Figure instance
            ax: Matplotlib 3D Axes instance
        """
        pass

    @abstractmethod
    def render_plotly_diagram(self) -> go.Figure:
        """
        Vykreslí interaktivní 3D diagram pomocí Plotly

        Returns:
            Plotly Figure instance s interaktivním 3D diagramem
        """
        pass

    def get_render_config(self) -> Dict[str, Any]:
        """
        Vrátí konfiguraci pro vykreslení (volitelné přepsání)

        Returns:
            Dictionary s nastavením pro vykreslení
        """
        from config.settings import PLOT_3D
        return {
            'axis_limits': PLOT_3D['axis_limits'],
            'box_aspect': PLOT_3D['box_aspect'],
            'elevation': PLOT_3D['elevation'],
            'azimuth': PLOT_3D['azimuth'],
        }

    def setup_axes(self, ax) -> None:
        """Nastaví osy podle konfigurace (helper metoda)"""
        config = self.get_render_config()
        limits = config['axis_limits']

        ax.set_xlim([limits[0], limits[1]])
        ax.set_ylim([limits[0], limits[1]])
        ax.set_zlim([limits[0], limits[1]])
        ax.set_box_aspect(config['box_aspect'])
        ax.view_init(elev=config['elevation'], azim=config['azimuth'])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    def __str__(self) -> str:
        return f"Step {self.metadata.number}: {self.metadata.title}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(number={self.metadata.number})>"
