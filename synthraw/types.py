"""Additional types used by synthraw."""

from typing_extensions import Protocol


class SizedIterable(Protocol):
    """An iterable that supports len()."""
    def __len__(self):
        pass

    def __iter__(self):
        pass
