import csv
import json
import re

from nltk.corpus import stopwords as nltk_stopwords
from xml.etree import ElementTree
from datetime import datetime


petr4_daily_file = open('files/petr4_daily.csv', 'rb')
petr4_daily = csv.DictReader(petr4_daily_file)

petr4_weekly_file = open('files/petr4_weekly.csv', 'rb')
petr4_weekly = csv.DictReader(petr4_weekly_file)

stopwords = nltk_stopwords.words("english")

log = open('files/log.json', 'w')

tree = ElementTree.parse('files/pbr_0216.xml')

pbr = tree.getroot()

pbr_with_duplicates = {}
pbr_without_duplicates = {}

for news in pbr[0]:
    try:
        news_id = news.attrib['newsID']
        doc = news.getchildren()
        
        news_date = datetime.strptime(doc[1].text[:-4], '%a %b %d, %Y %I:%M%p')
        for day in petr4_daily:
            if day['Date'] == news_date.strftime('%Y-%m-%d') and day['Volume'] != '000':
                if float(day['Close']) - float(day['Open']) > 0:
                    label = "positive"
                else:
                    label = "negative"

                doc = doc[2].text + doc[3].text
                doc = doc.lower().split()

                word_list = set()
                for word in doc:
                    clean_word = re.sub('[^a-z]', '', word)
                    if clean_word and clean_word not in stopwords:
                        word_list.add(clean_word)
                word_list = list(word_list)

                pbr_with_duplicates[news_id] = {}
                pbr_with_duplicates[news_id]['text'] = word_list
                pbr_with_duplicates[news_id]['label'] = label
                if word_list not in pbr_without_duplicates.values():
                    pbr_without_duplicates[news_id] = pbr_with_duplicates[news_id].copy()
                break
    except:
        log.write("\nInvalid news: " + news_id)

training_with_duplicates = open('files/training_with_duplicates.json', 'w')
training_without_duplicates = open('files/training_without_duplicates.json', 'w')

log.write("\n\nPBR With Duplicates Total: " + str(len(pbr_with_duplicates)))
log.write("\nPBR Without Duplicates Total: " + str(len(pbr_without_duplicates)))

json.dump(pbr_with_duplicates, training_with_duplicates)
json.dump(pbr_without_duplicates, training_without_duplicates)

training_with_duplicates.close()
training_without_duplicates.close()
log.close()

petr4_daily_file.close()
petr4_weekly_file.close()