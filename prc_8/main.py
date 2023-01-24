import requests
from bs4 import BeautifulSoup
import time


def test_request(url, retry=5):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                  "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

    }

    try:
        responce = requests.get(url=url, headers=headers)
        print(f"[+] {url} {responce.status_code}")
    except Exception as ex:
        time.sleep(3)
        if retry:
            print(f"[INFO] rentry={retry} => {url}")
            return test_request(url, retry=(retry - 1))
        else:
            raise
    else:
        return responce


def main():
    with open("books_urls.txt", encoding="utf-8") as file:
        books_urls = file.read().splitlines()

    for book_url in books_urls:
        # test_request(url=book_url)
        try:
            r = test_request(url=book_url)
            soup = BeautifulSoup(r.text, 'lxml')
            print(f"{soup.title.text}\n{'-' * 20}")
        except Exception as ex:
            continue


if __name__ == "__main__":
    main()
