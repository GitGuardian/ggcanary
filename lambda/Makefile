SHELL :=/bin/bash
.PHONY: \
	test \
	coverage \
	html-coverage \
	run-coverage \
	black \
	flake8 \
	lint


min_coverage := 45
html_coverage_dir := $(PWD)/.html-coverage

test:
	pipenv run python -m pytest --disable-pytest-warnings tests

coverage: run-coverage
	pipenv run coverage xml
	pipenv run coverage report --fail-under=$(min_coverage)

html-coverage: run-coverage
	pipenv run coverage html -d $(html_coverage_dir)

# Helper target for coverage and html-coverage
run-coverage:
	pipenv run coverage run --source lambda_py -m pytest --disable-pytest-warnings

black:
	pipenv run black .

flake8:
	pipenv run flake8

isort:
	pipenv run isort **/*.py

lint: flake8
	pipenv run black --check .
	pipenv run isort --check **/*.py
