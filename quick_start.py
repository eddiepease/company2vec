"""This module provides a quick way to start using company2vec"""

import json

from app.urls import URLFinder
from app.pipelines import Pipeline, return_company_embedding


def run_single(company_name):

    """
    Finds the URL, scrapes the website, returns the embedding

    :param company_name: company name
    :type company_name: str

    :return: json dictionary of company embedding dictionary
    """

    # finding URL
    print('Finding URL...')
    url = URLFinder().run(company_name)

    # running scrape
    print('Running scrape...')
    Pipeline(overwrite=False).run_scrape(url)

    # return embeddings
    print('Generating embedding...')
    scrape_file_location = 'app/scrape_output/result.json'
    with open(scrape_file_location) as json_file:
        data = json.load(json_file)
    embed = return_company_embedding(data)

    return embed


if __name__ == '__main__':

    company = 'bbc'
    embedding = run_single(company)
    print(embedding)

