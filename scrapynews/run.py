import logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapywork.utils import getarticlerules
from scrapywork.utils import send_maile
from scrapywork.utils import get_maile_content
from scrapywork.utils import get_allitem_count
from scrapywork.spiders.articleSpider import ArticleSpider
from twisted.internet import reactor
from scrapywork.spiders.autoSpider import AutoSpider
import datetime
import time
if __name__ =="__main__":
    settings=get_project_settings()
    configure_logging(settings)

    runner=CrawlerRunner(settings)
    rules=getarticlerules()
    for rule in rules:
        if rule.type=='crawl':
            runner.crawl(ArticleSpider,rule)
            pass
        elif rule.type=='base':
            runner.crawl(AutoSpider,rule)
            pass
    d=runner.join()
    d.addBoth(lambda _:reactor.stop())

    startcount=get_allitem_count()
    send_maile(subject='Spider Start', contents=get_maile_content(rules))
    starttime=datetime.datetime.now()

    reactor.run()

    endtime=datetime.datetime.now()
    endcount=get_allitem_count()
    logging.info('all finished.')

    contents=get_maile_content(rules)
    contents.insert(0,'use time : %s'% (endtime-starttime))
    contents.insert(0,'crawl item count : %s'%(endcount-startcount))
    send_maile(subject='Spider All finished',contents=contents)

