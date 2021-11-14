from . import (
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


CALLABLE = Union(Method(), Function(), Class(is_init=False))
# lambda x: x**2

POINT = Union(int, float)
COORDS = [POINT, POINT]
# [0, 5.5]

PIXEL_VAL = Int(0, 255)
RGB = [PIXEL_VAL, PIXEL_VAL, PIXEL_VAL]
RGBA = [PIXEL_VAL, PIXEL_VAL, PIXEL_VAL, PIXEL_VAL]
PIXEL = Union(RGB, RGBA)
# [255, 255, 255]
# [0, 0, 0, 255]

INT_LIST = [int, ...]
# [1, 2, 3, 4]

STR_LIST = [str, ...]
# ["a", "b", "c", "d"]

IMAGE = [[PIXEL, ...], ...]
"""
[
	[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
	[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
	[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
]

3x3 image full of black pixels
"""

_BIN_ALLOWED = ['0', '1']
_OCT_ALLOWED = ['0', '1', '2', '3', '4', '5', '6', '7']
_HEX_ALLOWED = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

_SEQ = "all((int(i) in {}) for i in list(%s.replace('{}', '')))"


BIN = Str(_check=_SEQ.format(_BIN_ALLOWED, '0b'))
# "0b1010"

OCT = Str(_check=_SEQ.format(_OCT_ALLOWED, '0o'))
# "0o12"

HEX = Str(_check=_SEQ.format(_HEX_ALLOWED, '0x'))
# "0xa"


ASCII_CHARS = [chr(x) for x in range(128)]
ASCII = Str(_check=f"all((c in {ASCII_CHARS}) for c in list(%s))")
# "abc"

FILE_LIST = [File(), ...]
# ["file.py", "another_file.txt"]