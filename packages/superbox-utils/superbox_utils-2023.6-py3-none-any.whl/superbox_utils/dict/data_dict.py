from collections.abc import MutableMapping
from typing import Any
from typing import Iterator


class DataDict(MutableMapping):
    """A container object that works like a dict.

    Attributes
    ----------
    data: dict
        Store the data for this container object.
    """

    def __init__(self) -> None:
        self.data: dict = {}

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.data})"
