
# Installation

Install via:
```python
python3 -m pip install gnar
```

Test installation:
```
$ python3
>>> from gnar import *
>>> "." | ls
["present", "working", "directory", "contents"]
```

## Usage

As seen previously, the contents of a directory can be output as a list with the `ls` command (implemented as a class with function overloading for the `|` operator).

Alternatively, commands that don't require initialization parameters can be called similar to `ls["."]`. This means that a command such as `cut` cannot be used with the bracket notation since it requires a field(s) to select and an optional delimiter. So, the following will work:
```
>>> "first:second" | cut(1, ":")
'first'
```

but this will _not_ since cut will not have enough information to perform its duty:
```
>>> cut["first:second"]
...
TypeError: cut.__init__() missing 1 required positional argument: 'f'
```

The basis of `gnar` is to mimic the shell in terms of its usage of pipes. There are two simple rules to follow for `gnar`:

