# CivicTech Toronto Members

This app aspires to be a simple way to store/edit data on CivicTechTO
members, for the purposes of displaying on a splash page.

It is backed by [an ethercalc sheet][sheet], with public data scraped
from services daily at 1:30am ET. There is no access control, so anyone
will be able to edit the data store.

   [sheet]: https://ethercalc.org/civictechto-members
   
The script is run daily on [Heroku][] via their [scheduler][], under the `civictechto-members` app.

   [Heroku]: https://www.heroku.com/about
   [scheduler]: https://devcenter.heroku.com/articles/scheduler

## Feature Roadmap

- [x] Add meetup attendance counts
- [ ] Resurface data as pretty one-pager [(Ethercalc API
  docs)](https://github.com/audreyt/ethercalc/blob/master/API.md)
- [ ] Add longest meetup streak counts
- [ ] Add slack message counts
- [ ] Consider tallying some GitHub metric
- [ ] Consider "last seen" for meetup or Slack
- [ ] Make account id columns non-overwriting

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

## Inspirations

- [Coala: Get Involved page](https://coala.io/#/getinvolved)
  - [Source code: UI](https://github.com/coala/landing-frontend)
  - [Source code: API](https://gitlab.com/coala/landing)
