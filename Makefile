# Makefile for the project to run tests in github actions

# Install dependencies
setup:
	pip install --upgrade pip && \
	pip install -r requirements.txt

# Run tests
test:
	PYTHONPATH=. python -m pytest tests
