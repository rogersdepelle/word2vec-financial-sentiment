import json
import re
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords as nltk_stopwords

stopwords = nltk_stopwords.words("english")

tree = ET.parse('files/pbr_0216.xml')

root = tree.getroot()

pbr = {}

for news in root[0]:
    #try:
    doc = news.getchildren()
    try:
        doc = doc[2].text + doc[3].text
        doc = doc.lower().split()
        word_list = set()
        for word in doc:
            clean_word = re.sub('[^a-z]', '', word)
            if clean_word and clean_word not in stopwords:
                word_list.add(clean_word)
        pbr[news.attrib['newsID']] = {'text':list(word_list)}
    except:
        print "Invalid: " + news.attrib['newsID']
        pass

training = open('training.json', 'w')

json.dump(pbr, training)

training.close()
