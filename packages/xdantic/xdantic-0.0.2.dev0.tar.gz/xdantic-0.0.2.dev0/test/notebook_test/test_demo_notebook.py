"""
All rights reserved to the Boston Consulting Group
"""
import logging
import os
from pathlib import Path

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS_DIR = os.path.join(Path(__file__).parent.parent.parent, "notebooks")
resources = {"metadata": {"path": NOTEBOOKS_DIR}}

log = logging.getLogger(__name__)


def test_notebooks_dir_exists():
    assert os.path.isdir(NOTEBOOKS_DIR)


def test_notebooks_dir_not_empty():
    assert (
        len(
            list(
                filter(lambda path: path.endswith(".ipynb"), os.listdir(NOTEBOOKS_DIR))
            )
        )
        > 0
    )


@pytest.mark.parametrize(
    "notebook", filter(lambda path: path.endswith(".ipynb"), os.listdir(NOTEBOOKS_DIR))
)
def test_notebook(notebook):
    notebook_path = os.path.join(NOTEBOOKS_DIR, notebook)
    log.info(f"Reading jupyter notebook from {notebook_path}")

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name="python")

    ep.preprocess(nb, resources=resources)
