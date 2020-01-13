""" This module defines a generic scrapy spider that can be used for any website"""

import os
import re
import json
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from app.items import WebsiteItem


class GenericSpider(CrawlSpider):

    """
    A generic spider, uses type() to make new spider classes for each domain.
    This is required so that different spiders can be created when more than
    one domain is scrapped.
    """

    name = 'generic'
    allowed_domains = []
    start_urls = []

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    dirname = os.path.dirname(__file__)
    with open(os.path.join('/'.join(dirname.split('/')[:-1]), 'data/', 'words_dictionary.json')) as json_file:
        lang_dictionary = json.load(json_file)

    @classmethod
    def create(cls, link):

        """
        class method to create each new spider

        :param link: URL link of domain
        :type link: str

        :return: instantiated spider class for that domain
        """

        domain = urlparse(link).netloc.lower()
        # generate a class name (e.g. www.google.com = GoogleComGenericSpider)
        class_name = (domain if not domain.startswith('www.')
                      else domain[4:]).title().replace('.', '') + cls.__name__
        return type(class_name, (cls,), {
            'allowed_domains': [domain],
            'start_urls': [link],
            'name': domain
        })

    # parse each url
    def parse_item(self, response):

        """
        Ordering the response from each URL

        :param response: response from URL
        :type response: dict

        :return: list of dictionaries- each element of list with 'company_url' & 'company_name' keys
        """

        # extract text
        item = WebsiteItem()
        item['company_url'] = response.url
        web_text = ''.join(response.xpath(
            "//*[not(self::script or self::style or self::footer)]/text()").extract())

        # clean text
        web_text = web_text.replace('\n', ' ')
        web_text = web_text.replace('\t', ' ')
        web_text = " ".join(web_text.split())
        web_text = re.sub(r'[^\w\s]', '', web_text).lower()

        # filter for english
        english_web_text = ' '.join([w for w in web_text.split() if w in self.lang_dictionary])

        item['company_text'] = english_web_text

        yield item
