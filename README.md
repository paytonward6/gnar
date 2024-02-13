# nar

Blend of shell and Python via a lib.


Various shell builtins are implemented, allowing for piping commands together.

`nar.Pipeable` can be implemented on an arbitrary class; this ABC only requires you to implement `Pipeable.run` that takes a single parameter.


## Examples

```
"/some/dir" | ls() | cat() | sed(r"this", r"that")
```

The above example replaces all occurrences of `this` with `that` for all files in `/some/dir`. Since `ls()` returns a list, `cat()` and `sed()` operate on each file in the list.

```
>>> "one:two:three:four" | cut([2,3], ":")
['two', 'three']
```
