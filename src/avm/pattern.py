from . import ext



class Pattern(ext.CType):
	"""
	avm.Pattern ~~~~~~~~~~~~~~~~~~~~~~~~~~

		variable = [1, 2, 3]

		typ = avm.Pattern([int, int, int])
		typ.check(file)

		# You are not forced to directly
		# use a pattern in you function
		# arguments types, because every
		# types annotations will be converted
		# to pattern.

	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	"""
	def __init__(self, pattern, containers=(list, tuple, set, dict)):
		self.pattern = pattern
		self._containers = containers


	def is_infinite(self, val):
		# [type, int | (int, int)] | (type, int | (int, int))
		if isinstance(val, (list, tuple)) and (len(val) == 2):
			if isinstance(val[1], (type(...), int, tuple)):
				if isinstance(val[0], (tuple, type)) or isinstance(val[0], tuple(ext.custom_types)):
					return True
		return False


	def check(self, variable):
		def _check(variable, pattern):
			if isinstance(pattern, self._containers) and not self.is_infinite(pattern):
				if not isinstance(variable, type(pattern)):
					return False 

				# prevent length error
				if len(pattern) != len(variable):
					return False 
				
				if isinstance(pattern, dict):
					for key, key_type in zip(variable, pattern):
						value, value_type = variable[key], pattern[key_type]

						res = _check(key, key_type)
						if not res:
							return False

						res = _check(value, value_type)
						if not res:
							return False
				else:
					for i, var in enumerate(variable):
						if isinstance(pattern[i], self._containers) and not self.is_infinite(pattern[i]):
							if len(pattern[i]) != len(var):
								return False 

						res = _check(var, pattern[i])
						if not res:
							return False

			elif self.is_infinite(pattern):
				ext.length_check(variable, pattern[1])

				if not isinstance(variable, type(pattern)):
					return False 

				for var in variable:
					if not ext.cisinstance(var, pattern[0]):
						return False

			elif isinstance(pattern, tuple(ext.custom_types)):
				return pattern.check(variable)

			elif pattern == None:
				return True

			else:
				if not isinstance(variable, pattern):
					return False 
			return True

		return _check(variable, self.pattern)