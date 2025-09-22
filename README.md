# Парсер товаров с сайта Divan.ru (DivanParser)

**Описание**

DivanParser — это учебный проект на Python для автоматического сбора данных о товарах с сайта [divan.ru].
Проект демонстрирует работу с Selenium WebDriver, экспорт данных в разные форматы (CSV, JSON, SQLite) и организацию 
архитектуры, удобной для расширения и тестирования.

Для демонстрации работы и тестирования реализованы мок-страницы и юнит-тесты. Это гарантирует, что проект будет 
стабильно работать даже при изменении структуры сайта.

---

## Основные возможности

* **Парсинг товаров с сайта divan.ru:**
  * Сбор названия, цены, ссылки и категории товара
  * Возможность указать категории для парсинга через аргументы командной строки
  * Доступны три категории для парсинга: svet, divany-i-kresla, stoly-i-stulya

* **Экспорт результатов в разные форматы**:
  * CSV — таблица с товарами
  * JSON — структурированные данные
  * SQLite — база данных

* **Гибкость запуска:**
  * Поддержка headless-режима браузера
  * Выбор выходного файла и формата
  * Простая интеграция новых экспортеров

* **Мок-тесты для парсера:**
  * Использование тестовой HTML-страницы (mock_divan.html)
  * Проверка работы парсера без обращения к реальному сайту

---

## Архитектура проекта

* **Парсер** — Selenium (Python 3.13).

* **Экспорт** — CSV, JSON, SQLite (через отдельные классы).

* **Тестирование** — unittest + unittest.mock.

* **Логирование** — встроенный logging.

---

## Установка и запуск

1. **Клонировать репозиторий**:

   ```bash
   git clone https://github.com/ваш_пользователь//divan_parser.git
   cd divan_parser
   ```
   
2. **Создать виртуальное окружение и установить зависимости**:

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
   ```

3. **Запуск парсера**:

* Пример запуска с сохранением в .csv:

   ```bash
   python divan_parsing.py --category svet divany-i-kresla stoly-i-stulya --format csv --headless
   ```
  
* Пример запуска с сохранением в .json:

   ```bash
   python divan_parsing.py --category svet divany-i-kresla stoly-i-stulya --format json --headless
   ```

* Пример запуска с сохранением в SQLite:

   ```bash
   python divan_parsing.py --category svet divany-i-kresla stoly-i-stulya --format SQLite --headless
   ```

---

## Пример результата

* CSV (products_export.csv):

name;price;link;category
Лампа Ralf;4999 ₽;https://www.divan.ru/product/torsher-ralf-beige;svet
Лампа Ferum;2999 ₽;https://www.divan.ru/product/podvesnoj-svetilnik-ferum-orange;svet
Настольная лампа Nidls;3999 ₽;https://www.divan.ru/product/nastolnaya-lampa-nidls-raffia-beige;svet

---

## Зависимости

Основные библиотеки:
* selenium — парсинг данных
* sqlite3 — база данных
* argparse — аргументы командной строки
* logging — логирование
* unittest — тесты

Полный список зависимостей в requirements.txt.

---

## Запуск тестов

1. **Перейти в папку проекта и выполнить:**

   ```bash
   python -m unittest discover tests
   ```
   
2. **Для более подробного отчета:**

    ```bash
   python -m unittest -v tests/test_parser.py
   ```
   
---

## Структура проекта

```
divan_parser/
├── divan_parsing.py         # точка входа (основной скрипт)
├── parser.py                # класс DivanParser
├── database.py              # работа с SQLite
├── exporters/               # экспортеры данных
│   ├── csv_exporter.py
│   ├── json_exporter.py
│   └── sqlite_exporter.py
├── utils.py                 # вспомогательные функции (логгер, WebDriverWait и др.)
├── requirements.txt         # зависимости
├── README.md                # документация
├── examples/                # примеры сохраненных файлов
│   └── products_export.csv
└── tests/                   # тесты
    ├── mock_pages/          # тестовые HTML-страницы
    │   └── mock_divan.html
    ├── test_parser.py       # unittest для DivanParser
    └── __init__.py
```

---

## Лицензия

Проект распространяется под MIT License.

