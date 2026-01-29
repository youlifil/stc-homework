"""
Модуль запуска из командной строки.

Этот модуль предоставляет интерфейс командной строки для решателя,
передавая ему указанные пользователем конфигурационные параметроы.
Использует библиотеку Click для создания CLI.
"""

import click
from config_parser import parse_config
from solver import sat_visible, SolverConfig


@click.command()
@click.option("-s", "--satellites", 
              required=True, 
              help="TLE-файл со спутниками")
@click.option("-c", "--config", 
              required=True, 
              help="JSON-файл с условиями задачи")
def main(satellites: str = "", config: str = "") -> None:
    """
    Основная функция командной строки.
    
    Парсит файл конфига и запускает решатель с указанными в конфиге параметрами.
    
    Args:
        satellites (str): Путь к TLE-файлу со спутниками.
        config (str): Путь к JSON-файлу с конфигом.
        
    Returns:
        None
        
    Raises:
        FileNotFoundError: Если указанные файлы не найдены.
        ValueError: Если данные в файлах некорректны.
    """
    solver_config: SolverConfig = parse_config(config)
    sat_visible(satellites, solver_config)


if __name__ == "__main__":
    main()
