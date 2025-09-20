from time import sleep
from parser import DivanParser


if __name__ == "__main__":
    parser = DivanParser(headless=True)

    try:
        categories = ["svet", "divany-i-kresla", "stoly-i-stulya"]

        for category in categories:
            parser.parse_category(category)
            sleep(2)  # пауза, чтобы сайт не забанил
    finally:
        parser.close()