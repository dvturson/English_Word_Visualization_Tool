from flask import Flask, request, jsonify, render_template
from bidi.algorithm import get_display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
from random import randint, choice
import requests

with open("english_words_grouped.json", "r") as f:
    word_data = json.load(f)

app = Flask(__name__)

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "for", "from", "had", "has",
    "he", "her", "him", "his", "i", "if", "in", "is", "it", "its", "me", "my", "of", "on",
    "or", "our", "she", "so", "that", "the", "their", "them", "there", "they", "this", "to",
    "was", "we", "were", "what", "when", "where", "which", "who", "with", "you", "your",
    "i'm", "you're", "he's", "she's", "it's", "we're", "they're", "i've", "you've", "we've", "they've",
    "i'd", "you'd", "he'd", "she'd", "we'd", "they'd", "i'll", "you'll", "he'll", "she'll", "we'll", "they'll",
    "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't", "won't", "wouldn't", "can't", "couldn't",
    "shouldn't"
}


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
    if word in STOP_WORDS:
        return f"/static/words/{word}.png"
    url = f"https://unsplash.com/s/photos/{word}?order_by=curated&orientation=portrait"
    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    images  = soup.find_all("img")
    
    image_list = []
    for img in images:
        src = img.get("src")
        if "https://plus.unsplash.com/premium_photo" in src or "https://images.unsplash.com/photo-" in src:
            image_list.append(src)
        # image_list.append(src)
    
    if not image_list:
        return "/static/welch.jpg"
    # print(image_list)
    return image_list[randint(0, (len(image_list) - 1))]

def fetch_img_api(word):
    if word in STOP_WORDS:
        return f"/static/words/{word}.png"
    ACCESS_KEY = UNSPLASH_API_KEY
    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": word,
        # "color": "black_and_white",
        "orientation": "portrait",
        "per_page": 5,
        "client_id": ACCESS_KEY,
    }

    try:
        res  = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"Error fetching image: {e}")
        return "/static/be.jpg"

    if not data["results"]:
        return "/static/be.jpg"
    
    return choice(data["results"])["urls"]["regular"]

options = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/suggest")
def suggest():
    prefix = request.args.get("prefix", "")
    return jsonify(get_suggestions(prefix))

@app.route("/fetch_image")
def fetch():
    word = request.args.get("word", "")
    img_url = fetch_img(driver, word)
    # img_url = fetch_img_api(word)
    return jsonify({"img": img_url})

if __name__ == "__main__":
    app.run(debug=True)