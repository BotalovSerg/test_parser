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

query = "cat"
query = query.replace(' ', '+')
URL = f"https://google.com/search?q={query}"

resp = requests.get(URL, headers=headers, proxies=proxies)

print(resp.status_code)
soup = BeautifulSoup(resp.content, "lxml")
for g in soup.find_all('div', class_='yuRUbf'):
    print(g)

# if resp.status_code == 200:
#
#     results = []
#     for g in soup.find_all('div', class_='yuRUbf'):
#         rc = g.find('div', class_='rc')
#         # description div
#         s = g.find('div', class_='s')
#         if rc:
#             divs = rc.find_all('div', recursive=False)
#             if len(divs) >= 2:
#                 anchor = divs[0].find('a')
#                 link = anchor['href']
#                 title = anchor.find('h3').text
#                 item = {
#                     "title": title,
#                     "link": link
#                 }
#                 results.append(item)
#     print(results)
