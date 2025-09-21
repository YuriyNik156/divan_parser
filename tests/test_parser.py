import unittest
import os
from unittest.mock import MagicMock, patch
from parser import DivanParser


class TestDivanParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Путь к мок-странице
        cls.mock_html_path = os.path.join(
            os.path.dirname(__file__), "mock_pages", "mock_divan.html"
        )
        if not os.path.exists(cls.mock_html_path):
            raise FileNotFoundError(f"Mock HTML file не найден: {cls.mock_html_path}")

    @patch("parser.webdriver.Chrome")  # Подменяем реальный Chrome
    def test_parse_mock_html(self, mock_chrome):
        # Создаем мок-драйвер и мок-элементы
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Читаем HTML
        with open(self.mock_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Подменяем метод get и find_elements, чтобы вернуть наши мок-элементы
        mock_driver.get.return_value = None

        class MockWebElement:
            def __init__(self, name, price, link):
                self._name = name
                self._price = price
                self._link = link

            def find_element(self, by, value):
                if value == "span[itemprop='name']":
                    return MagicMock(text=self._name)
                if value == "span[data-testid='price']":
                    return MagicMock(text=self._price)
                if by == "tag name" and value == "a":
                    return MagicMock(get_attribute=MagicMock(return_value=self._link))
                raise Exception("Не найден элемент")

            def get_attribute(self, attr):
                return html_content  # Не используем для теста

        # Задаем, что find_elements возвращает три мок-товара
        mock_driver.find_elements.return_value = [
            MockWebElement("Лампа Ralf", "4999 ₽", "https://www.divan.ru/product/torsher-ralf-beige"),
            MockWebElement("Лампа Ferum", "2999 ₽", "https://www.divan.ru/product/podvesnoj-svetilnik-ferum-orange"),
            MockWebElement("Настольная лампа Nidls", "3999 ₽", "https://www.divan.ru/product/nastolnaya-lampa-nidls-raffia-beige"),
        ]

        # Создаем парсер
        parser = DivanParser(headless=True)
        parser.driver = mock_driver  # подменяем драйвер на наш мок

        parser.parse_category("svet")

        # Проверяем, что парсер собрал все товары
        self.assertEqual(len(parser.products), 3)

        # Проверяем конкретные значения
        self.assertEqual(parser.products[0]["name"], "Лампа Ralf")
        self.assertEqual(parser.products[0]["price"], "4999 ₽")
        self.assertEqual(
            parser.products[0]["link"], "https://www.divan.ru/product/torsher-ralf-beige"
        )

        self.assertEqual(parser.products[1]["name"], "Лампа Ferum")
        self.assertEqual(parser.products[1]["price"], "2999 ₽")
        self.assertEqual(
            parser.products[1]["link"], "https://www.divan.ru/product/podvesnoj-svetilnik-ferum-orange"
        )

        self.assertEqual(parser.products[2]["name"], "Настольная лампа Nidls")
        self.assertEqual(parser.products[2]["price"], "3999 ₽")
        self.assertEqual(
            parser.products[2]["link"], "https://www.divan.ru/product/nastolnaya-lampa-nidls-raffia-beige"
        )

        # Закрываем парсер
        parser.close()


if __name__ == "__main__":
    unittest.main()
