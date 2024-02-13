# gnar

Shred the gnar in Python by using (half) pipes!


Various shell builtins are implemented, allowing for piping commands together.

`gnar.Pipeable` can be implemented on an arbitrary class; this class only requires you to implement `Pipeable.run` that takes a single parameter.


## Examples

```
"/some/dir" | ls | cat | sed(r"this", r"that")
```

The above example replaces all occurrences of `this` with `that` for all files in `/some/dir`. Since `ls()` returns a list, `cat()` and `sed()` operate on each file in the list.

Notice that both `ls` and `cat` can be used with out parenthesis; this is due to their constructors not requiring any parameters. Functions like `sed`, and others that require constructor parameters, must be called with parenthesis.

```
>>> "one:two:three:four" | cut([2,3], ":")
['two', 'three']
```
