import sqlite3
import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class DivanParser:
    """
    Парсер товаров с сайта divan.ru
    Собирает название, цену и ссылку на товар из указанной категории.
    Результаты сохраняются в базу данных SQLite.
    """

    BASE_URL = "https://www.divan.ru/category/"

    def __init__(self, db_name: str = "divan_products.db", headless: bool = True):
        self.db_name = db_name
        self._setup_logging()
        self.driver = self._init_driver(headless)
        self._init_db()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger("DivanParser")

    def _init_driver(self, headless: bool):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(options=options)

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
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
        conn.commit()
        conn.close()

    def parse_category(self, category: str):
        url = self.BASE_URL + category
        self.logger.info(f"Начинаю парсинг категории: {category} ({url})")

        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-testid='product-card']")
                )
            )
        except Exception as e:
            self.logger.error(f"Ошибка загрузки страницы {url}: {e}")
            return

        products = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")

        for product in products:
            try:
                # название (два варианта поиска)
                try:
                    name = product.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
                except NoSuchElementException:
                    name = product.find_element(By.CSS_SELECTOR, "a").text

                # цена
                price = product.find_element(By.CSS_SELECTOR, "span[data-testid='price']").text

                # ссылка
                link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

                self._save_to_db(name, price, link, category)
                self.logger.info(f"Сохранил товар: {name} — {price}")

            except Exception as e:
                self.logger.warning(f"Не удалось найти название. HTML:\n{product.get_attribute('outerHTML')}")

        self.logger.info(f"✅ Парсинг категории {category} завершён")

    def _save_to_db(self, name: str, price: str, link: str, category: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, link, category) VALUES (?, ?, ?, ?)",
            (name, price, link, category),
        )
        conn.commit()
        conn.close()

    def close(self):
        self.driver.quit()
        self.logger.info("Закрыл браузер")


if __name__ == "__main__":
    parser = DivanParser(headless=True)

    try:
        categories = ["svet", "divany-i-kresla", "stoly-i-stulya"]

        for category in categories:
            parser.parse_category(category)
            sleep(2)  # пауза, чтобы сайт не забанил
    finally:
        parser.close()