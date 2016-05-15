#BRUNO IOCHINS GRISCI

import json
import sys
import math

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

news_file_path = sys.argv[1]
news_file = open(news_file_path, "r")
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
    
terms_file = open("terms.json", "w")
json.dump(terms, terms_file)
terms_file.close()














    
