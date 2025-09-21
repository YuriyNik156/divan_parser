import csv
from typing import List, Dict


class CSVExporter:
    """
    Экспортер для сохранения данных в CSV-файл.
    """

    def __init__(self, filename: str = "products.csv"):
        """
        :param filename: Имя файла для сохранения CSV
        """
        self.filename = filename

    def export(self, data: List[Dict]) -> None:
        """
        Сохраняем данные в CSV.

        :param data: Список словарей с данными товаров
        """
        if not data:
            print("⚠ Нет данных для экспорта в CSV")
            return

        keys = data[0].keys()
        with open(self.filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=keys,
                delimiter=";"
            )
            writer.writeheader()
            writer.writerows(data)

        print(f"✅ Данные сохранены в {self.filename}")
