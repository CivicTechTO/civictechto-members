# CivicTech Toronto Members

This app aspires to be a simple way to display data on CivicTechTO
members.

It will be backed by an ethercalc pad, with data periodically scraped
from services. There will be no access control, so anyone will be able
to connect accounts.

## Usage

```
mkvirtualenv civictechto-members --python=`which python3`
workon civictechto-members
make pip-install

# If you have heroku-cli installed:
make setup
# Edit .env to add MEETUP_API_KEY
# Export envvars in .env file
export $(cat .env | xargs)
make scrape

# You may alternatively use heroku-cli to run with envvars loaded
heroku local:run make scrape
```
