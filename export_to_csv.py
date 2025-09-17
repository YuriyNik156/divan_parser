import sqlite3
import csv

def export_to_csv(db_path: str, csv_path: str):
    """Экспорт таблицы products в CSV."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name, price, link, category FROM products")
    rows = cursor.fetchall()

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Название товара", "Цена", "Ссылка", "Категория"])
        writer.writerows(rows)

    conn.close()
    print(f"✅ Данные экспортированы в {csv_path}")

if __name__ == "__main__":
    export_to_csv("divan_products.db", "products_export.csv")
