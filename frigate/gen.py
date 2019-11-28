from collections import OrderedDict
import itertools
import os.path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from frigate.utils import flatten

yaml = YAML()


def load_chart(chartdir):
    """Load the yaml information from a helm chart directory.

    Load in the `Chart.yaml` and `values.yaml` files from a helm
    chart.

    Args:
        chartdir (str): Path to the helm chart.

    Returns:
        chart (dict): Contents of `Chart.yaml` loaded into a dict.
        values (dict): Contents of `values.yaml` loaded into a dict.

    """
    with open(os.path.join(chartdir, "values.yaml"), "r") as fh:
        values = yaml.load(fh.read())
    with open(os.path.join(chartdir, "Chart.yaml"), "r") as fh:
        chart = yaml.load(fh.read())
    return chart, values


def get_comment(tree, key):
    """Extract the in-line comment from a ruamel.yaml.comments.Comment list.

    When ruamel.yaml parses a YAML file it also extracts a ruamel.yaml.comments.Comment
    object for each item. This is a list of CommentToken objects which represent comments
    adjacent to the item.

    This function attempts to extract the comment which is on the same line as the item.

    Examples:
        Extract a comment

        >>> from ruamel.yaml import YAML
        >>> yaml = YAML()
        >>> tree = yaml.load("hello: world  # this is the comment")
        >>> get_comment(tree, "hello")
        "This is the comment"

    Args:
        comments (list): List of CommentToken objects (potentially nested)

    Returns:
        str: Comment

    """
    comments = tree.ca.items[key]
    linecol = tree.lc.data[key]
    for comment in flatten(comments):
        if comment is not None and comment.start_mark.line == linecol[0]:
            first_line = comment.value.strip().split("\n")[0]
            return clean_comment(first_line)
    return ""


def clean_comment(comment):
    return comment.strip("# ").capitalize()


def traverse(tree, root=None):
    if root is None:
        root = []
    for key in tree:
        default = tree[key]
        if isinstance(default, dict) and default != {}:
            newroot = root + [key]
            for value in traverse(default, root=newroot):
                yield value
        else:
            if isinstance(default, list):
                default = [
                    (dict(item) if isinstance(item, CommentedMap) else item)
                    for item in default
                ]
            if isinstance(default, str):
                default = f"'{default}'"
            if isinstance(default, bool):
                default = "true" if default else "false"
            if isinstance(default, CommentedMap):
                default = dict(default)
            if default is None:
                default = "null"
            comment = ""
            if key in tree.ca.items:
                comment = get_comment(tree, key)
            param = ".".join(root + [key])
            yield [param, comment, default]


def format_template(values):
    print(
        """| Parameter                | Description             | Default        |
| ------------------------ | ----------------------- | -------------- |"""
    )
    for (param, comment, default) in values:
        print(f"| `{param}` | {comment} | {default} |")


def gen(chartdir):
    chart, values = load_chart(chartdir)

    format_template(traverse(values))
