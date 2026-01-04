"""
Základní geometrické třídy
Basic geometry classes for 3D structures
"""
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class Point3D:
    """Reprezentuje bod v 3D prostoru"""
    x: float
    y: float
    z: float

    @property
    def coords(self) -> np.ndarray:
        """Vrátí souřadnice jako numpy array"""
        return np.array([self.x, self.y, self.z])

    def distance_to(self, other: 'Point3D') -> float:
        """Vypočítá vzdálenost k jinému bodu"""
        return np.linalg.norm(self.coords - other.coords)

    def __iter__(self):
        """Umožní rozbalení: x, y, z = point"""
        return iter([self.x, self.y, self.z])


@dataclass
class Edge:
    """Reprezentuje hranu mezi dvěma vrcholy"""
    start: int  # Index počátečního vrcholu
    end: int    # Index koncového vrcholu

    def __iter__(self):
        """Umožní rozbalení: i, j = edge"""
        return iter([self.start, self.end])


@dataclass
class Face:
    """Reprezentuje stěnu (polygon)"""
    vertices: List[int]  # Indexy vrcholů tvořících stěnu

    def __iter__(self):
        """Umožní iteraci přes vrcholy"""
        return iter(self.vertices)


class GeometryHelper:
    """Pomocné geometrické funkce"""

    @staticmethod
    def calculate_edge_length(v1: Point3D, v2: Point3D) -> float:
        """Vypočítá délku hrany mezi dvěma body"""
        return v1.distance_to(v2)

    @staticmethod
    def calculate_centroid(points: List[Point3D]) -> Point3D:
        """Vypočítá těžiště (střed) množiny bodů"""
        coords = np.array([p.coords for p in points])
        center = np.mean(coords, axis=0)
        return Point3D(*center)

    @staticmethod
    def normalize_point(point: Point3D) -> Point3D:
        """Normalizuje bod na jednotkovou délku"""
        norm = np.linalg.norm(point.coords)
        if norm == 0:
            return point
        normalized = point.coords / norm
        return Point3D(*normalized)
