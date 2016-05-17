#BRUNO IOCHINS GRISCI

import json
import sys
import math
import os

def create_vocabulary(news):
    vocabulary = []
    for ide in news:
        vocabulary = vocabulary + news[ide]["text"]
    return set(vocabulary)

def count_labels(news):
    n_positive_news = 0.0
    n_negative_news = 0.0
    for ide in news:
        if news[ide]["label"] == "positive":
            n_positive_news += 1.0
        else:
            n_negative_news += 1.0
    return n_positive_news, n_negative_news
    
def count_words(news, vocabulary):
    positive_words = dict.fromkeys(vocabulary, 0.0)
    negative_words = dict.fromkeys(vocabulary, 0.0)
    total_words = 0.0
    for ide in news:
        if news[ide]["label"] == "positive":
            for w in news[ide]["text"]:
                positive_words[w] += 1.0
        else:
            for w in news[ide]["text"]:
                negative_words[w] += 1.0
        total_words += len(news[ide]["text"])
    return positive_words, negative_words, total_words
        
def compute_pmi(p_word, p_label, p_word_label):
    #print(p_word, p_label, p_word_label)
    if p_word_label / (p_word * p_label) != 0.0:
        pmi = math.log(p_word_label / (p_word * p_label), 2.0)
    else:
        pmi = 0.0
    return pmi

def pmi(path_input,path_output):
    #news_file_path = os.getcwd() +'/../files/training_with_duplicates.json'
    news_file = open(path_input, "r")
    training_set = json.load(news_file)
    news_file.close()
    #print(training_set)

    vocabulary = create_vocabulary(training_set)
    #print(vocabulary)

    n_positive_news, n_negative_news = count_labels(training_set)
    #print(n_positive_news, n_negative_news)

    positive_words, negative_words, total_words = count_words(training_set, vocabulary)
    #print(positive_words)
    #print(negative_words)
    #print(total_words)

    total_positive_words = 0.0
    for word in positive_words:
        total_positive_words += positive_words[word]

    total_negative_words = 0.0
    for word in negative_words:
        total_negative_words += negative_words[word]

    terms = {"positive":[], "negative":[]}
    for word in vocabulary:
        positive_pmi = compute_pmi((positive_words[word] + negative_words[word]) / total_words, n_positive_news / len(training_set), positive_words[word] / total_positive_words)
        terms["positive"].append((word, positive_pmi))
        negative_pmi = compute_pmi((positive_words[word] + negative_words[word]) / total_words, n_negative_news / len(training_set), negative_words[word] / total_negative_words)
        terms["negative"].append((word, negative_pmi))

    terms["positive"].sort(key=lambda tup: tup[1], reverse=True)
    terms["negative"].sort(key=lambda tup: tup[1], reverse=True)

    terms_file = open(path_output, "w")
    json.dump(terms, terms_file)
    terms_file.close()


def pmi_daily():
    #train data
    path_datatrain_json_1=os.getcwd() +'/../files/training_with_duplicates.json'
    path_datatrain_json_2=os.getcwd() +'/../files/training_without_duplicates.json'

    #output kterms
    pathoutput_k_terms1 = os.getcwd() +'/../files/terms01.json'
    pathoutput_k_terms2 = os.getcwd() +'/../files/terms02.json'

    pmi(path_datatrain_json_1,pathoutput_k_terms1)
    pmi(path_datatrain_json_2,pathoutput_k_terms2)

    pmi(path_datatrain_json_1,pathoutput_k_terms1)
    pmi(path_datatrain_json_2,pathoutput_k_terms2)

def pmi_weekly():
    #train data
    path_datatrain_json_1=os.getcwd() +'/../files2/weekly_with_duplicates_training.json'
    path_datatrain_json_2=os.getcwd() +'/../files2/weekly_without_duplicates_training.json'

    #output kterms
    pathoutput_k_terms1 = os.getcwd() +'/../files2/terms01.json'
    pathoutput_k_terms2 = os.getcwd() +'/../files2/terms02.json'

    pmi(path_datatrain_json_1,pathoutput_k_terms1)
    pmi(path_datatrain_json_2,pathoutput_k_terms2)

    pmi(path_datatrain_json_1,pathoutput_k_terms1)
    pmi(path_datatrain_json_2,pathoutput_k_terms2)

pmi_weekly()









    
