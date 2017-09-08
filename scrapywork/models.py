"""
Topic: 定义数据库模型实体
Desc :
"""

class ArticleRule():
    #规则类型
    type=''
    #规则名称
    name=''
    # 运行的域名列表，逗号隔开
    allow_domains=[]
    #主页url
    host_url=''
    # 开始URL列表，逗号隔开
    start_urls=[]
    # 下一页的xpath
    next_page = ''
    #自动爬取页面的url
    next_page_url=''
    #获取文章页面url的正则表达式
    url_regex=''
    #列表的网页链接的正则表达式
    list_page=''
    #列表的总页数的xpath
    list_page_total=''
    # 文章链接正则表达式(子串)
    allow_url = ''
    # 文章链接提取区域xpath
    extract_from = ''
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
    #文章中要去掉的正在表达式，辅助html_xpath
    html_regexexculde=''
    #文章全文text xpath
    text_xpath=''
    #图片链接
    imagelink_xpath=''
    #文件链接
    filelink_xpath=''
    # 规则是否生效
    enable = True

    #爬取的总页数
    pages=None
    #爬取的页面的间隔数
    pagesetp=None



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



import ctypes
from ctypes import *
from scrapywork.settings import hfs
from scrapywork.settings import IMAGES_STORE,FILES_STORE,IMAGES_UPLOAD_PATH_FULL,IMAGES_UPLOAD_PATH_SMALL,FILES_UPLOAD_PATH
import os

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



if __name__ == "__main__":
    h=CHfs()