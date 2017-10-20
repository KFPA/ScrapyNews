import os
'''
定义xml节点字典，方便以后更改
'''
xmlElements = {
    'RULE': 'rule',
    'CATEGORY': 'category',
    'NAME': 'name',
    'ALLOW_DOMAINS': 'allow_domains',
    'FOREIGN':'foreign',
    'URLS': 'urls',
    'HOST_URL': 'host_url',
    'START_URLS': 'start_urls',
    'URLLIST': 'urllist',
    'LIST_URL':'list_url',
    'LIST_URL_TOTAL':'list_url_total',
    'ALLOW_URL':'allow_url',
    'PAGESTEP': 'pagestep',
    'PAGES': 'pages',
    'URL_REGEX': 'url_regex',
    'NEXT_PAGE': 'next_page',
    'XPATH': 'xpath',
    'TITLE': 'title',
    'TIME': 'time',
    'TYPE': 'type',
    'PUBLISH': 'publish',
    'HTML': 'html',
    'REGEXEXCLUDE': 'regexexclude',
    'TEXT': 'text',
    'IMGLINK': 'imglink',
    'FILELINK': 'filelink',

}
'''
定义爬虫的类别对应规则的类别，不同的规则生成不同的爬虫
'''
SpiderCategory={
    'CRAWL':'crawl',
    'BASE':'base',
}

"""
Topic: 定义数据库模型实体
Desc :
"""

class ArticleRule():
    # 规则是否生效
    enable = True
    #规则类型
    category=''
    #规则名称
    name=''
    # 运行的域名列表，逗号隔开
    allow_domains=[]
    #是否是国外的网站，标识是否要翻墙，采用国外ip代理
    foreign=''
    #主页url
    host_url=''
    # 开始URL列表，逗号隔开
    start_urls=[]

    # 文章标题xpath
    title_xpath = ''
    # 文章发布时间xpath
    time_xpath = ''
    # 文章类型xpath
    type_xpath = ''
    # 文章发布方
    publish_xpath = ''
    #文章全文html xpath
    html_xpath=''
    # 文章中要去掉的正在表达式，辅助html_xpath
    html_regexexculde = ''
    #文章全文text xpath
    text_xpath=''
    #图片链接
    imagelink_xpath=''
    #文件链接
    filelink_xpath=''

'''
两个爬虫模板对应爬虫规则
'''
class CrawlRule(ArticleRule):
    # 下一页的xpath
    next_page = ''
    #列表的网页链接的正则表达式
    list_url=''
    #列表的总页数的xpath
    list_page_total=''
    # 文章链接正则表达式(子串)
    allow_url = ''

class BaseRule(ArticleRule):
    #爬取的总页数
    pages=None
    #爬取的页面的间隔数
    pagestep=None
    #自动爬取页面的url
    next_page_url=''
    #获取文章页面url的正则表达式
    url_regex=''

import xml.etree.ElementTree as ET
import logging

class SpiderRulesSingletion(object):
    def __init__(self):
        self.crawlrules=[]
        self.baserules=[]
        xmlpath=os.getcwd()+'\\scrapywork\\rules\\rules.xml'
        self._parsexml(xmlpath)

    def _parsexml(self,xmlpath):
        try:
            tree=ET.parse(xmlpath)
            root=tree.getroot()
            for rule in root.findall(xmlElements.get('RULE')):
                category=rule.get(xmlElements.get('CATEGORY'))
                if category==SpiderCategory.get('CRAWL'):
                    self._parseCrawlrules(rule)
                elif category==SpiderCategory.get('BASE'):
                    self._parseBaserules(rule)
                else:
                    pass
        except Exception as e:
            logging.error('error code:%s',e)
            return False

    def _parseCrawlrules(self,rule):
        spiderrule=CrawlRule()
        spiderrule.category=SpiderCategory.get('CRAWL')
        spiderrule.name=rule.get(xmlElements.get('NAME'))
        spiderrule.allow_domains=rule.get(xmlElements.get('ALLOW_DOMAINS'))
        spiderrule.foreign=rule.get(xmlElements.get('FOREIGN'))

        urls=rule.find(xmlElements.get('URLS'))
        spiderrule.host_url=urls.find(xmlElements.get('HOST_URL')).text
        spiderrule.start_urls=urls.find(xmlElements.get('START_URLS')).text

        urllist=urls.find(xmlElements.get('URLLIST'))
        spiderrule.list_url=urllist.get(xmlElements.get('LIST_URL'))
        spiderrule.list_page_total=urllist.get(xmlElements.get('LIST_URL_TOTAL'))
        spiderrule.allow_url=urllist.get(xmlElements.get('ALLOW_URL'))
        spiderrule.next_page=urllist.find(xmlElements.get('NEXT_PAGE')).text

        xpath=rule.find(xmlElements.get('XPATH'))
        spiderrule.title_xpath=xpath.find(xmlElements.get('TITLE')).text
        spiderrule.time_xpath=xpath.find(xmlElements.get('TIME')).text
        spiderrule.type_xpath=xpath.find(xmlElements.get('TYPE')).text
        spiderrule.publish_xpath=xpath.find(xmlElements.get('PUBLISH')).text
        spiderrule.html_xpath=xpath.find(xmlElements.get('HTML')).text
        spiderrule.text_xpath=xpath.find(xmlElements.get('TEXT')).text
        spiderrule.imagelink_xpath=xpath.find(xmlElements.get('IMGLINK')).text
        spiderrule.filelink_xpath=xpath.find(xmlElements.get('FILELINK')).text

        self.crawlrules.append(spiderrule)


    def _parseBaserules(self,rule):
        spiderrule=BaseRule()
        spiderrule.category = SpiderCategory.get('CRAWL')
        spiderrule.name = rule.get(xmlElements.get('NAME'))
        spiderrule.allow_domains = rule.get(xmlElements.get('ALLOW_DOMAINS'))
        spiderrule.foreign=rule.get(xmlElements.get('FOREIGN'))

        urls=rule.find(xmlElements.get('URLS'))
        spiderrule.host_url=urls.find(xmlElements.get('HOST_URL')).text
        spiderrule.start_urls=urls.find(xmlElements.get('START_URLS')).text

        urllist=urls.find(xmlElements.get('URLLIST'))
        spiderrule.pages=urllist.get(xmlElements.get('PAGES'))
        spiderrule.pagestep=urllist.get(xmlElements.get('PAGESTEP'))
        spiderrule.url_regex=urllist.get(xmlElements.get('URL_REGEX'))
        spiderrule.next_page_url=urllist.find(xmlElements.get('NEXT_PAGE')).text

        xpath=rule.find(xmlElements.get('XPATH'))
        spiderrule.title_xpath=xpath.find(xmlElements.get('TITLE')).text
        spiderrule.time_xpath=xpath.find(xmlElements.get('TIME')).text
        spiderrule.type_xpath=xpath.find(xmlElements.get('TYPE')).text
        spiderrule.publish_xpath=xpath.find(xmlElements.get('PUBLISH')).text
        html=xpath.find(xmlElements.get('HTML'))
        spiderrule.html_regexexculde = html.get(xmlElements.get('REGEXEXCLUDE'))
        spiderrule.html_xpath = html.text
        spiderrule.text_xpath=xpath.find(xmlElements.get('TEXT')).text
        spiderrule.imagelink_xpath=xpath.find(xmlElements.get('IMGLINK')).text
        spiderrule.filelink_xpath=xpath.find(xmlElements.get('FILELINK')).text

        self.baserules.append(spiderrule)

spiderRules=SpiderRulesSingletion()

################################################################################################################################


from scrapywork.items import articleItem
from bs4 import BeautifulSoup
import re
class ItemParser(object):
    def __init__(self,rule,response):
        self.rule=rule
        self.response=response

    def parse_item(self):
        articleInfo=articleItem()
        articleInfo['url'] = self.response.url
        articleInfo['site'] = self.rule.allow_domains

        if self.rule.title_xpath:
            title = self.response.xpath(self.rule.title_xpath).extract_first().strip()
            articleInfo['title'] = title
        else:
            articleInfo['title'] = ''

        if self.rule.time_xpath:
            time = self.response.xpath(self.rule.time_xpath).extract_first().split('/')[-1].strip()
            articleInfo['time'] = self._formatetime(time)
        else:
            articleInfo['time'] = ''

        if self.rule.type_xpath:
            type = self.response.xpath(self.rule.type_xpath).extract()
            articleInfo['type'] = ' '.join(type).strip()
        else:
            articleInfo['type'] = ''

        if self.rule.publish_xpath:
            publish = self.response.xpath(self.rule.publish_xpath).extract_first()
            if publish:
                articleInfo['publish'] = publish.strip()
            else:
                articleInfo['publish'] = ''
        else:
            articleInfo['publish'] = ''

        if self.rule.html_xpath:
            htmls = self.response.xpath(self.rule.html_xpath).extract()
            html = r'\r\n'.join(htmls)
            if self.rule.html_regexexculde:
                re_exclude = re.compile(self.rule.html_regexexculde, re.S)
                html = re_exclude.sub('', html)
            articleInfo['html'] = self._fixhtml(html)
        else:
            articleInfo['html'] = ''

        xml = html
        articleInfo['xml'] = xml

        texts = self.response.xpath(self.rule.text_xpath).extract()
        articleInfo['text'] = ''.join(texts).strip()

        if self.rule.imagelink_xpath:
            articleInfo['image_urls'] = self.response.xpath(self.rule.imagelink_xpath).extract()
        if self.rule.filelink_xpath:
            articleInfo['file_urls'] = self.response.xpath(self.rule.filelink_xpath).extract()

        return articleInfo


    ''''' 
    Created on 2017-7-28 
     html代码补全 
     "<tag>xxx</tag>"正常 
     "<tag/>"正常 
     "<tag>xxx"异常-没有关闭标签 
     "xxx</tag>"异常-没有开始标签 
    @author: bean 
    '''
    def _fixhtml(self,html):
        soup = BeautifulSoup(html, 'lxml')
        fixed_html = soup.prettify()
        return fixed_html.replace('\\r\\n', '')

    '''
    格式化时间
    '''
    def _formatetime(self,time):
        regextime = '\d+? [A-Z]{3} \d{4}'
        timeres = re.match(re.compile(regextime), time)

        if timeres:
            month = ''
            timetmp = time.split(' ')
            if timetmp[1] == 'JAN':
                month = str('01')
            elif timetmp[1] == 'FEB':
                month = str('02')
            elif timetmp[1] == 'MAR':
                month = str('03')
            elif timetmp[1] == 'APR':
                month = str('04')
            elif timetmp[1] == 'MAY':
                month = str('05')
            elif timetmp[1] == 'JUN':
                month = str('06')
            elif timetmp[1] == 'JUL':
                month = str('07')
            elif timetmp[1] == 'AUG':
                month = str('08')
            elif timetmp[1] == 'SEP':
                month = str('09')
            elif timetmp[1] == 'OCT':
                month = str('10')
            elif timetmp[1] == 'NOV':
                month = str('11')
            elif timetmp[1] == 'DEC':
                month = str('12')
            return '{}-{}-{}'.format(timetmp[2], month, timetmp[0])

        else:
            return time


##########################################################################################################################
import smtplib
from email.mime.multipart import  MIMEMultipart as MI
from email.mime.text import MIMEText as MIMET
from scrapywork.models import spiderRules as spiderrules

class Mail(object):
    def __init__(self,sender,passwd,receiver):
        self.sender=sender
        self.passwd=passwd
        self.receiver=receiver
        self.smtpserver='smtp.163.com'
        self.msg_root=MI('related')
        self.msg_root['From']=sender
        self.msg_root['To']=receiver

    def sendmail(self,subject,contents):
        self.msg_root['Subject']=subject

        msg_text_str = '''
        <h1>新闻爬虫-小蛛通知</h1>
        <div>
            <ul>
        '''
        for content in contents:
            msg_text_str='\n'.join([msg_text_str,'<li>'])
            msg_text_str='\n'.join([msg_text_str,'<p>%s<p>' % content])
            msg_text_str='\n'.join([msg_text_str,'</li>'])

        msg_text_str = "\n".join([msg_text_str, '</ul>'])
        msg_text_str = "\n".join([msg_text_str, '</div>'])

        msg_text = MIMET(msg_text_str, 'html', 'utf-8')
        self.msg_root.attach(msg_text)

        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        smtp.login(self.sender, self.passwd)
        smtp.sendmail(self.sender, self.receiver, self.msg_root.as_string())
        smtp.quit()


    def get_maile_content(self):
        contents = []
        contents.append('all item count:%s' % mysqldb.queryItemCount())
        for rule in spiderrules.baserules:
            contents.append('%s:%s' % (rule.allow_domains, mysqldb.queryItemCount(rule.allow_domains)))
        for rule in spiderrules.crawlrules:
            contents.append('%s:%s' % (rule.allow_domains, mysqldb.queryItemCount(rule.allow_domains)))
        return contents

    def get_allitem_count(self):
        return mysqldb.queryItemCount()







###########################################################################################################################
import pymysql
import logging
from scrapywork.settings import db
class DatabaseSingleton(object):
    def __init__(self):
        self.database=pymysql.connect(host=db.get('host'),user=db.get('user'),passwd=db.get('passwd'),db=db.get('db'),charset=db.get('charset'))
        self.table=db.get('table')
        self.ensuretableexist()

    def __del__(self):
        self.database.close()

    def ensuretableexist(self):
        try:
            cursor=self.database.cursor()
            cursor.execute('SELECT table_name FROM information_schema.TABLES WHERE table_name=%s',self.table)
            if not cursor.fetchone():
                sql='CREATE TABLE %s(id int(10) auto_increment primary key not null,url varchar(100),INDEX urlidx(url),site varchar(100),title varchar(100),time varchar(30),type varchar(100),publish varchar(30),abstract varchar(300),label varchar(30),keyword varchar(30),html text(65535),text text(65535),xml text(65535),source text(65535))' \
                    % self.table
                cursor.execute(sql)
        except Exception as e:
            self.database.rollback()
            logging.error('--------------ensure table false-------------------exception:%s',e)
        finally:
            cursor.close()

    def insertItem(self,url,site,title,time,type,publish,html,text,xml,sources):
        try:
            cursor=self.database.cursor()
            sql='INSERT INTO {}(url,site,title,time,type,publish,html,text,xml,source) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(self.table)
            cursor.execute( sql,(url, site, title, time, type, publish, html, text, xml, sources))
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            logging.error('--------------insert false-------------------exception:%s',e)
        finally:
            cursor.close()


    def queryItem(self,url):
        try:
            cursor=self.database.cursor()
            sql='SELECT * FROM {} WHERE url=%s'.format(self.table)
            cursor.execute(sql,url)
            if cursor.fetchall():
                logging.info('query url in database:%s'% url)
                return True
            else:
                return False
        except:
            logging.error('query database error in url:%s'% url)
            return False
        finally:
            cursor.close()


    def queryItemCount(self,site=None):
        try:
            cursor=self.database.cursor()
            if site:
                sql='SELECT COUNT(*) FROM {} WHERE site=%s'.format(self.table)
                cursor.execute(sql,site)
            else:
                sql='SELECT COUNT(*) FROM {}'.format(self.table)
                cursor.execute(sql)
            return cursor.fetchone()[0]
        except:
            logging.error('query site error in database:%s'% site)
        finally:
            cursor.close()




mysqldb=DatabaseSingleton()

################################################################################################################################################################

import ctypes
from ctypes import *
from scrapywork.settings import hfs
from scrapywork.settings import IMAGES_STORE,FILES_STORE,IMAGES_UPLOAD_PATH_FULL,IMAGES_UPLOAD_PATH_SMALL,FILES_UPLOAD_PATH


class CHfs(object):
    def __init__(self):
        dlldir=os.getcwd()+'\\scrapywork\\hfs\\hfsclient.dll'
        self.hfsdll=ctypes.CDLL(dlldir)
        if self.hfsdll:
            self.hfsdll.InitApplication.restype = c_bool
            self.hfsdll.InitApplication.argtypes = (c_char_p, c_uint, c_int, c_char_p, c_char_p)
            bRet=self.hfsdll.InitApplication(bytes(hfs.get('ipaddr'),'utf-8'), int(hfs.get('port')), int(hfs.get('appid')), bytes(hfs.get('appname'),'utf-8'),bytes(hfs.get('appkey'),'utf-8'))
            if not bRet:
                logging.error('----------------hfsdll init failed.----------------')
            else:
                logging.info('-------------------hfsdll load success.----------------')
        else:
            logging.error('----------------------load dll failed.------------------')

    def UploadStreamX(self,szsrc,szdst):
        if self.hfsdll:
            self.hfsdll.UploadStreamX.restype=c_bool
            self.hfsdll.UploadStreamX.argtypes=(c_char_p,c_char_p,c_char_p)
            bRet=self.hfsdll.UploadStreamX(bytes(szsrc,'utf-8'),bytes(szdst,'utf-8'),b'')
            if bRet:
                logging.info('upload %s to %s successed.'%(szsrc,szdst))
            else:
                logging.error('upload %s to %s failed.'%(szsrc,szdst))
        else:
            logging.error('hfsdll have not loaded.')


    '''
    上传图片文件包括原图和缩略图
    szimagename 图片名称
    '''
    def UploadStreamXImages(self,szimagename):
        if self.hfsdll:
            self.hfsdll.UploadStreamX.restype = c_bool
            self.hfsdll.UploadStreamX.argtypes = (c_char_p, c_char_p, c_char_p)

            szsrc=IMAGES_STORE+'\\full\\'+szimagename
            szdst=IMAGES_UPLOAD_PATH_FULL+'\\'+szimagename
            bRetfull = self.hfsdll.UploadStreamX(bytes(szsrc, 'utf-8'), bytes(szdst, 'utf-8'), b'')
            if bRetfull:
                logging.info('upload full image %s to %s successed.' % (szsrc, szdst))
            else:
                logging.error('upload full image %s to %s failed.' % (szsrc, szdst))

            szsrc = IMAGES_STORE + '\\thumbs\\small\\' + szimagename
            szdst = IMAGES_UPLOAD_PATH_SMALL + '\\' + szimagename
            bRetsmall = self.hfsdll.UploadStreamX(bytes(szsrc, 'utf-8'), bytes(szdst, 'utf-8'), b'')
            if bRetsmall:
                logging.info('upload small image %s to %s successed.' % (szsrc, szdst))
            else:
                logging.error('upload small image %s to %s failed.' % (szsrc, szdst))
        else:
            logging.error('hfsdll have not loaded.')
        return bRetsmall and bRetfull


    '''
    上传文件
    szfilename 文件名称
    '''
    def UploadStreamXFiles(self,szfilename):
        if self.hfsdll:
            self.hfsdll.UploadStreamX.restype = c_bool
            self.hfsdll.UploadStreamX.argtypes = (c_char_p, c_char_p, c_char_p)
            szsrc=FILES_STORE+'\\full\\'+szfilename
            szdst=FILES_UPLOAD_PATH+'\\'+szfilename
            bRet = self.hfsdll.UploadStreamX(bytes(szsrc, 'utf-8'), bytes(szdst, 'utf-8'), b'')
            if bRet:
                logging.info('upload file %s to %s successed.' % (szsrc, szdst))
            else:
                logging.error('upload file %s to %s failed.' % (szsrc, szdst))
        else:
            logging.error('hfsdll have not loaded.')
        return bRet


hfs=CHfs()


#################################################################################################################################################
import requests
import json
import random
class IPProxy(object):
    def __init__(self):
        self.inlandippool=[]
        self.foreignippool=[]
        self._initipproxy(0,20,10)

    def _initipproxy(self,types,inlandcount,foreigncount):
        try:
            inlandresponse=requests.get('http://127.0.0.1:8000/?types=%s&count=%s&country=%s' % (types,inlandcount,'国内'))
            inlandip_ports=json.loads(inlandresponse.text)
            for inlandip in inlandip_ports:
                self.inlandippool.append('%s:%s' % (inlandip[0],inlandip[1]))

            foreignresponse = requests.get('http://127.0.0.1:8000/?types=%s&count=%s&country=%s' % (types, foreigncount,'国外'))
            foreignip_ports = json.loads(foreignresponse.text)
            for foreignip in foreignip_ports:
                self.foreignippool.append('%s:%s' % (foreignip[0],foreignip[1]))

            logging.info(self.inlandippool,self.foreignippool)
        except Exception as e:
            logging.error('init ippool error code:%s',e)

    def getinlandipproxy(self):
        return random.choice(self.inlandippool)

    def getforeignipproxy(self):
        return random.choice(self.foreignippool)

Ipproxy=IPProxy()
##################################################################################################################################################

if __name__ == "__main__":
    #xmlpath = os.getcwd() + '\\rules\\rules.xml'
    #rule=SpiderRulesSingletion()
    #rule._parsexml(xmlpath)
    #print(rule.baserules)
    #print(rule.crawlrules)

    ip=IPProxy()