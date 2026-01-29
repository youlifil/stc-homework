"""
Модуль для парсинга файлов конфига.

Содержит функции для чтения и преобразования данных из JSON-файлов
в объекты конфигурации, используемые в решателе.
"""

import json
import re
from datetime import datetime
from typing import Any

from solver import SolverConfig, GeoCoordinate, GeoPosition


COORDINATE_PATTERN = r'(\d+)g(\d+)m(\d+)s'


def parse_geo_coordinate(coord_str: str) -> GeoCoordinate:
    """
    Парсит строчку с географической координатой в формате'XgYmZs'.
    Например координата 51°40′18″ задаётся строкой '51g40m18s'
    
    Args:
        coord_str (str): Строка координаты в формате '<градусы>g<минуты>m<секунды>s'.
        
    Returns:
        GeoCoordinate: Объект географической координаты.
        
    Raises:
        ValueError: Если строка не соответствует указанному выше паттерну.
    """
    parsed_coord = re.match(COORDINATE_PATTERN, coord_str)

    if not parsed_coord:
        raise ValueError(f"Плохой формат координаты: {coord_str}")

    return GeoCoordinate(
        deg=int(parsed_coord.group(1)),
        min=int(parsed_coord.group(2)),
        sec=int(parsed_coord.group(3))
    )


def parse_time(time_str: str) -> datetime:
    """
    Парсит строку времени в формате ISO 8601.
    
    Args:
        time_str (str): Строка времени в формате ISO 8601.
        
    Returns:
        datetime: Объект datetime.
    """
    return datetime.fromisoformat(time_str)


def parse_float(value_str: str) -> float:
    """
    Преобразует строку во float.
    
    Args:
        value_str (str): Строка, содержащая число.
        
    Returns:
        float: Число с плавающей точкой.
    """
    return float(value_str)


def parse_bool(value_str: str) -> bool:
    """
    Преобразует строку в bool. 
    
    Args:
        value_str (str): Строка 'true' или 'false' (в любом регистре).
        
    Returns:
        bool: Булево значение.
        
    Raises:
        ValueError: Если строка не содержит 'true' или 'false'.
    """
    if value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False
    else:
        raise ValueError(f"Плохой формат булевого значения: {value_str}")


def parse_config(config_file: str) -> SolverConfig:
    """
    Парсит JSON-файл конфига и создает на его основе объект SolverConfig.
    
    Args:
        config_file (str): Путь к JSON-файлу конфига.
        
    Returns:
        SolverConfig: Объект конфигурации решателя.
        
    Raises:
        FileNotFoundError: Если файл не найден.
        JSONDecodeError: Если файл содержит некорректный JSON.
        KeyError: Если в JSON отсутствуют обязательные поля.
        ValueError: Если значения полей имеют некорректный формат.
    """
    with open(config_file, 'r', encoding='ascii') as file:
        data: dict[str, Any] = json.load(file)

    lat: GeoCoordinate = parse_geo_coordinate(data["observer"]["latitude"])
    lon: GeoCoordinate = parse_geo_coordinate(data["observer"]["longitude"])
    pos: GeoPosition = GeoPosition(latitude=lat, longitude=lon)

    return SolverConfig(
        observer_position=pos,
        start_time=parse_time(data['start_time']),
        end_time=parse_time(data['end_time']),
        antenna_elevation=parse_float(data['antenna_elevation']),
        antenna_azimuth=parse_float(data['antenna_azimuth']),
        antenna_aspect_angle=parse_float(data['antenna_aspect_angle']),
        time_step=parse_float(data['time_step']),
        find_nearest_sat=parse_bool(data['find_nearest_sat'])
    )
