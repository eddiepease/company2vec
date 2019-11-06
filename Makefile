## The Makefile includes instructions on environment setup and lint tests
# Create and activate a virtual environment
# Install dependencies in requirements.txt
# Dockerfile should pass hadolint
# app.py should pass pylint
# (Optional) Build a simple integration test

# setup:
# 	# Create python virtualenv & source it
# 	# python3 -m venv ~/.venv
# 	source ~/.venv/bin/activate

install:
	# This should be run from inside a virtualenv
	# This builds the environment for the jenkins build
	pip install --upgrade pip
	pip install pylint

test:
	# Additional, optional, tests could go here
	python -m unittest discover tests/
	#python -m pytest -vv --cov=myrepolib tests/*.py
	#python -m pytest --nbval notebook.ipynb

lint:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# This is linter for Dockerfiles
	# hadolint Dockerfile
	# This is a linter for Python source code linter: https://www.pylint.org/
	# This should be run from inside a virtualenv
	pylint kleinapp.py --disable=E0401,C0103,W0613
	pylint app --disable=E0401,W0613,W0201,R0903

all: install lint test
