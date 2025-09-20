import logging
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ====== ЛОГГЕР ======
def get_logger(name: str = "DivanParser", level: int = logging.INFO) -> logging.Logger:
    """
    Настройка логгера (замена print)
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # чтобы не дублировались сообщения
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger


# ====== WebDriverWait ОБЁРТКИ ======
def wait_for_element(driver, selector: str, timeout: int = 20):
    """
    Ожидание появления одного элемента на странице
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def wait_for_elements(driver, selector: str, timeout: int = 20):
    """
    Ожидание появления списка элементов на странице
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )


# ====== ARGPARSE ======
def parse_args():
    """
    Парсинг аргументов командной строки
    Пример:
        python parser.py --category sofas --format csv --headless
    """
    parser = argparse.ArgumentParser(description="Парсер divan.ru")
    parser.add_argument(
        "--category",
        type=str,
        default="sofas",
        help="Категория товаров (например: sofas, chairs, svet)"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="sqlite",
        choices=["csv", "json", "sqlite"],
        help="Формат экспорта: csv / json / sqlite"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Запуск браузера в headless-режиме"
    )

    return parser.parse_args()