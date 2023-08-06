#!../../../../venv/bin/python3
__package__ = 'map'
from confattr import ConfigFile
from .example import Map

# ------- start -------
print(Map(ConfigFile(appname=__package__)).get_help())
