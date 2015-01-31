django-travis-saucelabs
=======================

[![Build Status](https://travis-ci.org/Victory/django-travis-saucelabs.svg?branch=master)](https://travis-ci.org/Victory/django-travis-saucelabs)

This badage links to all of my projects on saucelabs, not just this one.

[![Selenium Test Status](https://saucelabs.com/browser-matrix/Victory.svg)](https://saucelabs.com/u/Victory)


An demonstrative repo for using Django, Travis and Saucelabs together.

We will assume you have `virtualenv` installed, run the following:

     virtualenv pyenv
     source pyenv/bin/activate

Install `Django` and create an app

     pip install django
     django-admin.py startproject mysite

Make sure everything is working

    python mysite/manage.py runserver

Then navigate to `http://127.0.0.1:8000/admin`

    pip install PyVirtualDisplay
    pip install sauceclient
    pip install travis

This repo keeps a `requirements.txt`. You can use `pip freeze` to see
the versions of modules you are running. To get the correct versions:

    pip install -r requirements.txt

Got to https://travis-ci.org/profile and make sure you have this repo
set to `on`.

Get your key from saucelabs then run the following replacing `$KEY`
and repo name (i.e. `your-username/repo-name`). Your `$KEY` from sauce
labs will look something like `0aa48f52-7024-4934-8230-cd39919d2977`
(not a real key)

     travis encrypt "$KEY" -r 'Victory/django-travis-saucelabs'

Which will give you something like

     secure: "reallyLongStringWithEncryptedStuff"

Now update your `.travis.yml`

     addons:
       sauce_connect:
         username: "Victory"
         access_key:
             secure: "reallyLongStringWithEncryptedStuff"


Updated your `travis.yml`.

After, Run tests with the following:

    script:
      - python run-tests.py

Or run directly with

    python mysite/manage.py test saucetests

You may also run tests locally using

    python run-tests.py -l

The tests checks that the `/admin` page returns a `200 OK` status
code. The `/admin` page was choosen in this example because its
defined when creating a `django` project. Using the test not defined as it is not in `urls.py`.