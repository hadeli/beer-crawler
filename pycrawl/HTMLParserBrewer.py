__author__ = 'Eliesse HADJEM'

from html.parser import HTMLParser
import json
import urllib.request


class MyHTMLParserBrewer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__table = False
        self.__data = ""
        self.list_to_dump_itemprop = ["streetAddress", "addressLocality" "addressCountry", "postalCode", "name"]
        self.dump = {}

    def handle_starttag(self, tag, attrs):
        for att in attrs:
            # if "itemprop" in att:
            #     print("itemprop", tag, attrs)
            for itemprop in self.list_to_dump_itemprop:
                tmp_tuple = ("itemprop", itemprop)
                if tmp_tuple in attrs:
                    print(itemprop)
                    self.__data = itemprop
                    self.list_to_dump_itemprop.remove(itemprop)
                    return

    def handle_endtag(self, tag):
        if self.__table and tag == "table":
            # print("Encountered an end tag :", tag)
            self.__table = False
        pass

    def handle_data(self, data):
        if len(self.__data) > 0:
            self.dump[self.__data] = data
            self.__data = ""
            pass


words = ""
f = open('breweries-fr.json', 'w')
for word in urllib.request.urlopen("http://www.ratebeer.com/brewers/3-abbayes-cinarbo/13361/").readlines():
    str_tmp = word.strip()
    words += str_tmp.decode('utf-8', errors='ignore')  # utf-8 works in your case

parser = MyHTMLParserBrewer()
parser.feed(words)
print(json.dumps(parser.dump))
f.write(json.dumps(parser.dump, separators=(",\n ", ":\n ")))
