from . import errors, ext



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
	def __init__(self, pattern, raiseerror=True, containers=(list, tuple, set, dict)):
		self.pattern = pattern
		self._raiseerror = raiseerror
		self._containers = containers


	def _ret(self, value, arg):
		if self._raiseerror:
			raise errors.PatternError(
				f"arg: {arg!r} with value of {value!r} does not match Pattern: {self.pattern!r}")
		return False


	def is_infinite(self, val):
		# [type, int | (int, int)] | (type, int | (int, int))
		if isinstance(val, (list, tuple)) and (len(val) == 2):
			if isinstance(val[1], (int, tuple)):
				if isinstance(val[0], (tuple, type)) or isinstance(val[0], tuple(ext.custom_types)):
					return True
		return False


	def check(self, variable, arg: str = None):
		def _check(variable, pattern, arg, default_var):
			if isinstance(pattern, self._containers) and not self.is_infinite(pattern):
				if not isinstance(variable, type(pattern)):
					return self._ret(default_var, arg) 

				# prevent length error
				if len(pattern) != len(variable):
					return self._ret(default_var, arg) 
				
				if isinstance(pattern, dict):
					for key, key_type in zip(variable, pattern):
						value, value_type = variable[key], pattern[key_type]

						res = _check(key, key_type, arg, default_var)
						if not res:
							return self._ret(default_var, arg)

						res = _check(value, value_type, arg, default_var)
						if not res:
							return self._ret(default_var, arg)
				else:
					for i, var in enumerate(variable):
						if isinstance(pattern[i], self._containers) and not self.is_infinite(pattern[i]):
							if len(pattern[i]) != len(var):
								return self._ret(default_var, arg) 

						res = _check(var, pattern[i], arg, default_var)
						if not res:
							return self._ret(default_var, arg)

			elif self.is_infinite(pattern):
				ext.length_check(variable, pattern[1], arg)

				if not isinstance(variable, type(pattern)):
					return self._ret(default_var, arg) 

				for var in variable:
					if not ext.cisinstance(var, pattern[0]):
						return self._ret(default_var, arg)

			elif isinstance(pattern, tuple(ext.custom_types)):
				pattern.check(variable, arg)

			elif pattern == None:
				return True

			else:
				if not isinstance(variable, pattern):
					return self._ret(default_var, arg) 

			return True

		return _check(variable, self.pattern, arg, default_var=variable)