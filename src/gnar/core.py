from abc import abstractmethod
from typing import Any

class PipeableMeta(type):
    def __ror__(cls, other):
        instance = cls()
        return other | instance

    def __getitem__(cls, other):
        instance = cls()
        return other | instance


class Pipeable(metaclass=PipeableMeta):
    def __ror__(self, other):
        return self.run(other)

    @abstractmethod
    def run(self, other) -> Any:
        ...

    def _(self, other):
        return self.run(other)
