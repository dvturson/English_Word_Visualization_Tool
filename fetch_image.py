from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from random import randint

def fetch_img(driver, word):
    url = f"https://unsplash.com/s/photos/{word}"
    driver.get(url)

    # time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    images  = soup.find_all("img", {"srcset": True})
    list = []

    for img in images:
        src = img.get("src")
        if "images.unsplash.com/photo" in src or "plus.unsplash.com" in src:
            list.append(src)
            # return src
    

    return list[randint(0, (len(list) - 1))]

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

print(fetch_img(driver, "tree"))