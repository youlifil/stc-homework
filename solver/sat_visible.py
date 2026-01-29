"""
Модуль решателя для анализа видимости спутников.

Содержит функции для определения видимости спутников из заданной точки наблюдения
с использованием библиотеки Skyfield.
"""

from datetime import timedelta, timezone
from typing import List

import pandas as pd
import numpy as np
from skyfield.api import EarthSatellite, load, wgs84, Angle

from .config import SolverConfig, GeoPosition


def wgs84_observer_position(pos: GeoPosition):
    """
    Преобразует объект GeoPosition из конфига в координаты WGS84.
    
    Args:
        pos (GeoPosition): Объект географической позиции.
        
    Returns:
        wgs84.latlon: Объект позиции наблюдателя в системе WGS84.
    """
    lat_deg = pos.latitude.deg + pos.latitude.min/60 + pos.latitude.sec/3600
    lon_deg = pos.longitude.deg + pos.longitude.min/60 + pos.longitude.sec/3600
    return wgs84.latlon(lat_deg, lon_deg)


def sat_visible(tle_file: str, config: SolverConfig) -> None:
    """
    Анализирует видимость спутников на основе заданной конфигурации.
    
    Функция загружает данные о спутниках из TLE-файла, вычисляет их видимость
    из заданной точки наблюдения в указанный временной интервал и выводит
    результаты в консоль.
    
    Args:
        tle_file (str): Путь к TLE-файлу с данными спутников.
        config (SolverConfig): Конфиг решателя с параметрами наблюдения.
        
    Returns:
        None
        
    Raises:
        FileNotFoundError: Если TLE-файл не найден.
        ValueError: Если данные в TLE-файле некорректны.
    """
    # Временная шкала
    duration = (config.end_time - config.start_time).total_seconds()
    time_points = np.arange(0.0, duration + config.time_step, config.time_step)
    datetimes = [config.start_time + timedelta(seconds=float(dt)) for dt in time_points]

    ts = load.timescale()
    times = ts.from_datetimes(datetimes)

    n_time = len(times)


    # Загружаем спутники из TLE-файла
    satellites: List[EarthSatellite] = []
    norad_ids = []

    with open(tle_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i in range(0, len(lines), 3):
        sat = EarthSatellite(lines[i+1], lines[i+2], lines[i].strip(), ts)
        satellites.append(sat)
        norad_ids.append(sat.model.satnum)

    norad_ids = np.array(norad_ids)
    n_sat = len(satellites)


    # Положение наблюдателя
    observer = wgs84_observer_position(config.observer_position)


    # Положение спутников во времени
    sat_pos = np.empty((n_sat, n_time, 3))
    for i, sat in enumerate(satellites):
        sat_pos[i] = sat.at(times).position.km.T


    # Нормализованный вектор направления антенны
    antenna_vec = observer.at(times).from_altaz(
            az=Angle(degrees=config.antenna_azimuth),
            alt=Angle(degrees=config.antenna_elevation)
        ).position.km.T
    antenna_vec /= np.linalg.norm(antenna_vec, axis=1)[:, None]


    # Нормализованный вектор от наблюдателя к спутнику
    obs_pos = observer.at(times).position.km.T
    vec = sat_pos - obs_pos[None, :, :]
    u_sat = vec / np.linalg.norm(vec, axis=2, keepdims=True)


    # Косинус угла между антенной и направлением на спутник
    cos_theta = np.einsum("ijk,jk->ij", u_sat, antenna_vec)


    # Фильтруем по маске попадания в поле зрения антенны
    cos_limit = np.cos(np.deg2rad(config.antenna_aspect_angle / 2))

    visible_mask = np.any(cos_theta >= cos_limit, axis=1)
    visible_norad_ids = norad_ids[visible_mask]


    # Получаем видимые спутники
    df_visible = pd.DataFrame({
        "name": [sat.name for sat, visible in zip(satellites, visible_mask) if visible],
        "norad_id": norad_ids[visible_mask]
    })


    # Выводим результаты
    pd.set_option('display.max_rows', None) 
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None) 
    pd.set_option('display.width', None)
    
    print(df_visible)
    print(f"Найдено видимых спутников: {len(visible_norad_ids)}")


    if (config.find_nearest_sat):
        # Расстояние от наблюдателя до спутника (км)
        distances = np.linalg.norm(vec, axis=2)  # (Nsat, Ntime)

        # Игнорируем всё вне конуса
        distances_masked = np.where(cos_theta >= cos_limit, distances, np.inf)

        # Ищем ближайший спутник
        flat_index = np.argmin(distances_masked)
        sat_index, time_index = np.unravel_index(flat_index, distances_masked.shape)

        closest_norad_id = norad_ids[sat_index]
        closest_time = times[time_index].astimezone(timezone(timedelta(hours=3)))
        closest_distance_km = distances[sat_index, time_index]

        sat_closest = satellites[sat_index]

        # Положение относительно наблюдателя
        t_closest = times[time_index]
        diff = sat_closest.at(t_closest) - observer.at(t_closest)
        antenna_elev, antenna_az, _ = diff.altaz()

        altitude_deg = antenna_elev.degrees
        azimuth_deg = antenna_az.degrees

        print("Ближайший видимый спутник:")
        print(f"NORAD ID: {closest_norad_id}, NAME: {sat_closest.name}")
        print(f"Когда был виден: {closest_time}")
        print(f"Расстояние: {closest_distance_km:.2f} км")
        print(f"Угол места (altitude): {altitude_deg:.2f}°")
        print(f"Азимут: {azimuth_deg:.2f}°")
