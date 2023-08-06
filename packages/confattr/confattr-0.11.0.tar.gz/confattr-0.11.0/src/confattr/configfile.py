#!./runmodule.sh

'''
This module defines the ConfigFile class
which can be used to load and save config files.
'''

import os
import shlex
import platform
import re
import enum
import argparse
import inspect
import io
import abc
import typing
from collections.abc import Iterable, Iterator, Sequence, Callable

import appdirs

from .config import Config, DictConfig, MultiConfig, ConfigId
from .utils import HelpFormatter, HelpFormatterWrapper, SortedEnum, readable_quote

if typing.TYPE_CHECKING:
	from typing_extensions import Unpack

	# T is already used in config.py and I cannot use the same name because both are imported with *
	T2 = typing.TypeVar('T2')


#: If the name or an alias of :class:`ConfigFileCommand` is this value that command is used by :meth:`ConfigFile.parse_split_line` if an undefined command is encountered.
DEFAULT_COMMAND = ''



# ---------- UI notifier ----------

@enum.unique
class NotificationLevel(SortedEnum):
	INFO = 'info'
	ERROR = 'error'

UiCallback: 'typing.TypeAlias' = 'Callable[[Message], None]'

class Message:

	'''
	A message which should be displayed to the user.
	This is passed to the callback of the user interface which has been registered with :meth:`ConfigFile.set_ui_callback`.

	If you want full control how to display messages to the user you can access the attributes directly.
	Otherwise you can simply convert this object to a str, e.g. with ``str(msg)``.
	I recommend to use different colors for different values of :attr:`notification_level`.
	'''

	#: The value of :attr:`file_name` while loading environment variables.
	ENVIRONMENT_VARIABLES = 'environment variables'


	__slots__ = ('notification_level', 'message', 'file_name', 'line_number', 'line')

	#: The importance of this message. I recommend to display messages of different importance levels in different colors.
	#: :class:`ConfigFile` does not output messages which are less important than the :paramref:`~ConfigFile.notification_level` setting which has been passed to it's constructor.
	notification_level: NotificationLevel

	#: The string or exception which should be displayed to the user
	message: 'str|BaseException'

	#: The name of the config file which has caused this message.
	#: If this equals :const:`ENVIRONMENT_VARIABLES` it is not a file but the message has occurred while reading the environment variables.
	#: This is None if :meth:`ConfigFile.parse_line` is called directly, e.g. when parsing the input from a command line.
	file_name: 'str|None'

	#: The number of the line in the config file. This is None if :attr:`file_name` is not a file name.
	line_number: 'int|None'

	#: The line where the message occurred. This is an empty str if there is no line, e.g. when loading environment variables.
	line: str

	_last_file_name: 'str|None' = None

	@classmethod
	def reset(cls) -> None:
		'''
		If you are using :meth:`format_file_name_msg_line` or :meth:`__str__`
		you must call this method when the widget showing the error messages is cleared.
		'''
		cls._last_file_name = None

	def __init__(self, notification_level: NotificationLevel, message: 'str|BaseException', file_name: 'str|None' = None, line_number: 'int|None' = None, line: 'str' = '') -> None:
		self.notification_level = notification_level
		self.message = message
		self.file_name = file_name
		self.line_number = line_number
		self.line = line

	@property
	def lvl(self) -> NotificationLevel:
		'''
		An abbreviation for :attr:`notification_level`
		'''
		return self.notification_level

	def format_msg_line(self) -> str:
		'''
		The return value includes the attributes :attr:`message`, :attr:`line_number` and :attr:`line` if they are set.
		'''
		msg = str(self.message)
		if self.line:
			if self.line_number is not None:
				lnref = 'line %s' % self.line_number
			else:
				lnref = 'line'
			return f'{msg} in {lnref} {self.line!r}'

		return msg

	def format_file_name(self) -> str:
		'''
		:return: A header including the :attr:`file_name` if the :attr:`file_name` is different from the last time this function has been called or an empty string otherwise
		'''
		file_name = '' if self.file_name is None else self.file_name
		if file_name == self._last_file_name:
			return ''

		if file_name:
			out = f'While loading {file_name}:\n'
		else:
			out = ''

		if self._last_file_name is not None:
			out = '\n' + out

		type(self)._last_file_name = file_name

		return out


	def format_file_name_msg_line(self) -> str:
		'''
		:return: The concatenation of the return values of :meth:`format_file_name` and :meth:`format_msg_line`
		'''
		return self.format_file_name() + self.format_msg_line()


	def __str__(self) -> str:
		'''
		:return: The return value of :meth:`format_file_name_msg_line`
		'''
		return self.format_file_name_msg_line()

	def __repr__(self) -> str:
		return f'{type(self).__name__}(%s)' % ', '.join(f'{a}={self._format_attribute(getattr(self, a))}' for a in self.__slots__)

	@staticmethod
	def _format_attribute(obj: object) -> str:
		if isinstance(obj, enum.Enum):
			return obj.name
		return repr(obj)


class UiNotifier:

	'''
	Most likely you will want to load the config file before creating the UI (user interface).
	But if there are errors in the config file the user will want to know about them.
	This class takes the messages from :class:`ConfigFile` and stores them until the UI is ready.
	When you call :meth:`set_ui_callback` the stored messages will be forwarded and cleared.

	This object can also filter the messages.
	:class:`ConfigFile` calls :meth:`show_info` every time a setting is changed.
	If you load an entire config file this can be many messages and the user probably does not want to see them all.
	Therefore this object drops all messages of :const:`NotificationLevel.INFO` by default.
	Pass :obj:`notification_level` to the constructor if you don't want that.
	'''

	# ------- public methods -------

	def __init__(self, config_file: 'ConfigFile', notification_level: 'Config[NotificationLevel]|NotificationLevel' = NotificationLevel.ERROR) -> None:
		self._messages: 'list[Message]' = []
		self._callback: 'UiCallback|None' = None
		self._notification_level = notification_level
		self._config_file = config_file

	def set_ui_callback(self, callback: UiCallback) -> None:
		'''
		Call :paramref:`callback` for all messages which have been saved by :meth:`show` and clear all saved messages afterwards.
		Save :paramref:`callback` for :meth:`show` to call.
		'''
		self._callback = callback

		for msg in self._messages:
			callback(msg)
		self._messages.clear()


	@property
	def notification_level(self) -> NotificationLevel:
		'''
		Ignore messages that are less important than this level.
		'''
		if isinstance(self._notification_level, Config):
			return self._notification_level.value
		else:
			return self._notification_level

	@notification_level.setter
	def notification_level(self, val: NotificationLevel) -> None:
		if isinstance(self._notification_level, Config):
			self._notification_level.value = val
		else:
			self._notification_level = val


	# ------- called by ConfigFile -------

	def show_info(self, msg: str, *, ignore_filter: bool = False) -> None:
		'''
		Call :meth:`show` with :obj:`NotificationLevel.INFO`.
		'''
		self.show(NotificationLevel.INFO, msg, ignore_filter=ignore_filter)

	def show_error(self, msg: 'str|BaseException', *, ignore_filter: bool = False) -> None:
		'''
		Call :meth:`show` with :obj:`NotificationLevel.ERROR`.
		'''
		self.show(NotificationLevel.ERROR, msg, ignore_filter=ignore_filter)


	# ------- internal methods -------

	def show(self, notification_level: NotificationLevel, msg: 'str|BaseException', *, ignore_filter: bool = False) -> None:
		'''
		If a callback for the user interface has been registered with :meth:`set_ui_callback` call that callback.
		Otherwise save the message so that :meth:`set_ui_callback` can forward the message when :meth:`set_ui_callback` is called.

		:param notification_level: The importance of the message
		:param msg: The message to be displayed on the user interface
		:param ignore_filter: If true: Show the message even if :paramref:`notification_level` is smaller then the :paramref:`UiNotifier.notification_level`.
		'''
		if notification_level < self.notification_level and not ignore_filter:
			return

		message = Message(
			notification_level = notification_level,
			message = msg,
			file_name = self._config_file.context_file_name,
			line_number = self._config_file.context_line_number,
			line = self._config_file.context_line,
		)

		if self._callback:
			self._callback(message)
		else:
			self._messages.append(message)


# ---------- format help ----------

class SectionLevel(SortedEnum):

	#: Is used to separate different commands in :meth:`ConfigFile.write_help` and :meth:`ConfigFileCommand.save`
	SECTION = 'section'

	#: Is used for subsections in :meth:`ConfigFileCommand.save` such as the "data types" section in the help of the set command
	SUB_SECTION = 'sub-section'


class FormattedWriter(abc.ABC):

	@abc.abstractmethod
	def write_line(self, line: str) -> None:
		'''
		Write a single line of documentation.
		:paramref:`line` may *not* contain a newline.
		If :paramref:`line` is empty it does not need to be prefixed with a comment character.
		Empty lines should be dropped if no other lines have been written before.
		'''
		pass

	def write_lines(self, text: str) -> None:
		'''
		Write one or more lines of documentation.
		'''
		for ln in text.splitlines():
			self.write_line(ln)

	@abc.abstractmethod
	def write_heading(self, lvl: SectionLevel, heading: str) -> None:
		'''
		Write a heading.

		This object should *not* add an indentation depending on the section
		because if the indentation is increased the line width should be decreased
		in order to keep the line wrapping consistent.
		Wrapping lines is handled by :class:`confattr.utils.HelpFormatter`,
		i.e. before the text is passed to this object.
		It would be possible to use :class:`argparse.RawTextHelpFormatter` instead
		and handle line wrapping on a higher level but that would require
		to understand the help generated by argparse
		in order to know how far to indent a broken line.
		One of the trickiest parts would probably be to get the indentation of the usage right.
		Keep in mind that the term "usage" can differ depending on the language settings of the user.

		:param lvl: How to format the heading
		:param heading: The heading
		'''
		pass

	@abc.abstractmethod
	def write_command(self, cmd: str) -> None:
		'''
		Write a config file command.
		'''
		pass


class TextIOWriter(FormattedWriter):

	def __init__(self, f: 'typing.TextIO|None') -> None:
		self.f = f
		self.ignore_empty_lines = True

	def write_line_raw(self, line: str) -> None:
		if self.ignore_empty_lines and not line:
			return

		print(line, file=self.f)
		self.ignore_empty_lines = False


class ConfigFileWriter(TextIOWriter):

	def __init__(self, f: 'typing.TextIO|None', prefix: str) -> None:
		super().__init__(f)
		self.prefix = prefix

	def write_command(self, cmd: str) -> None:
		self.write_line_raw(cmd)

	def write_line(self, line: str) -> None:
		if line:
			line = self.prefix + line

		self.write_line_raw(line)

	def write_heading(self, lvl: SectionLevel, heading: str) -> None:
		if lvl is SectionLevel.SECTION:
			self.write_line('')
			self.write_line('')
			self.write_line('=' * len(heading))
			self.write_line(heading)
			self.write_line('=' * len(heading))
		else:
			self.write_line('')
			self.write_line(heading)
			self.write_line('-' * len(heading))

class HelpWriter(TextIOWriter):

	def write_line(self, line: str) -> None:
		self.write_line_raw(line)

	def write_heading(self, lvl: SectionLevel, heading: str) -> None:
		self.write_line('')
		if lvl is SectionLevel.SECTION:
			self.write_line(heading)
			self.write_line('=' * len(heading))
		else:
			self.write_line(heading)
			self.write_line('-' * len(heading))

	def write_command(self, cmd: str) -> None:
		pass  # pragma: no cover


# ---------- internal exceptions ----------

class ParseException(Exception):

	'''
	This is raised by :class:`ConfigFileCommand` implementations and functions passed to :paramref:`~ConfigFile.check_config_id` in order to communicate an error in the config file like invalid syntax or an invalid value.
	Is caught in :class:`ConfigFile`.
	'''

class MultipleParseExceptions(Exception):

	'''
	This is raised by :class:`ConfigFileCommand` implementations in order to communicate that multiple errors have occured on the same line.
	Is caught in :class:`ConfigFile`.
	'''

	def __init__(self, exceptions: 'Sequence[ParseException]') -> None:
		super().__init__()
		self.exceptions = exceptions

	def __iter__(self) -> 'Iterator[ParseException]':
		return iter(self.exceptions)


# ---------- data types for **kw args ----------

if hasattr(typing, 'TypedDict'):  # python >= 3.8  # pragma: no cover. This is tested but in a different environment which is not known to coverage.
	class SaveKwargs(typing.TypedDict, total=False):
		config_instances: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]]'
		ignore: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None'
		no_multi: bool
		comments: bool


# ---------- ConfigFile class ----------

class ArgPos:
	'''
	This is an internal class, the return type of :meth:`ConfigFile.find_arg`
	'''

	#: The index of the argument in :paramref:`~ConfigFile.find_arg.ln_split` where the cursor is located and which shall be completed. Please note that this can be one bigger than :paramref:`~ConfigFile.find_arg.ln_split` is long if the line ends on a space and the cursor is behind that space. In that case :attr:`in_between` is true.
	argument_pos: int

	#: If true: The cursor is between two arguments, before the first argument or after the last argument. :attr:`argument_pos` refers to the next argument, :attr:`argument_pos-1 <argument_pos>` to the previous argument. :attr:`i0` is the start of the next argument, :attr:`i1` is the end of the previous argument.
	in_between: bool

	#: The index in :paramref:`~ConfigFile.find_arg.line` where the argument having the cursor starts (inclusive) or the start of the next argument if :attr:`in_between` is true
	i0: int

	#: The index in :paramref:`~ConfigFile.find_arg.line` where the current word ends (exclusive) or the end of the previous argument if :attr:`in_between` is true
	i1: int


class ConfigFile:

	'''
	Read or write a config file.
	'''

	COMMENT = '#'
	COMMENT_PREFIXES = ('"', '#')
	ENTER_GROUP_PREFIX = '['
	ENTER_GROUP_SUFFIX = ']'

	#: The :class:`Config` instances to load or save
	config_instances: 'dict[str, Config[typing.Any]]'

	#: While loading a config file: The group that is currently being parsed, i.e. an identifier for which object(s) the values shall be set. This is set in :meth:`enter_group` and reset in :meth:`load_file`.
	config_id: 'ConfigId|None'

	#: Override the config file which is returned by :meth:`iter_config_paths`.
	#: You should set either this attribute or :attr:`config_directory` in your tests with :meth:`monkeypatch.setattr <pytest.MonkeyPatch.setattr>`.
	#: If the environment variable ``APPNAME_CONFIG_PATH`` is set this attribute is set to it's value in the constructor (where ``APPNAME`` is the value which is passed as :paramref:`appname <ConfigFile.appname>` to the constructor but in all upper case letters and hyphens and spaces replaced by underscores.)
	config_path: 'str|None' = None

	#: Override the config directory which is returned by :meth:`iter_user_site_config_paths`.
	#: You should set either this attribute or :attr:`config_path` in your tests with :meth:`monkeypatch.setattr <pytest.MonkeyPatch.setattr>`.
	#: If the environment variable ``APPNAME_CONFIG_DIRECTORY`` is set this attribute is set to it's value in the constructor (where ``APPNAME`` is the value which is passed as :paramref:`appname <ConfigFile.appname>` to the constructor but in all upper case letters and hyphens and spaces replaced by underscores.)
	config_directory: 'str|None' = None

	#: The name of the config file used by :meth:`iter_config_paths`.
	#: Can be changed with the environment variable ``APPNAME_CONFIG_NAME`` (where ``APPNAME`` is the value which is passed as :paramref:`appname <ConfigFile.appname>` to the constructor but in all upper case letters and hyphens and spaces replaced by underscores.).
	config_name = 'config'

	#: Contains the names of the environment variables for :attr:`config_path`, :attr:`config_directory` and :attr:`config_name`—in capital letters and prefixed with :attr:`envprefix`.
	env_variables: 'list[str]'

	#: A prefix that is prepended to the name of environment variables in :meth:`get_env_name`.
	#: It is set in the constructor by first setting it to an empty str and then passing the value of :paramref:`appname <ConfigFile.appname>` to :meth:`get_env_name` and appending an underscore.
	envprefix: str

	#: The name of the file which is currently loaded. If this equals :attr:`Message.ENVIRONMENT_VARIABLES` it is no file name but an indicator that environment variables are loaded. This is :obj:`None` if :meth:`parse_line` is called directly (e.g. the input from a command line is parsed).
	context_file_name: 'str|None' = None
	#: The number of the line which is currently parsed. This is :obj:`None` if :attr:`context_file_name` is not a file name.
	context_line_number: 'int|None' = None
	#: The line which is currently parsed.
	context_line: str = ''

	#: If true: ``[config-id]`` syntax is allowed in config file, config ids are included in help, config id related options are available for include.
	#: If false: It is not possible to set different values for different objects (but default values for :class:`MultiConfig` instances can be set)
	enable_config_ids: bool


	def __init__(self, *,
		notification_level: 'Config[NotificationLevel]' = NotificationLevel.ERROR,  # type: ignore [assignment]  # yes, passing a NotificationLevel directly is possible but I don't want users to do that in order to give the users of their applications the freedom to set this the way they need it
		appname: str,
		authorname: 'str|None' = None,
		config_instances: 'dict[str, Config[typing.Any]]' = Config.instances,
		commands: 'Sequence[type[ConfigFileCommand]]|None' = None,
		formatter_class: 'type[argparse.HelpFormatter]' = HelpFormatter,
		check_config_id: 'Callable[[ConfigId], None]|None' = None,
		enable_config_ids: 'bool|None' = None,
	) -> None:
		'''
		:param notification_level: A :class:`Config` which the users of your application can set to choose whether they want to see information which might be interesting for debugging a config file. A :class:`Message` with a priority lower than this value is *not* passed to the callback registered with :meth:`set_ui_callback`.
		:param appname: The name of the application, required for generating the path of the config file if you use :meth:`load` or :meth:`save` and as prefix of environment variable names
		:param authorname: The name of the developer of the application, on MS Windows useful for generating the path of the config file if you use :meth:`load` or :meth:`save`
		:param config_instances: The Config instances to load or save, defaults to :attr:`Config.instances`
		:param commands: The commands (as subclasses of :class:`ConfigFileCommand` or :class:`ConfigFileArgparseCommand`) allowed in this config file, if this is :const:`None`: use the return value of :meth:`ConfigFileCommand.get_command_types`
		:param formatter_class: Is used to clean up doc strings and wrap lines in the help
		:param check_config_id: Is called every time a configuration group is opened (except for :attr:`Config.default_config_id`—that is always allowed). The callback should raise a :class:`ParseException` if the config id is invalid.
		:param enable_config_ids: see :attr:`enable_config_ids`. If None: Choose True or False automatically based on :paramref:`check_config_id` and the existence of :class:`MultiConfig`/:class:`MultiDictConfig`
		'''
		self.appname = appname
		self.authorname = authorname
		self.ui_notifier = UiNotifier(self, notification_level)
		self.config_instances = config_instances
		self.config_id: 'ConfigId|None' = None
		self.formatter_class = formatter_class
		self.env_variables: 'list[str]' = []
		self.check_config_id = check_config_id

		if enable_config_ids is None:
			enable_config_ids = self.check_config_id is not None or any(isinstance(cfg, MultiConfig) for cfg in self.config_instances.values())
		self.enable_config_ids = enable_config_ids

		if not appname:
			# Avoid an exception if appname is None.
			# Although mypy does not allow passing None directly
			# passing __package__ is (and should be) allowed.
			# And __package__ is None if the module is not part of a package.
			appname = ''
		self.envprefix = ''
		self.envprefix = self.get_env_name(appname + '_')
		envname = self.envprefix + 'CONFIG_PATH'
		self.env_variables.append(envname)
		if envname in os.environ:
			self.config_path = os.environ[envname]
		envname = self.envprefix + 'CONFIG_DIRECTORY'
		self.env_variables.append(envname)
		if envname in os.environ:
			self.config_directory = os.environ[envname]
		envname = self.envprefix + 'CONFIG_NAME'
		self.env_variables.append(envname)
		if envname in os.environ:
			self.config_name = os.environ[envname]

		if commands is None:
			commands = ConfigFileCommand.get_command_types()
		self.command_dict = {}
		self.commands = []
		for cmd_type in commands:
			cmd = cmd_type(self)
			self.commands.append(cmd)
			for name in cmd.get_names():
				self.command_dict[name] = cmd


	def set_ui_callback(self, callback: UiCallback) -> None:
		'''
		Register a callback to a user interface in order to show messages to the user like syntax errors or invalid values in the config file.

		Messages which occur before this method is called are stored and forwarded as soon as the callback is registered.

		:param ui_callback: A function to display messages to the user
		'''
		self.ui_notifier.set_ui_callback(callback)

	def get_app_dirs(self) -> 'appdirs.AppDirs':
		'''
		Create or get a cached `AppDirs <https://github.com/ActiveState/appdirs/blob/master/README.rst#appdirs-for-convenience>`_ instance with multipath support enabled.

		When creating a new instance, `platformdirs <https://pypi.org/project/platformdirs/>`_, `xdgappdirs <https://pypi.org/project/xdgappdirs/>`_ and `appdirs <https://pypi.org/project/appdirs/>`_ are tried, in that order.
		The first one installed is used.
		appdirs, the original of the two forks and the only one of the three with type stubs, is specified in pyproject.toml as a hard dependency so that at least one of the three should always be available.
		I am not very familiar with the differences but if a user finds that appdirs does not work for them they can choose to use an alternative with ``pipx inject appname xdgappdirs|platformdirs``.

		These libraries should respect the environment variables ``XDG_CONFIG_HOME`` and ``XDG_CONFIG_DIRS``.
		'''
		if not hasattr(self, '_appdirs'):
			try:
				import platformdirs  # type: ignore [import]  # this library is not typed and not necessarily installed, I am relying on it's compatibility with appdirs
				AppDirs = typing.cast('type[appdirs.AppDirs]', platformdirs.PlatformDirs)  # pragma: no cover  # This is tested but in a different tox environment
			except ImportError:
				try:
					import xdgappdirs  # type: ignore [import]  # this library is not typed and not necessarily installed, I am relying on it's compatibility with appdirs
					AppDirs = typing.cast('type[appdirs.AppDirs]', xdgappdirs.AppDirs)  # pragma: no cover  # This is tested but in a different tox environment
				except ImportError:
					AppDirs = appdirs.AppDirs

			self._appdirs = AppDirs(self.appname, self.authorname, multipath=True)

		return self._appdirs

	# ------- load -------

	def iter_user_site_config_paths(self) -> 'Iterator[str]':
		'''
		Iterate over all directories which are searched for config files, user specific first.

		The directories are based on :meth:`get_app_dirs`
		unless :attr:`config_directory` has been set.
		If :attr:`config_directory` has been set
		it's value is yielded and nothing else.
		'''
		if self.config_directory:
			yield self.config_directory
			return

		appdirs = self.get_app_dirs()
		yield from appdirs.user_config_dir.split(os.path.pathsep)
		yield from appdirs.site_config_dir.split(os.path.pathsep)

	def iter_config_paths(self) -> 'Iterator[str]':
		'''
		Iterate over all paths which are checked for config files, user specific first.

		Use this method if you want to tell the user where the application is looking for it's config file.
		The first existing file yielded by this method is used by :meth:`load`.

		The paths are generated by joining the directories yielded by :meth:`iter_user_site_config_paths` with
		:attr:`ConfigFile.config_name`.

		If :attr:`config_path` has been set this method yields that path instead and no other paths.
		'''
		if self.config_path:
			yield self.config_path
			return

		for path in self.iter_user_site_config_paths():
			yield os.path.join(path, self.config_name)

	def load(self, *, env: bool = True) -> None:
		'''
		Load the first existing config file returned by :meth:`iter_config_paths`.

		If there are several config files a user specific config file is preferred.
		If a user wants a system wide config file to be loaded, too, they can explicitly include it in their config file.
		:param env: If true: call :meth:`load_env` after loading the config file.
		'''
		for fn in self.iter_config_paths():
			if os.path.isfile(fn):
				self.load_file(fn)
				break

		if env:
			self.load_env()

	def load_env(self) -> None:
		'''
		Load settings from environment variables.
		The name of the environment variable belonging to a setting is generated with :meth:`get_env_name`.

		Environment variables not matching a setting or having an invalid value are reported with :meth:`self.ui_notifier.show_error() <UiNotifier.show_error>`.

		:raises ValueError: if two settings have the same environment variable name (see :meth:`get_env_name`) or the environment variable name for a setting collides with one of the standard environment variables listed in :attr:`env_variables`
		'''
		old_file_name = self.context_file_name
		self.context_file_name = Message.ENVIRONMENT_VARIABLES

		config_instances: 'dict[str, Config[object]]' = {}
		for key, instance in self.config_instances.items():
			name = self.get_env_name(key)
			if name in self.env_variables:
				raise ValueError(f'setting {instance.key!r} conflicts with environment variable {name!r}')
			elif name in config_instances:
				raise ValueError(f'settings {instance.key!r} and {config_instances[name].key!r} result in the same environment variable {name!r}')
			else:
				config_instances[name] = instance

		for name, value in os.environ.items():
			if not name.startswith(self.envprefix):
				continue
			if name in self.env_variables:
				continue

			if name in config_instances:
				instance = config_instances[name]
				try:
					instance.set_value(config_id=None, value=instance.parse_value(value))
					self.ui_notifier.show_info(f'set {instance.key} to {instance.format_value(config_id=None)}')
				except ValueError as e:
					self.ui_notifier.show_error(f"{e} while trying to parse environment variable {name}='{value}'")
			else:
				self.ui_notifier.show_error(f"unknown environment variable {name}='{value}'")

		self.context_file_name = old_file_name


	def get_env_name(self, key: str) -> str:
		'''
		Convert the key of a setting to the name of the corresponding environment variable.

		:return: An all upper case version of :paramref:`key` with all hyphens, dots and spaces replaced by underscores and :attr:`envprefix` prepended to the result.
		'''
		out = key
		out = out.upper()
		for c in ' .-':
			out = out.replace(c, '_')
		out = self.envprefix + out
		return out

	def load_file(self, fn: str) -> None:
		'''
		Load a config file and change the :class:`Config` objects accordingly.

		Use :meth:`set_ui_callback` to get error messages which appeared while loading the config file.
		You can call :meth:`set_ui_callback` after this method without loosing any messages.

		:param fn: The file name of the config file (absolute or relative path)
		'''
		self.config_id = None
		self.load_without_resetting_config_id(fn)

	def load_without_resetting_config_id(self, fn: str) -> None:
		old_file_name = self.context_file_name
		self.context_file_name = fn

		with open(fn, 'rt') as f:
			for lnno, ln in enumerate(f, 1):
				self.context_line_number = lnno
				self.parse_line(line=ln)
				self.context_line_number = None

		self.context_file_name = old_file_name

	def parse_line(self, line: str) -> bool:
		'''
		:param line: The line to be parsed
		:return: True if line is valid, False if an error has occurred

		:meth:`parse_error` is called if something goes wrong (i.e. if the return value is False), e.g. invalid key or invalid value.
		'''
		ln = line.strip()
		if not ln:
			return True
		if self.is_comment(ln):
			return True
		if self.enable_config_ids and self.enter_group(ln):
			return True

		self.context_line = ln

		try:
			ln_split = self.split_line(ln)
		except Exception as e:
			self.parse_error(str(e))
			out = False
		else:
			out = self.parse_split_line(ln_split)

		self.context_line = ''
		return out

	def split_line(self, line: str) -> 'list[str]':
		return shlex.split(line, comments=True)

	def split_line_ignore_errors(self, line: str) -> 'list[str]':
		out = []
		lex = shlex.shlex(line, posix=True)
		lex.whitespace_split = True
		while True:
			try:
				t = lex.get_token()
			except:
				out.append(lex.token)
				return out
			if t is None:
				return out  # type: ignore [unreachable]  # yes, with posix=True lex.get_token returns None at the end
			out.append(t)

	def is_comment(self, line: str) -> bool:
		'''
		Check if :paramref:`line` is a comment.

		:param line: The current line
		:return: :const:`True` if :paramref:`line` is a comment
		'''
		for c in self.COMMENT_PREFIXES:
			if line.startswith(c):
				return True
		return False

	def enter_group(self, line: str) -> bool:
		'''
		Check if :paramref:`line` starts a new group and set :attr:`config_id` if it does.
		Call :meth:`parse_error` if :attr:`check_config_id` raises a :class:`ParseException`.

		:param line: The current line
		:return: :const:`True` if :paramref:`line` starts a new group
		'''
		if line.startswith(self.ENTER_GROUP_PREFIX) and line.endswith(self.ENTER_GROUP_SUFFIX):
			config_id = typing.cast(ConfigId, line[len(self.ENTER_GROUP_PREFIX):-len(self.ENTER_GROUP_SUFFIX)])
			if self.check_config_id and config_id != Config.default_config_id:
				try:
					self.check_config_id(config_id)
				except ParseException as e:
					self.parse_error(str(e))
			self.config_id = config_id
			if self.config_id not in MultiConfig.config_ids:
				MultiConfig.config_ids.append(self.config_id)
			return True
		return False

	def parse_split_line(self, ln_split: 'Sequence[str]') -> bool:
		'''
		Call the corresponding command in :attr:`command_dict`.
		If any :class:`ParseException` or :class:`MultipleParseExceptions` is raised catch it and call :meth:`parse_error`.

		:return: False if a :class:`ParseException` or :class:`MultipleParseExceptions` has been caught, True if no exception has been caught
		'''
		cmd = self.get_command(ln_split)
		try:
			cmd.run(ln_split)
		except ParseException as e:
			self.parse_error(str(e))
			return False
		except MultipleParseExceptions as exceptions:
			for exc in exceptions:
				self.parse_error(str(exc))
			return False

		return True

	def get_command(self, ln_split: 'Sequence[str]') -> 'ConfigFileCommand':
		cmd_name = ln_split[0]
		if cmd_name in self.command_dict:
			cmd = self.command_dict[cmd_name]
		elif DEFAULT_COMMAND in self.command_dict:
			cmd = self.command_dict[DEFAULT_COMMAND]
		else:
			cmd = UnknownCommand(self)
		return cmd


	# ------- save -------

	def get_save_path(self) -> str:
		'''
		:return: The first existing and writable file returned by :meth:`iter_config_paths` or the first path if none of the files are existing and writable.
		'''
		paths = tuple(self.iter_config_paths())
		for fn in paths:
			if os.path.isfile(fn) and os.access(fn, os.W_OK):
				return fn

		return paths[0]

	def save(self,
		**kw: 'Unpack[SaveKwargs]',
	) -> str:
		'''
		Save the current values of all settings to the file returned by :meth:`get_save_path`.
		Directories are created as necessary.

		:param config_instances: Do not save all settings but only those given. If this is a :class:`list` they are written in the given order. If this is a :class:`set` they are sorted by their keys.
		:param ignore: Do not write these settings to the file.
		:param no_multi: Do not write several sections. For :class:`MultiConfig` instances write the default values only.
		:param comments: Write comments with allowed values and help.
		:return: The path to the file which has been written
		'''
		fn = self.get_save_path()
		# "If, when attempting to write a file, the destination directory is non-existent an attempt should be made to create it with permission 0700.
		#  If the destination directory exists already the permissions should not be changed."
		# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
		os.makedirs(os.path.dirname(fn), exist_ok=True, mode=0o0700)
		self.save_file(fn, **kw)
		return fn

	def save_file(self,
		fn: str,
		**kw: 'Unpack[SaveKwargs]'
	) -> None:
		'''
		Save the current values of all settings to a specific file.

		:param fn: The name of the file to write to. If this is not an absolute path it is relative to the current working directory.
		:raises FileNotFoundError: if the directory does not exist

		For an explanation of the other parameters see :meth:`save`.
		'''
		with open(fn, 'wt') as f:
			self.save_to_open_file(f, **kw)


	def save_to_open_file(self,
		f: typing.TextIO,
		**kw: 'Unpack[SaveKwargs]',
	) -> None:
		'''
		Save the current values of all settings to a file-like object
		by creating a :class:`ConfigFileWriter` object and calling :meth:`save_to_writer`.

		:param f: The file to write to

		For an explanation of the other parameters see :meth:`save`.
		'''
		writer = ConfigFileWriter(f, prefix=self.COMMENT + ' ')
		self.save_to_writer(writer, **kw)

	def save_to_writer(self, writer: FormattedWriter, **kw: 'Unpack[SaveKwargs]') -> None:
		'''
		Save the current values of all settings.

		Ensure that all keyword arguments are passed with :meth:`set_save_default_arguments`.
		Iterate over all :class:`ConfigFileCommand` objects in :attr:`self.commands` and do for each of them:

		- set :attr:`~ConfigFileCommand.should_write_heading` to :obj:`True` if :python:`getattr(cmd.save, 'implemented', True)` is true for two or more of those commands or to :obj:`False` otherwise
		- call :meth:`~ConfigFileCommand.save`
		'''
		self.set_save_default_arguments(kw)
		commands = self.commands
		write_headings = len(tuple(cmd for cmd in commands if getattr(cmd.save, 'implemented', True))) >= 2
		for cmd in commands:
			cmd.should_write_heading = write_headings
			cmd.save(writer, **kw)

	def set_save_default_arguments(self, kw: 'SaveKwargs') -> None:
		'''
		Ensure that all arguments are given in :paramref:`kw`.
		'''
		kw.setdefault('config_instances', set(self.config_instances.values()))
		kw.setdefault('ignore', None)
		kw.setdefault('no_multi', not self.enable_config_ids)
		kw.setdefault('comments', True)


	def quote(self, val: str) -> str:
		'''
		Quote a value if necessary so that it will be interpreted as one argument.

		The default implementation calls :func:`readable_quote`.
		'''
		return readable_quote(val)

	def write_config_id(self, writer: FormattedWriter, config_id: ConfigId) -> None:
		'''
		Start a new group in the config file so that all following commands refer to the given :paramref:`config_id`.
		'''
		writer.write_command(self.ENTER_GROUP_PREFIX + config_id + self.ENTER_GROUP_SUFFIX)

	def get_help_config_id(self) -> str:
		'''
		:return: A help how to use :class:`MultiConfig`. The return value still needs to be cleaned with :meth:`inspect.cleandoc`.
		'''
		return f'''
			You can specify the object that a value shall refer to by inserting the line `{self.ENTER_GROUP_PREFIX}config-id{self.ENTER_GROUP_SUFFIX}` above.
			`config-id` must be replaced by the corresponding identifier for the object.
		'''


	# ------- help -------

	def write_help(self, writer: FormattedWriter) -> None:
		import platform
		formatter = self.create_formatter()
		writer.write_lines('The first existing file of the following paths is loaded:')
		for path in self.iter_config_paths():
			writer.write_line('- %s' % path)

		writer.write_line('')
		writer.write_line('This can be influenced with the following environment variables:')
		if platform.system() == 'Linux':  # pragma: no branch
			writer.write_line('- XDG_CONFIG_HOME')
			writer.write_line('- XDG_CONFIG_DIRS')
		for env in self.env_variables:
			writer.write_line(f'- {env}')

		writer.write_line('')
		writer.write_lines(formatter.format_text(f'''\
You can also use environment variables to change the values of the settings listed under `set` command.
The corresponding environment variable name is the name of the setting in all upper case letters
with dots, hypens and spaces replaced by underscores and prefixed with "{self.envprefix}".'''))

		writer.write_lines(formatter.format_text('Lines in the config file which start with a %s are ignored.' % ' or '.join('`%s`' % c for c in self.COMMENT_PREFIXES)))

		writer.write_lines('The config file may contain the following commands:')
		for cmd in self.commands:
			names = '|'.join(cmd.get_names())
			writer.write_heading(SectionLevel.SECTION, names)
			writer.write_lines(cmd.get_help())

	def create_formatter(self) -> HelpFormatterWrapper:
		return HelpFormatterWrapper(self.formatter_class)

	def get_help(self) -> str:
		'''
		A convenience wrapper around :meth:`write_help`
		to return the help as a str instead of writing it to a file.

		This uses :class:`HelpWriter`.
		'''
		doc = io.StringIO()
		self.write_help(HelpWriter(doc))
		# The generated help ends with a \n which is implicitly added by print.
		# If I was writing to stdout or a file that would be desired.
		# But if I return it as a string and then print it, the print adds another \n which would be too much.
		# Therefore I am stripping the trailing \n.
		return doc.getvalue().rstrip('\n')


	# ------- auto complete -------

	def get_completions(self, line: str, cursor_pos: int) -> 'tuple[str, list[str], str]':
		'''
		Provide an auto completion for commands that can be executed with :meth:`parse_line`.

		:param line: The entire line that is currently in the text input field
		:param cursor_pos: The position of the cursor
		:return: start of line, completions, end of line.
			*completions* is a list of possible completions for the word where the cursor is located.
			If *completions* is an empty list there are no completions available and the user input should not be changed.
			If *completions* is not empty it should be displayed by a user interface in a drop down menu.
			The *start of line* is everything on the line before the completions.
			The *end of line* is everything on the line after the completions.
			In the likely case that the cursor is at the end of the line the *end of line* is an empty str.
			*start of line* and *end of line* should be the beginning and end of :paramref:`line` but they may contain minor changes in order to keep quoting feasible.
		'''
		original_ln = line
		stripped_line = line.lstrip()
		indentation = line[:len(line) - len(stripped_line)]
		cursor_pos -= len(indentation)
		line = stripped_line
		if self.enable_config_ids and line.startswith(self.ENTER_GROUP_PREFIX):
			out = self.get_completions_enter_group(line, cursor_pos)
		else:
			out = self.get_completions_command(line, cursor_pos)

		out = (indentation + out[0], out[1], out[2])
		return out

	def get_completions_enter_group(self, line: str, cursor_pos: int) -> 'tuple[str, list[str], str]':
		'''
		For a description of parameters and return type see :meth:`get_completions`.

		:meth:`get_completions` has stripped any indentation from :paramref:`line`
		and will prepend it to the first item of the return value.
		'''
		start = line
		groups = [self.ENTER_GROUP_PREFIX + str(cid) + self.ENTER_GROUP_SUFFIX for cid in MultiConfig.config_ids]
		groups = [cid for cid in groups if cid.startswith(start)]
		return '', groups, ''

	def get_completions_command(self, line: str, cursor_pos: int) -> 'tuple[str, list[str], str]':
		'''
		For a description of parameters and return type see :meth:`get_completions`.

		:meth:`get_completions` has stripped any indentation from :paramref:`line`
		and will prepend it to the first item of the return value.
		'''
		if not line:
			return self.get_completions_command_name(line, cursor_pos, start_of_line='', end_of_line='')

		ln_split = self.split_line_ignore_errors(line)
		assert ln_split
		a = self.find_arg(line, ln_split, cursor_pos)

		if a.in_between:
			start_of_line = line[:cursor_pos]
			end_of_line = line[cursor_pos:]
		else:
			start_of_line = line[:a.i0]
			end_of_line = line[a.i1:]

		if a.argument_pos == 0:
			return self.get_completions_command_name(line, cursor_pos, start_of_line=start_of_line, end_of_line=end_of_line)
		else:
			cmd = self.get_command(ln_split)
			return cmd.get_completions(ln_split, a.argument_pos, cursor_pos-a.i0, in_between=a.in_between, start_of_line=start_of_line, end_of_line=end_of_line)

	def find_arg(self, line: str, ln_split: 'list[str]', cursor_pos: int) -> ArgPos:
		'''
		This is an internal method used by :meth:`get_completions_command`
		'''
		CHARS_REMOVED_BY_SHLEX = ('"', "'", '\\')
		assert cursor_pos <= len(line)  # yes, cursor_pos can be == len(str)
		out = ArgPos()
		out.in_between = True

		# init all out attributes just to be save, these should not never be used because line is not empty and not white space only
		out.argument_pos = 0
		out.i0 = 0
		out.i1 = 0

		n_ln = len(line)
		i_ln = 0
		n_arg = len(ln_split)
		out.argument_pos = 0
		i_in_arg = 0
		assert out.argument_pos < n_ln
		while True:
			if out.in_between:
				assert i_in_arg == 0
				if i_ln >= n_ln:
					assert out.argument_pos >= n_arg - 1
					out.i0 = i_ln
					return out
				elif line[i_ln].isspace():
					i_ln += 1
				else:
					out.i0 = i_ln
					if i_ln >= cursor_pos:
						return out
					out.in_between = False
			else:
				if i_ln >= n_ln:
					assert out.argument_pos >= n_arg - 1
					out.i1 = i_ln
					return out
				elif out.argument_pos >= n_arg:
					# This is a comment
					out.i1 = n_ln
					return out
				elif i_in_arg >= len(ln_split[out.argument_pos]):
					if line[i_ln].isspace():
						out.i1 = i_ln
						if i_ln >= cursor_pos:
							return out
						out.in_between = True
						i_ln += 1
						out.argument_pos += 1
						i_in_arg = 0
					elif line[i_ln] in CHARS_REMOVED_BY_SHLEX:
						i_ln += 1
					else:
						# unlike bash shlex treats a comment character inside of an argument as a comment character
						assert line[i_ln] == '#'
						assert out.argument_pos == n_arg - 1
						out.i1 = i_ln
						return out
				elif line[i_ln] == ln_split[out.argument_pos][i_in_arg]:
					i_ln += 1
					i_in_arg += 1
				else:
					assert line[i_ln] in CHARS_REMOVED_BY_SHLEX
					i_ln += 1


	def get_completions_command_name(self, line: str, cursor_pos: int, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		start = line[:cursor_pos]
		completions = [cmd for cmd in self.command_dict.keys() if cmd.startswith(start)]
		return start_of_line, completions, end_of_line


	# ------- error handling -------

	def parse_error(self, msg: str) -> None:
		'''
		Is called if something went wrong while trying to load a config file.

		This method is called when a :class:`ParseException` or :class:`MultipleParseExceptions` is caught.
		This method compiles the given information into an error message and calls :meth:`self.ui_notifier.show_error() <UiNotifier.show_error>`.

		:param msg: The error message
		'''
		self.ui_notifier.show_error(msg)


# ---------- base classes for commands which can be used in config files ----------

class ConfigFileCommand(abc.ABC):

	'''
	An abstract base class for commands which can be used in a config file.

	Subclasses must implement the :meth:`run` method which is called when :class:`ConfigFile` is loading a file.
	Subclasses should contain a doc string so that :meth:`get_help` can provide a description to the user.
	Subclasses may set the :attr:`name` and :attr:`aliases` attributes to change the output of :meth:`get_name` and :meth:`get_names`.

	All subclasses are remembered and can be retrieved with :meth:`get_command_types`.
	They are instantiated in the constructor of :class:`ConfigFile`.
	'''

	#: The name which is used in the config file to call this command. Use an empty string to define a default command which is used if an undefined command is encountered. If this is not set :meth:`get_name` returns the name of this class in lower case letters and underscores replaced by hyphens.
	name: str

	#: Alternative names which can be used in the config file.
	aliases: 'tuple[str, ...]|list[str]'

	#: A description which may be used by an in-app help. If this is not set :meth:`get_help` uses the doc string instead.
	help: str

	#: If a config file contains only a single section it makes no sense to write a heading for it. This attribute is set by :meth:`ConfigFile.save_to_writer` if there are several commands which implement the :meth:`save` method. If you implement :meth:`save` and this attribute is set then :meth:`save` should write a section header. If :meth:`save` writes several sections it should always write the headings regardless of this attribute.
	should_write_heading: bool = False

	#: The :class:`ConfigFile` that has been passed to the constructor. It determines for example the :paramref:`~ConfigFile.notification_level` and the available :paramref:`~ConfigFile.commands`.
	config_file: ConfigFile

	#: The :class:`UiNotifier` of :attr:`config_file`
	ui_notifier: UiNotifier


	_subclasses: 'list[type[ConfigFileCommand]]' = []
	_used_names: 'set[str]' = set()

	@classmethod
	def get_command_types(cls) -> 'tuple[type[ConfigFileCommand], ...]':
		'''
		:return: All subclasses of :class:`ConfigFileCommand` which have not been deleted with :meth:`delete_command_type`
		'''
		return tuple(cls._subclasses)

	@classmethod
	def delete_command_type(cls, cmd_type: 'type[ConfigFileCommand]') -> None:
		'''
		Delete :paramref:`cmd_type` so that it is not returned anymore by :meth:`get_command_types` and that it's name can be used by another command.
		Do nothing if :paramref:`cmd_type` has already been deleted.
		'''
		if cmd_type in cls._subclasses:
			cls._subclasses.remove(cmd_type)
			for name in cmd_type.get_names():
				cls._used_names.remove(name)

	@classmethod
	def __init_subclass__(cls, replace: bool = False, abstract: bool = False) -> None:
		'''
		Add the new subclass to :attr:`subclass`.

		:param replace: Set :attr:`name` and :attr:`aliases` to the values of the parent class if they are not set explicitly, delete the parent class with :meth:`delete_command_type` and replace any commands with the same name
		:param abstract: This class is a base class for the implementation of other commands and shall *not* be returned by :meth:`get_command_types`
		:raises ValueError: if the name or one of it's aliases is already in use and :paramref:`replace` is not true
		'''
		if replace:
			parent_commands = [parent for parent in cls.__bases__ if issubclass(parent, ConfigFileCommand)]

			# set names of this class to that of the parent class(es)
			parent = parent_commands[0]
			if 'name' not in cls.__dict__:
				cls.name = parent.get_name()
			if 'aliases' not in cls.__dict__:
				cls.aliases = list(parent.get_names())[1:]
				for parent in parent_commands[1:]:
					cls.aliases.extend(parent.get_names())

			# remove parent class from the list of commands to be loaded or saved
			for parent in parent_commands:
				cls.delete_command_type(parent)

		if not abstract:
			cls._subclasses.append(cls)
			for name in cls.get_names():
				if name in cls._used_names and not replace:
					raise ValueError('duplicate command name %r' % name)
				cls._used_names.add(name)

	@classmethod
	def get_name(cls) -> str:
		'''
		:return: The name which is used in config file to call this command.
		
		If :attr:`name` is set it is returned as it is.
		Otherwise a name is generated based on the class name.
		'''
		if 'name' in cls.__dict__:
			return cls.name
		return cls.__name__.lower().replace("_", "-")

	@classmethod
	def get_names(cls) -> 'Iterator[str]':
		'''
		:return: Several alternative names which can be used in a config file to call this command.
		
		The first one is always the return value of :meth:`get_name`.
		If :attr:`aliases` is set it's items are yielded afterwards.

		If one of the returned items is the empty string this class is the default command
		and :meth:`run` will be called if an undefined command is encountered.
		'''
		yield cls.get_name()
		if 'aliases' in cls.__dict__:
			for name in cls.aliases:
				yield name

	def __init__(self, config_file: ConfigFile) -> None:
		self.config_file = config_file
		self.ui_notifier = config_file.ui_notifier

	@abc.abstractmethod
	def run(self, cmd: 'Sequence[str]') -> None:
		'''
		Process one line which has been read from a config file

		:raises ParseException: if there is an error in the line (e.g. invalid syntax)
		:raises MultipleParseExceptions: if there are several errors in the same line
		'''
		raise NotImplementedError()

	def create_formatter(self) -> HelpFormatterWrapper:
		return self.config_file.create_formatter()

	def get_help_attr_or_doc_str(self) -> str:
		'''
		:return: The :attr:`help` attribute or the doc string if :attr:`help` has not been set, cleaned up with :meth:`inspect.cleandoc`.
		'''
		if hasattr(self, 'help'):
			doc = self.help
		elif self.__doc__:
			doc = self.__doc__
		else:
			doc = ''

		return inspect.cleandoc(doc)

	def add_help_to(self, formatter: HelpFormatterWrapper) -> None:
		'''
		Add the return value of :meth:`get_help_attr_or_doc_str` to :paramref:`formatter`.
		'''
		formatter.add_text(self.get_help_attr_or_doc_str())

	def get_help(self) -> str:
		'''
		:return: A help text which can be presented to the user.

		This is generated by creating a formatter with :meth:`create_formatter`,
		adding the help to it with :meth:`add_help_to` and
		stripping trailing new line characters from the result of :meth:`HelpFormatterWrapper.format_help`.

		Most likely you don't want to override this method but :meth:`add_help_to` instead.
		'''
		formatter = self.create_formatter()
		self.add_help_to(formatter)
		return formatter.format_help().rstrip('\n')

	def save(self,
		writer: FormattedWriter,
		**kw: 'Unpack[SaveKwargs]',
	) -> None:
		'''
		Implement this method if you want calls to this command to be written by :meth:`ConfigFile.save`.

		If you implement this method write a section heading with :meth:`writer.write_heading('Heading') <FormattedWriter.write_heading>` if :attr:`should_write_heading` is true.
		If this command writes several sections then write a heading for every section regardless of :attr:`should_write_heading`.

		Write as many calls to this command as necessary to the config file in order to create the current state with :meth:`writer.write_command('...') <FormattedWriter.write_command>`.
		Write comments or help with :meth:`writer.write_lines('...') <FormattedWriter.write_lines>`.

		There is the :attr:`config_file` attribute (which was passed to the constructor) which you can use to:

		- quote arguments with :meth:`ConfigFile.quote`
		- call :attr:`ConfigFile.write_config_id`

		You probably don't need the comment character :attr:`ConfigFile.COMMENT` because :paramref:`writer` automatically comments out everything except for :meth:`FormattedWriter.write_command`.

		The default implementation does nothing.
		'''
		pass

	save.implemented = False  # type: ignore [attr-defined]


	# ------- auto complete -------

	def get_completions(self, cmd: 'Sequence[str]', argument_pos: int, cursor_pos: int, *, in_between: bool, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		'''
		:param cmd: The line split into arguments (including the name of this command as cmd[0])
		:param argument_pos: The index of the argument which shall be completed. Please note that this can be one bigger than :paramref:`cmd` is long if the line ends on a space and the cursor is behind that space. In that case :paramref:`in_between` is true.
		:param cursor_pos: The index inside of the argument where the cursor is located. This is undefined and should be ignored if :paramref:`in_between` is true. The input from the start of the argument to the cursor should be used to filter the completions. The input after the cursor can be ignored.
		:param in_between: If true: The cursor is between two arguments, before the first argument or after the last argument. :paramref:`argument_pos` refers to the next argument, :paramref:`argument_pos-1 <argument_pos>` to the previous argument. :paramref:`cursor_pos` is undefined.
		:param start_of_line: The first return value. If ``cmd[argument_pos]`` has a pattern like ``key=value`` you can append ``key=`` to this value and return only completions of ``value`` as second return value.
		:param end_of_line: The third return value.
		:return: start of line, completions, end of line.
			*completions* is a list of possible completions for the word where the cursor is located.
			If *completions* is an empty list there are no completions available and the user input should not be changed.
			This should be displayed by a user interface in a drop down menu.
			The *start of line* is everything on the line before the completions.
			The *end of line* is everything on the line after the completions.
			In the likely case that the cursor is at the end of the line the *end of line* is an empty str.
			*start of line* and *end of line* should be the beginning and end of :paramref:`line` but they may contain minor changes in order to keep quoting feasible.
		'''
		completions: 'list[str]' = []
		return start_of_line, completions, end_of_line

	def get_completions_for_file_name(self, start: str, *, relative_to: str, exclude: 'str|None' = None, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		r'''
		:param start: The start of the path to be completed
		:param relative_to: If :paramref:`start` is a relative path it's relative to this directory
		:param exclude: A regular expression. The default value :obj:`None` is interpreted differently depending on the :meth:`platform.platform`. For ``Windows`` it's ``$none`` so that nothing is excluded. For others it's ``^\.`` so that hidden files and directories are excluded.
		:return: All files and directories that start with :paramref:`start` and do not match :paramref:`exclude`. Directories are appended with :const:`os.path.sep`. :const:`os.path.sep` is appended after quoting so that it can be easily stripped if undesired (e.g. if the user interface cycles through all possible completions instead of completing the longest common prefix).
		'''
		if exclude is None:
			if platform.platform() == 'Windows' or os.path.split(start)[1].startswith('.'):
				exclude = '$none'
			else:
				exclude = r'^\.'
		reo = re.compile(exclude)

		# I cannot use os.path.split because that would ignore the important difference between having a trailing separator or not
		if os.path.sep in start:
			directory, start = start.rsplit(os.path.sep, 1)
			directory += os.path.sep
			quoted_directory = self.quote_path(directory)

			start_of_line += quoted_directory
			directory = os.path.expanduser(directory)
			if not os.path.isabs(directory):
				directory = os.path.join(relative_to, directory)
			directory = os.path.normpath(directory)
		else:
			directory = relative_to

		try:
			names = os.listdir(directory)
		except (FileNotFoundError, NotADirectoryError):
			return start_of_line, [], end_of_line

		out: 'list[str]' = []
		for name in names:
			if reo.match(name):
				continue
			if not name.startswith(start):
				continue

			quoted_name = self.config_file.quote(name)
			if os.path.isdir(os.path.join(directory, name)):
				quoted_name += os.path.sep

			out.append(quoted_name)

		return start_of_line, out, end_of_line

	def quote_path(self, path: str) -> str:
		path_split = path.split(os.path.sep)
		i0 = 1 if path_split[0] == '~' else 0
		for i in range(i0, len(path_split)):
			if path_split[i]:
				path_split[i] = self.config_file.quote(path_split[i])
		return os.path.sep.join(path_split)


class ArgumentParser(argparse.ArgumentParser):

	def error(self, message: str) -> 'typing.NoReturn':
		'''
		Raise a :class:`ParseException`.
		'''
		raise ParseException(message)

class ConfigFileArgparseCommand(ConfigFileCommand, abstract=True):

	'''
	An abstract subclass of :class:`ConfigFileCommand` which uses :mod:`argparse` to make parsing and providing help easier.

	You must implement the class method :meth:`init_parser` to add the arguments to :attr:`parser`.
	Instead of :meth:`run` you must implement :meth:`run_parsed`.
	You don't need to add a usage or the possible arguments to the doc string as :mod:`argparse` will do that for you.
	You should, however, still give a description what this command does in the doc string.

	You may specify :attr:`ConfigFileCommand.name`, :attr:`ConfigFileCommand.aliases` and :meth:`ConfigFileCommand.save` like for :class:`ConfigFileCommand`.
	'''

	def __init__(self, config_file: ConfigFile) -> None:
		super().__init__(config_file)
		self._names = set(self.get_names())
		self.parser = ArgumentParser(prog=self.get_name(), description=self.get_help_attr_or_doc_str(), add_help=False, formatter_class=self.config_file.formatter_class)
		self.init_parser(self.parser)

	@abc.abstractmethod
	def init_parser(self, parser: ArgumentParser) -> None:
		'''
		:param parser: The parser to add arguments to. This is the same object like :attr:`parser`.

		This is an abstract method which must be implemented by subclasses.
		Use :meth:`ArgumentParser.add_argument` to add arguments to :paramref:`parser`.
		'''
		pass

	def get_help(self) -> str:
		'''
		Creates a help text which can be presented to the user by calling :meth:`parser.format_help`.
		The return value of :meth:`ConfigFileCommand.write_help` has been passed as :paramref:`description` to the constructor of :class:`ArgumentParser`, therefore :attr:`help`/the doc string are included as well.
		'''
		return self.parser.format_help().rstrip('\n')

	def run(self, cmd: 'Sequence[str]') -> None:
		# if the line was empty this method should not be called but an empty line should be ignored either way
		if not cmd:
			return  # pragma: no cover
		# cmd[0] does not need to be in self._names if this is the default command, i.e. if '' in self._names
		if cmd[0] in self._names:
			cmd = cmd[1:]
		args = self.parser.parse_args(cmd)
		self.run_parsed(args)

	@abc.abstractmethod
	def run_parsed(self, args: argparse.Namespace) -> None:
		'''
		This is an abstract method which must be implemented by subclasses.
		'''
		pass

	# ------- auto complete -------

	def get_completions(self, cmd: 'Sequence[str]', argument_pos: int, cursor_pos: int, *, in_between: bool, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if in_between:
			start = ''
		else:
			start = cmd[argument_pos][:cursor_pos]

		if self.after_positional_argument_marker(cmd, argument_pos):
			pos = self.get_position(cmd, argument_pos)
			return self.get_completions_for_positional_argument(pos, start, start_of_line=start_of_line, end_of_line=end_of_line)

		if argument_pos > 0:  # pragma: no branch  # if argument_pos was 0 this method would not be called, command names would be completed instead
			prevarg = self.get_option_name_if_it_takes_an_argument(cmd, argument_pos-1)
			if prevarg:
				return self.get_completions_for_option_argument(prevarg, start, start_of_line=start_of_line, end_of_line=end_of_line)

		if self.is_option_start(start):
			if '=' in start:
				i = start.index('=')
				option_name = start[:i]
				i += 1
				start_of_line += start[:i]
				start = start[i:]
				return self.get_completions_for_option_argument(option_name, start, start_of_line=start_of_line, end_of_line=end_of_line)
			return self.get_completions_for_option_name(start, start_of_line=start_of_line, end_of_line=end_of_line)

		pos = self.get_position(cmd, argument_pos)
		return self.get_completions_for_positional_argument(pos, start, start_of_line=start_of_line, end_of_line=end_of_line)

	def get_position(self, cmd: 'Sequence[str]', argument_pos: int) -> int:
		'''
		:return: the position of a positional argument, not counting options and their arguments
		'''
		pos = 0
		n = len(cmd)
		options_allowed = True
		# I am starting at 1 because cmd[0] is the name of the command, not an argument
		for i in range(1, argument_pos):
			if options_allowed and i < n:
				if cmd[i] == '--':
					options_allowed = False
					continue
				elif self.is_option_start(cmd[i]):
					continue
				# > 1 because cmd[0] is the name of the command
				elif i > 1 and self.get_option_name_if_it_takes_an_argument(cmd, i-1):
					continue
			pos += 1

		return pos

	def is_option_start(self, start: str) -> bool:
		return start.startswith('-') or start.startswith('+')

	def after_positional_argument_marker(self, cmd: 'Sequence[str]', argument_pos: int) -> bool:
		'''
		:return: true if this can only be a positional argument. False means it can be both, option or positional argument.
		'''
		return '--' in cmd and cmd.index('--') < argument_pos

	def get_option_name_if_it_takes_an_argument(self, cmd: 'Sequence[str]', argument_pos: int) -> 'str|None':
		if argument_pos >= len(cmd):
			return None  # pragma: no cover  # this does not happen because this method is always called for the previous argument

		arg = cmd[argument_pos]
		if '=' in arg:
			# argument of option is already given within arg
			return None
		if not self.is_option_start(arg):
			return None
		if arg.startswith('--'):
			action = self.get_action_for_option(arg)
			if action is None:
				return None
			if action.nargs != 0:
				return arg
			return None

		# arg is a combination of single character flags like in `tar -xzf file`
		for c in arg[1:-1]:
			action = self.get_action_for_option('-' + c)
			if action is None:
				continue
			if action.nargs != 0:
				# c takes an argument but that is already given within arg
				return None

		out = '-' + arg[-1]
		action = self.get_action_for_option(out)
		if action is None:
			return None
		if action.nargs != 0:
			return out
		return None


	def get_completions_for_option_name(self, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		completions = []
		for a in self.parser._get_optional_actions():
			for opt in a.option_strings:
				if len(opt) <= 2:
					# this is trivial to type but not self explanatory
					# => not helpful for auto completion
					continue
				if opt.startswith(start):
					completions.append(opt)
		return start_of_line, completions, end_of_line

	def get_completions_for_option_argument(self, option_name: str, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		return self.get_completions_for_action(self.get_action_for_option(option_name), start, start_of_line=start_of_line, end_of_line=end_of_line)

	def get_completions_for_positional_argument(self, position: int, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		return self.get_completions_for_action(self.get_action_for_positional_argument(position), start, start_of_line=start_of_line, end_of_line=end_of_line)


	def get_action_for_option(self, option_name: str) -> 'argparse.Action|None':
		for a in self.parser._get_optional_actions():
			if option_name in a.option_strings:
				return a
		return None

	def get_action_for_positional_argument(self, argument_pos: int) -> 'argparse.Action|None':
		actions = self.parser._get_positional_actions()
		if argument_pos < len(actions):
			return actions[argument_pos]
		return None

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if action is None:
			completions: 'list[str]' = []
		elif not action.choices:
			completions = []
		else:
			completions = [str(val) for val in action.choices]
			completions = [val for val in completions if val.startswith(start)]
			completions = [self.config_file.quote(val) for val in completions]
		return start_of_line, completions, end_of_line


# ---------- implementations of commands which can be used in config files ----------

class Set(ConfigFileCommand):

	r'''
	usage: set key1=val1 [key2=val2 ...] \\
	       set key [=] val

	Change the value of a setting.

	In the first form set takes an arbitrary number of arguments, each argument sets one setting.
	This has the advantage that several settings can be changed at once.
	That is useful if you want to bind a set command to a key and process that command with ConfigFile.parse_line() if the key is pressed.

	In the second form set takes two arguments, the key and the value. Optionally a single equals character may be added in between as third argument.
	This has the advantage that key and value are separated by one or more spaces which can improve the readability of a config file.
	'''

	#: The separator which is used between a key and it's value
	KEY_VAL_SEP = '='

	#: Help for data types. This is used by :meth:`get_help_for_data_types`. Change this with :meth:`set_help_for_type`.
	help_for_types = {
		str : 'A text. If it contains spaces it must be wrapped in single or double quotes.',
		int : '''\
			An integer number in python 3 syntax, as decimal (e.g. 42), hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g. 0b101010).
			Leading zeroes are not permitted to avoid confusion with python 2's syntax for octal numbers.
			It is permissible to group digits with underscores for better readability, e.g. 1_000_000.''',
		#bool,
		float : 'A floating point number in python syntax, e.g. 23, 1.414, -1e3, 3.14_15_93.',
	}


	# ------- load -------

	def run(self, cmd: 'Sequence[str]') -> None:
		'''
		Call :meth:`set_multiple` if the first argument contains :attr:`KEY_VAL_SEP` otherwise :meth:`set_with_spaces`.

		:raises ParseException: if something is wrong (no arguments given, invalid syntax, invalid key, invalid value)
		'''
		if len(cmd) < 2:
			raise ParseException('no settings given')

		if self.is_vim_style(cmd):
			self.set_multiple(cmd)
		else:
			self.set_with_spaces(cmd)

	def is_vim_style(self, cmd: 'Sequence[str]') -> bool:
		'''
		:paramref:`cmd` has one of two possible styles:
		- vim inspired: set takes an arbitrary number of arguments, each argument sets one setting. Is handled by :meth:`set_multiple`.
		- ranger inspired: set takes two arguments, the key and the value. Optionally a single equals character may be added in between as third argument. Is handled by :meth:`set_with_spaces`.

		:return: true if cmd has a vim inspired style, false if cmd has a ranger inspired style
		'''
		return self.KEY_VAL_SEP in cmd[1]  # cmd[0] is the name of the command, cmd[1] is the first argument

	def set_with_spaces(self, cmd: 'Sequence[str]') -> None:
		'''
		Process one line of the format ``set key [=] value``

		:raises ParseException: if something is wrong (invalid syntax, invalid key, invalid value)
		'''
		n = len(cmd)
		if n == 3:
			cmdname, key, value = cmd
			self.parse_key_and_set_value(key, value)
		elif n == 4:
			cmdname, key, sep, value = cmd
			if sep != self.KEY_VAL_SEP:
				raise ParseException(f'separator between key and value should be {self.KEY_VAL_SEP}, not {sep!r}')
			self.parse_key_and_set_value(key, value)
		elif n == 2:
			raise ParseException(f'missing value or missing {self.KEY_VAL_SEP}')
		else:
			assert n >= 5
			raise ParseException(f'too many arguments given or missing {self.KEY_VAL_SEP} in first argument')

	def set_multiple(self, cmd: 'Sequence[str]') -> None:
		'''
		Process one line of the format ``set key=value [key2=value2 ...]``

		:raises MultipleParseExceptions: if something is wrong (invalid syntax, invalid key, invalid value)
		'''
		exceptions = []
		for arg in cmd[1:]:
			try:
				if not self.KEY_VAL_SEP in arg:
					raise ParseException(f'missing {self.KEY_VAL_SEP} in {arg!r}')
				key, value = arg.split(self.KEY_VAL_SEP, 1)
				self.parse_key_and_set_value(key, value)
			except ParseException as e:
				exceptions.append(e)
		if exceptions:
			raise MultipleParseExceptions(exceptions)

	def parse_key_and_set_value(self, key: str, value: str) -> None:
		'''
		Find the corresponding :class:`Config` instance for :paramref:`key` and call :meth:`set_value` with the return value of :meth:`parse_value`.

		:raises ParseException: if key is invalid or if :meth:`parse_value` or :meth:`set_value` raises a :class:`ValueError`
		'''
		if key not in self.config_file.config_instances:
			raise ParseException(f'invalid key {key!r}')

		instance = self.config_file.config_instances[key]
		try:
			self.set_value(instance, self.parse_value(instance, value))
		except ValueError as e:
			raise ParseException(str(e))

	def parse_value(self, instance: 'Config[T2]', value: str) -> 'T2':
		'''
		Parse a value to the data type of a given setting by calling :meth:`instance.parse_value(value) <Config.parse_value>`
		'''
		return instance.parse_value(value)

	def set_value(self, instance: 'Config[T2]', value: 'T2') -> None:
		'''
		Assign :paramref:`value` to :paramref`instance` by calling :meth:`Config.set_value` with :attr:`ConfigFile.config_id` of :attr:`config_file`.
		Afterwards call :meth:`UiNotifier.show_info`.
		'''
		instance.set_value(self.config_file.config_id, value)
		self.ui_notifier.show_info(f'set {instance.key} to {instance.format_value(self.config_file.config_id)}')


	# ------- save -------

	def iter_config_instances_to_be_saved(self, **kw: 'Unpack[SaveKwargs]') -> 'Iterator[Config[object]]':
		'''
		:param config_instances: The settings to consider
		:param ignore: Skip these settings

		Iterate over all given :paramref:`config_instances` and expand all :class:`DictConfig` instances into the :class:`Config` instances they consist of.
		Sort the resulting list if :paramref:`config_instances` is not a :class:`list` or a :class:`tuple`.
		Yield all :class:`Config` instances which are not (directly or indirectly) contained in :paramref:`ignore` and where :meth:`Config.wants_to_be_exported` returns true.
		'''
		config_instances = kw['config_instances']
		ignore = kw['ignore']

		config_keys = []
		for c in config_instances:
			if isinstance(c, DictConfig):
				config_keys.extend(sorted(c.iter_keys()))
			else:
				config_keys.append(c.key)
		if not isinstance(config_instances, (list, tuple)):
			config_keys = sorted(config_keys)

		if ignore is not None:
			tmp = set()
			for c in tuple(ignore):
				if isinstance(c, DictConfig):
					tmp |= set(c._values.values())
				else:
					tmp.add(c)
			ignore = tmp

		for key in config_keys:
			instance = self.config_file.config_instances[key]
			if not instance.wants_to_be_exported():
				continue

			if ignore is not None and instance in ignore:
				continue

			yield instance

	def save(self, writer: FormattedWriter, **kw: 'Unpack[SaveKwargs]') -> None:
		'''
		:param writer: The file to write to
		:param bool no_multi: If true: treat :class:`MultiConfig` instances like normal :class:`Config` instances and only write their default value. If false: Separate :class:`MultiConfig` instances and print them once for every :attr:`MultiConfig.config_ids`.
		:param bool comments: If false: don't write help for data types

		Iterate over all :class:`Config` instances with :meth:`iter_config_instances_to_be_saved`,
		split them into normal :class:`Config` and :class:`MultiConfig` and write them with :meth:`save_config_instance`.
		But before that set :attr:`last_name` to None (which is used by :meth:`write_config_help`)
		and write help for data types based on :meth:`get_help_for_data_types`.
		'''
		no_multi = kw['no_multi']
		comments = kw['comments']

		config_instances = list(self.iter_config_instances_to_be_saved(**kw))
		normal_configs = []
		multi_configs = []
		if no_multi:
			normal_configs = config_instances
		else:
			for instance in config_instances:
				if isinstance(instance, MultiConfig):
					multi_configs.append(instance)
				else:
					normal_configs.append(instance)

		self.last_name: 'str|None' = None

		if normal_configs:
			if multi_configs:
				writer.write_heading(SectionLevel.SECTION, 'Application wide settings')
			elif self.should_write_heading:
				writer.write_heading(SectionLevel.SECTION, 'Settings')

			if comments:
				type_help = self.get_help_for_data_types(normal_configs)
				if type_help:
					writer.write_heading(SectionLevel.SUB_SECTION, 'Data types')
					writer.write_lines(type_help)

			for instance in normal_configs:
				self.save_config_instance(writer, instance, config_id=None, **kw)

		if multi_configs:
			if normal_configs:
				writer.write_heading(SectionLevel.SECTION, 'Settings which can have different values for different objects')
			elif self.should_write_heading:
				writer.write_heading(SectionLevel.SECTION, 'Settings')

			if comments:
				type_help = self.get_help_for_data_types(multi_configs)
				if type_help:
					writer.write_heading(SectionLevel.SUB_SECTION, 'Data types')
					writer.write_lines(type_help)

			for instance in multi_configs:
				self.save_config_instance(writer, instance, config_id=instance.default_config_id, **kw)

			for config_id in MultiConfig.config_ids:
				writer.write_line('')
				self.config_file.write_config_id(writer, config_id)
				for instance in multi_configs:
					self.save_config_instance(writer, instance, config_id, **kw)

	def save_config_instance(self, writer: FormattedWriter, instance: 'Config[object]', config_id: 'ConfigId|None', **kw: 'Unpack[SaveKwargs]') -> None:
		'''
		:param writer: The file to write to
		:param instance: The config value to be saved
		:param config_id: Which value to be written in case of a :class:`MultiConfig`, should be :const:`None` for a normal :class:`Config` instance
		:param bool comments: If true: call :meth:`write_config_help`

		Convert the :class:`Config` instance into a value str with :meth:`format_value`,
		wrap it in quotes if necessary with :meth:`config_file.quote` and write it to :paramref:`writer`.
		'''
		if kw['comments']:
			self.write_config_help(writer, instance)
		value = self.format_value(instance, config_id)
		value = self.config_file.quote(value)
		ln = f'{self.get_name()} {instance.key} = {value}'
		writer.write_command(ln)

	def format_value(self, instance: Config[typing.Any], config_id: 'ConfigId|None') -> str:
		'''
		:param instance: The config value to be saved
		:param config_id: Which value to be written in case of a :class:`MultiConfig`, should be :const:`None` for a normal :class:`Config` instance
		:return: A str representation to be written to the config file

		Convert the value of the :class:`Config` instance into a str with :meth:`Config.format_value`.
		'''
		return instance.format_value(config_id)

	def write_config_help(self, writer: FormattedWriter, instance: Config[typing.Any], *, group_dict_configs: bool = True) -> None:
		'''
		:param writer: The output to write to
		:param instance: The config value to be saved

		Write a comment which explains the meaning and usage of this setting
		based on :meth:`Config.format_allowed_values_or_type` and :attr:`Config.help`.

		Use :attr:`last_name` to write the help only once for all :class:`Config` instances belonging to the same :class:`DictConfig` instance.
		'''
		if group_dict_configs and instance.parent is not None:
			name = instance.parent.key_prefix
		else:
			name = instance.key
		if name == self.last_name:
			return

		formatter = HelpFormatterWrapper(self.config_file.formatter_class)
		writer.write_heading(SectionLevel.SUB_SECTION, name)
		writer.write_lines(formatter.format_text(instance.format_allowed_values_or_type()).rstrip())
		#if instance.unit:
		#	writer.write_line('unit: %s' % instance.unit)
		if isinstance(instance.help, dict):
			for key, val in instance.help.items():
				key_name = instance.format_any_value(key)
				val = inspect.cleandoc(val)
				writer.write_lines(formatter.format_item(bullet=key_name+': ', text=val).rstrip())
		elif isinstance(instance.help, str):
			writer.write_lines(formatter.format_text(inspect.cleandoc(instance.help)).rstrip())

		self.last_name = name


	@classmethod
	def set_help_for_type(cls, t: 'type[object]', help_text: str) -> None:
		'''
		:meth:`get_help_for_data_types` is used by :meth:`save` and :meth:`get_help`.
		Usually it uses the :attr:`help` attribute of the class.
		But if the class does not have a :attr:`help` attribute or if you want a different help text
		you can set the help with this method.

		:param t: The type for which you want to specify a help
		:param help_text: The help for :paramref:`t`. It is cleaned up in :meth:`get_data_type_name_to_help_map` with :func:`inspect.cleandoc`.
		'''
		cls.help_for_types[t] = help_text

	def get_data_type_name_to_help_map(self, config_instances: 'Iterable[Config[object]]') -> 'dict[str, str]':
		'''
		:param config_instances: All config values to be saved
		:return: A dictionary containing the type names as keys and the help as values

		The returned dictionary contains the help for all data types except enumerations
		which occur in :paramref:`config_instances`.
		The help is gathered from the :attr:`help` attribute of the type
		or the str registered with :meth:`set_help_for_type`.
		The help is cleaned up with :func:`inspect.cleandoc`.
		'''
		help_text: 'dict[str, str]' = {}
		for instance in config_instances:
			t = instance.type if instance.type != list else instance.item_type
			name = getattr(t, 'type_name', t.__name__)
			if name in help_text:
				continue

			if t in self.help_for_types:
				h = self.help_for_types[t]
			elif hasattr(t, 'help'):
				h = t.help
			elif issubclass(t, enum.Enum) or t is bool:
				# an enum does not need a help if the values have self explanatory names
				# bool is treated like an enum
				continue
			else:
				raise AttributeError('No help given for {typename} ({classname}). Please specify it as help attribute or with set_help_for_type.'.format(typename=name, classname=t.__name__))

			help_text[name] = inspect.cleandoc(h)

		return help_text

	def add_help_for_data_types(self, formatter: HelpFormatterWrapper, config_instances: 'Iterable[Config[object]]') -> None:
		help_map = self.get_data_type_name_to_help_map(config_instances)
		if not help_map:
			return

		for name in sorted(help_map.keys()):
			formatter.add_start_section(name)
			formatter.add_text(help_map[name])
			formatter.add_end_section()

	def get_help_for_data_types(self, config_instances: 'Iterable[Config[object]]') -> str:
		formatter = self.create_formatter()
		self.add_help_for_data_types(formatter, config_instances)
		return formatter.format_help().rstrip('\n')

	# ------- help -------

	def add_help_to(self, formatter: HelpFormatterWrapper) -> None:
		super().add_help_to(formatter)

		kw: 'SaveKwargs' = {}
		self.config_file.set_save_default_arguments(kw)
		config_instances = list(self.iter_config_instances_to_be_saved(**kw))
		self.last_name = None

		formatter.add_start_section('data types')
		self.add_help_for_data_types(formatter, config_instances)
		formatter.add_end_section()

		if self.config_file.enable_config_ids:
			normal_configs = []
			multi_configs = []
			for instance in config_instances:
				if isinstance(instance, MultiConfig):
					multi_configs.append(instance)
				else:
					normal_configs.append(instance)
		else:
			normal_configs = config_instances
			multi_configs = []

		if normal_configs:
			if self.config_file.enable_config_ids:
				formatter.add_start_section('application wide settings')
			else:
				formatter.add_start_section('settings')
			for instance in normal_configs:
				self.add_config_help(formatter, instance)
			formatter.add_end_section()

		if multi_configs:
			formatter.add_start_section('settings which can have different values for different objects')
			formatter.add_text(inspect.cleandoc(self.config_file.get_help_config_id()))
			for instance in multi_configs:
				self.add_config_help(formatter, instance)
			formatter.add_end_section()

	def add_config_help(self, formatter: HelpFormatterWrapper, instance: Config[typing.Any]) -> None:
		formatter.add_start_section(instance.key)
		formatter.add_text(instance.format_allowed_values_or_type())
		#if instance.unit:
		#	formatter.add_item(bullet='unit: ', text=instance.unit)
		if isinstance(instance.help, dict):
			for key, val in instance.help.items():
				key_name = instance.format_any_value(key)
				val = inspect.cleandoc(val)
				formatter.add_item(bullet=key_name+': ', text=val)
		elif isinstance(instance.help, str):
			formatter.add_text(inspect.cleandoc(instance.help))
		formatter.add_end_section()

	# ------- auto complete -------

	def get_completions(self, cmd: 'Sequence[str]', argument_pos: int, cursor_pos: int, *, in_between: bool, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if argument_pos >= len(cmd):
			start = ''
		else:
			start = cmd[argument_pos][:cursor_pos]

		if len(cmd) <= 1:
			return self.get_completions_for_key(start, start_of_line=start_of_line, end_of_line=end_of_line)
		elif self.is_vim_style(cmd):
			return self.get_completions_for_vim_style_arg(cmd, argument_pos, start, start_of_line=start_of_line, end_of_line=end_of_line)
		else:
			return self.get_completions_for_ranger_style_arg(cmd, argument_pos, start, start_of_line=start_of_line, end_of_line=end_of_line)

	def get_completions_for_vim_style_arg(self, cmd: 'Sequence[str]', argument_pos: int, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if self.KEY_VAL_SEP in start:
			key, start = start.split(self.KEY_VAL_SEP, 1)
			start_of_line += key + self.KEY_VAL_SEP
			return self.get_completions_for_value(key, start, start_of_line=start_of_line, end_of_line=end_of_line)
		else:
			return self.get_completions_for_key(start, start_of_line=start_of_line, end_of_line=end_of_line)

	def get_completions_for_ranger_style_arg(self, cmd: 'Sequence[str]', argument_pos: int, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if argument_pos == 1:
			return self.get_completions_for_key(start, start_of_line=start_of_line, end_of_line=end_of_line)
		elif argument_pos == 2 or (argument_pos == 3 and cmd[2] == self.KEY_VAL_SEP):
			return self.get_completions_for_value(cmd[1], start, start_of_line=start_of_line, end_of_line=end_of_line)
		else:
			return start_of_line, [], end_of_line

	def get_completions_for_key(self, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		completions = [key for key in self.config_file.config_instances.keys() if key.startswith(start)]
		return start_of_line, completions, end_of_line

	def get_completions_for_value(self, key: str, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		instance = self.config_file.config_instances.get(key)
		if instance is None:
			return start_of_line, [], end_of_line

		t: 'None|type[object]' = None
		if instance.type is list:
			first, start = start.rsplit(instance.LIST_SEP)
			start_of_line += first + instance.LIST_SEP
			t = instance.item_type

		completions = [self.config_file.quote(val) for val in instance.get_stringified_allowed_values(t) if val.startswith(start)]
		return start_of_line, completions, end_of_line


class Include(ConfigFileArgparseCommand):

	'''
	Load another config file.

	This is useful if a config file is getting so big that you want to split it up
	or if you want to have different config files for different use cases which all include the same standard config file to avoid redundancy
	or if you want to bind several commands to one key which executes one command with ConfigFile.parse_line().
	'''

	help_config_id = '''
	By default the loaded config file starts with which ever config id is currently active.
	This is useful if you want to use the same values for several config ids:
	Write the set commands without a config id to a separate config file and include this file for every config id where these settings shall apply.

	After the include the config id is reset to the config id which was active at the beginning of the include
	because otherwise it might lead to confusion if the config id is changed in the included config file.
	'''

	def init_parser(self, parser: ArgumentParser) -> None:
		parser.add_argument('path', help='The config file to load. Slashes are replaced with the directory separator appropriate for the current operating system. If the path contains a space it must be wrapped in single or double quotes.')
		if self.config_file.enable_config_ids:
			assert parser.description is not None
			parser.description += '\n\n' + inspect.cleandoc(self.help_config_id)
			group = parser.add_mutually_exclusive_group()
			group.add_argument('--reset-config-id-before', action='store_true', help='Ignore any config id which might be active when starting the include')
			group.add_argument('--no-reset-config-id-after', action='store_true', help='Treat the included lines as if they were written in the same config file instead of the include command')

		self.nested_includes: 'list[str]' = []

	def run_parsed(self, args: argparse.Namespace) -> None:
		fn_imp = args.path
		fn_imp = fn_imp.replace('/', os.path.sep)
		fn_imp = os.path.expanduser(fn_imp)
		if not os.path.isabs(fn_imp):
			fn = self.config_file.context_file_name
			if fn is None:
				fn = self.config_file.get_save_path()
			fn_imp = os.path.join(os.path.dirname(os.path.abspath(fn)), fn_imp)

		if fn_imp in self.nested_includes:
			raise ParseException(f'circular include of file {fn_imp!r}')
		if not os.path.isfile(fn_imp):
			raise ParseException(f'no such file {fn_imp!r}')

		self.nested_includes.append(fn_imp)

		if self.config_file.enable_config_ids and args.no_reset_config_id_after:
			self.config_file.load_without_resetting_config_id(fn_imp)
		elif self.config_file.enable_config_ids and args.reset_config_id_before:
			config_id = self.config_file.config_id
			self.config_file.load_file(fn_imp)
			self.config_file.config_id = config_id
		else:
			config_id = self.config_file.config_id
			self.config_file.load_without_resetting_config_id(fn_imp)
			self.config_file.config_id = config_id

		assert self.nested_includes[-1] == fn_imp
		del self.nested_includes[-1]

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		# action does not have a name and metavar is None if not explicitly set, dest is the only way to identify the action
		if action is not None and action.dest == 'path':
			return self.get_completions_for_file_name(start, relative_to=os.path.dirname(self.config_file.get_save_path()), start_of_line=start_of_line, end_of_line=end_of_line)
		return super().get_completions_for_action(action, start, start_of_line=start_of_line, end_of_line=end_of_line)


class UnknownCommand(ConfigFileCommand, abstract=True):

	name = DEFAULT_COMMAND

	def run(self, cmd: 'Sequence[str]') -> None:
		raise ParseException('unknown command %r' % cmd[0])
