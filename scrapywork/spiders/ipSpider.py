import requests
import urllib
import logging
from scrapywork.settings import IPPOOL
from scrapywork.settings import USE_SPECIFIED_IPPOOL
import re

def gethtmlXiciDaili():
    start_url='http://www.xicidaili.com/wn/'
    try:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }
        r=requests.get(start_url,headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ''

def parsehtml(html):
    patips='<td>([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)</td>'
    ips=re.compile(patips).findall(html)
    patports='<td>([0-9]+)</td>'
    ports=re.compile(patports).findall(html)
    IPPOOL.clear()
    for (ip,port) in zip(ips,ports):
        ipaddr={}
        ipaddr['ipaddr']='{}:{}'.format(ip,port)
        if detectip(ipaddr['ipaddr']):
            IPPOOL.append(ipaddr)

def detectip(ipaddr):
        detctipurl='http://www.whatismyip.com.tw/'
        detcttimeout=0.5
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({'http':ipaddr}))
        urllib.request.install_opener(opener)
        try:
            response = urllib.request.urlopen(detctipurl,timeout=detcttimeout)
            print('%s is available.' % ipaddr)
            return True
        except:
            logging.info('%s is disavailable.'% ipaddr)
            return False



def initIPPOOL():
    if not USE_SPECIFIED_IPPOOL:
        logging.info('构建IP池')
        html = gethtmlXiciDaili()
        parsehtml(html)
        logging.info('IP池构建完成，%s 个IP可用',len(IPPOOL))

if __name__=='__main__':
    initIPPOOL()
    print(IPPOOL)