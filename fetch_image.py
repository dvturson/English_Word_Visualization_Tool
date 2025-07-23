from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def fetch(driver, word):
    url = f"https://unsplash.com/s/photos/{word}"
    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    images  = soup.find_all("img", {"srcset": True})

    for img in images:
        src = img.get("src")
        if "images.unsplash.com/photo" in src:
            return src
        
    return None

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

print(fetch(driver, "tree"))