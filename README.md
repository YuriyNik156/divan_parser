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

## План разработки

Проект рассчитан на 7 дней:

1. Этап 1 (День 1): настройка окружения, создание архитектуры проекта (parser.py, database.py, exporters/, utils.py), подготовка requirements.txt и README.md
2. Этап 2 (День 2): реализация базового парсера (DivanParser), первичная логика извлечения карточек товаров (название, цена, ссылка)
3. Этап 3 (День 3): настройка экспорта данных в CSV и JSON, создание примеров экспорта в папке examples/
4. Этап 4 (День 4): интеграция SQLite: реализация сохранения товаров в БД, Подготовка database.py с моделями и методами работы
5. Этап 5 (День 5): создание папки tests/, добавление mock_divan.html для мок-тестов, написание тестов для парсера (test_parser.py)
6. Этап 6 (День 6): тестирование экспорта (CSV, JSON, SQLite), добавление логирования и обработок ошибок в utils.py
7. Этап 7 (День 7): финальная отладка, дополнение README.md (ограничения проекта, инструкция по тестам), подготовка проекта к публикации в портфолио

---

## Ограничения проекта

* HTML-разметка на divan.ru динамически изменяется, поэтому парсинг реального сайта может работать нестабильно.
* На данный момент в проекте реализован успешный парсинг только мок-страниц, которые полностью контролируются внутри репозитория.
* Реальные данные с сайта могут не отображаться корректно (например, названия и цены могут оставаться пустыми).
* Проект создан в первую очередь как демонстрационный пример: он показывает навыки работы с HTML-парсингом, тестами и структурированием кода.

---

## Лицензия

Проект распространяется под MIT License.

---

## Скриншоты

**Пример работы парсера**
![Пример файла json.jpg](screenshots/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20%D1%84%D0%B0%D0%B9%D0%BB%D0%B0%20json.jpg)

**Пример мок-страницы**
![Пример файла json.jpg](screenshots/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20%D1%84%D0%B0%D0%B9%D0%BB%D0%B0%20json.jpg)

**Пример файла json**
![Пример файла json.jpg](screenshots/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20%D1%84%D0%B0%D0%B9%D0%BB%D0%B0%20json.jpg)

