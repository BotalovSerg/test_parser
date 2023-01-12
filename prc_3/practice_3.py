import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-encoding": "gzip, deflate",
        "Accept-language": "en",
        "Cache-control": "max-age=0",
        "Connection": "keep-alive",
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    # r = requests.get(url=url, headers=headers)
    #
    # with open("index.html", "w", encoding="utf-8") as file:
    #     file.write(r.text)

    r = requests.get("https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most", headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    hotels_cards = soup.find_all('div', class_='hotel_card_dv')

    for hotel_url in hotels_cards:
        hotel_url = hotel_url.find('a').get('href')
        print(hotel_url)


def get_data_with_selenium(url):
    # try:
    #     driver = webdriver.Chrome()
    #
    #     driver.get(url=url)
    #     time.sleep(5)
    #
    #     with open("index_selenium.html", "w", encoding="utf-8") as file:
    #         file.write(driver.page_source)
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     driver.close()
    #     driver.quit()

    with open("index_selenium.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    hotels_cards = soup.find_all('div', class_='hotel_card_dv')

    for hotel_url in hotels_cards:
        hotel_url = "https://www.tury.ru" + hotel_url.find('a').get('href')
        print(hotel_url)


def main():
    # get_data("https://tury.ru/hotel/most_luxe.php")
    get_data_with_selenium("https://tury.ru/hotel/most_luxe.php")


if __name__ == '__main__':
    main()
