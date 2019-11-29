import os
import os.path

import pytest

import frigate

MODULE_ROOT = os.path.abspath(os.path.dirname(frigate.__file__))


@pytest.fixture
def simple_chart_path():
    return os.path.join(MODULE_ROOT, "tests", "mockcharts", "simple")


@pytest.fixture
def simple_chart(simple_chart_path):
    from frigate.gen import load_chart

    return load_chart(simple_chart_path)


@pytest.fixture
def rich_chart_path():
    return os.path.join(MODULE_ROOT, "tests", "mockcharts", "rich")


@pytest.fixture
def rich_chart(rich_chart_path):
    from frigate.gen import load_chart

    return load_chart(rich_chart_path)


@pytest.fixture
def yaml():
    from ruamel.yaml import YAML

    return YAML()


def test_load_chart(simple_chart):
    chart, values = simple_chart

    assert "name" in chart and chart["name"] == "simple"
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


def test_traversal(simple_chart, rich_chart):
    from frigate.gen import traverse

    _, values = simple_chart
    simple_output = list(traverse(values))

    assert len(simple_output) == 17
    assert ["replicaCount", "", "1"] in simple_output

    _, values = rich_chart
    rich_output = list(traverse(values))

    assert [
        "replicaCount",
        "Number of nginx pod replicas to create",
        "1",
    ] in rich_output


def test_custom_template(rich_chart_path):
    from frigate import DOTFILE_NAME
    from frigate.gen import gen

    test_phrase = "rich chart"

    assert test_phrase in gen(rich_chart_path, "markdown")
