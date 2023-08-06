#  __    _  __   __  __   __  _______  ______    ___   __    _  _______ 
# |  |  | ||  | |  ||  |_|  ||       ||    _ |  |   | |  |  | ||       |
# |   |_| ||  | |  ||       ||    ___||   | ||  |   | |   |_| ||    ___|
# |       ||  |_|  ||       ||   |___ |   |_||_ |   | |       ||   | __ 
# |  _    ||       ||       ||    ___||    __  ||   | |  _    ||   ||  |
# | | |   ||       || ||_|| ||   |___ |   |  | ||   | | | |   ||   |_| |
# |_|  |__||_______||_|   |_||_______||___|  |_||___| |_|  |__||_______|
# 

import requests

"""
# Numering
### Yet another number package.


+ ## random_float
    - random float number in range of A and B
  
+ ## random_element
    - random element from list

+ ## sizeof
    - size of an element

## Examples

### Generating random float number
```py
import numering

a, b = 1, 2

print(numering.random_float(a, b), decimals=3)

# 1.736
```

### Selecting random element from list
```py
import numering

my_list = [1, 2, 3, 4, 5]

print(numering.random_element(my_list))

# 3
```

### Getting size of element (list, tuple, dict)
```py
import numering

my_list = [1, 2, 3, 4, 5]

print(numering.sizeof(mylist))

# 4
```"""

import time, typing

__version__ = "0.9"

_all_ = [
    "random_float",
    "random_element",
    "sizeof",
    "e",
    "e.rand_from_time",
    "_in_seed"
]

_in_seed = 1.03141592563

class e:
    def rand_from_time(seed: float=_in_seed):
      return (time.time() * 10000000 % seed)
    
def random_float(a: float, b: float, **options):
    r"""Generates random float number

    :param a: start
    :param b: end
    :param options: \*\*kwargs arguments for return
    
    :return: :float:`float`"""

    return format(a + (b - a) * e.rand_from_time(), '.'+str(options.pop('decimals', '16'))+'f')

def random_element(list: list):
    r"""Returns random element from list
    
    :param list: `list` with elements
    
    :return: random element from list"""

    index = int(str(e.rand_from_time(_in_seed)-int(e.rand_from_time(_in_seed)))[2:]) % len(list)
    return list[int(format(index, '.0f'))]

def sizeof(l_element: typing.Any):
    return sum(1 for _ in l_element)