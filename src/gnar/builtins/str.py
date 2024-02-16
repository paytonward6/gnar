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
    """Wrapper around `str.strip`

    Usage:
        ```
        >>> "    contents      " | strip
        >>> "!!!!contents!!!!" | strip("!!")
        ```
    """
    def __init__(self, chars = None):
        self.chars = chars

    def run(self, other):
        return _dispatch(other, str.strip, args=(self.chars,))


class upper(Pipeable):
    """Wrapper around `str.upper`

    Usage:
        ```
        >>> "lowercase text" | upper
        ```
    """
    def run(self, other):
        return _dispatch(other, str.upper)


class lower(Pipeable):
    """Wrapper around `str.lower`

    Usage:
        ```
        >>> "UPPERCASE text" | lower
        ```
    """
    def run(self, other):
        return _dispatch(other, str.lower)


class replace(Pipeable):
    """Wrapper around `str.replace`

    Usage:
        ```
        >>> "Hello, world!" | replace("world", "mars")
        ```
    """
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def run(self, other):
        return _dispatch(other, str.replace, args=(self.old, self.new))


class rstrip(Pipeable):
    """Wrapper around `str.rstrip`

    Usage:
        ```
        >>> "      Hello, world!      " | rstrip
        >>> "Hello, world!!!!!!!!!!!" | rstrip("!")
        ```
    """
    def __init__(self, chars = None):
        self.chars = chars

    def run(self, other):
        return _dispatch(other, str.rstrip, args=(self.chars,))


class split(Pipeable):
    """Wrapper around `str.split`

    Usage:
        ```
        >>> "first:second:third" | split(":")
        ```
    """
    def __init__(self, sep=None, maxsplit=-1):
        self.sep = sep
        self.maxsplit =  maxsplit

    def run(self, other):
        return _dispatch(other, str.split, args=(self.sep, self.maxsplit))


class swapcase(Pipeable):
    """Wrapper around `str.swapcase`

    Usage:
        ```
        >>> "lower UPPER" | swapcase
        ```
    """
    def run(self, other):
        return _dispatch(other, str.swapcase)
