__author__ = 'Eliesse HADJEM'

import urllib.request
from html.parser import HTMLParser
import json

WORD_URL = "http://www.ratebeer.com/breweries/france/0/72/"


class MyHTMLParserCountry(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__table = False
        self.dump = []

    def handle_starttag(self, tag, attrs):
        if self.__table and "a" == tag:
            # print("Encountered a start tag:", tag, attrs)
            for tuples in attrs:
                if "href" in tuples:
                    tmp_tuple = tuples[1]
                    if "#" == tmp_tuple:
                        pass
                    else:
                        self.dump.append("http://www.ratebeer.com" + tuples[1])
        for tuples in attrs:
            if "brewerTable" in tuples:
                # print("Encountered a start tag:", tag, attrs)
                self.__table = True

    def handle_endtag(self, tag):
        if self.__table and tag == "table":
            # print("Encountered an end tag :", tag)
            self.__table = False
        pass

    def handle_data(self, data):
        if self.__table:
            # print("Encountered some data  :", data)
            pass


words = ""
f = open('breweries-fr.json', 'w')
for word in urllib.request.urlopen(WORD_URL).readlines():
    str_tmp = word.strip()
    words += str_tmp.decode('utf-8', errors='ignore')  # utf-8 works in your case

parser = MyHTMLParserCountry()
parser.feed(words)
print(json.dumps(parser.dump))
f.write(json.dumps(parser.dump, separators=(",\n ", ":\n ")))
