from .main import (
	type_check,
	convertor,
	parameters
)

from .errors import (
	PatternError,
	FileExtensionError
)

from .pattern import Pattern

from .types import (
	Function,
	Method,
	Module,
	Class,
	Union,
	File,
	Dict,
	Int,
	Str
)

from .ext import (
	CType,
	custom_types,
	add_ctype,
	str_of,
	length_check
)

custom_types += [
	Function,
	Pattern,
	Method,
	Module,
	Class,
	Union,
	File,
	Dict,
	Int,
	Str
]


def check():
	r"""
	must be changed to be able to use this module

	In typing module ~~~~~~~~~~~~~~~~~~
		from inspect import getfile
		import typing
		print(getfile(typing))
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	[ replace ]:
	-	"def get_type_hints(obj, globalns=None, localns=None, include_extras=False):"
	-	"        if name in defaults and defaults[name] is None:"

	[ by ]:
	-	"def get_type_hints(obj, globalns=None, localns=None, include_extras=False, change_opt=True):"
	-	"        if name in defaults and defaults[name] is None and change_opt:"

	this will just make a functionnality optionnal
	all the other programs will work the same way dont worry
	"""
	from inspect import getfile
	import typing

	INVALID_LINES = [
		"def get_type_hints(obj, globalns=None, localns=None, include_extras=False):",
		"        if name in defaults and defaults[name] is None:"
	]

	class ModuleCheckError(Exception):
		pass

	path = getfile(typing)
	try:
		lines = open(path, 'r', encoding='utf-8')\
			.read()\
			.split('\n')
	except (PermissionError, FileNotFoundError):
		raise ModuleCheckError(
			f"module typing with path {path!r} cannot be checked !")

	for line in lines:
		if line in INVALID_LINES:
			raise ModuleCheckError(
				f"module typing with path {path} has some invalid"
				f" lines check this file for more information:\n\t{__file__}")


check()
del check


__all__ = (
	'type_check',
	'convertor',
	'parameters',
	
	'Function',
	'Module',
	'Class',
	'Union',
	'File',
	'Dict',
	'Int',
	'Str',
	
	'Pattern',

	'CType',
	
	'str_of', 'add_ctype', 'length_check',

	'custom_types',
	
	'FileExtensionError',
	'PatternError'
)

__version__ = '0.8.0'
__author__ = (
	'Grosse pastèque#6705',
	'https://github.com/Grosse-pasteque',
	'Big watermelon'
)