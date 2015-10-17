#!/usr/bin/env  python

import urllib
from time import strftime
from HTMLParser import HTMLParser

# create a subclass and override the handler methods                                                    
class MTHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.count = 0
        self.data = ''
    
    def handle_data(self, data):
        if data.strip() != '':
            if self.count % 6 != 0:
                self.data =  self.data.strip() + ',' + data.strip()
            else:
                if self.count > 0:
                    print str(self.count/6) + self.data
                self.data = ''    
            self.count += 1

def get_city_url(self):
    url = 'http://www.meituan.com/api/v1/divisions'
    htmlF = urllib.urlopen(url)
    htmlDOM = htmlF.read()
    parser = MTHTMLParser()
    parser.feed(htmlDOM)
    parser.close()
    #print htmlDOM 


if __name__ == '__main__':
    #print "######## Start crawling city data ########"
    get_city_url(None)
    #print "######## Crawl city data finished ########"
