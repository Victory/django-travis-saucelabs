import argparse
import os

from subprocess import call

from pyvirtualdisplay import Display

parser = argparse.ArgumentParser(
    description='Run Tests locally or on Saucelabs')
parser.add_argument(
    '-l', '--local',
    help="Locally Run Tests", action="store_true")
args = parser.parse_args()
os.environ['RUN_TESTS_LOCAL'] = str(args.local)

errs = 0

err = call(["python", "mysite/manage.py", "test", "saucetests"])
errs += err

exit(err)
