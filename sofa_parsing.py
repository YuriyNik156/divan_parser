import argparse
import os
from time import sleep

from parser import DivanParser


def main():
    """Главная функция запуска парсинга товаров с divan.ru."""
    parser_args = argparse.ArgumentParser(
        description="Парсер товаров с divan.ru"
    )
    parser_args.add_argument(
        "--category",
        nargs="+",
        default=["svet", "divany-i-kresla", "stoly-i-stulya"],
        help=(
            "Категории для парсинга (через пробел). "
            "Пример: --category svet divany-i-kresla"
        ),
    )
    parser_args.add_argument(
        "--format",
        choices=["csv", "json", "sqlite"],
        default="csv",
        help="Формат сохранения данных (csv, json, sqlite)",
    )
    parser_args.add_argument(
        "--output",
        default=None,
        help="Путь к файлу для сохранения. "
        "Пример: --output examples/products.csv",
    )
    parser_args.add_argument(
        "--headless",
        action="store_true",
        help="Запуск браузера в фоновом режиме",
    )

    args = parser_args.parse_args()

    # Создаём парсер
    divan_parser = DivanParser(export_format=args.format, headless=args.headless)

    try:
        # Парсим все указанные категории
        for category in args.category:
            divan_parser.parse_category(category)
            sleep(2)  # задержка, чтобы сайт не забанил

        # Определяем путь для сохранения
        output_path = args.output or os.path.join(
            "examples", f"products.{args.format}"
        )

        # Экспортируем результаты
        divan_parser.export_results(output_path)
        print(f"\n✅ Парсинг завершён. Данные сохранены в: {output_path}")

    finally:
        divan_parser.close()


if __name__ == "__main__":
    main()