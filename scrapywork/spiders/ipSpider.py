import requests
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
'''
#ip_list > tbody > tr:nth-child(2)
#ip_list > tbody > tr:nth-child(2) > td:nth-child(2)
#ip_list > tbody > tr:nth-child(2) > td:nth-child(2)
'''
def parsehtml(html):
    patips='<td>([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)</td>'
    ips=re.compile(patips).findall(html)
    patports='<td>([0-9]+)</td>'
    ports=re.compile(patports).findall(html)
    IPPOOL.clear()
    for (ip,port) in zip(ips,ports):
        ipaddr={}
        ipaddr['ipaddr']='{}:{}'.format(ip,port)
        IPPOOL.append(ipaddr)

def initIPPOOL():
    if not USE_SPECIFIED_IPPOOL:
        html = gethtmlXiciDaili()
        parsehtml(html)