"""This module generates company embeddings given company data and pre-trained word embeddings"""

import csv
from collections import defaultdict
import numpy as np


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

        :return: dictionary of embeddings, key:word, value:embedding
        """

        embeddings = defaultdict(list)
        with open('app/data/glove.6B.50d.txt', encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE)
            for row in spamreader:
                embeddings[row[0]] = row[1:]
        return embeddings

    def create_single_embedding(self, company_data):

        """
        Create single embedding for company

        :param company_data: scraped company text
        :type company_data: dict

        :return: embedding for single company, numpy array
        """

        # # reading company text
        # scrape_file_location = 'app/scrape_output/' + company_name + '.json'
        # with open(scrape_file_location) as json_file:
        #     data = json.load(json_file)
        company_text = ' '.join([ent['company_text'] for ent in company_data])

        # generate embedding
        num_words = 0
        company_embedding = np.zeros(shape=(1, self.embedding_size), dtype=np.float32)
        for word in company_text.split():
            try:
                company_embedding += np.array(self.embeddings[word], dtype=np.float32)
                num_words += 1
            except ValueError:
                continue

        # normalize array
        company_embedding_arr = company_embedding * (1/num_words)
        company_embedding_lst = company_embedding_arr.tolist()[0]

        # # remove scraped file
        # os.remove(scrape_file_location)

        return company_embedding_lst
