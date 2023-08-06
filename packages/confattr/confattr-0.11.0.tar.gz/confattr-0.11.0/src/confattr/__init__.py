#!./runmodule.sh

'''
Config Attributes

A python library to read and write config files
with a syntax inspired by vimrc and ranger config.
'''

__version__ = '0.11.0'

from .config import *
from .configfile import *

__all__ = [
	# -------- for normal usage -------
	# imported from config
	'Config',
	'DictConfig',
	'ConfigTrackingChanges',
	'MultiConfig',
	'MultiDictConfig',
	'ConfigId',
	# imported from configfile
	'ConfigFile',
	'NotificationLevel',
	'Message',
	'ParseException',
	# -------- for extending/customizing this package -------
	# imported from config
	'InstanceSpecificDictMultiConfig',
	# imported from configfile
	'DEFAULT_COMMAND',
	'SectionLevel',
	'FormattedWriter',
	'ConfigFileWriter',
	'HelpWriter',
	'SaveKwargs',
	'ParseLineKwargs',
	'ConfigFileCommand',
	'ConfigFileArgparseCommand',
	'ArgumentParser',
	'Set',
	'Include',
	'readable_quote',
	'UiCallback',
	'MultipleParseExceptions',
]
