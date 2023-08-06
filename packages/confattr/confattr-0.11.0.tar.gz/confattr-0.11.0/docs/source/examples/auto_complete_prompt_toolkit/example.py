#!../../../../venv/bin/python3

__package__ = 'auto-completion-example'

# ------- start -------
import os
import argparse
from collections.abc import Iterator

from confattr import Config, DictConfig, ConfigFile, Message, NotificationLevel, ConfigFileArgparseCommand

from prompt_toolkit import print_formatted_text, PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.styles.named_colors import NAMED_COLORS

COLOR_CHOICES = (
	'ansiblack', 'ansired', 'ansigreen', 'ansiyellow', 'ansiblue', 'ansimagenta', 'ansicyan', 'ansigray',
	'ansibrightblack', 'ansibrightred', 'ansibrightgreen', 'ansibrightyellow', 'ansibrightblue', 'ansibrightmagenta', 'ansibrightcyan', 'ansiwhite',
) + tuple(c.lower() for c in NAMED_COLORS.keys())
COLORS = DictConfig('color', {NotificationLevel.ERROR: 'ansired', NotificationLevel.INFO: ''}, allowed_values=COLOR_CHOICES)


class ConfigFileCompleter(Completer):

	def __init__(self, config_file: ConfigFile) -> None:
		super().__init__()
		self.config_file = config_file

	def get_completions(self, document: Document, complete_event: CompleteEvent) -> 'Iterator[Completion]':
		start_of_line, completions, end_of_line = self.config_file.get_completions(document.text, document.cursor_position)
		for word in completions:
			yield Completion(start_of_line + word.rstrip(os.path.sep), display=word, start_position=-document.cursor_position)


class Quit(ConfigFileArgparseCommand):

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		pass

	def run_parsed(self, args: argparse.Namespace) -> None:
		raise EOFError()

class Echo(ConfigFileArgparseCommand):

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('-c', '--color', choices=COLOR_CHOICES)
		parser.add_argument('msg', nargs=argparse.ONE_OR_MORE)

	def run_parsed(self, args: argparse.Namespace) -> None:
		colored_print(args.color, ' '.join(args.msg))

def colored_print(color: 'str|None', msg: str) -> None:
		if color:
			print_formatted_text(FormattedText([(color, str(msg))]))
		else:
			print_formatted_text(str(msg))

def main() -> None:
	# creating 2 ConfigFile instances with different notification level filters
	config_file = ConfigFile(appname=__package__, notification_level=Config('notification-level.config-file', NotificationLevel.ERROR))
	config_file.load()
	cli = ConfigFile(appname=__package__, notification_level=Config('notification-level.cli', NotificationLevel.INFO))
	cli.command_dict['include'].config_file = config_file

	# show errors in config
	def on_config_message(msg: Message) -> None:
		color = COLORS.get(msg.notification_level)
		colored_print(color, str(msg))
	config_file.set_ui_callback(on_config_message)
	cli.set_ui_callback(on_config_message)

	# main user interface
	p: 'PromptSession[str]' = PromptSession('>>> ', completer=ConfigFileCompleter(config_file))
	while True:
		Message.reset()
		try:
			cli.parse_line(p.prompt())
		except EOFError:
			break

if __name__ == '__main__':
	main()
