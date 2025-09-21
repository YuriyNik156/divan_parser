import json
from typing import List, Dict


class JSONExporter:
    """
    Экспортер для сохранения данных в JSON-файл.
    """

    def __init__(self, filename: str = "products.json"):
        """
        :param filename: Имя файла для сохранения JSON
        """
        self.filename = filename

    def export(self, data: List[Dict]) -> None:
        """
        Сохраняем данные в JSON.

        :param data: Список словарей с данными товаров
        """
        if not data:
            print("⚠ Нет данных для экспорта в JSON")
            return

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(f"✅ Данные сохранены в {self.filename}")
