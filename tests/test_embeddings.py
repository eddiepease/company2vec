from unittest import TestCase
from app.embeddings import Embeddings


class TestEmbeddings(TestCase):

    embed = Embeddings()

    def test_embedding_read(self):
        """
        Test that embedding being correctly read in
        """
        embed_bool = len(self.embed.embeddings) > 100000
        self.assertTrue(embed_bool)

    def test_embedding_type(self):
        """
        Test that list is returned from embedding
        """
        test_data = [{'company_url': 'http://www.test.com', 'company_text': 'first test'},
                     {'company_url': 'http://www.test.com', 'company_text': 'second test'}]
        test_embedding = self.embed.create_single_embedding(company_data=test_data)
        self.assertIsInstance(test_embedding, list)

    def test_embedding_calc(self):
        """
        Test that default embedding (just zeros) is not returned
        """
        test_data = [{'company_url': 'http://www.test.com', 'company_text': 'first test'},
                     {'company_url': 'http://www.test.com', 'company_text': 'second test'}]
        test_embedding = self.embed.create_single_embedding(company_data=test_data)
        default_embedding = [0] * self.embed.embedding_size
        self.assertNotEqual(sum(test_embedding), sum(default_embedding))
