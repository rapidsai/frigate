import os.path

import pytest

import frigate

MODULE_ROOT = os.path.abspath(os.path.dirname(frigate.__file__))


@pytest.fixture
def nginx_chart():
    from frigate.gen import load_chart

    nginx_chart_path = os.path.join(MODULE_ROOT, "tests", "mockcharts", "nginx")
    return load_chart(nginx_chart_path)


@pytest.fixture
def yaml():
    from ruamel.yaml import YAML

    return YAML()


def test_load_chart(nginx_chart):
    chart, values = nginx_chart

    assert "name" in chart and chart["name"] == "nginx"
    assert "image" in values


def test_get_comment(yaml):
    from frigate.gen import get_comment

    tree = yaml.load("hello: world  # this is the comment")
    assert get_comment(tree, "hello") == "This is the comment"

    tree = yaml.load(
        """
    # this is not the comment you are looking for
    hello: world  # this is the comment
    # this is also not the comment
    """
    )
    assert get_comment(tree, "hello") == "This is the comment"

    tree = yaml.load(
        """
        # top level comment

    # this is not the comment you are looking for
    hello: world  # this is the comment
    # this is also not the comment
    """
    )
    assert get_comment(tree, "hello") == "This is the comment"

    tree = yaml.load(
        """
    # top level comment
    some: option

    # this is not the comment you are looking for
    hello: world  # this is the comment
    # this is also not the comment
    """
    )
    assert get_comment(tree, "hello") == "This is the comment"

    tree = yaml.load(
        """
    # top level comment
    hello: world

    # there is no comment to be found
    some: option
    """
    )
    assert get_comment(tree, "hello") == ""


def test_clean_comment():
    from frigate.gen import clean_comment

    assert clean_comment("# hello world") == "Hello world"
    assert clean_comment("hello world") == "Hello world"
    assert clean_comment("## # ## ## hello world") == "Hello world"
    assert clean_comment(" # hello world  ") == "Hello world"


def test_traversal(nginx_chart):
    from frigate.gen import traverse

    _, values = nginx_chart
    output = list(traverse(values))

    assert len(output) == 17
    assert ["replicaCount", "", 1] in output
