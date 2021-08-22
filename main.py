import pickle
from tld import get_tld
import whois
import requests
import numpy as np
import pandas as pd
import en_core_web_md
import sys
from sklearn.feature_extraction.text import CountVectorizer
import en_core_web_md
text_to_nlp = en_core_web_md.load()
print("yay")

def tokenize(text):
    clean_tokens = []
    for token in text_to_nlp(text):
        if (not token.is_stop) & (token.lemma_ != '-PRON-') & (
                not token.is_punct
        ):  # -PRON- is a special all inclusive "lemma" spaCy uses for any pronoun, we want to exclude these
            clean_tokens.append(token.lemma_)
    return clean_tokens


X_text = pd.read_csv("combined.csv")['html']
bow_transformer = CountVectorizer(analyzer=tokenize,
                                  max_features=1600).fit(X_text)

model = pickle.load(open("model.pkl", "rb"))
countries = {
    None: 1,
    'US': 2,
    'CN': 3,
    'AU': 4,
    'CA': 5,
    'KR': 6,
    'GB': 7,
    'NL': 8,
    'IN': 9,
    'PA': 0,
    'SK': 10,
    'VG': 12,
    'KY': 13,
    'IS': 14,
    'RO': 15,
    'HU': 16,
    'HK': 17,
    'EE': 18,
    'CM': 19,
    'REDACTED FOR PRIVACY': 20,
    'UA': 21,
    'RU': 22,
    'BS': 23,
    'United States': 24
}
domain = {
    'com': 0,
    'org': 1,
    'shopping': 2,
    'co': 3,
    'tk': 4,
    'club': 5,
    'com.es': 6,
    'net': 7,
    'netlify.app': 8,
    'tech': 9,
    'tv': 10,
    'ca': 11,
    'io': 12,
    'co.uk': 13,
    'money': 14,
    'shop': 15,
    'cn': 16,
    'ws': 17
}


def pred(url):
    def prep_site(url):
        try:
            country = countries[whois(url)]
        except:
            country = 1

        try:
            d = domain[get_tld(url)]
        except:
            d = 0

        html = bow_transformer.transform([str(str(requests.get(url))[:10000])])
        return html

    return model.predict(prep_site(url))


print(pred(sys.argv[1]))