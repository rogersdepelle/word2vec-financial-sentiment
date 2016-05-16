"for run(in up dir): $python pre_processing"

import csv
import json
import re
import random

from nltk.corpus import stopwords as nltk_stopwords
from xml.etree import ElementTree
from datetime import datetime


def gen_test(pbr_file):
    test_keys = random.sample(pbr_file, int(len(pbr_file)*0.2))
    test = {}
    for key in test_keys:
        test[key] = pbr_file[key]
        del pbr_file[key]
    return test


petr4_daily_file = open('files/petr4_daily.csv', 'r')
petr4_daily = csv.DictReader(petr4_daily_file)
petr4_daily = [x for x in petr4_daily]

petr4_weekly_file = open('files/petr4_weekly.csv', 'r')
petr4_weekly = csv.DictReader(petr4_weekly_file)
petr4_weekly = [x for x in petr4_weekly]

stopwords = nltk_stopwords.words("english")

tree = ElementTree.parse('files/pbr_0216.xml')

pbr = tree.getroot()

pbr_with_duplicates = {}
pbr_without_duplicates = {}
news_list = set()
invalide_news = []
weekend_news = []

for news in pbr[0]:
    try:
        news_id = news.attrib['newsID']
        doc = news.getchildren()
        
        news_date = datetime.strptime(doc[1].text[:-4], '%a %b %d, %Y %I:%M%p')
        for day in petr4_daily:
            if day['Date'] == news_date.strftime('%Y-%m-%d'):
                if day['Volume'] != '000':
                    if float(day['Close']) - float(day['Open']) >= 0:
                        label = "positive"
                    else:
                        label = "negative"

                    doc = doc[2].text + " " + doc[3].text
                    clean_doc = doc.lower()
                    clean_doc = re.sub("[^a-z]", " ", clean_doc).split()

                    word_list = set()
                    for word in clean_doc:
                        clean_word = re.sub('[^a-z]', '', word)
                        if clean_word and clean_word not in stopwords:
                            word_list.add(clean_word)
                    word_list = list(word_list)

                    pbr_with_duplicates[news_id] = {}
                    pbr_with_duplicates[news_id]['text'] = word_list
                    pbr_with_duplicates[news_id]['label'] = label
                    if doc not in news_list:
                        pbr_without_duplicates[news_id] = pbr_with_duplicates[news_id].copy()
                        news_list.add(doc)
                    break
                else:
                    weekend_news.append(news_id)
    except:
        invalide_news.append(news_id)

petr4_daily_file.close()
petr4_weekly_file.close()

test_with_duplicates = open('files/test_with_duplicates.json', 'w')
json.dump(gen_test(pbr_with_duplicates), test_with_duplicates)
test_with_duplicates.close()

training_with_duplicates = open('files/training_with_duplicates.json', 'w')
json.dump(pbr_with_duplicates, training_with_duplicates)
training_with_duplicates.close()

test_without_duplicates = open('files/test_without_duplicates.json', 'w')
json.dump(gen_test(pbr_without_duplicates), test_without_duplicates)
test_without_duplicates.close()

training_without_duplicates = open('files/training_without_duplicates.json', 'w')
json.dump(pbr_without_duplicates, training_without_duplicates)
training_without_duplicates.close()

log = open('files/log.json', 'w')
log.write("Pre Processing Logs")
log.write("\n\nPBR With Duplicates Total: " + str(len(pbr_with_duplicates)))
log.write("\nPBR Without Duplicates Total: " + str(len(pbr_without_duplicates)))
log.write("\n\nInvalid News: " + str(invalide_news))
log.write("\nWeekend News: " + str(weekend_news))
log.close()
