#!../../../../venv/bin/python3

__package__ = 'exampleapp'

from confattr import ConfigFile, ConfigFileWriter

from utils import run
run('no_multi_example.py', main=False, nextto=__file__)

config_file = ConfigFile(appname=__package__)
config_file.save_to_writer(ConfigFileWriter(f=None, prefix='# '))
