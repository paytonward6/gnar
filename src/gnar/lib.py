import os
import re
import shutil
import subprocess
from typing import Sequence

from .core import Pipeable


class ls(Pipeable):
    def run(self, other) -> list[bytes] | list[str]:
        path = os.path.expanduser(other)
        return os.listdir(path)


class cd(Pipeable):
    def run(self, other):
        current = os.getcwd()
        path = os.path.expanduser(other)
        os.chdir(path)
        return current


class pwd(Pipeable):
    def run(self, _):
        return os.getcwd()


class cat(Pipeable):
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
    def run(self, other):
        print(other)
        return other


class tee(Pipeable):
    def __init__(self, filename):
        self.filename = filename

    def run(self, other):
        with open(self.filename, "w") as f:
            if isinstance(other, list) or isinstance(other, tuple):
                f.writelines(map(lambda s: f"{s}\n", other))
            else:
                f.write(str(other))
        print(other)
        return other


class who(Pipeable):
    def run(self, _):
        return os.getlogin()


class ps(Pipeable):
    def run(self, _):
        result = subprocess.run(["ps", "aux"], capture_output=True).stdout
        return result.splitlines()


class cut(Pipeable):
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
    def __init__(self, pattern, repl, file=False, in_place=False):
        self.pattern = pattern
        self.repl = repl

    def run(self, other):
        if isinstance(other, list):
            result = []
            for line in other:
                result.append(re.sub(self.pattern, self.repl, line))
            return result
        elif isinstance(other, str):
            return re.sub(self.pattern, self.repl, other)


class shell(Pipeable):
    def run(self, other):
        return subprocess.run(other, capture_output=True)


class cp(Pipeable):
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


