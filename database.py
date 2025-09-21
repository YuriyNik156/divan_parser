import sqlite3
import logging
from typing import List, Dict


def init_db(db_name: str, logger=None):
    """Создание таблицы и очистка её перед новым парсингом."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            link TEXT NOT NULL,
            category TEXT NOT NULL
        )
        """
    )
    cursor.execute("DELETE FROM products")
    conn.commit()
    conn.close()
    if logger:  # ✅ защита от None
        logger.info("База данных очищена перед новым парсингом")
    else:
        print("🗄️ База данных создана/очищена")


def save_to_db(db_name: str, data: List[Dict], logger=None):
    """Сохраняем список товаров в БД."""
    if not data:
        if logger:
            logger.warning("⚠ Нет данных для сохранения в БД")
        else:
            print("⚠ Нет данных для сохранения в БД")
        return

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for item in data:
        cursor.execute(
            "INSERT INTO products (name, price, link, category) VALUES (?, ?, ?, ?)",
            (item.get("name"), item.get("price"), item.get("link"), item.get("category")),
        )

    conn.commit()
    conn.close()

    if logger:
        logger.info(f"💾 Сохранено {len(data)} записей в {db_name}")
    else:
        print(f"💾 Сохранено {len(data)} записей в {db_name}")