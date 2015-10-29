import urllib2
import re
import threading
import time

class ProxyCheck(threading.Thread):
    def __init__(self,lock,proxy):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.timeout = 5
        self.test_url ="http://www.baidu.com/"
        self.test_str = "030173"

    def run(self):
        global checkedProxyList
        cookies = urllib2.HTTPCookieProcessor()
        #print proxy                                                                                                                                                                                                                                                            
        arr = proxy.split(":")
        proxy_handler = urllib2.ProxyHandler({"http" : r'' + proxy })
        opener = urllib2.build_opener(cookies,proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A537a Safari/419.3')]
        urllib2.install_opener(opener)
        starttime=time.time()
        try:
            req = urllib2.urlopen(self.test_url,timeout=self.timeout)
            result = req.read()
            timeused = time.time()-starttime
            pos = result.find(self.test_str)
            if pos > -1:
                checkedProxyList.append((str(arr[0]),str(arr[1]),timeused))
                print str(arr[0]) + ":"+str(arr[1]) + " " + str(timeused)                                                                                                                                                                                                      
        except Exception,e:
            None#print e.message                                                                                                                                                                                                                                                

if __name__ == '__main__':
    pname = "proxy.txt"
    with open(pname) as f:
        proxylist = f.readlines()
    lock = threading.Lock()
    checkedProxyList=[]
    for proxy in proxylist:
        t = ProxyCheck(lock,proxy)
        t.start()
