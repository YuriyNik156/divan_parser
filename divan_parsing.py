import argparse
import os
from time import sleep
from parser import DivanParser


def main():
    parser_args = argparse.ArgumentParser(
        description="Парсер товаров с divan.ru"
    )
    parser_args.add_argument(
        "--category",
        nargs="+",
        default=["svet", "divany-i-kresla", "stoly-i-stulya"],
        help="Категории для парсинга (через пробел). Пример: --category sofas chairs"
    )
    parser_args.add_argument(
        "--format",
        choices=["csv", "json", "sqlite"],
        default="csv",
        help="Формат сохранения данных (csv, json, sqlite)"
    )
    parser_args.add_argument(
        "--output",
        default=None,
        help="Путь к файлу для сохранения. Пример: --output examples/products.csv"
    )
    parser_args.add_argument(
        "--headless",
        action="store_true",
        help="Запуск браузера в фоновом режиме"
    )

    args = parser_args.parse_args()

    # создаём парсер
    divan_parser = DivanParser(export_format=args.format, headless=args.headless)

    try:
        for category in args.category:
            divan_parser.parse_category(category)
            sleep(2)  # задержка, чтобы сайт не забанил

        if args.output:
            output_path = args.output
        else:
            output_path = os.path.join("examples", f"products.{args.format}")

        # сохраняем результат
        if args.output:
            # передаём путь прямо в экспортер
            if args.format == "csv":
                from exporters.csv_exporter import CSVExporter
                exporter = CSVExporter(args.output)
            elif args.format == "json":
                from exporters.json_exporter import JSONExporter
                exporter = JSONExporter(args.output)
            elif args.format == "sqlite":
                from exporters.sqlite_exporter import SQLiteExporter
                exporter = SQLiteExporter(args.output)
            exporter.export(divan_parser.products)
        else:
            divan_parser.export_results()

    finally:
        divan_parser.close()

if __name__ == "__main__":
    main()