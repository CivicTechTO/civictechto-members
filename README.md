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
export MEETUP_API_KEY=<my-key>
make scrape
```
