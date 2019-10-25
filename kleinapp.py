from klein import Klein
from app.model import Company2Vec
# from app.pipelines import URLScraper


app = Klein()


@app.route("/")
def home(request):

    """
    A welcome function used for testing
    :return: string
    """

    return "Welcome to the Company2Vec API!"


@app.route("/company/<company_name>", methods=['GET'])
def create_embedding(request, company_name):

    """
    Creates embedding after scrape
    :param company_name: string of company name
    :return:
    """

    c2v = Company2Vec(company_name)
    result = c2v.run()

    return result.jsonify()


if __name__ == '__main__':
    app.run('localhost', port=5000)
