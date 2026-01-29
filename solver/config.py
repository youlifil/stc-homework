"""
Модуль содержит классы для параметров конфигурации для решателя
"""

from datetime import datetime
from dataclasses import dataclass


@dataclass
class GeoCoordinate:
    """
    Класс для представления географической координаты в формате градусы-минуты-секунды.

    Attributes:
        deg (int): Градусы.
        min (int): Минуты.
        sec (float): Секунды.
    """
    deg: int
    min: int
    sec: float


@dataclass
class GeoPosition:
    """
    Класс для представления географической позиции.

    Содержит информацию о долготе и широте позиции.
    
    Attributes:
        longitude (GeoCoordinate): Координата долготы.
        latitude (GeoCoordinate): Координата широты.
    """
    longitude: GeoCoordinate
    latitude: GeoCoordinate


@dataclass
class SolverConfig:
    """
    Класс конфигурации для решателя.
    
    Содержит все необходимые параметры для вычислений, связанный с решением тестового задания.
    
    Attributes:
        observer_position (GeoPosition): Географическая позиция наблюдателя.
        start_time (datetime): Время начала наблюдения, включительно.
        end_time (datetime): Время окончания наблюдения, включительно.
        antenna_elevation (float): Угол места направления антенны, в градусах.
        antenna_azimuth (float): Азимут направления антенны, в градусах.
        antenna_aspect_angle (float): Угол обзора антенны, в градусах.
        time_step (float, optional): Шаг по времени для вычислений, в секундах. По умолчанию 1.
        find_nearest_sat (bool, optional): Флаг, обозначающий, нужно ли искать ближайший спутник. 
                                           По умолчанию нужно.
    """
    observer_position: GeoPosition
    start_time: datetime
    end_time: datetime
    antenna_elevation: float
    antenna_azimuth: float
    antenna_aspect_angle: float
    time_step: float = 1
    find_nearest_sat: bool = True
