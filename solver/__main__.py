"""
Модуль точки входа для запуска пакета как модуля через python -m solver.

Вызывает интерфейс командной строки решателя.
"""
from .cli import cli_main

if __name__ == "__main__":
    cli_main()
