import csv
from typing import List, Dict


class CSVExporter:
    def __init__(self, filename: str = "products.csv"):
        self.filename = filename

    def export(self, data: List[Dict]):
        """Сохраняем данные в CSV."""
        if not data:
            print("⚠ Нет данных для экспорта в CSV")
            return

        keys = data[0].keys()
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys, delimiter=";")
            writer.writeheader()
            writer.writerows(data)

        print(f"✅ Данные сохранены в {self.filename}")