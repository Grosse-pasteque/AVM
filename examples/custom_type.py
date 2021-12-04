from avm import (
	type_check, add_ctype,
	CType
)



class MyCustomType(CType):
	"""
		[ Custom Type ] :
	- must be str
	- must include self.letter
		= Str(only=letter), (but it's only an example)
	"""
	def __init__(self, letter: str):
		self.letter = letter


	def check(self, var, arg: str = 'arg'):
		if not isinstance(var, str):
			raise TypeError(
				f'arg: {arg!r} with value {var!r} must be {str} !')

		if self.letter not in var:
			raise ValueError(
				f'{self.letter!r} must be in {arg} !')



add_ctype(MyCustomType)


@type_check
def test(text: MyCustomType('a')):
	return


test('abc')
test('efg') # ValueError