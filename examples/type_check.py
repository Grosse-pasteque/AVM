from avm import (
	type_check,
	Union, File, Class, Str, Int, Dict
)


@type_check
def test_0(*args: int, **kwargs: Union(str, bytes)):
	"""
	*args:		only int
	**kwargs:	str or bytes
	"""
	pass


@type_check
def test_1(b: Union(int, str), a: str, c='he', d: str = 'a'):
	"""
	b:			int or str
	a:			only str
	c:			any (no specified type)
	d:			only str
	"""
	pass


@type_check
def test_2(file: File(extension='.py')):
	"""
	file:		any python file that exists
	"""
	pass


@type_check
def test_3(a: [int, str, int, [tuple]]):
	"""
	a:			only pattern of [int, str, int, [tuple]]
	"""
	pass


@type_check
def test_4(_class: Class()):
	"""
	_class:		only class
	"""
	pass


@type_check
def test_5(a: Int(0, 10), b: Str(length=3)):
	"""
	a:			only int in range(0, 10)
	b:			only str with length of 3
	"""
	pass


@type_check
def test_6(_dict: Dict(str, int, 10)):
	"""
	_dict:		only pattern of {str: None}
		- arg of type dict
		- with keys type str
		- with value type int
		- with max length of 10
	"""
	pass


@type_check
def test_7(l0: [int, (2, 10)], l1: (str, -1)):
	"""
	l0:			list of:
		- 2 <= length <= 10
		- only int
	l1:			tuple of:
		- infinite lenght
		- only str
	"""
	pass


@type_check
def test_8(*args: int):
	"""
	*args:		only int
	"""
	pass



class test: pass

test_0(2, 2, a='b', b='a', c=bytes('hey', 'utf-8'))	# good
test_1(1, 'hey')									# good
test_2('convertor.py')								# good
test_3([1, 'a', 2, [(1, 'anything here')]])			# good
test_4(test)										# good
test_5(3, 'acd')									# good
test_6({'a': 0, 'b': 1, 'c': 2})					# good
test_7([1, 2, 3, 4], ('a', 'b', 'c'))				# good
test_8(1, 2, 3, 'd')								# bad