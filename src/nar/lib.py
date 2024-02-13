import os
import re
import subprocess
from typing import Any, Sequence


class Pipeable:
    def __ror__(self, other):
        return self.operation(other)

    def operation(self, other) -> Any:
        ...


class ls(Pipeable):
    def operation(self, other) -> list[bytes] | list[str]:
        path = os.path.expanduser(other)
        return os.listdir(path)


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

    def operation(self, other):
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
    def operation(self, other):
        print(other)
        return other


class who(Pipeable):
    def operation(self, _):
        return os.getlogin()


class ps(Pipeable):
    def operation(self, _):
        result = subprocess.run(["ps", "aux"], capture_output=True).stdout
        return result.splitlines()


class cut(Pipeable):
    def __init__(self, f: int | Sequence[int], d=","):
        if not isinstance(f, int):
            assert len(f) == 2

        self.field = f
        self.delim = d

    def operation(self, other):
        split = other.split(self.delim)

        if isinstance(self.field, int):
            return split[self.field - 1]
        else:
            return split[self.field[0] - 1:self.field[1]]


class sed(Pipeable):
    def __init__(self, pattern, repl):
        self.pattern = pattern
        self.repl = repl

    def operation(self, other):
        if isinstance(other, list):
            result = []
            for line in other:
                result.append(re.sub(self.pattern, self.repl, line))
            return result
        elif isinstance(other, str):
            return re.sub(self.pattern, self.repl, other)


