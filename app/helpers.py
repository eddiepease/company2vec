import os
import re
import csv
import json
import numpy as np
import enchant
import requests
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field
from scrapy.settings import Settings
import scrapy.crawler as crawler
from collections import defaultdict


class URLFinder:

    """
    Uses the azure search API to search for company url given name
    """

    def __init__(self):
        self.subscription_key = 'd91d74d8fb644cd5b08fac45691fa01d'
        self.search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    def choose_url(self, results_json, url_count=0):

        """
        Extracts the url most likely to be the company website
        :param results_json: output from the API
        :param url_count:
        :return:
        """

        excluded_words = ['wikipedia', 'linkedin', 'bloomberg']
        url = results_json['webPages']['value'][url_count]['url']

        if url_count >= 10:
            url = results_json['webPages']['value'][0]['url']
        elif any(substring in url for substring in excluded_words):
            return self.choose_url(results_json, url_count=url_count + 1)

        return url

    def run(self, company):

        """
        Calls the Azure API and returns the
        :param company: company name string
        :return: url: most likely company URL
        """

        # access API
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {"q": company, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(self.search_url, headers=headers, params=params)
        results = response.json()

        # extract url from response
        url = self.choose_url(results_json=results)

        return url


class WebsiteItem(Item):

    """
    Defines the item output
    """

    company_url = Field()
    company_text = Field()


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

    lang_dictionary = enchant.Dict("en_GB")

    @classmethod
    def create(cls, link):

        """
        class method to create each new spider
        :param link: URL link of domain
        :return: insantiated spider class for that domain
        """

        domain = urlparse(link).netloc.lower()
        # generate a class name such that domain www.google.com results in class name GoogleComGenericSpider
        class_name = (domain if not domain.startswith('www.') else domain[4:]).title().replace('.', '') + cls.__name__
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
        :return: list of dictionaries, with each element of list with 'company_url' and 'company_name' keys
        """

        # extract text
        item = WebsiteItem()
        item['company_url'] = response.url
        web_text = ''.join(response.xpath(
            "//*[not(self::script or self::style or self::footer)]/text()").extract())

        # clean text
        web_text = web_text.replace('\n',' ')
        web_text = web_text.replace('\t',' ')
        web_text = " ".join(web_text.split())
        web_text = re.sub(r'[^\w\s]','',web_text).lower()

        # filter for english
        english_web_text = ' '.join([w for w in web_text.split() if self.lang_dictionary.check(w)])

        item['company_text'] = english_web_text

        yield item


class WebsiteSettings(Settings):

    """
    Defining the settings for the scraper
    """

    def generate_settings_dict(self, file_location):

        """
        Generating the settings dictionary
        :param file_location: string to temporary file location
        :return: settings_dict: dict detailing settings
        """

        settings_dict = {

            'FEED_FORMAT': 'json',
            'FEED_URI': file_location,
            'DOWNLOAD_MAXSIZE': 100000,
            'COOKIES_ENABLED': False,
            'RETRY_ENABLED': False,
            'DOWNLOAD_TIMEOUT': 15,
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
            'LOG_LEVEL': 'CRITICAL',
            'DEPTH_LIMIT': 1,
            'DEPTH_PRIORITY': 1,
            'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
            'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
            'CLOSESPIDER_ITEMCOUNT': 5

        }

        return settings_dict


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
        process = crawler.CrawlerProcess(settings=WebsiteSettings().generate_settings_dict(file_location=scrape_file_location))
        process.crawl(self.scraper.create(url))
        process.start()


class Embeddings:

    """
    Helper class for embeddings
    """

    def __init__(self):
        self.embeddings = self.read_glove_embeddings()
        self.embedding_size = len(self.embeddings['the'])

    @classmethod
    def read_glove_embeddings(cls):

        """
        Class method to read in embeddings
        :return: embeddings: dictionary of embeddings, key:word, value:embedding
        """

        embeddings = defaultdict(list)
        with open('app/data/glove.6B.50d.txt') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE)
            for row in spamreader:
                embeddings[row[0]] = row[1:]
        return embeddings

    def create_single_embedding(self, company_name):

        """
        Create single embedding for company
        :param company_name: company name string
        :return: company_embedding: embedding for single company, numpy array
        """

        # reading company text
        scrape_file_location = 'app/scrape_output/' + company_name + '.json'
        with open(scrape_file_location) as json_file:
            data = json.load(json_file)
        company_text = ' '.join([ent['company_text'] for ent in data])

        # generate embedding
        num_words = 0
        company_embedding = np.zeros(shape=(1, self.embedding_size), dtype=np.float32)
        for w in company_text.split():
            try:
                company_embedding += np.array(self.embeddings[w], dtype=np.float32)
                num_words += 1
            except ValueError:
                continue

        # normalize array
        company_embedding = company_embedding * (1/num_words)

        # remove scraped file
        os.remove(scrape_file_location)

        return company_embedding
