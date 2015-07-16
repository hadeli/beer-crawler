# -*- coding: utf-8 -*-

__author__ = 'Eliesse HADJEM'

from html.parser import HTMLParser
import json
import urllib.request

ACCENT_AIGU = "\\u00e9"
ACCENT_GRAVE = "\\u00e8"
C_CEDILLE = "\\u00e7"
A_ACCENTUE = "\\u00e0"
E_CIRCONFLEXE = "\\u00ea"

decoder = {ACCENT_AIGU: "é",
           ACCENT_GRAVE: "è",
           C_CEDILLE: "ç",
           A_ACCENTUE: "à",
           E_CIRCONFLEXE: "ê"}

class MyHTMLParserBrewer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__table = False
        self.__data = ""
        self.list_to_dump_itemprop = ["streetAddress", "addressLocality", "addressCountry", "postalCode", "name",
                                      "telephone"]
        self.list_to_dump_links = ["Web:", "Facebook", "Twitter"]
        self.dump = {}

    def handle_starttag(self, tag, attrs):
        if "span" == tag:
            # print(tag, attrs)
            pass
        for att in attrs:
            # if "itemprop" in att:
            #     print("itemprop", tag, attrs)
            for itemprop in self.list_to_dump_itemprop:

                if "itemprop" in att and itemprop in att:
                    #print(itemprop)
                    self.__data = itemprop

    def handle_endtag(self, tag):
        if self.__table and tag == "table":
            #print("Encountered an end tag :", tag)
            self.__table = False
        pass

    def handle_data(self, data):
        if len(self.__data) > 0:
            for key in decoder:
                # print("La chaine ", key, " dans la ", data, "a été trouvé ", data.find(key))
                data = data.replace(key, decoder[key])
            self.dump[self.__data] = data
            #print(data)
            self.__data = ""
            pass
        for tag_link in self.list_to_dump_links:
            if tag_link in data:
                self.__data = tag_link


words = ""
json_file_out = open('brewer.json', 'w')
json_file_in = open("breweries-fr.json")
breweries_list = json.loads(json_file_in.read())
breweries_infos = []
i = 0
n = len(breweries_list)
for brewer in breweries_list:
    # print(brewer)
    microbrewery = False
    for word in urllib.request.urlopen(brewer).readlines():
        str_tmp = word.strip()
        str_tmp_decoded = str_tmp.decode('utf8', 'ignore')  # utf-8 works in your case
        if str_tmp_decoded.find("Microbrewery") > -1:
            microbrewery = True
        words += str_tmp_decoded
    if microbrewery:
        parser = MyHTMLParserBrewer()
        parser.feed(words)
        breweries_infos.append(parser.dump)
        i += 1
        print("Brasserie ", i, "/", n, ". Microbrasserie : ", microbrewery)
json_file_out.write(json.dumps(breweries_infos, separators=(",\n ", ": "), indent=2))
#print(json.dumps(parser.dump, separators=(",\n ", ": ")))
