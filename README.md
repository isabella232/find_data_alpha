[![Build Status](https://travis-ci.org/datagovuk/find_data_alpha.svg?branch=master)](https://travis-ci.org/datagovuk/find_data_alpha)


# Find Data

This repository contains the alpha-stage data discovery component of data.gov.uk.

## Development

To just run on your machine with Sqlite3

``` bash
# Make and active a virtualenv for Python 3
git clone <REPO>
cd find_data_alpha
pip install -r requirements.txt
cd src
export DJANGO_SETTINGS_MODULE="find_data.settings.dev"
./manage.py migrate
./manage.py runserver
```

### Configuration

To successfully run the server, you will require a local_settings.py file that is stored in ```src/publish_data/settings/local_settings.py```.  The file should have the following contents:

```python


# CKAN specific settings.
CKAN_HOST = "URL of a CKAN Server"
CKAN_ADMIN = "An administrators API Key"
```

## Static assets (CSS, JS, images)

This application is built using [govuk_elements](https://github.com/alphagov/govuk_elements)
and [govuk_template](https://github.com/alphagov/govuk_template/).

Assets from those packages are already included in this repository.
Additionally the SCSS in `govuk_elements` is precompiled and the
resulting CSS is also included in the repository.

The reason assets are copied and pre-compiled here is to simplify
deployments.  That way, we're avoiding retrieving the `govuk_`
repositories, compiling the SASS (which would require installing
nodejs and npm), concatenating and minifying.

As a consequence, if changes are made to the javascript or SCSS files,
the developer will have to recompile locally. This will require
installing nodejs and npm, and running the following steps:

```
> npm install
> gulp styles
> gulp javascripts
```

If a new version of the `govuk` packages is needed, you will have to
copy and compile them again, and add the resulting files in this
repository.


## Acceptance testing

End-to-end tests can be found in the `tests` directory. They are run using
[nightwatch](http://nightwatchjs.com). To install nightwatch, use:
`npm install -g nightwatch`.

The variables at the top of the `Makefile` should be set to suit your
local environment.

Then you can just run `make test` to run the test suite.
