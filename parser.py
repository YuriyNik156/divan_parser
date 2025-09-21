import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from exporters import CSVExporter, JSONExporter, SQLiteExporter


class DivanParser:
    """
    Парсер товаров с сайта divan.ru.
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
        """Настройка логирования."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger("DivanParser")

    def _init_driver(self, headless: bool):
        """Инициализация Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(options=options)

    def parse_category(self, category: str):
        """Парсинг товаров указанной категории."""
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

        products = self.driver.find_elements(
            By.CSS_SELECTOR, "div[data-testid='product-card']"
        )

        for product in products:
            try:
                # Название товара
                try:
                    name = product.find_element(
                        By.CSS_SELECTOR, "span[itemprop='name']"
                    ).text
                except NoSuchElementException:
                    try:
                        name = product.find_element(
                            By.CSS_SELECTOR, "a[data-testid='product-title']"
                        ).text
                    except NoSuchElementException:
                        try:
                            name = product.find_element(By.CSS_SELECTOR, ".PJZwc").text
                        except NoSuchElementException:
                            name = "Без названия"

                # Цена
                try:
                    price = product.find_element(
                        By.CSS_SELECTOR, "span[data-testid='price']"
                    ).text
                except NoSuchElementException:
                    try:
                        price = product.find_element(
                            By.CSS_SELECTOR, "meta[itemprop='price']"
                        ).get_attribute("content")
                    except NoSuchElementException:
                        try:
                            price = product.find_element(
                                By.CSS_SELECTOR, ".ui-LD-ZU.TA0JV"
                            ).text
                        except NoSuchElementException:
                            price = "Не указана"

                # Ссылка
                try:
                    link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                except NoSuchElementException:
                    link = "Нет ссылки"

                # Сохраняем в список
                self.products.append({
                    "name": name,
                    "price": price,
                    "link": link,
                    "category": category
                })

                self.logger.info(f"Нашёл товар: {name} — {price}")

            except Exception as e:
                self.logger.warning(
                    f"Не удалось распарсить товар. Ошибка: {e}\n"
                    f"HTML:\n{product.get_attribute('outerHTML')}"
                )

        self.logger.info(f"✅ Парсинг категории {category} завершён")

    def export_results(self, output_path: str = None):
        """
        Сохраняем данные в выбранный формат.
        :param output_path: Путь к файлу для сохранения. Если None, создаётся в examples/
        """
        if not self.products:
            self.logger.warning("⚠ Нет данных для экспорта")
            return

        exporters = {
            "csv": CSVExporter,
            "json": JSONExporter,
            "sqlite": SQLiteExporter,
        }

        ExporterClass = exporters.get(self.export_format)
        if not ExporterClass:
            raise ValueError("Неверный формат! Используй: csv / json / sqlite")

        # Формируем путь по умолчанию, если не указан
        if output_path is None:
            output_path = os.path.join(
                "examples", f"products.{self.export_format}"
            )

        # Создаём директорию, если её нет
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        exporter = ExporterClass(output_path)
        exporter.export(self.products)
        self.logger.info(f"Данные экспортированы в {self.export_format.upper()}: {output_path}")

    def close(self):
        """Закрываем браузер."""
        self.driver.quit()
        self.logger.info("Закрыл браузер")
