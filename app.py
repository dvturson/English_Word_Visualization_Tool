from flask import Flask, request, jsonify, render_template
from bidi.algorithm import get_display
import json

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/suggest")
def suggest():
    prefix = request.args.get("prefix", "")
    return jsonify(get_suggestions(prefix))

if __name__ == "__main__":
    app.run(debug=True)