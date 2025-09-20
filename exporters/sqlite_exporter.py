import sqlite3
from typing import List, Dict
from database import init_db, save_to_db


class SQLiteExporter:
    def __init__(self, db_name: str = "divan_products.db"):
        self.db_name = db_name
        init_db(self.db_name)  # инициализация базы

    def export(self, data: List[Dict]):
        """Сохраняем данные в SQLite."""
        if not data:
            print("⚠ Нет данных для экспорта в SQLite")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for product in data:
            save_to_db(
                cursor,
                product["name"],
                product["price"],
                product["link"],
                product["category"],
            )

        conn.commit()
        conn.close()
        print(f"✅ Данные сохранены в {self.db_name}")