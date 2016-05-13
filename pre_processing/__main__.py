import re
import xml.etree.ElementTree as ET

tree = ET.parse('files/pbr_0216.xml')

root = tree.getroot()

for news in root[0]:
	try:
		doc = news.getchildren()
		doc = doc[2].text + doc[3].text
		doc = doc.lower().split()
		doc = re.sub('\W*<', ' ', doc)
	except:
		pass

for word in doc:
	print word
#parser

#save new file