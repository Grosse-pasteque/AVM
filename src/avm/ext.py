import abc


def length_check(obj, length, arg):
	msg = f"arg: {arg} don't have the correct lenght: {str(length).replace('Ellipsis', '-1')} !"
	if isinstance(length, tuple):
		if any([
			length[0] not in [-1, ...] and len(obj) < length[0],
			length[1] not in [-1, ...] and len(obj) > length[1]
		]):
			raise ValueError(msg)
	else:
		if length not in [-1, ...] and len(obj) > length:
			raise ValueError(msg)


def str_of(of):
	attrs = ', '.join(
		"{}={!r}".format(attr, getattr(of, attr))
		for attr in dir(of)
		if all([
			not attr.startswith('_'),
			getattr(of, attr) and getattr(of, attr) != -1,
			str(type(getattr(of, attr))) not in ["<class 'function'>", "<class 'method'>"]
		])
	)

	try:
		bases = list(of.__class__.__bases__)
		if object in bases:
			bases.remove(object)
		bases = [b.__name__ for b in bases]
		bases = "<%s>" % ', '.join(bases)
	except:
		bases = ''

	return "<{}{}{}>".format(
		of.__class__.__name__,
		bases,
		(f" ({attrs})" if attrs != '' else '')
	).replace("<class '", '').replace("'>", '')


custom_types = []


def add_ctype(ctype):
	if CType not in ctype.__bases__:
		raise TypeError(
			f'Custom type {ctype} must inherit from {CType!r} !')
	custom_types.append(ctype)



class CType(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def check(self):
		raise NotImplementedError


	def error(self, arg):
		raise TypeError(
			f'arg: {arg!r} must be {self} !')


	def __str__(self):
		return str_of(self)



# Here to avoid circular import
from . import pattern


def tuple_check(_pattern, variable):
	check = []
	for typ in _pattern:
		try:
			# dont need to check if arg is str for File
			# because it will raise error
			res = pattern.Pattern(typ).check(variable)

			# res is True if CType is correct
			# if not raiseerror: res is False
			check.append(res) # check is good

			if res:
				# dont need to check others because one is correct
				break
		except:
			check.append(False) # Fails

	return True in check


def cisinstance(variable, types):
	if isinstance(types, tuple):
		if not tuple_check(types, variable):
			return False
	elif isinstance(types, tuple(custom_types)):
		try:
			types.check(variable)
		except:
			return False
	elif not isinstance(variable, types):
		return False
	return True


def is_type_tuple(var):
	if not isinstance(var, tuple):
		var = (var, )
	for t in var:
		if True not in [
			isinstance(t, tuple(custom_types)),
			isinstance(t, type)
		]:
			return False
	return True


def is_length(var):
	if True not in [isinstance(var, (int, tuple)), var == ...]:
		return False

	if isinstance(var, int) and -1 > var:
		return False

	if isinstance(var, tuple):
		if len(var) != 2:
			return False
		if False in [
			isinstance(var[0], (int, type(...))),
			isinstance(var[1], (int, type(...)))
		]:
			return False
		if any([
			var[0] != ... and -1 > var[1],
			var[1] != ... and -1 > var[0]
		]):
			return False
	return True


def exp_check(check, var, arg):
	if check == None:
		return

	exp = check.replace('%s', str(var))
	try:
		res = eval(exp)

	except:
		raise ValueError(
			f'expression: {exp!r} failled to execute !') from None

	if not res:
		raise ValueError(
			f"arg: {arg!r} doesn't respect check expression !")