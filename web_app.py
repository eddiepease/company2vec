from flask import Flask
from app.model import Company2Vec


app = Flask(__name__)

@app.route("/")
def home():

    """
    A welcome function used for testing
    :return: string
    """

    return "Welcome to the Company2Vec API!"


@app.route("/company/<company_name>", methods=['GET'])
def create_embedding(company_name):

    """
    Creates embedding after scrape
    :param company_name: string of company name
    :return:
    """

    c2v = Company2Vec(company_name)
    result = c2v.run()

    return result.jsonify()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
