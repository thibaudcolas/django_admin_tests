# [Django admin tests](http://thibaudcolas.github.io/django_admin_tests/) [![Build Status](https://travis-ci.com/thibaudcolas/django_admin_tests.svg?branch=master)](https://travis-ci.com/thibaudcolas/django_admin_tests)

> Automated accessibility CI tests for Django, based on Pa11y and Lighthouse, inspired by [wagtail-tooling](https://github.com/thibaudcolas/wagtail-tooling). [View latest report](http://thibaudcolas.github.io/django_admin_tests/)

- django-developers discussion: [Admin accessibility](https://groups.google.com/g/django-developers/c/FsBrNGTxvCA)
- Demo report: [Django admin tests report | Pa11y + Lighthouse](http://thibaudcolas.github.io/django_admin_tests/)

## Contents

- Demo site set up with `django-admin startproject django_admin_tests`, with Polls app from the Django tutorial
- Automated accessibility tests of the Django admin with Axe and HTML CodeSniffer via [Pa11y](https://pa11y.org/), for a range of predefined [scenarios](./pa11y/scenarios.js).
- Automated [Lighthouse](https://github.com/GoogleChrome/lighthouse) accessibility reports for all page-level scenarios.
- Bespoke [report generation](http://thibaudcolas.github.io/django_admin_tests/) based on the test results.

### Understanding the report

The report is based on Axe and HTML CodeSniffer, which can only find [30 to 40%](https://alphagov.github.io/accessibility-tool-audit/) of accessibility issues. It’s very useful to use multiple tools together to find as much as possible, but they do often report the same issues.

As of now the tests are always run for the whole page without any filtering of errors, which means that page-level errors are likely to be reported on multiple pages. This is especially true for pages relying on browser automation, which are likely to show all "page load" errors, as well as those triggered by additional interactions.

The Lighthouse reports are provided for reference – a score of 100% doesn’t mean a page is accessible. Lighthouse reports are based on Axe, and as such shouldn’t contain any issue not identified elsewhere.

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
