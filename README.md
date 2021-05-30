# [Django admin tests](http://thibaudcolas.github.io/django_admin_tests/) [![Build status](https://github.com/thibaudcolas/django_admin_tests/workflows/CI/badge.svg)](https://github.com/thibaudcolas/django_admin_tests/actions)

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

Requirements: `nvm`, Python 3.9.

```sh
# First, clone the repository and install the Node and Python dependencies.
git clone git@github.com:thibaudcolas/django_admin_tests.git
cd django_admin_tests
nvm use
npm install
virtualenv -p python3.9 .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
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

## Scope for audits

### Django admin

To be refined

- [Django admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/)
- [Django admindocs](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/admindocs/)
- [GIS](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/) Geo Admin

### Django output

- [Django forms](https://docs.djangoproject.com/en/3.0/ref/forms/)
  - Default widgets
  - as_p, as_ul, as_table
- Ex-contrib [comments](https://github.com/django/django-contrib-comments)
- Ex-contrib [formtools](https://github.com/jazzband/django-formtools)
- ([PDFs](https://docs.djangoproject.com/en/3.0/howto/outputting-pdf/)?)
- Examples from Django docs
  - [Pagination example template](https://docs.djangoproject.com/en/3.0/topics/pagination/#paginating-a-listview)
  - [WeekArchiveView example template](https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-date-based/#weekarchiveview)
- Error pages: 404, 500, 403, 400, CSRF
- Welcome page / Default URL conf
- Static’s directory listing
- (Flatpages?)

### High-profile third-party packages

- [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- [cookiecutter-django](https://github.com/pydanny/cookiecutter-django)
- [django-recaptcha](https://github.com/praekelt/django-recaptcha)
- [django-phonenumber-field](https://github.com/stefanfoulis/django-phonenumber-field)

### Docs

- Locally-built docs
- [docs.djangoproject.com](https://docs.djangoproject.com/)

## Improving the Pa11y test suite

The test suite is an unusual setup of Pa11y,

- [pa11y/scenarios.js](https://github.com/thibaudcolas/django_admin_tests/blob/main/pa11y/scenarios.js) contains all of the test cases, with more metadata than strictly needed. This is to facilitate the generation of custom reports based on this metadata.
  - The scenarios also inherit from their parents, grouping related scenarios for ease of understanding.
- [pa11y/test.js](https://github.com/thibaudcolas/django_admin_tests/blob/main/pa11y/test.js) runs the tests. The run starts by logging into the admin (only once), and each test with Pa11y is followed by a test with Lighthouse.
  - The test runs produce a single JSON file with all of the issues decorated with additional metadata from the scenarios, as well as Lighthouse results.
- [pa11y/report.js](https://github.com/thibaudcolas/django_admin_tests/blob/main/pa11y/report.js) runs on the generated report, separately from test runs. This makes it easy to iterate on the report format.
