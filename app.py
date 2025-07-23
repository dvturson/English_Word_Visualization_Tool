from flask import Flask, request, jsonify, render_template
from bidi.algorithm import get_display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
from random import randint

with open("english_words_grouped.json", "r") as f:
    word_data = json.load(f)

app = Flask(__name__)

def get_suggestions(prefix, max_results=5):
    if not prefix:
        return []
    first_letter = prefix[0]
    candidates = word_data.get(first_letter, [])

    matches = [
            (word[0] , int(word[1]))
            for word in candidates 
            if word[0].startswith(prefix)
    ]

    matches.sort(key=lambda x: -x[1])
    
    return [get_display(word[0]) for word in matches[:max_results]]

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/suggest")
def suggest():
    prefix = request.args.get("prefix", "")
    return jsonify(get_suggestions(prefix))

@app.route("/fetch")
def fetch():
    word = request.args.get("word", "")
    img_url = fetch_img(driver, word)
    return jsonify({"img": img_url})

if __name__ == "__main__":
    app.run(debug=True)