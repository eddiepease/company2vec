# Company2Vec

[![CircleCI](https://circleci.com/gh/eddiepease/company2vec.svg?style=shield)](https://circleci.com/gh/eddiepease/company2vec)

This repository generates a company vector embedding given a company name. Many machine 
learning use cases in business require a numerical representation of company. 
This repo is designed to aid this process by being easy to understand and generalizable to different companies/industries. 
 

## Getting started

To try out the package, follow the steps below:

* Clone this repository to local machine
* cd in folder root
* `chmod +x setup.sh` to make bash file executable
* `./setup.sh` to run executable - this installs a virtualenv and downloads relevant data
* Setup a Bing API on Azure and replace the subscription key in `config.py` (there is a free version)
* Change the company name in the 'main' function of `quick_start.py`, then run

## Features

Vector embeddings are often used for natural language processing in machine learning. They are used to represent a 
concept as a vector - this vector can then be used in a machine learning model. The embedding is created though a 
combination of an Azure API (to find the company website), scrapy (to do a shallow scrape of the company website) and
pre-trained GloVe embeddings.

To return a small number of company embeddings, use `quick_start.py`. To generate company embeddings at scale, build a
web app using `kleinapp.py` and `Dockerfile` and deploy this docker image to the cloud.


## Documentation

Documentation can be found [here](https://eddiepease.github.io/company2vec/).


## Contributing

Please do contribute to improve the repository. If you have an issue with the current code/documentation, do open an issue
[here](https://github.com/eddiepease/company2vec/issues)


## Licensing

This project is licensed under [MIT License](https://opensource.org/licenses/MIT).