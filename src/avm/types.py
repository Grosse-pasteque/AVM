import os

import inspect
from . import errors, ext


# All of these Custom types examples (class.__doc__)
# are correct and wont raise any errors if you test them
arguments_err = lambda self: f'invalid arguments found see arguments types for {self}.'



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
		if not isinstance(extension, str):
			raise TypeError(arguments_err(self))
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
		# dont really needs type checking because we directly
		# convert to pattern with ext.tuple_check()

		# if not ext.is_type_tuple(types):
			# raise TypeError(arguments_err(self))
		self.types = types


	def check(self, var, arg: str = 'arg'):
		if not ext.tuple_check(self.types, var):
			self.error(arg)



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
		*,
		subclass: tuple = (object,)
	):
		if False in [
			isinstance(is_init, bool),
			isinstance(subclass, tuple) and \
				False not in [inspect.isclass(c) for c in subclass]
		]:
			raise TypeError(arguments_err(self))
		self.is_init = is_init
		self.subclass = subclass


	def check(self, var, arg: str = 'arg'):
		if self.is_init:
			var = type(var)
		if not inspect.isclass(var):
			self.error(arg)
		# self.subclass need to be either a class or tuple of class
		if not issubclass(var, self.subclass):
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
		if not inspect.ismodule(var): self.error(arg)



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
		if not inspect.isfunction(var): self.error(arg)



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
		if inspect.ismethod(var): self.error(arg)



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
		exp:	str = None
	):
		# check : "0 < %d < 10"
		if False in [
			_min and isinstance(_min, int) or not _min,
			_max and isinstance(_max, int) or not _max,
			exp and isinstance(exp, str) or not exp
		]:
			raise TypeError(arguments_err(self))
		self._min = _min
		self._max = _max
		self.exp = exp


	def check(self, var, arg: str = 'arg'):
		try:
			int(var) # checks if var is int
		except:
			self.error(arg)
		if self._min and self._min > var:
			raise ValueError(
				f'arg: {arg} must be <= {self._min} !')
		if self._max and self._max < var:
			raise ValueError(
				f'arg: {arg} must be >= {self._max} !')
		ext.exp_check(self.exp, var, arg)



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
		only:		(str, list) = [],
		exclude:	(str, list) = [],
		startswith:	str = "",
		endswith:	str = "",
		length:		(int, tuple) = -1,
		exp:		str = None,
		ignore:		dict = {"prefix": False, "suffix": False}
	):
		# length: (int, int) | int
		# check: "'a' in %s"
		if False in [
			ext.is_length(length),
			exp and isinstance(exp, str) or not exp,
			isinstance(only, (str, list)),
			isinstance(exclude, (str, list)),
			isinstance(startswith, str),
			isinstance(endswith, str),
			isinstance(ignore, dict)
		]:
			raise TypeError(arguments_err(self))
		self.only = list(only)
		self.exclude = list(exclude)
		self.startswith = startswith
		self.endswith = endswith
		self.length = length
		self.exp = exp
		self._ignore = ignore


	def check(self, var, arg: str = 'arg'):
		if not isinstance(var, str):
			self.error(arg)

		if any([
			not var.startswith(self.startswith),
			not var.endswith(self.endswith)
		]):
			self.error(arg)

		if self._ignore.setdefault('prefix', False):
			var = var[len(self.startswith):]
		if self._ignore.setdefault('suffix', False):
			var = var[:len(self.endswith)]

		for l in list(var):
			if l not in self.only or l in self.exclude:
				self.error(arg)

		ext.length_check(var, self.length, arg)
		ext.exp_check(self.exp, var, arg)



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
		if False in [
			ext.is_type_tuple(key_type),
			ext.is_type_tuple(value_type),
			ext.is_length(length)
		]:
			raise TypeError(arguments_err(self))
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



class Generator(ext.CType):
	"""
	avm.Generator ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = (i for i in range(0, 20, 2))

		typ = avm.Generator()
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def check(self, var, arg: str = 'arg'):
		if not inspect.isgenerator(var):
			self.error(arg)