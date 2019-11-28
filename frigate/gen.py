from collections import OrderedDict
from ruamel.yaml import YAML

yaml = YAML()


def get_comment(comments):
    for comment in comments:
        if comment is not None:
            if isinstance(comment, list):
                return get_comment(comment)
            else:
                first_line = comment.value.strip().split("\n")[0]
                return clean_comment(first_line)


def clean_comment(comment):
    return comment.strip("# ").capitalize()


def traverse(tree, root=[]):
    for key in tree:
        default = tree[key]
        if isinstance(default, dict):
            root = root.copy()
            root.append(key)
            traverse(default, root=root)
        else:
            if isinstance(default, list):
                default = []
            if isinstance(default, str):
                default = f"'{default}'"
            if default is None:
                default = "null"
            comment = ""
            if key in tree.ca.items:
                comment = get_comment(tree.ca.items[key])
            print(f"| `{'.'.join(root + [key])}` | {comment} | {default} |")


def gen(filename):
    with open(filename, "r") as fh:
        config = fh.read()

    print(
        """| Parameter                | Description             | Default        |
| ------------------------ | ----------------------- | -------------- |"""
    )

    code = yaml.load(config)
    traverse(code)
