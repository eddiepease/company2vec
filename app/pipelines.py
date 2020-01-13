"""This module defines all the objects necessary to control the app"""

import os
import json
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from app.spiders.website_spider import GenericSpider
from app.settings import WebsiteSettings
from app.embeddings import Embeddings


class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):

        """
        Launch a crawl and return output as deferred

        :param crawler_or_spidercls: scrapy crawler
        :type crawler_or_spidercls: cls

        :return: deferred object with crawled output
        """

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

        """
        Append each individual item scraped

        :param item: scrapy item
        :type item: cls

        :return: None
        """

        self.items.append(item)

    def return_items(self, result):

        """
        Return scrapy items

        :return scrapy items
        """

        return self.items


def return_spider_output(output):

    """
    Turns scrapy output into dictionaries
    :param output: items scraped by CrawlerRunner
    :type output: dict

    :return: json with list of items
    """

    # this just turns items into dictionaries
    return [dict(item) for item in output]


def return_company_embedding(company_data):

    """
    Turns scrapy output into an embedding

    :param company_data: scraped data for the company, list of dictionaries
    :type company_data: list

    :return: company embedding dictionary
    """

    embed = Embeddings()
    company_embedding = embed.create_single_embedding(company_data)
    company_dict = json.dumps({'company_embedding': company_embedding})

    return company_dict


class Pipeline:

    """
    Brings together all the scrapy components
    """

    def __init__(self, overwrite):
        self.scraper = GenericSpider()
        self.overwrite = overwrite

    def run(self, url):

        """
        Carry out scrape of website

        :param url: URL of website
        :type url: str

        :return: deferred object
        """

        # remove historic file
        scrape_file_location = 'app/scrape_output/result.json'
        if os.path.exists(scrape_file_location):
            os.remove(scrape_file_location)

        # conduct scrape
        runner = MyCrawlerRunner(settings=WebsiteSettings().
                                 generate_settings_dict(file_location=scrape_file_location))
        deferred = runner.crawl(self.scraper.create(url))
        deferred.addCallback(return_spider_output)
        deferred.addCallback(return_company_embedding)
        return deferred

    def run_scrape(self, url):

        """
        Runs a twisted reactor and returns the scraped output to a local file

        :param url: URL of website
        :type url: str

        :return: None
        """

        # remove historic file
        scrape_file_location = 'app/scrape_output/result.json'
        if os.path.exists(scrape_file_location):
            os.remove(scrape_file_location)

        # conduct scrape
        runner = MyCrawlerRunner(settings=WebsiteSettings().
                                 generate_settings_dict(file_location=scrape_file_location))
        deferred = runner.crawl(self.scraper.create(url))

        # run reactor
        reactor.callLater(30, reactor.stop)
        reactor.run()
