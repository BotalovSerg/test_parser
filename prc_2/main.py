import json

import requests
from bs4 import BeautifulSoup
import lxml

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

fests_urls_list = []
for i in range(0, 192, 24):

    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May"
    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)

    html_response = json_data["html"]

    with open(f"data/index_{i}.html", "w", encoding="utf-8") as file:
        file.write(html_response)

    with open(f"data/index_{i}.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    cards = soup.find_all("a", class_="card-img-link")

    for item in cards:
        fest_url = "https://www.skiddle.com" + item.get("href")
        fests_urls_list.append(fest_url)
cnt = 0
fest_list_result = []
for url in fests_urls_list:
    req = requests.get(url=url, headers=headers)
    cnt += 1
    print(cnt)
    print(url)

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_name = soup.find('h1', class_='MuiTypography-root MuiTypography-body1 css-r2lffm').text.strip()
        fest_date_loc = soup.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')
        fest_date = fest_date_loc[0].text
        fest_loc = fest_date_loc[1].text

        fest_list_result.append(
            {
                "Fest name": fest_name,
                "Fest date": fest_date,
                "Fest location": fest_loc,
                "URL": url
            }
        )

    except Exception as ex:
        print(ex)
        print("Damn...error")

with open("fest_list_result.json", "a", encoding="utf-8") as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)
