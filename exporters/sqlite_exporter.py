import sqlite3
from typing import List, Dict
from database import init_db, save_to_db


class SQLiteExporter:
    def __init__(self, db_name: str = "divan_products.db", logger = None):
        self.db_name = db_name
        self.logger = logger
        init_db(self.db_name, logger)  # инициализация базы

    def export(self, data: List[Dict]):
        """Сохраняем данные в SQLite."""
        save_to_db(self.db_name, data, self.logger)
        if self.logger:
            self.logger.info(f"✅ Данные сохранены в {self.db_name}")
        else:
            print(f"✅ Данные сохранены в {self.db_name}")
        if not data:
            print("⚠ Нет данных для экспорта в SQLite")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
