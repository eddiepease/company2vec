import os
import json
from scrapy import signals
from scrapy.crawler import CrawlerRunner

from .spiders.website_spider import GenericSpider
from .settings import WebsiteSettings


class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        return self.items


def return_spider_output(output):
    """
    :param output: items scraped by CrawlerRunner
    :return: json with list of items
    """
    # this just turns items into dictionaries
    # you may want to use Scrapy JSON serializer here
    return json.dumps([dict(item) for item in output])


class URLScraper:

    """
    Brings together all the scrapy components
    """

    def __init__(self, overwrite):
        self.scraper = GenericSpider()
        self.overwrite = overwrite

    def scrape_website(self, company_name, url):

        """
        Carry out scrape of website
        :param url: URL string
        :param company_name: company name string
        :return: None
        """

        # remove temporary output file, if exists
        scrape_file_location = 'app/scrape_output/' + company_name + '.json'
        if os.path.exists(scrape_file_location):
            if self.overwrite:
                os.remove(scrape_file_location)
            else:
                return None

        # conduct scrape
        runner = MyCrawlerRunner(settings=WebsiteSettings().generate_settings_dict(file_location=scrape_file_location))
        deferred = runner.crawl(self.scraper.create(url))
        deferred.addCallback(return_spider_output)
        return deferred



