import os
import re
import subprocess
from typing import Any


class Pipeable:
    def __init__(self, value = None):
        self._value = value

    def __ror__(self, other):
        return self._operation(other)

    def operation(self, other) -> Any:
        ...

    def _operation(self, other):
        if isinstance(other, Pipeable):
            result = self.operation(other.value)
        else:
            result = self.operation(other)
        return result

    def __rrshift__(self, other):
        result = self._operation(other)
        return Pipeable(result)

    @property
    def value(self):
        return self._value


class ls(Pipeable):
    def operation(self, other) -> list[bytes] | list[str]:
        return os.listdir(other)


class cat(Pipeable):
    def __init__(self, strip: bool = False):
        super().__init__()
        self.strip = strip

    def operation(self, other) -> str:
        with open(other, "r") as f:
            contents = f.read()
            if self.strip:
                contents = contents.strip()
            return contents


class echo(Pipeable):
    def operation(self, other):
        print(other)
        return other


class who(Pipeable):
    def operation(self, other):
        return os.getlogin()


class ps(Pipeable):
    def operation(self, other):
        result = subprocess.run(["ps", "aux"], capture_output=True).stdout
        return result.splitlines()


class cut(Pipeable):
    def __init__(self, f: int | tuple[int, int], d=","):
        self.field = f
        self.delim = d

    def operation(self, other):
        split = other.split(self.delim)

        if isinstance(self.field, int):
            return split[self.field - 1]

        elif isinstance(self.field, tuple):
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


def _main():
    print(["this:that:other", "this"] | sed(r"(this|other)", r"shum"))


if __name__ == "__main__":
    _main()
