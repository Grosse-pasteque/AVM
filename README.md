# Advanced Variable Manager: avm

## By Grosse pastèque#6705


-------------


### WARNING :

__**This modules need some typing modifications !**__
**If you try to run it without these modifications, an Error will occur.**

For more informations go **[Here](./avm/__init__.py)**


-------------


### Usage :

- Function's args type checking
- Function's args fast converting
- Pattern matching
- Variable checking
- More types


------------


### Installation :

This module is now disponible on PyPi since version 0.9.1
So you can do `python -m pip install python-avm` or `pip install python-avm`

Then you will be able to use it as a module.

```python
import avm

...
```


-------------


### Functionnalities :

##### Functions :

| Functions | Decorator | Usage |
| :------------: | :------------: | :------------: |
| type_check | `YES` | Check function's args types. |
| convertor | `YES` | Convert function's args values. |
| parameters | `NO` | Return all arguments of the passed function |
| str_of | `YES` | Return a string vizualisation of the given class |
| add_ctype | `YES` | Adds a custom type to `custom_types` |
| length_check | `YES` | Check the length `(int: max-lenght, int: max-lenght) | int: max-lenght` of and object |
| *custom_types* | `NO` | Variable that contains all the Custom Types |

##### Custom Types :

| CType | Has arguments | Usage |
| :------------:| :------------:| :------------: | 
| Function | `NO` | Function checking (*NB: lambda functions types is also function*) |
| Module | `NO` | Module checking |
| Class | `YES` | Class checking (`is_init=False`) |
| Union | `YES` | Value type in `*args` |
| File | `YES` | File checking (checks if file exists) |
| Dict | `YES` | Better dict checing |
| Int | `YES` | Better int checking |
| Str | `YES` | Better str checking |

##### Important Features :
| Function | Usage |
| :------------:| :------------:|
| Pattern | Check a variable for the given pattern (uses recursions) |
| CType | Used as parent for new custom types |

##### Errors :
| Error | Usage |
| :------------:| :------------:|
| FileExtensionError | When file doesn't exists |
| PatternError | When patterns is incorrect |


------------


### Examples :

I have created three examples to help you understand a bit more if you want.
In [Here](./examples/).