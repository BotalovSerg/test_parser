import requests
from bs4 import BeautifulSoup
from random import choice


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('table', {'class': 'table table-striped table-bordered'}).find_all('tr')[1:]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[2].text.lower().strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)

    return choice(proxies)


def get_html():
    p = get_proxy()

    proxy = f"{p['schema']}://{p['address']}"

    return proxy


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
p = get_html()
proxies = {
    'https': p,
    'http': p
}
print(proxies)


def get_locations(url):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, "lxml")

    ip = soup.find('div', class_='ip').text.strip()
    location = soup.find('div', class_='value-country').text.strip()
    print(f"IP: {ip}\nLocation: {location}")


def main():
    get_locations(url="https://2ip.ru/")


# def start():
#     url = 'https://www.google.com/'
#     print(get_html(url))


if __name__ == '__main__':
    main()
