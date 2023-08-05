"""Checker for optional non-keyword only parameters."""

from __future__ import annotations

import ast
import enum
import re
import sys
from typing import ClassVar, Dict, TYPE_CHECKING, Tuple, cast

import flake8_keyword_params

from typing_extensions import Protocol

if (TYPE_CHECKING):
	import tokenize
	from collections.abc import Iterator, Sequence, Mapping
	from flake8.options.manager import OptionManager


try:
	try:
		from importlib.metadata import version
	except ModuleNotFoundError:  # python < 3.8 use polyfill
		from importlib_metadata import version  # type: ignore
	package_version = version(__package__)
except Exception:
	package_version = 'unknown'


LogicalResult = Tuple[Tuple[int, int], str]  # (line, column), text
PhysicalResult = Tuple[int, str]  # (column, text)
ASTResult = Tuple[int, int, str, type]  # (line, column, text, type)


SAFELIST_FUNCTIONS = {
	'__exit__': ['.*'],
	'__aexit__': ['.*'],
	'get': ['default'],
}


class Options(Protocol):
	"""Protocol for options."""

	keyword_params_include_name: bool
	keyword_params_safelist: Sequence[str]
	keyword_params_exclude_safelist: Sequence[str]


class Message(enum.Enum):
	"""Messages."""

	NON_KEWORD_OPTIONAL = (1, "Optional parameter '{param}' should be keyword only")

	@property
	def code(self) -> str:
		return (flake8_keyword_params.plugin_prefix + str(self.value[0]).rjust(6 - len(flake8_keyword_params.plugin_prefix), '0'))

	def text(self, **kwargs) -> str:
		return self.value[1].format(**kwargs)


def _func_re(func: str, option: str) -> re.Pattern:
	try:
		return re.compile(func.strip())
	except re.error as error:
		print(f"Error compiling regular expression for {option} function '{func.strip()}', {error}")
		sys.exit(2)


def _param_re(func: str, param: str, option: str) -> re.Pattern:
	try:
		return re.compile(param.strip())
	except re.error as error:
		print(f"Error compiling regular expression for {option} function '{func.strip()}' parameter '{param.strip()}', {error}")
		sys.exit(2)


class Checker:
	"""Base class for checkers."""

	name: ClassVar[str] = __package__.replace('_', '-')
	version: ClassVar[str] = package_version
	plugin_name: ClassVar[str]
	safelist: ClassVar[dict[re.Pattern, list[re.Pattern]]] = {}

	@classmethod
	def add_options(cls, option_manager: OptionManager) -> None:
		option_manager.add_option('--keyword-params-safelist', default=[], action='append',
		                          parse_from_config=True, dest='keyword_params_safelist',
		                          help="Functions and parameters that don't require keywords")
		option_manager.add_option('--keyword-params-exclude-safelist', default=[], action='append',
		                          parse_from_config=True, dest='keyword_params_exclude_safelist',
		                          help='Remove functions and parameters from safelist')

		option_manager.add_option('--keyword-params-include-name', default=False, action='store_true',
		                          parse_from_config=True, dest='keyword_params_include_name',
		                          help='Include plugin name in messages (enabled by default)')
		option_manager.add_option('--keyword-params-no-include-name', default=None, action='store_false',
		                          parse_from_config=False, dest='keyword_params_include_name',
		                          help='Remove plugin name from messages')

	@classmethod
	def parse_options(cls, options: Options) -> None:
		cls.plugin_name = (' (' + cls.name + ')') if (options.keyword_params_include_name) else ''

		for func, params in SAFELIST_FUNCTIONS.items():
			cls.safelist[re.compile(func)] = [re.compile(param) for param in params]

		safelist = options.keyword_params_safelist
		if (isinstance(safelist, str)):
			safelist = safelist.split()
		for entry in safelist:
			entry = entry.strip()
			if (':' in entry):
				func, param = entry.split(':', 1)
				func_re = _func_re(func, 'safelist')
				if (func_re not in cls.safelist):
					cls.safelist[func_re] = []
				cls.safelist[func_re].append(_param_re(func, param, 'safelist'))
			else:
				cls.safelist[_func_re(entry, 'safelist')] = [re.compile('.*')]

		exclude = options.keyword_params_exclude_safelist
		if (isinstance(exclude, str)):
			exclude = exclude.split()
		for entry in exclude:
			entry = entry.strip()
			if (':' in entry):
				func, param = entry.split(':', 1)
				func_re = _func_re(func, 'exclude-safelist')
				if (func_re not in cls.safelist):
					continue

				param_re = _param_re(func, param, 'exclude-safelist')
				if (param_re in cls.safelist[func_re]):
					cls.safelist[func_re].remove(param_re)

				if (not cls.safelist[func_re]):
					del cls.safelist[func_re]
			else:
				func_re = _func_re(entry, 'exclude-safelist')
				if (func_re not in cls.safelist):
					continue
				del cls.safelist[func_re]

	def _logical_token_message(self, token: tokenize.TokenInfo, message: Message, **kwargs) -> LogicalResult:
		return (token.start, f'{message.code}{self.plugin_name} {message.text(**kwargs)}')

	def _pyhsical_token_message(self, token: tokenize.TokenInfo, message: Message, **kwargs) -> PhysicalResult:
		return (token.start[1], f'{message.code}{self.plugin_name} {message.text(**kwargs)}')

	def _ast_token_message(self, token: tokenize.TokenInfo, message: Message, **kwargs) -> ASTResult:
		return (token.start[0], token.start[1], f'{message.code}{self.plugin_name} {message.text(**kwargs)}', type(self))

	def _ast_node_message(self, node: ast.AST, message: Message, **kwargs) -> ASTResult:
		return (node.lineno, node.col_offset, f'{message.code}{self.plugin_name} {message.text(**kwargs)}', type(self))


Violation = Tuple[ast.AST, Message, Dict[str, str]]


class ParamVisitor(ast.NodeVisitor):
	"""Param visitor."""

	violations: list[Violation]
	safelist: Mapping[re.Pattern, Sequence[re.Pattern]]

	def __init__(self, safelist: Mapping[re.Pattern, Sequence[re.Pattern]]) -> None:
		self.violations = []
		self.safelist = safelist

	def visit_FunctionDef(self, function: ast.FunctionDef) -> None:  # noqa: N802
		self.generic_visit(function)
		safe_params: list[re.Pattern] = []
		for func, params in self.safelist.items():
			if (func.match(function.name)):
				safe_params += params

		arguments = function.args
		defaults = arguments.defaults[-len(arguments.args):]
		if (defaults):
			for arg in arguments.args[-len(defaults):]:
				for safe_param in safe_params:
					if (safe_param.match(arg.arg)):
						break
				else:
					self.violations.append((arg, Message.NON_KEWORD_OPTIONAL, {'param': arg.arg}))

	def visit_AsyncFunctionDef(self, function: ast.AsyncFunctionDef) -> None:  # noqa: N802
		self.visit_FunctionDef(cast(ast.FunctionDef, function))


class ParamChecker(Checker):
	"""Parameter checker."""

	tree: ast.AST

	def __init__(self, tree: ast.AST) -> None:
		self.tree = tree

	def __iter__(self) -> Iterator[ASTResult]:
		"""Primary call from flake8, yield error messages."""
		param_visitor = ParamVisitor(self.safelist)
		param_visitor.visit(self.tree)

		for node, message, kwargs in param_visitor.violations:
			yield self._ast_node_message(node, message, **kwargs)
