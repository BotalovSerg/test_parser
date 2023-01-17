import json
import time

import requests
from bs4 import BeautifulSoup
import datetime
import csv

start_time = time.time()


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Размер скидки",
                "Наличие на складе"
            )
        )
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                  "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

    }
    url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"

    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

    books_data = []

    for page in range(1, pages_count + 1):
        # for page in range(1, 2):
        url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"

        response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "Нет названия книги"

            try:
                book_author = book_data[1].text.strip()
            except:
                book_author = "Нет автора"

            try:
                # book_publishing = book_data[2].text
                book_publishing = book_data[2].find_all("a")
                book_publishing = ": ".join([bp.text for bp in book_publishing])
            except:
                book_publishing = "Нет издательства"

            try:
                book_new_price = book_data[3].find("div", class_="price").find("span").find(
                    "span").text.strip().replace(" ", "")
            except:
                book_new_price = "Not new price"

            try:
                book_old_price = book_data[3].find("span", class_="price-gray").text.strip().replace(" ", "")
            except:
                book_old_price = "Not old price"

            try:
                book_sale = round(((int(book_old_price) - int(book_new_price)) / int(book_old_price)) * 100)
            except:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "Нет статуса"

            # print(book_title)
            # print(book_author)
            # print(book_publishing)
            # print(book_new_price)
            # print(book_old_price)
            # print(book_sale)
            # print(book_status)
            # print("#*" * 15)

            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )

            with open(f"labirint_{cur_time}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )
        print(f"Обработано {page}/{pages_count}")
        time.sleep(1)

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затрачено времени на работу: {finish_time}")


if __name__ == '__main__':
    main()
