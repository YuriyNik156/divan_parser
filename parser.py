import logging
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from exporters import CSVExporter, JSONExporter, SQLiteExporter


class DivanParser:
    """
    Парсер товаров с сайта divan.ru
    Собирает название, цену и ссылку на товар из указанной категории.
    Результаты сохраняются в выбранный формат (CSV / JSON / SQLite).
    """

    BASE_URL = "https://www.divan.ru/category/"

    def __init__(self, export_format: str = "sqlite", headless: bool = True):
        """
        :param export_format: Формат сохранения ('csv', 'json', 'sqlite')
        :param headless: Запуск браузера в фоновом режиме
        """
        self.export_format = export_format.lower()
        self._setup_logging()
        self.driver = self._init_driver(headless)
        self.products = []  # список для хранения результатов

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
                # название
                try:
                    name = product.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
                except NoSuchElementException:
                    try:
                        name = product.find_element(By.CSS_SELECTOR, "a[data-testid='product-title']").text
                    except NoSuchElementException:
                        try:
                            name = product.find_element(By.CSS_SELECTOR, ".PJZwc").text
                        except NoSuchElementException:
                            name = "Без названия"

                # цена
                try:
                    price = product.find_element(By.CSS_SELECTOR, "span[data-testid='price']").text
                except NoSuchElementException:
                    try:
                        price = product.find_element(By.CSS_SELECTOR, "meta[itemprop='price']").get_attribute("content")
                    except NoSuchElementException:
                        try:
                            price = product.find_element(By.CSS_SELECTOR, ".ui-LD-ZU.TA0JV").text
                        except NoSuchElementException:
                            price = "Не указана"

                # ссылка
                try:
                    link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                except NoSuchElementException:
                    link = "Нет ссылки"

                # сохраняем в список
                self.products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "category": category
                })

                self.logger.info(f"Нашёл товар: {name} — {price}")

            except Exception as e:
                self.logger.warning(
                    f"Не удалось распарсить товар. Ошибка: {e}\nHTML:\n{product.get_attribute('outerHTML')}"
                )

        self.logger.info(f"✅ Парсинг категории {category} завершён")

    def export_results(self):
        """Сохраняем данные в выбранный формат"""
        if not self.products:
            self.logger.warning("⚠ Нет данных для экспорта")
            return

        if self.export_format == "csv":
            exporter = CSVExporter("products.csv")
        elif self.export_format == "json":
            exporter = JSONExporter("products.json")
        elif self.export_format == "sqlite":
            exporter = SQLiteExporter("divan_products.db")
        else:
            raise ValueError("Неверный формат! Используй: csv / json / sqlite")

        exporter.export(self.products)
        self.logger.info(f"Данные экспортированы в {self.export_format.upper()}")

    def close(self):
        self.driver.quit()
        self.logger.info("Закрыл браузер")