# -*- coding: utf-8 -*-
import re
import sys

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
    def __init__(self, url=None):
        super().__init__()
        self.__table = False
        self.__data = ""
        self.list_to_dump_itemprop = ["streetAddress", "addressLocality", "addressCountry", "postalCode", "name",
                                      "telephone"]
        self.list_to_dump_links = ["Web:", "Facebook", "Twitter"]
        self.dump = {"url": url}
        self.reg_ex = re.compile(r'[-a-z0-9._]+@([-a-z0-9]+)(\.[-a-z0-9]+)+', re.IGNORECASE)

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
        email = self.reg_ex.search(data)
        if email is not None:
            # print(email.string)
            self.dump["email"] = email.string
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

json_file_out = open('brewer.json', 'w')
json_file_in = open("breweries-fr.json")
breweries_list = json.loads(json_file_in.read())
breweries_infos = []
brewers_per_file = 50
i = 0
n = len(breweries_list)
for brewer in breweries_list:
    # print(brewer)
    microbrewery = False
    words = ""
    for word in urllib.request.urlopen(brewer).readlines():
        str_tmp = word.strip()
        str_tmp_decoded = str_tmp.decode(sys.stdout.encoding, 'replace')  # utf-8 works in your case
        if str_tmp_decoded.find("Microbrewery") > -1:
            microbrewery = True
        words += str_tmp_decoded
    if microbrewery:
        parser = MyHTMLParserBrewer(brewer)
        parser.feed(words)
        breweries_infos.append(parser.dump)
        i += 1
        print("Brasserie ", i, "/", n, ". Brasserie : ", parser.dump["name"])
        del parser
    if i > 1 and i % brewers_per_file == 0:
        num_file = i / brewers_per_file
        json_file_out = open('brewer' + str(int(num_file)) + '.json', 'w')
        json_file_out.write(json.dumps(breweries_infos, separators=(",\n ", ": "), indent=2, ensure_ascii=False))
        print("Ecriture du fichier")
        breweries_infos = []

json_file_out = open('brewer' + str(int(i / brewers_per_file + 1)) + '.json', 'w')
json_file_out.write(json.dumps(breweries_infos, separators=(",\n ", ": "), indent=2))
#print(json.dumps(parser.dump, separators=(",\n ", ": ")))
