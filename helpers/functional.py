from functools import reduce

def compose(*functions):
    def compose2(f1, f2):
        """Compose two functions"""
        return lambda *args: f1(f2(*args))
    return reduce(compose2, functions)

def curry2(func):
    """Curry function with two arguments"""
    return lambda x : lambda y: func(x,y)

def curry3(func):
    """Curry function with three arguments"""
    return lambda x: lambda y: lambda z : func(x, y, z)

curried_map = curry2(map)
curried_filter = curry2(filter)
curried_zip = curry2(zip)
