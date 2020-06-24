# Django admin tests [![Build Status](https://travis-ci.com/thibaudcolas/django_admin_tests.svg?branch=master)](https://travis-ci.com/thibaudcolas/django_admin_tests)

> Automated CI tests for Django, inspired by [wagtail-tooling](https://github.com/thibaudcolas/wagtail-tooling).

- django-developers discussion: [Admin accessibility](https://groups.google.com/g/django-developers/c/FsBrNGTxvCA)
- Demo report: [Django admin tests report | Pa11y + Lighthouse](http://thibaudcolas.github.io/django_admin_tests/)

## Contents

- Demo site set up with `django-admin startproject django_admin_tests`, with Polls app from the Django tutorial
- Automated accessibility tests of the Django admin with Axe and HTML CodeSniffer via [Pa11y](https://pa11y.org/), for a range of predefined [scenarios](./pa11y/scenarios.js).
- Automated [Lighthouse](https://github.com/GoogleChrome/lighthouse) accessibility reports for all page-level scenarios.
- Bespoke report generation based on the test results.

## Local setup

Requirements: `nvm`, Python 3.6.

```sh
# First, clone the repository and install the Node and Python dependencies.
git clone git@github.com:thibaudcolas/django_admin_tests.git
cd django_admin_tests
nvm use
npm install
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
# Then, set up the demo site
./manage.py migrate
./manage.py loaddata fixtures.json
./manage.py runserver
# Prepare for running the test suite.
mkdir pa11y/lighthouse
mkdir pa11y/screenshots
```

## Running the test suite

To run the test suite:

```sh
npm run test
# And generate the report:
node pa11y/report.js
```

- `pa11y.json` contains the list of all reported issues.
- `report.html` is a high-level overview generated from the list of issues, and scenarios.
- `screenshots/` contains the screenshots for all scenarios (including sub-state scenarios).
- `ligthhouse/` contains the Lighthouse reports for all scenarios (including sub-state scenarios, but without any browser interaction taken into account).
