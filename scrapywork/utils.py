from scrapywork.models import ArticleRule
import re


def getarticlerules():
    rules = []
    init_rule(rules)
    return rules


def init_rule(rules):
    article_rule_iaaf=ArticleRule()
    article_rule_iaaf.type='base'
    article_rule_iaaf.name='iaaf'
    article_rule_iaaf.allow_domains='iaaf.org'
    article_rule_iaaf.host_url='https://www.iaaf.org'
    article_rule_iaaf.start_urls='https://www.iaaf.org/news'
    article_rule_iaaf.next_page_url='https://www.iaaf.org/data/news/typegroup/?take=12&skip={}'
    article_rule_iaaf.url_regex='\"Articleurl\":\"(.*?)\"'
    article_rule_iaaf.pagestep=12
    article_rule_iaaf.pages=1000
    article_rule_iaaf.title_xpath='//div[@id="news"]/div/div/h1[@itemprop="name"]/text()'
    article_rule_iaaf.time_xpath='//div[@id="news"]/div/div/span/span[@itemprop="datePublished"]/text()'
    article_rule_iaaf.type_xpath='//div[@id="news"]/div/div/span/span[@class="_label type"]/a/text()'
    article_rule_iaaf.publish_xpath='//div[@id="news"]/div[1]/div[3]/span/span[@class="_label location"]/text()'
    article_rule_iaaf.html_xpath='//div[@id="news"]'
    article_rule_iaaf.html_regexexculde = '<ul class="col-md-12 prev-next".*?</ul>'
    article_rule_iaaf.text_xpath='//div[@id="news"]/div/div/article[@itemprop="articleBody"]/p/text()'
    article_rule_iaaf.imagelink_xpath = '//div[@id="news"]/div/div/ul/li/picture/img/@src | //div[@id="news"]/div/div/ul/li/picture/source/@srcset'
    article_rule_iaaf.filelink_xpath = ''
    article_rule_iaaf.enable=1

    article_rule_mp=ArticleRule()
    article_rule_mp.type='base'
    article_rule_mp.name='mp'
    article_rule_mp.allow_domains='kuaizhan.com'
    article_rule_mp.host_url='https://482809.kuaizhan.com'
    article_rule_mp.start_urls='https://482809.kuaizhan.com/'
    article_rule_mp.next_page_url='https://www.kuaizhan.com/post/ajax-postlist?site_id=4216466368&param=a891b9bfac46d41ebace9eccf88f5bbb&cur_page={}'
    article_rule_mp.url_regex='href=\'(.*?)\''
    article_rule_mp.pages=1000
    article_rule_mp.pagestep = 1
    article_rule_mp.publish_xpath='/html/body/div/div/div[@class="cell site-title"]/div/a/p/text()'
    article_rule_mp.title_xpath='//div[@id="page-content"]/div/div[@class="mod-title t0 "]/h2/text()'
    article_rule_mp.time_xpath='//div[@id="page-content"]/div/div/span[@class="time"]/text()'
    article_rule_mp.html_xpath='//div[@id="page-content"]/div[@class="mod mod-layout_floor article-hd"] | //div[@id="page-content"]/div/div/div[@class="mod mod-html"]'
    article_rule_mp.text_xpath='//div[@id="page-content"]/div/div/div/div[@class="mp-content"]/p/span/text()'
    article_rule_mp.imagelink_xpath='//div[@id="page-content"]/div/div/div/div[@class="mp-content"]/p/img/@src'


    article_rule_athletics=ArticleRule()
    article_rule_athletics.type='crawl'
    article_rule_athletics.name='athletics'
    article_rule_athletics.allow_domains='athletics.org.cn'
    article_rule_athletics.start_urls='http://www.athletics.org.cn'
    article_rule_athletics.next_page='//div[@class="nav styfff fl clear"]/ul/li/a | //div[@class="wjxz styff"]/ul/li/a'
    article_rule_athletics.list_page='.*/list.html'
    article_rule_athletics.list_page_total='//div[@class="page"]/div[@class="page02"]/text()[1]'
    article_rule_athletics.allow_url='.*/[0-9]{4}-[0-9]{2}-[0-9]{2}/[0-9]*?\.html'
    article_rule_athletics.title_xpath='//div[@class="main"]/div[@class="atitle"]/text() | //div[@class="main"]/div[@class="atitle"]/font/text()'
    article_rule_athletics.time_xpath='//div[@class="main"]/div[@class="a01 sty999"]/span/text()'
    article_rule_athletics.type_xpath='//div[@class="wei"]/a[2]/text()'
    article_rule_athletics.publish_xpath='//div[@class="main"]/div[@class="a01 sty999"]/a/text()'
    article_rule_athletics.html_xpath='//div[@class="main"]'
    article_rule_athletics.text_xpath='//div[@class="main"]/div[@class="atext"]/p/text()'
    article_rule_athletics.imagelink_xpath='//div[@class="main"]/div[@class="atext"]/p/img/@src'
    article_rule_athletics.filelink_xpath='//div[@class="main"]/div[@class="atext"]/p/a/@href'
    article_rule_athletics.enable=True

    rules.append(article_rule_iaaf)
    rules.append(article_rule_mp)
    rules.append(article_rule_athletics)

def parse_item(rule,response,articleInfo):
    articleInfo['url'] = response.url
    articleInfo['site']=rule.allow_domains

    if rule.title_xpath:
        title=response.xpath(rule.title_xpath).extract_first().strip()
        articleInfo['title'] = title
    else:
        articleInfo['title'] =''

    if rule.time_xpath:
        time = response.xpath(rule.time_xpath).extract_first().split('/')[-1].strip()
        articleInfo['time'] = formate_time(time)
    else:
        articleInfo['time'] =''

    if rule.type_xpath:
        type = response.xpath(rule.type_xpath).extract()
        articleInfo['type'] = ' '.join(type).strip()
    else:
        articleInfo['type'] =''

    if rule.publish_xpath:
        publish = response.xpath(rule.publish_xpath).extract_first()
        if publish:
            articleInfo['publish'] = publish.strip()
        else:
            articleInfo['publish']=''
    else:
        articleInfo['publish'] = ''

    if rule.html_xpath:
        htmls = response.xpath(rule.html_xpath).extract()
        html=r'\r\n'.join(htmls)
        if rule.html_regexexculde:
            re_exclude=re.compile(rule.html_regexexculde,re.S)
            html=re_exclude.sub('',html)
        articleInfo['html'] = fixhtml(html)
    else:
        articleInfo['html'] =''

    xml = html
    articleInfo['xml'] = xml

    texts = response.xpath(rule.text_xpath).extract()
    articleInfo['text']= ''.join(texts).strip()

    if rule.imagelink_xpath:
        articleInfo['image_urls']=response.xpath(rule.imagelink_xpath).extract()
    if rule.filelink_xpath:
        articleInfo['file_urls']=response.xpath(rule.filelink_xpath).extract()



def formate_time(time):
    regextime='\d+? [A-Z]{3} \d{4}'
    timeres=re.match(re.compile(regextime),time)

    if timeres:
        month=''
        timetmp=time.split(' ')
        if timetmp[1] == 'JAN':
            month = str('01')
        elif timetmp[1] == 'FEB':
            month=str('02')
        elif timetmp[1] == 'MAR':
            month = str('03')
        elif timetmp[1] == 'APR':
            month = str('04')
        elif timetmp[1] == 'MAY':
            month = str('05')
        elif timetmp[1] == 'JUN':
            month = str('06')
        elif timetmp[1] == 'JUL':
            month=str('07')
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



''''' 
Created on 2017-7-28 
 html代码补全 
 "<tag>xxx</tag>"正常 
 "<tag/>"正常 
 "<tag>xxx"异常-没有关闭标签 
 "xxx</tag>"异常-没有开始标签 
@author: bean 
'''
from bs4 import BeautifulSoup
def fixhtml(html):
    soup =BeautifulSoup(html,'lxml')
    fixed_html=soup.prettify()
    return fixed_html.replace('\\r\\n','')


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''发送电子邮件通知管理员'''
def send_maile(subject,contents):
    sender='kfpapanda@163.com'
    receiver='wpp10345@cnki.net'
    smtpserver='smtp.163.com'
    username='kfpapanda@163.com'
    passwd='kfpapanda163'
    msg_root=MIMEMultipart('related')
    msg_root['Subject']=subject
    msg_root['From']=sender
    msg_root['To']=receiver

    msg_text_str='''
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

    msg_text = MIMEText(msg_text_str, 'html', 'utf-8')
    msg_root.attach(msg_text)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, passwd)
    smtp.sendmail(sender, receiver, msg_root.as_string())
    smtp.quit()

from scrapywork.models import mysqldb
def get_maile_content(rules):
    contents=[]
    contents.append('all item count:%s'% mysqldb.queryItemCount())
    for rule in rules:
        contents.append('%s:%s'% (rule.allow_domains,mysqldb.queryItemCount(rule.allow_domains)))
    return contents

def get_allitem_count():
    return  mysqldb.queryItemCount()


