pip-install:
	pip install -r requirements.txt

setup:
	cp --no-clobber sample.env .env

scrape:
	python scrape_meetup.py
