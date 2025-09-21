from typing import List, Dict
from database import init_db, save_to_db
import sqlite3


class SQLiteExporter:
    """
    Экспортер для сохранения данных в SQLite-базу.
    """

    def __init__(self, db_name: str = "divan_products.db", logger=None):
        """
        :param db_name: Имя файла базы данных
        :param logger: Опциональный логгер для сообщений
        """
        self.db_name = db_name
        self.logger = logger
        init_db(self.db_name, self.logger)  # Инициализация базы

    def export(self, data: List[Dict]) -> None:
        """
        Сохраняем данные в SQLite.

        :param data: Список словарей с данными товаров
        """
        if not data:
            if self.logger:
                self.logger.warning("⚠ Нет данных для экспорта в SQLite")
            else:
                print("⚠ Нет данных для экспорта в SQLite")
            return

        save_to_db(self.db_name, data, self.logger)

        if self.logger:
            self.logger.info(f"✅ Данные сохранены в {self.db_name}")
        else:
            print(f"✅ Данные сохранены в {self.db_name}")
