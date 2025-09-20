import sqlite3
import logging


def init_db(db_name: str, logger: logging.Logger):
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
    logger.info("База данных очищена перед новым парсингом")


def save_to_db(db_name: str, name: str, price: str, link: str, category: str):
    """Сохранение товара в БД."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, link, category) VALUES (?, ?, ?, ?)",
        (name, price, link, category),
    )
    conn.commit()
    conn.close()