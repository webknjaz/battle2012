### -*- coding: utf-8 -*- ####################################################

import re
import urlparse

from scrapy import log # This module is useful for printing out debug information
from scrapy.item import Item
from scrapy.http import Request

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.contrib.linkextractors.lxmlhtml import LxmlParserLinkExtractor
from scrapy.contrib.loader import XPathItemLoader

from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst

from scrapy.selector import HtmlXPathSelector
from scrapy.exceptions import CloseSpider

from jobinator.collector.items import CollectorItem
from jobinator.collector.settings import CRAWL_LIMIT


class WorkJobLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('\s+', ' ', s.strip()))
    default_output_processor = TakeFirst()


class WorkSpider(CrawlSpider):
    """
    Crawls site, takes items with next data: salary, city, title, contract
    """
    name = 'workua'
    allowed_domains = ['work.ua']
    start_urls = ["http://www.work.ua/jobs/?category=1&region=0&page=1"]

    counter = 0

    rules = (
        #Let's extract all links of pages:
        #Rule(SgmlLinkExtractor(allow=('jobs\/\?category=1\&region=0\&page=\d+.*')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=("//div[@class='perpageNavigation']/span/following-sibling::noindex")), follow=True),
        #Extract jobs links
        Rule(SgmlLinkExtractor(allow=('jobs\/\d+\/.*')), callback="parse_job"),
        )


    def parse_job(self, response):
        self.counter += 1
        if self.counter > CRAWL_LIMIT:
            raise CloseSpider(reason="Crawl limit exceeded")

        hps = HtmlXPathSelector(response)
        l = WorkJobLoader(CollectorItem(), hps)
        l.add_xpath("title",    u'//div[@class="changeCenter"]/h1/text()')
        l.add_xpath("salary",   u'//div[@class="changeCenter"]/p[@class="salaryJob"]/text()')
        l.add_xpath("company",  u'//div[@class="shortInfo"]/dl/dd/b[@class="left"]/a/text()')
        l.add_xpath("contract", u'//div[@class="shortInfo"]/dl/dt[text()="Вид занятости:"]/following::dd[1]/text()')
        l.add_xpath("region",   u'//div[@class="shortInfo"]/dl/dt[text()="Город:"]/following::dd[1]/text()')
        l.add_xpath("preview",  u'//div[@class="changeCenter"]') # TODO: finish this part
        item = l.load_item()
        item["url"] = response.url

        return item


class HHSpider(CrawlSpider):
    """
    Crawls site, takes items with next data: salary, city, title, contract
    """
    name = 'hhua'
    allowed_domains = ['hh.ua']
    start_urls = ["http://hh.ua/applicant/searchvacancyresult.xml?orderBy=2&itemsOnPage=1000&areaId=5&professionalAreaId=1&compensationCurrencyCode=UAH&searchPeriod=30&page=1"]

    counter = 0

    rules = (
        #Let's extract all links of pages:
        #Rule(SgmlLinkExtractor(allow=('jobs\/\?category=1\&region=0\&page=\d+.*')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=("//div[@class='b-pager']/ul/li")), follow=True),
        #Extract jobs links
        Rule(SgmlLinkExtractor(restrict_xpaths=("//div[@class='searchresult__name']/span[@class='b-marker']")), callback="parse_job"),
#        Rule(SgmlLinkExtractor(allow=('vacancy\/\d+.*')), callback="parse_job"),
        )


    def parse_job(self, response):
        self.counter += 1
        if self.counter > CRAWL_LIMIT:
            raise CloseSpider(reason="Crawl limit exceeded")

        hps = HtmlXPathSelector(response)
        l = WorkJobLoader(CollectorItem(), hps)
        l.add_xpath("title",    u'//div[@class="b-vacancy-custom g-round"]/h1[@class="b-title b-vacancy-title"]/text()')
        l.add_xpath("salary",   u'//div[@class="b-important b-vacancy-info"]/table/tr[2]/td[1]/div/text()')
        l.add_xpath("company",  u'//div[@class="employer-marks g-clearfix"]/div[@class="companyname"]/a/text()')
        l.add_xpath("contract", u'//div[@class="b-vacancy-employmentmode l-paddings"]/div[@class="l-content-paddings"]/text()')
        l.add_xpath("region",   u'//div[@class="b-important b-vacancy-info"]/table/tr[2]/td[2]/div/text()')
        l.add_xpath("experience",   u'//div[@class="b-important b-vacancy-info"]/table/tr[2]/td[3]/div/text()')
        l.add_xpath("description",  u'//div[@id="hypercontext"]/index')
        l.add_xpath("preview",  u'//div[@id="hypercontext"]/index')
        item = l.load_item()
        item["url"] = response.url

        return item


class JobUkrSpider(CrawlSpider):
    name = 'jobukrnet'
    allowed_domains = ['job.ukr.net']
    start_urls = ["http://job.ukr.net"]

    counter = 0

    rules = (
        #Let's extract all links of pages:
        #Rule(SgmlLinkExtractor(allow=('jobs\/\?category=1\&region=0\&page=\d+.*')), follow=True),
        Rule(SgmlLinkExtractor(allow=('city/[a-z-]+/$'), deny=('city/all')), follow=True),
        Rule(SgmlLinkExtractor(allow=('it-.*')), callback='parse_first_page'),
        Rule(SgmlLinkExtractor(allow=('it-[a-z]+/[a-z-]+/$')), callback='parse_first_page'),
        Rule(SgmlLinkExtractor(allow=('vacancy/\?.*')), follow=True),
        # Rule(SgmlLinkExtractor(allow='city/it-[a-z]+/[a-z-]+/$', follow=True),
        #Extract jobs links
        Rule(SgmlLinkExtractor(allow=('vacancy/[a-z0-9-]+\d+/$'), deny=('vacancy/pay',)), callback="parse_job"),
        )

    page_url = ("http://job.ukr.net/vacancy/?RegionId=%(region)s&CityId=&"
                "page=%(page)s&Categories=%(category)s&AjaxRequest=1")

    def parse_first_page(self, response):
        self.check_limits()
        self.log('parse_first_page, url=%s' % response.url)
        hxs = HtmlXPathSelector(response)
        lastp = 1
        sel = hxs.select('//div[@class="pagerNew pagerNew2"]/a[last()]/text()')
        if sel:
            lastp = sel.extract()[0]
            u = hxs.select('//div[@class="pagerNew pagerNew2"]/a[last()]/@href').extract()[0]
            res = urlparse.urlparse(u)
            d = urlparse.parse_qs(res.query)
            if 'RegionId' in d and 'CategoryId' in d and lastp.isdigit():
                region = ['RegionId'][0]
                category = d['CategoryId'][0]
                lastp = int(lastp)
                for p in range(1, lastp + 1):
                    yield Request(self.page_url % {'region': region, 'page': p, 'category': category},)

    def parse_job(self, response):
        self.check_limits()
        hps = HtmlXPathSelector(response)
        l = WorkJobLoader(CollectorItem(), hps)
        l.add_xpath("title",    u'//div[@class="header"]//h1/text()') # 
        l.add_xpath("salary",   u'//div[@class="header"]//span[@class="salary"]/*/text()')
        l.add_xpath("company",  u'//div[@class="header"]//span[@class="companyName"]/a/text()')
        l.add_xpath("contract", u'//div[@class="vacancyBlock"]/div[@class="parameters"]/span[2]/text()')
        l.add_xpath("experience", u'//div[@class="vacancyBlock"]/div[@class="parameters"]/span[4]/text()')
        l.add_xpath("region",   u'//div[@class="search"]/span[@class="fieldValue"]/text()')
        l.add_xpath("description",  u'//div[@class="vacancyBlock"]/div[@class="description"]/*')
        l.add_xpath("preview",  u'//div[@class="vacancyBlock"]/../*')
        item = l.load_item()
        item["url"] = response.url

        return item

    def check_limits(self):
        self.counter += 1
        if self.counter > CRAWL_LIMIT:
            raise CloseSpider(reason="Crawl limit exceeded")



class DouSpider(CrawlSpider):
    name = 'douua'
    allowed_domains = ['jobs.dou.ua']
    start_urls = ["http://jobs.dou.ua/companies/"]

    rules = (
        # Let's extract all links of pages: go through all vacancies of all companies
        Rule(SgmlLinkExtractor(allow=('companies/[a-zA-Z0-9-]+/companies/$')), follow=True),
        Rule(SgmlLinkExtractor(allow=('companies/[a-zA-Z0-9-]+/vacancies/$')), follow=True),
        #Extract jobs links
        Rule(SgmlLinkExtractor(allow=('companies/[a-zA-Z0-9-]+/vacancies/\d+/$')), callback="parse_job"),
        )

    def parse_job(self, response):
        hps = HtmlXPathSelector(response)
        l = WorkJobLoader(CollectorItem(), hps)
        l.add_xpath("title",    u'//div[@class="b-vacancy"]/h1[@class="g-h2"]/text()')
        l.add_xpath("keys",    u'//div[@class="keys"]/ul/li/a')
        l.add_xpath("salary",   u'//span[@class="salary"]/text()')
        l.add_xpath("company",  u'//div[@class="company"]//div[@class="l-n"]//a[1]/text()')
        l.add_xpath("region",   u'//div[@class="sh-info"]/span[@class="place"]/text()')
        l.add_xpath("contract", u'//span[@class="place"]/span[@class="busy"]/text()')
        l.add_xpath("preview",  u'//div[@class="l-vacancy"]/*')
        description = l.get_xpath(u'//div[@class="l-vacancy"]/div[@class="requirements"]/*')
        description += l.get_xpath(u'//div[@class="l-vacancy"]/div[@class="bonuses"]/*')
        description += l.get_xpath(u'//div[@class="l-vacancy"]/div[@class="duty"]/*')
        description += l.get_xpath(u'//div[@class="l-vacancy"]/div[@class="project"]/*')
        l.add_value("description", "".join(description))

        item = l.load_item()
        item["url"] = response.url

        return item