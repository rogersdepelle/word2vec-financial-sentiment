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

def pmi_odd(path_input,path_output):
    with open(path_input, "r") as news_file:
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

    with open(path_output, "w") as terms_file:
        json.dump(terms, terms_file)

def pmi_odds_daily():
    #train data
    path_datatrain_json_1=os.getcwd() +'/../files/training_with_duplicates.json'
    path_datatrain_json_2=os.getcwd() +'/../files/training_without_duplicates.json'

    #output kterms
    pathoutput_k_terms3 = os.getcwd() +'/../files/terms03.json'
    pathoutput_k_terms4 = os.getcwd() +'/../files/terms04.json'

    pmi_odd(path_datatrain_json_1,pathoutput_k_terms3)
    pmi_odd(path_datatrain_json_2,pathoutput_k_terms4)

def pmi_odds_weekly():
    #train data
    path_datatrain_json_1=os.getcwd() +'/../files2/weekly_with_duplicates_training.json'
    path_datatrain_json_2=os.getcwd() +'/../files2/weekly_without_duplicates_training.json'

    #output kterms
    pathoutput_k_terms3 = os.getcwd() +'/../files2/terms03.json'
    pathoutput_k_terms4 = os.getcwd() +'/../files2/terms04.json'

    pmi_odd(path_datatrain_json_1,pathoutput_k_terms3)
    pmi_odd(path_datatrain_json_2,pathoutput_k_terms4)
