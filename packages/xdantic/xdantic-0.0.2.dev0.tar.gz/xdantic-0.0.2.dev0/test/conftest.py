"""
All rights reserved to the Boston Consulting Group
"""

import os
from pathlib import Path

import pytest

P_RESOURCES = Path(os.path.dirname(__file__)).joinpath("resources").absolute()


@pytest.fixture(scope="session")
def yaml_configs_folder() -> Path:
    return P_RESOURCES.joinpath("test_config_files").absolute()
