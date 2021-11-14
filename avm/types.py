import os
import re

from . import errors, ext


# All of these Custom types examples (class.__doc__)
# are correct and wont raise any errors if you test them


class File(ext.CType):
	"""
	avm.File ~~~~~~~~~~~~~~~~~~~~~~~~~~

		file = "file.txt"

		typ = avm.File()
		typ.check(file)

		#	or :

		typ = avm.File(extension='.txt')
		typ.check(file)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(self, extension: str = ""):
		self.extension = extension


	def check(self, var, arg: str = 'file'):
		if not isinstance(var, str):
			self.error(arg)
		
		if not os.path.exists(var):
			raise FileNotFoundError(
				f"[Errno 2] No such file or directory: {var!r}")

		if not var.endswith(self.extension):
			raise errors.FileExtensionError(
				f'extension of file {var!r} is icorrect for arg {arg!r}')



class Class(ext.CType):
	"""
	avm.Class ~~~~~~~~~~~~~~~~~~~~~~~~~~

		Class something:
			def __init__(self):
				pass

		typ = avm.Class()
		typ.check(something)

		#	or :

		my_class = something()

		typ = avm.Class(is_init=True)
		typ.check(my_class)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		is_init: bool = False,
		regexp: str = r"<class '(([^\.]+\.)+[^\.]+)'>"
	):
		self.regexp = regexp
		self.is_init = is_init


	def check(self, var, arg: str = 'arg'):
		if self.is_init:
			var = type(var)
		if not re.fullmatch(self.regexp, str(var)):
			self.error(arg)



class Module(ext.CType):
	"""
	avm.Module ~~~~~~~~~~~~~~~~~~~~~~~~~~

		import math

		typ = avm.Module()
		typ.check(math)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def check(self, var, arg: str = 'arg'):
		if str(type(var)) != "<class 'module'>":
			self.error(arg)



class Function(ext.CType):
	"""
	avm.Function ~~~~~~~~~~~~~~~~~~~~~~~~~~

		def function():
			pass

		typ = avm.Function()
		typ.check(function)

		# also works with lambda functions.

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def check(self, var, arg: str = 'arg'):
		if str(type(var)) != "<class 'function'>":
			self.error(arg)



class Method(ext.CType):
	"""
	avm.Method ~~~~~~~~~~~~~~~~~~~~~~~~~~

		class test:
			def __init__(self): pass
			def method(self): pass

		t = test()

		typ = avm.Method()
		typ.check(t.method)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def check(self, var, arg: str = 'arg'):
		if str(type(var)) != "<class 'method'>":
			self.error(arg)



class Union(ext.CType):
	"""
	avm.Union ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = 0.1

		typ = avm.Union(int, float)
		typ.check(variable)

		# this is an equialent to typing.Union
		# but supports custom types

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		*types: (type, tuple)
	):
		self.types = types


	def check(self, var, arg: str = 'arg'):
		if not ext.tuple_check(self.types, var):
			self.error(arg)



class Int(ext.CType):
	"""
	avm.Int ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = 12

		typ = avm.Int(5, 25)
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		_min:	int = None,
		_max:	int = None,
		_check:	str = None
	):
		# check : "0 < %d < 10"
		if _min and not isinstance(_min, int):
			raise TypeError(
				'arg: _min must be int !')

		if _max and not isinstance(_max, int):
			raise TypeError(
				'arg: _max must be int !')

		if _check and not isinstance(_check, str):
			raise TypeError(
				'arg: check must be str !')

		self._min = _min
		self._max = _max
		self._check = _check


	def check(self, var, arg: str = 'arg'):
		try: int(var)
		except: self.error(arg)

		if self._min:
			if self._min > var:
				raise ValueError(
					f'arg: {arg} must be <= {self._min} !')

		if self._max:
			if self._max < var:
				raise ValueError(
					f'arg: {arg} must be >= {self._max} !')

		ext.exp_check(self._check, var, arg)



class Str(ext.CType):
	"""
	avm.Str ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = "abc"

		typ = avm.Str(length=3)
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		length:	(int, tuple) = -1,
		_check:	str = None
	):
		# length: (int, int) | int
		# check: "'a' in %s"
		if _check and not isinstance(_check, str):
			raise TypeError(
				'arg: check must be str !')

		self.length = length
		self._check = _check


	def check(self, var, arg: str = 'arg'):
		if not isinstance(var, str):
			self.error(arg)

		ext.length_check(var, self.length, arg)
		ext.exp_check(self._check, var, arg)



class Dict(ext.CType):
	"""
	avm.Dict ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = {"a": 0, "b": 1, "c": 2}

		typ = avm.Dict(str, int, length=(1, 3))
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		key_type:	(type, tuple) = None,
		value_type:	(type, tuple) = None,
		length: 	(int, tuple) = -1
	):
		self.key_type = key_type,
		self.value_type = value_type
		self.length = length


	def check(self, var, arg: str = 'arg'):
		if not isinstance(var, dict):
			self.error(arg)

		ext.length_check(var, self.length, arg)

		for key, value in var.items():
			if any([
				self.key_type and not ext.cisinstance(key, self.key_type),
				self.value_type and not ext.cisinstance(value, self.value_type)
			]):
				self.error(arg)