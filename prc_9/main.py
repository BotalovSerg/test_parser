import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def get_source_url(url):
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(5)

        while True:
            find_more_element = driver.find_element(By.CLASS_NAME, 'catalog-button-showMore')

            if driver.find_elements(By.CLASS_NAME, 'hasmore-text'):
                with open("index_page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(4)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_source_url(
        url='https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10')


if __name__ == "__main__":
    main()
