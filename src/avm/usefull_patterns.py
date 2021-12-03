from . import (
	Pattern,
	Function,
	Method,
	Module,
	Class,
	Union,
	File,
	Dict,
	Int,
	Str
)


Callable = Union(Method(), Function(), Class(is_init=False))
# lambda x: x**2

Point = Union(int, float)
Coords = [Point, Point]
# [0, 5.5]

PIXEL_VAL = Int(0, 255)
RGB = [PIXEL_VAL, 3]
RGBA = [PIXEL_VAL, 4]
Pixel = Union(RGB, RGBA)
# [255, 255, 255]
# [0, 0, 0, 255]

Image = [[Pixel, -1], -1]
"""
[
	[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
	[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
	[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
]

3x3 image full of black pixels
"""

Binnary = Str(startswith="0b", only="01", ignore={'prefix': True})
# "0b1010"

Octal = Str(startswith="0o", only="01234567", ignore={'prefix': True})
# "0o12"

Hexadecimal = Str(startswith="0x", only="0123456789abcdef", ignore={'prefix': True})
# "0xa"

Ascii = Str(only=[chr(x) for x in range(128)])
# "abc"

IntList = [int, -1]
# [1, 2, 3, 4]

StrList = [str, -1]
# ["a", "b", "c", "d"]

FileList = [File(), -1]
# ["file.py", "another_file.txt"]

FunctionList = [Function(), -1]
# [func, other_func, lambda x: x, ...]