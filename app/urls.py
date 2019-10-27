import requests


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
