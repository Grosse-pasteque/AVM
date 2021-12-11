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
		return all([
			isinstance(var, str),
			self.letter in var
		])



add_ctype(MyCustomType)


@type_check
def test(text: MyCustomType('a')):
	return


test('abc')
test('efg') # ValueError