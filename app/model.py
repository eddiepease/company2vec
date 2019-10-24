from .helpers import URLScraper
from .helpers import URLFinder
from .helpers import Embeddings


class Company2Vec:

    """
    Class to create company embeddings
    """

    def __init__(self, company_name, overwrite=True):
        self.company_name = company_name
        self.company_url = URLFinder().run(company=company_name)
        self.overwrite = overwrite

    def scrape(self):

        """
        Scrape all websites in company dict
        :return: None
        """

        print('Starting scrape...')
        scraper = URLScraper(overwrite=self.overwrite)
        scraper.scrape_website(company_name=self.company_name, url=self.company_url)

    def create_embeddings(self):

        """
        Create embedding from scraped file
        :return: company_embedding: numpy array of company embedding
        """

        print('Starting embeddings creation...')
        embed = Embeddings()
        company_embedding = embed.create_single_embedding(company_name=self.company_name)

        return {'company_embedding': company_embedding}

    def run(self):

        """
        Scrape website and create embeddings
        :return: company_embedding: numpy array of company embedding
        """

        print('Starting scrape...')
        self.scrape()
        print('Starting embeddings creation...')
        company_embedding = self.create_embeddings()

        return company_embedding
