import logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapywork.spiders.crawlspider import CrawlspiderTemplate as crawspider
from scrapywork.spiders.basespider import BasespiderTemplate as basespider
from scrapywork.spiders.ipSpider import initIPPOOL
from scrapywork.models import spiderRules as spiderrules
from twisted.internet import reactor
from scrapywork.models import Mail
import datetime

if __name__ =="__main__":
    #initIPPOOL()
    settings=get_project_settings()
    configure_logging(settings)
    mail=Mail(sender='********',passwd='********',receiver='********')
    runner=CrawlerRunner(settings)
    for rule in spiderrules.crawlrules:
        runner.crawl(crawspider,rule)
    for rule in spiderrules.baserules:
        runner.crawl(basespider,rule)
    d=runner.join()
    d.addBoth(lambda _:reactor.stop())

    startcount=mail.get_allitem_count()
    mail.sendmail(subject='Spider Start', contents=mail.get_maile_content())
    starttime=datetime.datetime.now()

    reactor.run()

    endtime=datetime.datetime.now()
    endcount=mail.get_allitem_count()
    logging.info('all finished.')

    contents=mail.get_maile_content()
    contents.insert(0,'use time : %s'% (endtime-starttime))
    contents.insert(0,'crawl item count : %s'%(endcount-startcount))
    mail.send_mail(subject='Spider All finished',contents=contents)

