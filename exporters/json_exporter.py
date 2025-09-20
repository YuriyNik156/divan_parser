import json
from typing import List, Dict


class JSONExporter:
    def __init__(self, filename: str = "products.json"):
        self.filename = filename

    def export(self, data: List[Dict]):
        """Сохраняем данные в JSON."""
        if not data:
            print("⚠ Нет данных для экспорта в JSON")
            return

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"✅ Данные сохранены в {self.filename}")