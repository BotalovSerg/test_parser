import requests
from bs4 import BeautifulSoup
from queue import Queue

BASE_URL = 'telderi.ru'
DOMAIN = f'https://{BASE_URL}/'
URLS_QUEUE = Queue()
URLS_BASE = set()
FILTER = {'#', 'search', 'javascript', 'system', 'default', 'None', 'viewBid', '.jpg', 'uploads'}


def crawler():
    while True:

        if URLS_QUEUE.qsize() == 0:
            break

        url = URLS_QUEUE.get()
        URLS_BASE.add(url)

        response = requests.get(url)
        response.raise_for_status()
        print('Scan url ', url, 'Status code ', response.status_code)

        soup = BeautifulSoup(response.content, 'lxml')
        for link in soup.find_all('a'):
            link = link.get('href')
            # print(link)

            if BASE_URL not in str(link):
                continue
            if any(part in str(link) for part in FILTER):
                continue
            URLS_QUEUE.put(link)
    return URLS_BASE


if __name__ == '__main__':
    URLS_QUEUE.put(DOMAIN)
    try:
        crawler()
    except requests.HTTPError as error:
        print(error)
