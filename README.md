django-travis-saucelabs
=======================

An Instructive Repo for using Django, Travis and Saucelabs together.

We will assume you have `virtualenv` installed

     virtualenv pyenv
     source pyenv/bin/activate

Install `Django` and create an app

     pip install django
     django-admin.py startproject mysite

Make sure everything is working

    python mysite/manage.py runserver

Then navigate to `http://127.0.0.1:8000/`

    pip install PyVirtualDisplay
    pip install sauceclient
    pip install travis

This repo keeps a `requirements.txt` you can use `pip freeze` to see
the versions of modules you are running

So you could run

    pip install -r requirements.txt

Got to https://travis-ci.org/profile and make sure you have this repo
set to `on`

Get your key from saucelabs then run the following replacing `$KEY`
and repo name (i.e. `your-username/repo-name`). Your `$KEY` from sauce
labs will look something like `0aa48f52-7024-4934-8230-cd39919d2977`
(not a real key)

     travis encrypt "$KEY" -r 'Victory/realpython-tdd'

Which will give you something like

     secure: "reallyLongStringWithEncryptedStuff"

Now update your `.travis.yml`

     addons:
       sauce_connect:
         username: "Victory"
         access_key:
             secure: "reallyLongStringWithEncryptedStuff"

Run tests with the following and updated your `travis.yml`

    python mysite/manage.py test saucetests
