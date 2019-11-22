#!/bin/bash

# setup virtualenv
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# copy data for app from s3
aws s3 cp s3://company2vec-data app/data --recursive --no-sign-request
