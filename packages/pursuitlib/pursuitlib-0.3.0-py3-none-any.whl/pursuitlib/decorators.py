# This decorator can be used to easily create decorators that
# can optionally take arguments
def decorator(function):
    def wrapper(*args, **kwargs):
        # If the decorator is used without parenthesis, the first argument
        # is the function that needs to be passed to "decorator"
        if len(args) == 1 and callable(args[0]) and len(kwargs) == 0:
            fn = args[0]
            return function(fn)
        else: return lambda f: function(f, *args, **kwargs)
    return wrapper


# This decorator can be used to cache the result of a method
def cached(function):
    def wrapper(self, *args, force_update: bool = False, **kwargs):
        cached_field = f"__cached_{function.__name__}"

        # Use the cached value when available
        if not force_update and hasattr(self, cached_field):
            return getattr(self, cached_field)

        result = function(self, *args, **kwargs)
        setattr(self, cached_field, result)  # Update the cache
        return result
    return wrapper
