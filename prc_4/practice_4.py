import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv


def get_all_pages():
    headers = {

        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    # r = requests.get(url="https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/", headers=headers, verify=False)
    #
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open("data/index.html", "w", encoding="utf-8") as file:
    #     file.write(r.text)


with open("data/index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
items_cards = soup.find_all("a", class_="product-item__link")
data = []
cur_data = datetime.now().strftime("%d_%m_%Y")
with open(f"data_{cur_data}.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            "Артикул",
            "Ссылка",
            "Цена"
        )
    )
for item in items_cards:
    product_article = item.find("p", class_="product-item__articul").text.strip()
    product_url = f'https://shop.casio.ru{item.get("href")}'

    data.append(
        {
            "product_article": product_article,
            "product_url": product_url,
            "price": None
        }
    )

    with open(f"data_{cur_data}.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                product_article,
                product_url,
                "No"
            )
        )

with open(f"data_{cur_data}.json", "a", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    get_all_pages()


if __name__ == '__main__':
    main()
