#!/usr/bin/env  python
# This Python file uses the following encoding: utf-8

import urllib
from time import strftime
from HTMLParser import HTMLParser

# create a subclass and override the handler methods                                                    
class FoodHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.count = 0
        self.data = ''
        self.result = '{'
        self.isNext = False;
        
    def handle_starttag(self, tag, attrs):
        self.data +=  '\'' + tag + '\':'

    def handle_endtag(self, tag):
        if tag == 'data':
            self.isNext = True;

    def handle_data(self, data):
        if data.strip() != '':
            self.data += '\''+ data.strip() + '\','
            #print self.data
            self.result += self.data
        self.data = ''
        if self.isNext:
            self.result = str(self.count) + '.' + self.result[:-1] + '}'
            print self.result 
            self.isNext = False;
            self.result = '{'
            self.count += 1
    
def get_food_url(self):
    fname = 'keyword.txt'
    with open(fname) as f:
        keywords = f.readlines()
    print keywords

    for key in keywords:
        print "######## " + key
        url = 'http://api.union.meituan.com/data/api?city=杭州&category=美食&limit=10000&district_name=萧山区&key=c6d3fd8c667c3cc4ecd1ef83337e15e7993&keyword=' + key + '&sort=1'
        htmlF = urllib.urlopen(url)
        htmlDOM = htmlF.read()
        parser = FoodHTMLParser()
        parser.feed(htmlDOM)
        parser.close()
        #print htmlDOM


if __name__ == '__main__':
    print "######## Start crawling food data ########"
    get_food_url(None)
    print "######## Crawl food data finished ########"
