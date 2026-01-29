"""
Пакет solver - решатель для тестового задания.

Предоставляет типы для конфига решателя, и код, делающий необходимые вычисления для тестового.
"""
from .sat_visible import sat_visible
from .config import SolverConfig, GeoPosition, GeoCoordinate

__all__ = ["sat_visible", "SolverConfig", "GeoPosition", "GeoCoordinate"]
