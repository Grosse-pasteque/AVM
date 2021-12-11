import os

import inspect
from . import ext


# All of these Custom types examples (class.__doc__)
# are correct and wont raise any errors if you test them
def arguments_err(self):
	anno = self.__init__.__annotations__
	args = '\n   - '.join(
		f"{name}:  {an}"
		for name, an in anno.items()
	)
	return "Args of avm.types.{}.__init__ must be:\n   - {}".format(
		self.__class__.__name__,
		args.replace("<class '", '').replace("'>", ''))



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


	def check(self, var):
		if not isinstance(var, str):
			return False
		
		if not os.path.exists(var):
			return False
		return var.endswith(self.extension)



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


	def check(self, var):
		return ext.tuple_check(self.types, var)


	def __or__(self, other):
		self.types = (*self.types, other)



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
		subclass: tuple = None
	):
		if False in [
			isinstance(is_init, bool),
			not subclass or (isinstance(subclass, tuple) and \
				False not in [inspect.isclass(c) for c in subclass])
		]:
			raise TypeError(arguments_err(self))
		self.is_init = is_init
		self.subclass = subclass


	def check(self, var):
		if self.is_init:
			var = type(var)

		if not inspect.isclass(var):
			return False

		# self.subclass need to be either a class or tuple of class
		if self.subclass and not issubclass(var, self.subclass):
			return False
		return True



class Module(ext.CType):
	"""
	avm.Module ~~~~~~~~~~~~~~~~~~~~~~~~~~

		import math

		typ = avm.Module()
		typ.check(math)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def check(self, var):
		return inspect.ismodule(var)



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
	def check(self, var):
		return inspect.isfunction(var)



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
	def check(self, var):
		return inspect.ismethod(var)



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
		self.min = _min
		self.max = _max
		self.exp = exp


	def check(self, var):
		if not isinstance(var, int):
			return False

		if self.min and self.min > var:
			return False

		if self.max and self.max < var:
			return False
		return ext.exp_check(self.exp, var)



class Float(ext.CType):
	"""
	avm.Float ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = 3.141

		typ = avm.Float(3, 1.0, 4.0)
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		decimals:	int = None,
		_min:		float = None,
		_max:		float = None,
		exp:		str = None
	):
		if False in [
			decimals and isinstance(decimals, int) or not decimals,
			_min and isinstance(_min, float) or not _min,
			_max and isinstance(_max, float) or not _max,
			exp and isinstance(exp, str) or not exp
		]:
			raise TypeError(arguments_err(self))
		self.decimals = decimals
		self.min = _min
		self.max = _max
		self.exp = exp


	def check(self, var):
		if not isinstance(var, float):
			return False

		if self.min and self.min > var:
			return False

		if self.max and self.max < var:
			return False

		if len(str(var).split('.')[1]) > self.decimals:
			return False
		return ext.exp_check(self.exp, var)



class Str(ext.CType):
	"""
	avm.Str ~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


	def check(self, var):
		if not isinstance(var, str):
			return False

		if any([
			not var.startswith(self.startswith),
			not var.endswith(self.endswith)
		]):
			return False

		if self._ignore.setdefault('prefix', False):
			var = var[len(self.startswith):]
		if self._ignore.setdefault('suffix', False):
			var = var[:len(self.endswith)]

		for l in list(var):
			if (self.only and l not in self.only) or (self.exclude and l in self.exclude):
				return False

		if not ext.length_check(var, self.length):
			return False
		return ext.exp_check(self.exp, var)



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
			ext.is_type_tuple(key_type) or not key_type,
			ext.is_type_tuple(value_type) or not value_type,
			ext.is_length(length)
		]:
			raise TypeError(arguments_err(self))
		self.key_type = key_type,
		self.value_type = value_type
		self.length = length


	def check(self, var):
		if not isinstance(var, dict):
			return False

		if not ext.length_check(var, self.length):
			return False

		for key, value in var.items():
			if any([
				self.key_type and not ext.cisinstance(key, self.key_type),
				self.value_type and not ext.cisinstance(value, self.value_type)
			]):
				return False
		return True



class Generator(ext.CType):
	"""
	avm.Generator ~~~~~~~~~~~~~~~~~~~~~

		variable = (i for i in range(0, 20, 2))

		typ = avm.Generator()
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def check(self, var):
		return inspect.isgenerator(var)



class Length(ext.CType):
	"""
	avm.Length ~~~~~~~~~~~~~~~~~~~~~~~~

		variable = [1, 2, 3]

		typ = avm.Length(2, 10) # length between 2 and 10
		typ.check(variable)

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(
		self,
		*length:	(int, tuple),
		containers:	(type, tuple) = (list, tuple, set, dict, str, bytes, bytearray)
	):
		if False in [
			ext.is_length(length),
			ext.is_type_tuple(containers)
		]:
			raise TypeError(arguments_err(self))
		if len(length) == 1 and isinstance(length, tuple):
			length = length[0]
		self.length = length
		self.containers = containers


	def check(self, var):
		if not isinstance(var, self.containers):
			return False
		return ext.length_check(var, self.length)



class BRange(ext.CType):
	"""
	avm.BRange ~~~~~~~~~~~~~~~~~~~~~~~~

		# stands for Better Range

		a, b, c = 3, -1, 0.2

		range_1 = avm.BRange(10)
		range_1.check(a)
		a in range_1

		range_2 = avm.BRange(5, float('-inf'))
		range_2.check(b)
		b in range_2

		range_3 = avm.BRange(0, 10, 0.2)
		range_3.check(c)
		c in range_3

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(self, *args: int):
		if len(args) == 3:
			start, end, step = args
		elif len(args) == 2:
			start, end, step = *args, 1
		elif len(args) == 1:
			start, end, step = 0, *args, 1
		else:
			raise ValueError(
				'Invalid BRange !')

		VALID = (int, float)
		if not all([
			isinstance(start, VALID),
			isinstance(end, VALID),
			isinstance(step, VALID)
		]):
			raise TypeError(
				f"start, end, step must be float or int !")

		def count_decimal(n):
			if self.is_infinite(n):
				return 0
			dec = str(float(n)).split('.')[1]
			return (0 if dec == '0' else len(dec))

		self.decimal = max(
			count_decimal(start),
			count_decimal(end),
			count_decimal(step)
		)

		if any([
			self.is_infinite(start),
			self.is_infinite(step)
		]):
			raise ValueError(
				"start and step can't be infinite !")

		self.start = start
		self.end = end
		self.step = step

		self.range = None
		if not self.is_infinite(self.end):
			self.range = [
				x
				for x in self.generate()
			]


	def is_infinite(self, var):
		return var in [
			float('inf'),
			float('-inf')
		]


	def check(self, var: (int, float)):
		if not isinstance(var, (int, float)):
			return False

		if self.is_infinite(self.end):
			# infinite support
			if any([
				self.end == float('inf') and (
					not self.start <= var or \
					not ((var + self.start) / self.step).is_integer()
				),
				self.end == float('-inf') and (
					not self.start >= var or \
					not ((var + self.start) / self.step).is_integer()
				)
			]):
				return False
		return var in self.range


	def generate(self, last=False):
		if self.is_infinite(self.end):
			while True:
				yield self.start
				self.start += self.step
		while True:
			yield self.start
			self.start += self.step
			self.start = round(self.start, self.decimal)
			if any([
				last and self.start > self.end,
				not last and self.start >= self.end
			]):
				break


	def __iter__(self):
		if self.range:
			return iter(self.range)
		return iter([self.end])

	
	def __contains__(self, other):
		if self.is_infinite(self.end):
			return self.check(other)
		if self.range:
			return other in self.range
		return False