from typing import TypeVar, Iterable, Iterator, Callable, Optional

###############################################################
# Iterator that allow the use of transformers using methods   #
# rather than functions                                       #
###############################################################


T = TypeVar("T")
R = TypeVar("R")

class ChainableIterator(Iterator[T]):
    def __init__(self, base: Iterator[T]):
        self.base = base

    def first(self) -> T:
        return next(self.base)

    def first_or_default(self, default: Optional[T] = None) -> Optional[T]:
        try:
            return next(self.base)
        except StopIteration:
            return default

    def filter(self, function: Callable[[T], bool]) -> "ChainableIterator[T]":
        iterator = filter(function, self.base)
        return ChainableIterator(iterator)

    def map(self, function: Callable[[T], R]) -> "ChainableIterator[R]":
        iterator = map(function, self.base)
        return ChainableIterator(iterator)

    def to_list(self):
        return list(self.base)

    # Warning: This consumes the iterator
    def count(self):
        return sum((1 for _ in self.base))

    def __next__(self) -> T:
        return next(self.base)


def citer(iterable: Iterable[T]) -> ChainableIterator[T]:
    return ChainableIterator(iter(iterable))
