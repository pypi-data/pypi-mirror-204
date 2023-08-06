#!../../../../venv/bin/python3

__package__ = 'exampleapp'

from confattr import ConfigFile, ConfigFileWriter
from argparse import RawTextHelpFormatter

from utils import run
run('example.py', main=False, nextto=__file__)

config_file = ConfigFile(appname=__package__, formatter_class=RawTextHelpFormatter)
config_file.save_to_writer(ConfigFileWriter(f=None, prefix='# '))
