import collections.abc
import os

from frigate import TEMPLATES_PATH


def flatten(nested_list):
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
    for element in nested_list:
        if isinstance(element, collections.abc.Iterable) and not isinstance(
            element, (str, bytes)
        ):
            yield from flatten(element)
        else:
            yield element


def list_templates():
    templates = []
    for template in os.listdir(TEMPLATES_PATH):
        [template, _] = template.split(".")
        templates.append(template)
    return templates
