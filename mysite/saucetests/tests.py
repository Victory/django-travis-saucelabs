import os
import sys

from selenium import webdriver
from django.test import LiveServerTestCase

from sauceclient import SauceClient


def setupLocal():
    try:
        fh = open(
            os.path.dirname(os.path.realpath(__file__)) + '/sauce-key.txt')
        ln = fh.read().strip()
        bits =  ln.split(":")
        username = bits[0]
        key = bits[1]
        os.environ.setdefault('SAUCE_USERNAME', username)
        os.environ.setdefault('SAUCE_ACCESS_KEY', key)
    except:
        if not os.environ.get('SAUCE_USERNAME'):
            print "Warning Sauce Username Not Found"
        if not os.environ.get('SAUCE_ACCESS_KEY'):
            print "Warning Sauce Key Not Found"

USERNAME = os.environ.get('SAUCE_USERNAME')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

sauce = SauceClient(USERNAME, ACCESS_KEY)


browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": ""},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"}]


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = type(name, (base_class,), d)
    return decorator


#@on_platforms(browsers)
class HelloSauceTest(LiveServerTestCase):
    """
    Runs a test using travis-ci and saucelabs
    """

    def setUp(self):
        self.desired_capabilities = {}
        self.desired_capabilities['name'] = self.id()
        self.desired_capabilities['tunnel-identifier'] = \
            os.environ['TRAVIS_JOB_NUMBER']
        self.desired_capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
        self.desired_capabilities['tags'] = \
            [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']

        print self.desired_capabilities

        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(5)

    def tearDown(self):
        print("\nLink to your job: \n "
              "https://saucelabs.com/jobs/%s \n" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

    def test_sauce(self):
        self.driver.get(self.live_server_url + '/admin')
        assert "Log in" in self.driver.title
