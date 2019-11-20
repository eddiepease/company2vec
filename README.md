# Company2Vec API

This repository creates an API on AWS which generates a company vector embedding given a company name. Many machine 
learning use cases in business require a company representation. This repo is designed to aid this process by being
easy to understand, generalizable to different companies/industries and scalable. 
 

## Getting started

To get the API up and running, follow the steps below:


* Run `git clone https://github.com/eddiepease/company2vec-api` on local machine
* Setup a Bing API on Azure and replace the subscription key in `urls.py`
* Setup an AWS account and replace AWS account details variables in `Jenkinsfile`
* Setup a jenkins server, installing eksctl, docker and all dependencies in `requirements.txt`. Also add AWS credentials

## Features

Vector embeddings are often used for natural language processing in machine learning. They are used to represent a 
concept as a vector - this vector can then be used in a machine learning model. The embedding is created though a 
combination of an Azure API (to find the company website), scrapy (to do a shallow scrape of the company website) and
pre-trained GloVe embeddings.

The API is deployed, via a Jenkins CI/CD pipeline, onto EKS in AWS.


## Documentation

Documentation is a work in progress and will be added in due course.


## Contributing

Please do contribute to improve the repository. If you have an issue with the current code/documentation, do open an issue
[here](https://github.com/eddiepease/company2vec-api/issues)


## Licensing

This project is licensed under [MIT License](https://opensource.org/licenses/MIT).

[issues]:https://github.com/jehna/readme-best-practices/issues/new