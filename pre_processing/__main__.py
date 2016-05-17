"""
    news
    {
        'daily_with_duplicates':[
            {'id1':{'text':['word1', 'word2'...],"label":"positive"}}...
        ],
        'daily_without_duplicates':[
            {'id1':{'text':['word1', 'word2'...],"label":"negative"}}...
        ],
        'weekly_with_duplicates':[
            {'id1':{'text':['word1', 'word2'...],"label":"positive"}}...
        ],
        'weekly_without_duplicates':[
            {'id1':{'text':['word1', 'word2'...],"label":"negative"}}...
        ],
    }
"""


import csv
import json
import re
import random
import sys

from os.path import isfile
from nltk.corpus import stopwords as nltk_stopwords
from xml.etree import ElementTree
from datetime import datetime, timedelta


def get_news(file_patch):
    """
        Perform the news parse in file, returns news dict.
    """
    try:
        tree = ElementTree.parse(file_patch)
        root = tree.getroot()
    except:
        print "Invalid News File!"
        sys.exit()


    stopwords = nltk_stopwords.words("english")
    news_list = []
    news = {
        'with_duplicates':{},
        'without_duplicates':{},
    }
    log = {
        'invalid_news': [],
        'holiday_news': [],
    }

    for news_obj in root[0]:
        news_id = news_obj.attrib['newsID']
        doc = news_obj.getchildren()

        news_date = datetime.strptime(doc[1].text[:-4], '%a %b %d, %Y %I:%M%p')
        try:
            doc = doc[2].text + " " + doc[3].text
        except:
            log['invalid_news'].append(news_id)
            continue

        doc = doc.lower()
        doc = re.sub("[^a-z]", " ", doc).split()

        word_list = set()
        for word in doc:
            clean_word = re.sub('[^a-z]', '', word)
            if clean_word and clean_word not in stopwords:
                word_list.add(clean_word)
        word_list = list(word_list)

        news['with_duplicates'][news_id] = {}
        news['with_duplicates'][news_id]['text'] = word_list
        news['with_duplicates'][news_id]['date'] = news_date
        if word_list not in news_list:
            news['without_duplicates'][news_id] = news['with_duplicates'][news_id].copy()
            news_list.append(word_list)

    return news, log


def set_label_news(docs, log, days, weeks):
    """
        Assign a label to the news according to variation in share price.
    """
    daily = {}
    weekly = {}

    for doc in docs:
        for day in days:
            if day['Date'] == docs[doc]['date'].strftime('%Y-%m-%d'):
                if day['Volume'] != '000':
                    new_doc = {}
                    if float(day['Close']) - float(day['Open']) >= 0:
                        new_doc['label'] = "positive"
                    else:
                        new_doc['label'] = "negative"
                    new_doc['text'] = docs[doc]['text']
                    daily[doc] = new_doc
                    break
                else:
                   log['holiday_news'].append(news_id)

        for week in weeks:
            week_begin = datetime.strptime(week['Date'], '%Y-%m-%d')
            week_end = week_begin + timedelta(days=7)
            if week_begin <= docs[doc]['date'] < week_end:
                if float(week['Close']) - float(week['Open']) >= 0:
                    new_doc['label'] = "positive"
                else:
                    new_doc['label'] = "negative"
                weekly[doc] = new_doc
                break
    return daily, weekly


def set_label(news, log, daily_file, weekly_file):
    """
        Call set_label_news for each dict news.
    """
    try:
        daily_file = open(daily_file, 'r')
        days = csv.DictReader(daily_file)
        days = [x for x in days]
        daily_file.close()
    except:
        print "Invalid Quotations Daily File!"
        sys.exit()

    try:
        weekly_file = open(weekly_file, 'r')
        weeks = csv.DictReader(weekly_file)
        weeks = [x for x in weeks]
        weekly_file.close()
    except:
        print "Invalid Quotations Weekly File!"
        sys.exit()

    news['daily_with_duplicates'], news['weekly_with_duplicates'] = set_label_news(news['with_duplicates'], log, days, weeks)
    news['daily_without_duplicates'], news['weekly_without_duplicates'] = set_label_news(news['without_duplicates'], log, days, weeks)
    del news['with_duplicates']
    del news['without_duplicates']

def gen_test(news):
    """
        Divides the set into two sets, training(80%) and test(20%)
    """
    test_keys = random.sample(news, int(len(news)*0.2))
    test = {}
    for key in test_keys:
        test[key] = news[key]
        del news[key]
    return test


def save_files(news):
    """
        Saves the news dictionaries in 8 different files, training and test
    """
    file = open('files/daily_with_duplicates_test.json', 'w')
    json.dump(gen_test(news['daily_with_duplicates']), file)
    file.close()

    file = open('files/daily_with_duplicates_training.json', 'w')
    json.dump(news['daily_with_duplicates'], file)
    file.close()

    file = open('files/weekly_with_duplicates_test.json', 'w')
    json.dump(gen_test(news['weekly_with_duplicates']), file)
    file.close()

    file = open('files/weekly_with_duplicates_training.json', 'w')
    json.dump(news['weekly_with_duplicates'], file)
    file.close()

    file = open('files/daily_without_duplicates_test.json', 'w')
    json.dump(gen_test(news['daily_without_duplicates']), file)
    file.close()

    file = open('files/daily_without_duplicates_training.json', 'w')
    json.dump(news['daily_without_duplicates'], file)
    file.close()

    file = open('files/weekly_without_duplicates_test.json', 'w')
    json.dump(gen_test(news['weekly_without_duplicates']), file)
    file.close()

    file = open('files/weekly_without_duplicates_training.json', 'w')
    json.dump(news['weekly_without_duplicates'], file)
    file.close()

def save_log(log, news):
    """
        Saves the log dict in log file
    """
    log_file = open('files/log.json', 'w')
    log_file.write("Pre Processing Logs")
    log_file.write("\n\nTotal With Duplicates: " + str(len(news['weekly_with_duplicates'])))
    log_file.write("\nTotal Without Duplicates: " + str(len(news['weekly_without_duplicates'])))
    log_file.write("\n\nInvalid News: " + str(log['invalid_news']))
    log_file.write("\nWeekend News: " + str(log['holiday_news']))
    log_file.close()


def main():
    if len(sys.argv) >= 4:
        news, log = get_news(sys.argv[1])
        set_label(news, log, sys.argv[2], sys.argv[3])
        save_files(news)
        save_log(log, news)
    else:
        print "Insert files path."


if __name__ == "__main__":
    main()