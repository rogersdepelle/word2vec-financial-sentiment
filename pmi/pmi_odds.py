"""pmi_odds.py: computes the PMI (Pointwise mutual information) with odds

"""
import json
import os

from probabilities import pmi_odds

__author__      = "Edimar Manica"

def create_vocabulary(news):
    vocabulary = []
    for ide in news:
        vocabulary = vocabulary + news[ide]["text"]
    return set(vocabulary)

def frequencies(news, vocabulary):
    positive_words = dict.fromkeys(vocabulary, 0.0)
    negative_words = dict.fromkeys(vocabulary, 0.0)
    pn = 0; #number of POSITIVE news
    nn = 0; #number of NEGATIVE news

    for id in news:
        if news[id]["label"] == "positive":
            pn += 1
            for w in set(news[id]["text"]):
                positive_words[w] += 1.0
        else:
            nn += 1
            for w in set(news[id]["text"]):
                negative_words[w] += 1.0

    return pn, nn, positive_words, negative_words


with open(os.getcwd() + '/../files/training_with_duplicates.json', "r") as news_file:
    training_set = json.load(news_file)
#print(training_set)

vocabulary = create_vocabulary(training_set)
#print(vocabulary)

pn, nn, positive_words, negative_words = frequencies(training_set, vocabulary)
#print (pn, nn, positive_words, negative_words)

terms = {"positive":[], "negative":[]}
for word in vocabulary:
    #print (word, pn, nn, positive_words[word], negative_words[word])
    positive_pmi = pmi_odds(positive_words[word], pn, negative_words[word], nn)
    terms["positive"].append((word, positive_pmi))
    negative_pmi = pmi_odds(negative_words[word], nn, positive_words[word], pn)
    terms["negative"].append((word, negative_pmi))


terms["positive"].sort(key=lambda tup: tup[1], reverse=True)
terms["negative"].sort(key=lambda tup: tup[1], reverse=True)

with open(os.getcwd() + '/../files/terms02.json', "w") as terms_file:
    json.dump(terms, terms_file)



