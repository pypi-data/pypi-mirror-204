"""
All rights reserved to the Boston Consulting Group
"""
from typing import Dict, List, Tuple

import pytest
from pydantic import BaseModel, ValidationError

from xdantic import XConfig, XConfigSingleton


class DummyMetrics(BaseModel):
    AUC: float
    recall: int


class DummyConfig(XConfig):
    metrics: Tuple[DummyMetrics, ...]
    param_str: str
    param_x: int
    param_y: int = -1


def test_yaml_config(yaml_configs_folder):
    config_path = yaml_configs_folder / "yaml_test.yaml"

    config = DummyConfig.from_yaml(config_path)

    assert config.param_str == "a_string_param"
    assert config.param_x == 42
    assert config.param_y == -1
    assert config.metrics[0].AUC == 2.5
    assert config.metrics[0].recall == 50
    assert config.metrics[1].AUC == 10
    assert config.metrics[1].recall == 100


def test_yaml_config_override(yaml_configs_folder):
    config_path = yaml_configs_folder / "yaml_test.yaml"
    override_path = yaml_configs_folder / "yaml_test_override.yaml"

    config = DummyConfig.from_yaml(config_path, override_path)

    assert config.param_str == "overriden_param"
    assert config.param_x == 42
    assert config.param_y == 25
    assert config.metrics[0].AUC == 0
    assert config.metrics[0].recall == 50
    assert config.metrics[1].AUC == 10
    assert config.metrics[1].recall == 0
    assert config.metrics[2].AUC == 20
    assert config.metrics[2].recall == 20


def test_config_with_updated_values():
    class DummyMetricExtension(DummyMetrics):
        label: str

    updated_values = {
        "param_str": "updated_str",
        "metrics": [{"recall": 10, "label": "updated"}, DummyMetrics(AUC=1, recall=2)],
    }
    config = DummyConfig(
        metrics=tuple(
            [
                DummyMetricExtension(AUC=10, recall=20, label="test"),
                DummyMetricExtension(AUC=10, recall=20, label="test"),
            ]
        ),
        param_str="original_str",
        param_x=1,
    )
    updated_config = config.with_updated_values(**updated_values)

    assert updated_config.param_str == "updated_str"
    assert updated_config.param_x == 1
    assert updated_config.param_y == -1
    assert updated_config.metrics[0].AUC == 10
    assert updated_config.metrics[0].recall == 10
    assert updated_config.metrics[0].label == "updated"
    assert updated_config.metrics[1].AUC == 1
    assert updated_config.metrics[1].recall == 2
    assert updated_config.metrics[1].label == "test"


def test_yaml_config_validation(yaml_configs_folder):
    config_path = yaml_configs_folder / "yaml_test_wrong_schema.yaml"

    with pytest.raises(
        expected_exception=ValidationError,
    ):
        DummyConfig.from_yaml(config_path)


def test_with_updated_config_validation():
    config = DummyConfig(
        metrics=tuple([DummyMetrics(AUC=10, recall=20)]),
        param_str="original_str",
        param_x=1,
    )

    with pytest.raises(
        expected_exception=ValidationError,
    ):
        config.with_updated_values(param_str=["not a str"], param_x=10)


def test_singleton():
    class SingletonTest(XConfigSingleton):
        attr_int: int = 1
        attr_dict: Dict[str, str]

    instance = SingletonTest(attr_int=2, attr_dict={"a": "b"})
    instance.attr_dict["b"] = "c"
    del instance

    second_instance = SingletonTest(xconfig_update=False, attr_dict={"c": "d"})

    assert second_instance.attr_int == 2
    assert second_instance.attr_dict["a"] == "b"
    assert "b" not in second_instance.attr_dict
    assert "c" not in second_instance.attr_dict


def test_multiple_singletons_are_independent():
    class Singleton1(XConfigSingleton):
        attr_int: int = 1
        attr_dict: Dict[str, str]

    class Singleton2(XConfigSingleton):
        attr_int: int = 2
        attr_str: str = "test"
        attr_list: List[int]

    first_instance = Singleton1(attr_int=2, attr_dict={"a": "b"})
    second_instance = Singleton2(attr_int=1, attr_list=[])

    assert first_instance.attr_int == 2
    assert first_instance.attr_dict["a"] == "b"
    assert second_instance.attr_int == 1
    assert second_instance.attr_str == "test"
    assert second_instance.attr_list == []
