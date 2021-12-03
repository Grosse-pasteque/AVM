import traceback
import inspect
import typing

from . import types, pattern


def _reformat_args(args, base):
	real_args = [
		p.split(':')[0]
		for p in str(base)[1:-1].replace(' ', '').split(',')
	]

	for i, _ in enumerate(zip(real_args, list(args.keys()))):
		part, key = _
		name = part.split(':')[0].split('=')[0].replace(' ', '')
		
		if key == name.replace('*', ''):
			values = args[key]
			args.pop(key)
			args[name] = values

	return args


def _change_args(func, arguments):
	kwargs = {}

	line = traceback.extract_stack()[0].line
	# func(...)
	line = line.split(func.__name__)[1]
	# (...)
	line = line.split(';')[0][1:-1].replace(' ', '')
	# ...
	for name, value in list(arguments.items()):
		if name + '=' in line:
			kwargs[name] = value
			arguments.pop(name)
	args = tuple(arguments.values())
	return args, kwargs


def parameters(func, args, kwargs):
	types.Function().check(func)
	data = inspect.signature(func).bind(*args, **kwargs)
	arguments = _reformat_args(
		dict(data.arguments),
		data.signature)
	annotations = _reformat_args(
		typing.get_type_hints(func, change_opt=False),
		data.signature)
	return (arguments, annotations)


def convertor(func):
	logs = []
	def wrapper(*args, **kwargs):
		arguments, annotations = parameters(func, args, kwargs)

		for name, conv in annotations.items():
			try:
				types.Function().check(conv)
				try:
					new_value = conv(arguments[name])
					values = {
						'old': arguments[name],
						'new': new_value
					}
					logs.append(
						f"SUCCESS: convertor {conv!r} succeeded for arg {name!r} with {values}")
					arguments[name] = new_value
				except:
					logs.append(
						f"FATAL: convertor {conv!r} failled for arg {name!r}")
					continue

			except TypeError:
				logs.append(
					f"INFO: no convertor for arg {name!r}")
				continue

		nargs, nkwargs = _change_args(func, arguments)
		return func(*nargs, **nkwargs)

	wrapper.__logs__ = logs
	wrapper.__name__ = func.__name__
	return wrapper


def type_check(output=False, private=False):
	# checks output type (if True)
	# checks private attributes type ("_attr" or "__attr__") (if True)
	def inner(func):
		if inspect.isclass(func):
			for name in dir(func):
				attr = getattr(func, name)
				if inspect.isfunction(attr):
					new = type_check(output=output, private=private)(attr)
					setattr(func, name, new)

		def wrapper(*args, **kwargs):
			arguments, annotations = parameters(func, args, kwargs)

			for name, value in arguments.items():
				if private == False and name.startswith('_'):
					continue

				if name in annotations:
					if name.startswith('*'):
						if isinstance(annotations[name], dict) or name.startswith('**'):
							value = tuple(value.values())

						for arg in value:
							if isinstance(annotations[name], pattern.Pattern):
								p = annotations[name]
							else:
								p = pattern.Pattern(annotations[name])
							valid = p.check(arg, name)

					else:
						if isinstance(annotations[name], pattern.Pattern):
							p = annotations[name]
						else:
							p = pattern.Pattern(annotations[name])
						valid = p.check(value, name)

					if not valid:
						raise TypeError(
							f"{func.__name__} arg: {name!r} must be {p} , not {type(value)} !")

			returned = func(*args, **kwargs)

			if "return" in annotations and output == True:
				err = f"func: {func.__name__} returned: {type(returned)}, "\
					f"instead of: {annotations['return']}"

				if isinstance(annotations[name], pattern.Pattern):
					p = annotations['return']
				else:
					p = pattern.Pattern(annotations['return'])
				try:
					valid = p.check(returned, 'return')
				except:
					valid = False
				if not valid:
					raise ValueError(err)
			return returned

		wrapper.__name__ = func.__name__
		return wrapper

	if inspect.isfunction(output):
		return inner(output)

	return inner


def make_class(method, private=False):
	if not inspect.isfunction(method):
		raise TypeError(
			'arg: method must be a function !')

	def inner(cls):
		if not inspect.isclass(cls):
			return cls

		for name in dir(cls):
			if not private and name.startswith('_'):
				continue

			attr = getattr(cls, name)
			if inspect.isclass(attr):
				make_class(method)(attr)

			if inspect.isfunction(attr):
				setattr(cls, name, method(attr))
		return cls
	return inner