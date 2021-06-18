import os
import os.path
import shutil
import pytest

import frigate

MODULE_ROOT = os.path.abspath(os.path.dirname(frigate.__file__))

@pytest.fixture()
def charts(tmp_path) :
    tmp_charts = os.path.join(tmp_path,"data")
    shutil.copytree(os.path.join(MODULE_ROOT, "tests", "mockcharts"), tmp_charts)
    return tmp_charts

def test_hook_all(charts):
    from frigate.pre_commit_hook import main
    os.chdir(charts)
    assert main("README.rst", "rst") == 3


def test_hook_simple(charts):
    from frigate.pre_commit_hook import main

    os.chdir(os.path.join(charts, "simple"))
    assert main("README.md", "markdown") == 1
    assert os.path.isfile("README.md")
