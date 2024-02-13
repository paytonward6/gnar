from gnar.core import Pipeable


def _dispatch(other, fn, args = None):
    if isinstance(other, str):
        if args:
            return fn(other, *args)
        else:
            return fn(other)
    elif isinstance(other, list):
        result = []
        for string in other:
            if args:
                to_append = fn(string, *args)
            else:
                to_append = fn(string)
            result.append(to_append)
        return result


class strip(Pipeable):
    def run(self, other):
        return _dispatch(other, str.strip)


class upper(Pipeable):
    def run(self, other):
        return _dispatch(other, str.upper)


class lower(Pipeable):
    def run(self, other):
        return _dispatch(other, str.lower)


class replace(Pipeable):
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def run(self, other):
        return _dispatch(other, str.replace, args=(self.old, self.new))


class rstrip(Pipeable):
    def __init__(self, chars):
        self.chars = chars

    def run(self, other):
        return _dispatch(other, str.replace, args=(self.chars))


class split(Pipeable):
    def __init__(self, sep=None, maxsplit=-1):
        self.sep = sep
        self.maxsplit =  maxsplit

    def run(self, other):
        return _dispatch(other, str.split, args=(self.sep, self.maxsplit))


class swapcase(Pipeable):
    def run(self, other):
        return _dispatch(other, str.swapcase)
