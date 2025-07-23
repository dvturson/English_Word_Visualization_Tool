from bidi.algorithm import get_display
from collections import defaultdict
from pprint import pprint
import csv
import json
import nltk
nltk.download("words")
from nltk.corpus import words as nltk_words
from wordfreq import zipf_frequency


with open("english_words.csv", "r") as file:
    words = list(csv.reader(file))[1:]

nltk_words = set(w.lower() for w in nltk_words.words())
grouped = defaultdict(list)
excluded = defaultdict(list)

def is_valid(word):
    return zipf_frequency(word, 'en') > 3.0

for word in words:
    if word and len(word[0]) > 1 and is_valid(word[0]):
        grouped[word[0][0]].append(word)
    else:
        excluded[word[0][0]].append(word)

grouped_dict = dict(grouped)
excluded_dict = dict(excluded)

with open("english_words_grouped.json", "w") as data:
    json.dump(grouped_dict, data, indent=2)

with open("excluded.json", "w") as data:
    json.dump(excluded_dict, data, indent=2)

print("saved")