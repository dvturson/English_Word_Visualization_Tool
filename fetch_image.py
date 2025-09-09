from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from random import randint

# def fetch_img(driver, word):
#     url = f"https://unsplash.com/s/photos/{word}"
#     driver.get(url)

#     # time.sleep(3)

#     soup = BeautifulSoup(driver.page_source, "html.parser")

#     images = soup.find_all("img", {"srcset": True})
#     image_list = []

#     for img in images:
#         src = img.get("src")
#         if "images.unsplash.com/photo" in src or "plus.unsplash.com" in src:
#             image_list.append(src)
#             # return src
    
#     if not image_list:
#         return "/static/welch.jpg"

#     return image_list[randint(0, (len(image_list) - 1))]

def fetch_img(driver, word):
    url = f"https://pdimagearchive.org/search/?q={word}"
    driver.get(url)
    # input()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    images  = soup.find_all("img")
    
    image_list = []
    for img in images:
        src = img.get("src")
        image_list.append(src)
    
    if not image_list:
        return "/static/welch.jpg"
    # print(image_list)
    return image_list[randint(0, (len(image_list) - 1))]

options = Options()
options.add_argument("--headless")
options.add_argument("-log-level=3")
driver = webdriver.Chrome(options=options)

print(fetch_img(driver, "tree"))