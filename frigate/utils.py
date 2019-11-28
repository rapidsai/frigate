import collections.abc


def flatten(l):
    """Flatten a list of nested lists with unknown depth.

    Iterate over nested lists and yield each item sequentially regardless
    of the nesting.

    Examples:
        Traversing the following YAML config would yield this list.

        >>> list(flatten([['a', 'b'], ['c', 'd'], ['e', 'f', ['g', 'h']]])
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    Args:
        l (list): Nested list of lists of lists of lists, etc.

    Yields:
        obj: Flattened list items.

    """
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(
            el, (str, bytes)
        ):
            yield from flatten(el)
        else:
            yield el
