"""This module provides a quick way to start using company2vec"""

from app.pipelines import Pipeline
from app.urls import URLFinder


def run_single(company_name):

    """
    Finds the URL, scrapes the website, returns the embedding
    :param company_name: string of company name
    :return: result: json dictionary of company embedding
    """

    url = URLFinder().run(company=company_name)
    result = Pipeline(overwrite=False).run(url=url)

    return result


def run_multiple(company_list):

    """
    Returns a list of a company embeddigs, given a respective list of company names
    :param company_list: a list of company names (string)
    :return: result: a list of embeddings (list of dicts)
    """

    result = []
    for cmp in company_list:
        result.append(run_single(company_name=cmp))

    return result


if __name__ == '__main__':
    companies = ['bbc', 'pharmaforesight']
    embeddings = run_multiple(company_list=companies)
    print('Company embeddings are:', embeddings)
