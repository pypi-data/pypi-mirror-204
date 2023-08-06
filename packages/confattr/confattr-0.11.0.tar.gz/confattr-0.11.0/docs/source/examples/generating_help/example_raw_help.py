#!../../../../venv/bin/python3

__package__ = 'exampleapp'

from confattr import ConfigFile
from argparse import RawTextHelpFormatter

from utils import run
run('example.py', main=False, nextto=__file__)

config_file = ConfigFile(appname=__package__, formatter_class=RawTextHelpFormatter)
print(config_file.get_help())
