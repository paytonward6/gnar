import os
import re
import shutil
import subprocess
from typing import Sequence

from .core import IgnorablePipeable, Pipeable


class ls(Pipeable):
    """List the contents of a directory

    Usage:
        ```
        >>> "/path/to/dir" | ls
        >>> # or
        >>> ls["path/to/dir"]
        ```
    """
    def run(self, other) -> list[bytes] | list[str]:
        path = os.path.expanduser(other)
        return os.listdir(path)


class cd(Pipeable):
    """Change current working directory

    Usage:
        ```
        >>> "/path/to/dir" | cd
        >>> # or
        >>> cd["path/to/dir"]
        ```
    """
    def run(self, other):
        current = os.getcwd()
        path = os.path.expanduser(other)
        os.chdir(path)
        return current


class pwd(Pipeable):
    """Get current working directory

    Usage:
        ```
        >>> "ignores input" | pwd
        >>> # or
        >>> pwd["ignores input"]
        ```
    """
    def run(self, _):
        return os.getcwd()


class cat(Pipeable):
    """Print the file, or list of files

    If the input is a filename, the output will be a string.
    If the input is a list of filenames, the output will be a list of strings

    Usage:
        ```
        >>> "/path/to/file" | cat
        >>> # or
        >>> "/path/to/file" | cat(strip=True)
        >>> # or
        >>>  ["/path/to/file1", "/path/to/file2"] | cat(strip=True)
        >>> # or
        >>>  cat["/path/to/file"]
        ```

    """
    def __init__(self, strip: bool = False):
        self.strip = strip

    def _read_file(self, filename: str) -> str:
        path = os.path.expanduser(filename)
        with open(path, "r") as f:
            contents = f.read()
            if self.strip:
                contents = contents.strip()
            return contents

    def run(self, other):
        if isinstance(other, str):
            return self._read_file(other)
        elif isinstance(other, list):
            results = []
            for filename in other:
                if os.path.isdir(filename):
                    continue
                contents = self._read_file(filename)
                results.append(contents)
            return results


class echo(Pipeable):
    """Print and return an object

    Usage:
        ```
        >>> "Hello, world!" | echo
        >>> # or
        >>> echo["Hello, world!"]
        ```
    """
    def run(self, other):
        print(other)
        return other


class tee(Pipeable):
    """Print and return an object
    Will overwrite files by default!

    Usage:
        ```
        >>> "Hello, world!" | tee("file.txt")
        ```
    """
    def __init__(self, filename, mode: str = "w"):
        self.filename = filename
        self.mode = mode

    def run(self, other):
        with open(self.filename, self.mode) as f:
            if isinstance(other, list) or isinstance(other, tuple):
                f.writelines(map(lambda s: f"{s}\n", other))
            else:
                f.write(str(other))
        print(other)
        return other


class who(IgnorablePipeable):
    """Get the current user

    Usage:
        ```
        >>> "ignores input" | who
        >>> # or
        >>> who[""]
        ```
    """
    def run(self, _ = None):
        return os.getlogin()


class ps(IgnorablePipeable):
    """Get the full process list

    Usage:
        ```
        >>> "" | ps
        >>> # or
        >>> ps[""]
        >>> ps()._
        ```
    """
    def run(self, _ = None):
        result = subprocess.run(["ps", "aux"], capture_output=True).stdout
        return result.splitlines()


class cut(Pipeable):
    """Select an element(s) from a string, split by a delimiter

    Usage:
        ```
        >>> "first:second:third" | cut(1, ":")
        'first'
        >>> "first:second:third" | cut([1, 2], ":")
        ['first', 'second']
        ```
    """

    def __init__(self, f: int | Sequence[int], d=","):
        if not isinstance(f, int):
            assert len(f) == 2

        self.field = f
        self.delim = d

    def run(self, other):
        split = other.split(self.delim)

        if isinstance(self.field, int):
            return split[self.field - 1]
        else:
            return split[self.field[0] - 1:self.field[1]]


class sed(Pipeable):
    """Replace `pattern` with `repl` in a file, str, list[str], list[file]

    Usage:
        ```
        >>> "Hello, Earth!" | sed(r"Earth", "Mars")
        >>> ["Hello, Earth!", "Earth is red"] | sed(r"Earth", "Mars")

        ```
    """
    def __init__(self, pattern, repl, file=False, in_place=False):
        self.pattern = pattern
        self.repl = repl
        self.file = file
        self.in_place = in_place

    def run(self, other):
        if isinstance(other, list):
            result = []
            for line in other:
                result.append(re.sub(self.pattern, self.repl, line))
            return result
        elif isinstance(other, str):
            return re.sub(self.pattern, self.repl, other)


class shell(Pipeable):
    """Run a command in a subprocess.

    Returns:
        CompleteProcess[bytes]

    Usage:
        ```
        >>> "ls" | shell
        >>> # to get stdout do:
        >>> ("ls" | shell).stdout.decode()
        ```
    """

    def run(self, other):
        return subprocess.run(other, capture_output=True)


class cp(Pipeable):
    """Copy src to dst given a pair of filenames, or list of pairs of filenames

    Usage:
        ```
        >>> ["src_file.txt", "dst_file.txt"] | cp
        >>> [["src_file1.txt", "dst_file1.txt"], ["src_file2.txt", "dst_file2.txt"]] | cp
        ```
    """
    def __init__(self, recursive=False):
        self.recursive = recursive

    def run(self, other):
        if not (isinstance(other, list) or isinstance(other, tuple)):
            raise ValueError("cp must be passed a list[str] or list[list[str]]")

        if isinstance(other[0], list) or isinstance(other[0], tuple):
            for pair in other:
                src, dst = pair
                shutil.copy(src, dst)
        else:
            src, dst = other
            shutil.copy(src, dst)


class mv(Pipeable):
    """Move src to dst given a pair of filenames of list of pairs of filenames

    Usage:
        ```
        >>> ["src_file.txt", "dst_file.txt"] | mv
        >>> [["src_file1.txt", "dst_file1.txt"], ["src_file2.txt", "dst_file2.txt"]] | mv
        ```
    """
    def __init__(self, recursive=False):
        self.recursive = recursive

    def run(self, other):
        if not (isinstance(other, list) or isinstance(other, tuple)):
            raise ValueError("mv must be passed a list[str] or list[list[str]]")

        if isinstance(other[0], list) or isinstance(other[0], tuple):
            for pair in other:
                src, dst = pair
                shutil.move(src, dst)
        else:
            src, dst = other
            shutil.move(src, dst)


