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
def deps_chart_path():
    return os.path.join(MODULE_ROOT, "tests", "mockcharts", "deps")


@pytest.fixture
def deps_chart(deps_chart_path):
    from frigate.gen import load_chart

    return load_chart(deps_chart_path)


@pytest.fixture
def yaml():
    from ruamel.yaml import YAML

    return YAML()


def test_load_chart(simple_chart):
    chart, values = simple_chart

    assert "name" in chart and chart["name"] == "simple"
    assert any(["image" in value[0] for value in values])


def test_get_comment(yaml):
    from frigate.gen import get_comment

    tree = yaml.load("hello: world  # this is the comment")
    assert get_comment(tree, "hello") == "this is the comment"

    tree = yaml.load(
        """
    # this is not the comment you are looking for
    hello: world  # this is the comment
    # this is also not the comment
    """
    )
    assert get_comment(tree, "hello") == "this is the comment"

    tree = yaml.load(
        """
        # top level comment

    # this is not the comment you are looking for
    hello: world  # this is the comment
    # this is also not the comment
    """
    )
    assert get_comment(tree, "hello") == "this is the comment"

    tree = yaml.load(
        """
    # top level comment
    some: option

    # this is not the comment you are looking for
    hello: world  # this is the comment
    # this is also not the comment
    """
    )
    assert get_comment(tree, "hello") == "this is the comment"

    tree = yaml.load(
        """
    # top level comment
    hello: world

    # there is no comment to be found
    some: option
    """
    )
    assert get_comment(tree, "hello") == ""

    tree = yaml.load("hello: world  # Use a `LoadBalancer`.")
    assert get_comment(tree, "hello") == "Use a `LoadBalancer`."


def test_clean_comment():
    from frigate.gen import clean_comment

    assert clean_comment("# hello world") == "hello world"
    assert clean_comment("hello world") == "hello world"
    assert clean_comment("## # ## ## hello world") == "hello world"
    assert clean_comment(" # hello world  ") == "hello world"


def test_traversal(simple_chart, rich_chart):
    _, values = simple_chart
    simple_output = values

    assert len(simple_output) == 17
    assert ["replicaCount", "", "1"] in simple_output

    _, values = rich_chart
    rich_output = values

    assert [
        "replicaCount",
        "number of nginx pod replicas to create",
        "1",
    ] in rich_output


def test_custom_template(rich_chart_path):
    from frigate.gen import gen

    test_phrase = "rich chart"

    assert test_phrase in gen(rich_chart_path, "markdown")


def test_deps(deps_chart_path):
    from frigate.gen import gen

    docs = gen(deps_chart_path, "markdown")

    assert "<td>simple.image.repository</td>" in docs
    assert "<td>\n\n\"mainline\"\n\n</td>" in docs


def test_squash_duplicates():
    from frigate.gen import squash_duplicate_values

    values = squash_duplicate_values([["hello", "", "world"], ["hello", "", "there"]])

    assert len(values) == 1
    assert values[0][2] == "world"


def test_load_pre_packaged_chart(deps_chart_path):
    from frigate.gen import gen

    docs = gen(deps_chart_path, "markdown", update=False)
    assert "image.repository" in docs
    assert "<td>\n\n\"nginx\"\n\n</td>" in docs
