import argparse
import csv
import os
import sys
from typing import List

from tabulate import tabulate

from reports import REPORTS


def parse():
    """Парсинг аргументов командной строки"""

    parser = argparse.ArgumentParser(description='Анализ рейтинга брендов')

    # добавляем аргументы, которые мы хотим принимать
    parser.add_argument(
        "--files",
        nargs="+", # означает "один или несколько аргументов"
        required=True,  # обязательно для ввода
        help="Список CSV-файлов для обработки"
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчёта (например, 'average-rating')"
    )
    return parser.parse_args()


def get_valid_files(file_paths: List[str]) -> List[str]:
    """
    Проверяет список путей к файлам, возвращает только существующие файлы
    с абсолютными путями. Если ни одного файла нет — завершает скрипт с ошибкой.

    Args:
        file_paths (List[str]): Список путей к файлам (относительных или абсолютных)

    Returns:
        List[str]: Список валидных абсолютных путей к файлам
    """
    valid_files = []
    for fpath in file_paths:
        abs_path = os.path.abspath(fpath)
        if os.path.isfile(abs_path):
            valid_files.append(abs_path)
        else:
            print(f"Файл не найден или не является файлом: {fpath}", file=sys.stderr)

        if not valid_files:
            print("Нет корректных файлов для обработки. Выход.", file=sys.stderr)
            sys.exit(1)

    return valid_files


def validate_report(report_name: str) -> str:
    """
    Проверяет, существует ли отчёт с указанным именем в REPORTS.
    Если нет — выводит ошибку и завершает скрипт.

    Returns:
        str: имя валидного отчёта
    """
    if report_name not in REPORTS:
        print(
            f"Ошибка: неизвестный отчёт '{report_name}'. "
            f"Доступные отчёты: {', '.join(REPORTS.keys())}",
            file=sys.stderr
        )
        sys.exit(1)
    return report_name

def get_data(files):
    """
    Читает CSV-файлы и возвращает объединённый список словарей с данными
    """

    data = []

    for fpath in files:
        with open(fpath, newline='', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

    return data

def print_result(result):
    """Выводит результат отчёта в виде красивой таблицы
    с сортировкой по убыванию рейтинга."""
    if result:
        result.sort(key=lambda x: x["performance"], reverse=True)
        table = [
            [i+1, item['position'], item['performance']]
             for i, item in enumerate(result)
        ]
    headers = [" ", "position", "performance"]

    floatfmt = ("", "", ".2f")
    print(tabulate(table, headers=headers, tablefmt="grid", floatfmt=floatfmt))


def main():
    args = parse()

    # Валидация файлов
    valid_files = get_valid_files(args.files)

    # Валидация отчёта
    report_name = validate_report(args.report)

    # Читаем данные из CSV
    data = get_data(valid_files)

    report_class = REPORTS[report_name]
    report = report_class()
    result =report.value(data)
    print_result(result)


if __name__ == "__main__":
    main()
