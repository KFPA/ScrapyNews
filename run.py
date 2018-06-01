import logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapywork.spiders.crawlspider import CrawlspiderTemplate as crawspider
from scrapywork.spiders.basespider import BasespiderTemplate as basespider
from scrapywork.models import spiderRules as spiderrules
from twisted.internet import reactor
from scrapywork.models import Mail
import datetime

if __name__ =="__main__":
    starttime=datetime.datetime.now()
    configure_logging(install_root_handler=False)
    settings=get_project_settings()
    configure_logging(settings)
    mail=Mail(sender='kfpapanda@163.com',passwd='WUPANWANG123',receiver='kfpapanda@163.com')
    runner=CrawlerRunner(settings)
    for rule in spiderrules.crawlrules:
        runner.crawl(crawspider,rule)
    for rule in spiderrules.baserules:
        runner.crawl(basespider,rule)
    d=runner.join()
    d.addBoth(lambda _:reactor.stop())

    startcount=mail.get_allitem_count()

    reactor.run()

    endtime=datetime.datetime.now()
    endcount=mail.get_allitem_count()
    logging.info('all finished.')
    contents=mail.get_maile_content()
    contents.insert(0,'use time : %s'% (endtime-starttime))
    contents.insert(0,'crawl item count : %s'%(endcount-startcount))
    mail.sendmail(subject='Spider Reports',contents=contents)

