#!/usr/bin/env  python
# This Python file uses the following encoding: utf-8

import urllib2,httplib
import threading,Queue,re
import sys,socket,time,random
from HTMLParser import HTMLParser
from functools import wraps
from gzip import GzipFile
from StringIO import StringIO

class ContentEncodingProcessor(urllib2.BaseHandler):
  """A handler to add gzip capabilities to urllib2 requests """
 
  # add headers to requests
  def http_request(self, req):
    req.add_header("Accept-Encoding", "gzip, deflate")
    return req
 
  # decode
  def http_response(self, req, resp):
    old_resp = resp
    # gzip
    if resp.headers.get("content-encoding") == "gzip":
        gz = GzipFile(
                    fileobj=StringIO(resp.read()),
                    mode="r"
                  )
        resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
        resp.msg = old_resp.msg
    # deflate
    if resp.headers.get("content-encoding") == "deflate":
        gz = StringIO( deflate(resp.read()) )
        resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
        resp.msg = old_resp.msg
    return resp
 
# deflate support
import zlib
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
  try:               # so on top of all there's this workaround:
    return zlib.decompress(data, -zlib.MAX_WBITS)
  except zlib.error:
    return zlib.decompress(data)

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
            self.result = self.result[:-1] + '}'
            print self.result 
            self.isNext = False;
            self.result = '{'
            self.count += 1

class MeituanThread(threading.Thread):
    """docstring for MeituanThread"""

    def __init__(self, thread_id, name, counter) :
        super(MeituanThread, self).__init__()  #调用父类的构造函数 
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self) :
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


def get_food_url(self):
    cname = "finalCity.out"
    with open(cname) as f:
        cityData = f.readlines()
        
    fname = 'keyword.txt'
    with open(fname) as f:
        keywords = f.readlines()

    pname = 'proxy.txt'
    with open(pname) as f:
        proxy_list = f.readlines()

    uname = 'useragent.txt'
    with open(uname) as f:
        userAgent_list = f.readlines()
    
    for data in cityData:
        sp = []
        sp = data.split(',')
        city = sp[0].strip()
        area = sp[1].strip()

        for key in keywords:
            proxy = random.choice(proxy_list)
            userAgent = random.choice(userAgent_list)
            time.sleep(1)
            print "###### " + city.strip() + " ==> " + area.strip() + " ==> " + key.strip() + ", proxy==>" + proxy.strip() + " ######"
            url = 'http://api.union.meituan.com/data/api?city=' + city.strip() + '&category=美食&limit=10000&district_name=' + area.strip() + '&key=c6d3fd8c667c3cc4ecd1ef83337e15e7993&keyword=' + key.strip() + '&sort=1'
            processData(url, proxy, userAgent)

def retry(ExceptionToCheck, tries=3, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

class MeituanException(Exception):
    pass

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def processData(url,proxy, userAgent):
    try:
        encoding_support = ContentEncodingProcessor
        proxy_handler = urllib2.ProxyHandler({"http" : r'' + proxy.strip() })
        opener = urllib2.build_opener(encoding_support, proxy_handler)
        opener.addheaders = [('User-agent', userAgent[:-2]),('Accept-Encoding',"gzip, deflate")]
        urllib2.install_opener(opener)
        req = urllib2.urlopen(url.strip(), timeout=5)
        result = req.read()
        parser = FoodHTMLParser()
        parser.feed(result)
        parser.close()
    except urllib2.URLError, e:
        print "Time out error."
        reProcessData(url, proxy, userAgent)
    except socket.error, e:
        print "Connection Refused:" + proxy
        reProcessData(url, proxy, userAgent)
    except httplib.BadStatusLine:
        print "Bad status line:" + proxy
        reProcessData(url, proxy, userAgent)
    except httplib.IncompleteRead as e:
        print "IncompleteRead over long."
        reProcessData(url, proxy, userAgent)

@retry(urllib2.URLError, tries=3, delay=3, backoff=2)
def reProcessData(url,proxy, userAgent):
    try:
        encoding_support = ContentEncodingProcessor
        proxy_handler = urllib2.ProxyHandler({"http" : r'' + proxy.strip() })
        opener = urllib2.build_opener(encoding_support, proxy_handler)
        opener.addheaders = [('User-agent', userAgent[:-2]),('Accept-Encoding',"gzip, deflate")]
        urllib2.install_opener(opener)
        req = urllib2.urlopen(url.strip(), timeout=5)
        result = req.read()
        parser = FoodHTMLParser()
        parser.feed(result)
        parser.close()
    except urllib2.URLError, e:
        print "Time out error."
        pass
    except socket.error, e:
        print "Connection Refused:" + proxy
        pass
    except httplib.BadStatusLine:
        print "Bad status line:" + proxy
        pass
    except httplib.IncompleteRead as e:
        print "IncompleteRead over long."
        pass
            
if __name__ == '__main__':
    print "######## Start  crawling Meituan data ########"
    get_food_url(None)
    print "######## Finish crawling Meituan data ########"
