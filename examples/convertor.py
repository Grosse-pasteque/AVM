from avm import (
	convertor, type_check
)


# convertor function only gets passed the value to convert
# so dont if you want to be able to use more args use default args
def ignore_alpha(pixel):
	# RGBA -> RGB
	# [R, G, B, A] -> [R, G, B]
	return pixel[:3]


@type_check	# executed after @convertor
@convertor	# must convert before processing to variable check
def my_function(pixel: ignore_alpha, add: int = 0):
	r, g, b = pixel
	return [r + add, g + add, b + add]



pixel = my_function(
	[100, 100, 100, 255],
	add=50
)

print(pixel)
# >>> [150, 150, 150]