"""
All rights reserved to the Boston Consulting Group
"""

from abc import ABC
from enum import Enum
from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional, Sequence, Type, TypeVar, Union

from pydantic import BaseModel, BaseSettings
from pydantic.env_settings import DotenvType
from pydantic.typing import StrPath
from yaml import Loader, load

__all__ = ["XConfig", "XConfigSingleton"]

# Generics type annotation;
# ConfigurationClass can only be an XConfig or subtype of XConfig
ConfigurationClass = TypeVar("ConfigurationClass", bound="XConfig")


class XConfig(BaseSettings, ABC):
    """
    Base class for configuration settings.
    Users of the config module should inherit their configuration class from `XConfig`.
    >>> class CustomConfig(XConfig):
    ...     v1: str = "v1"
    ...     v2: int = 3
    To provide nested configuration, sub-class the `BaseModel` class from Pydantic.
    >>> from pydantic import BaseModel
    ...
    >>> class SubConfig(BaseModel):
    ...    v3: float = 0.4
    ...
    >>> class CustomConfig(XConfig):
    ...    sub: SubConfig
    ...
    >>> import os
    ... os.environ['SUB__V3'] = '0.9'
    ... assert CustomConfig().sub.v3 == 0.9
    """

    class Config:
        env_file = ".env"
        env_nested_delimiter: str = "__"

    @classmethod
    def from_yaml(
        cls: Type[ConfigurationClass], *file_paths: Path
    ) -> ConfigurationClass:
        """Instantiate class instance given a yaml file path
        Parameters
        ----------
        file_paths : Path
            full path to yaml config files
        Returns
        -------
        XConfig
            Xconfig class
        """
        merged_configs = {}
        for file_path in file_paths:
            with open(str(file_path), "r", encoding="utf-8") as yaml_file:
                config = load(yaml_file, Loader=Loader)
                merged_configs = _merge(merged_configs, config)
        return cls(**merged_configs)

    def with_updated_values(
        self: ConfigurationClass, **values: Any
    ) -> ConfigurationClass:
        """Returns copy of config with uodated values from a dictionary or another config object
        Parameters
        ----------
        values : Dict[str, Any]
            values to be updated in the config object
        Returns
        -------
        XConfig
            Xconfig class
        """
        merged = _merge(self, values)
        if isinstance(merged, BaseModel):
            return merged
        else:
            return self.__class__(**merged)


class XConfigSingleton(XConfig, ABC):
    """
    Singleton version of the XConfig class. Will save the initialization argumets in
    a class scoped property, and return copies if the `xconfig_update` parameter is set to False
    """

    class _Single(NamedTuple):
        init_kwargs: Dict[str, Any]
        env_file: Optional[DotenvType] = None
        env_file_encoding: Optional[str] = None
        env_nested_delimiter: Optional[str] = None
        secrets_dir: Optional[StrPath] = None

    _single: Optional[_Single] = None
    xconfig_update: bool = True

    def _build_values(
        self,
        init_kwargs: Dict[str, Any],
        _env_file: Optional[DotenvType] = None,
        _env_file_encoding: Optional[str] = None,
        _env_nested_delimiter: Optional[str] = None,
        _secrets_dir: Optional[StrPath] = None,
    ) -> Dict[str, Any]:
        cls = self.__class__
        if init_kwargs.pop("xconfig_update", True) or not cls._single:
            cls._single = cls._Single(
                init_kwargs=init_kwargs,
                env_file=_env_file,
                env_file_encoding=_env_file_encoding,
                env_nested_delimiter=_env_nested_delimiter,
                secrets_dir=_secrets_dir,
            )

        return super()._build_values(
            init_kwargs=cls._single.init_kwargs,
            _env_file=cls._single.env_file,
            _env_file_encoding=cls._single.env_file_encoding,
            _env_nested_delimiter=cls._single.env_nested_delimiter,
            _secrets_dir=cls._single.secrets_dir,
        )

    def __getstate__(self):
        state = super().__getstate__()
        cls = self.__class__
        state["__dict__"]["_single"] = cls._single
        return state


T = TypeVar("T")
U = TypeVar("U")


def _merge(original: T, new: U) -> Union[T, U]:
    """Merge the two objects together into a single one.
    Priority will go to the ``new`` object when there are conflicts.
    Args:
        original (T): Object to merge the new values into
        new (U): Object to merge into the original
    Returns:
        Union[T, U]: Merged object containing values from both of the objects
    """
    # If any value ia a basic type, there is no merging to be done and we return the new value
    basic_types = (str, int, float, complex, bool, bytes, Enum)
    if isinstance(new, basic_types) or isinstance(original, basic_types):
        return new

    # Now we check for mergeable types.
    # Whenever the types are not compatible to be merged (Dict and List for ex.) we return the new

    if isinstance(original, Sequence):
        if isinstance(new, Sequence):
            return _merge_sequence(original, new)
        else:
            return new

    if isinstance(original, BaseModel):
        if isinstance(new, BaseModel):
            return _merge_models(original, new)
        elif isinstance(new, Dict):
            original_dict = _get_shallow_model_dict(original)
            merged_dict = _merge_dicts(original_dict, new)
            return original.__class__(**merged_dict)
        else:
            return new

    if isinstance(original, Dict):
        if isinstance(new, Dict):
            return _merge_dicts(original, new)
        else:
            return new

    # finally if the original value is of an unkown type, we cannot merge it and just return the new
    return new


def _merge_sequence(original: Sequence, new: Sequence) -> Sequence:
    # merge each member of the sequences
    merged = [_merge(o, n) for o, n in zip(original, new)]
    if len(original) != len(new):
        # If the sequeces are of different sizes, we get the umerged values from the longest
        longest = new if len(new) > len(original) else original
        merged = merged + [item for item in longest[len(merged) :]]
    return merged


def _merge_models(original: BaseModel, new: BaseModel) -> BaseModel:
    original_dict = _get_shallow_model_dict(original)
    new_dict = _get_shallow_model_dict(new)
    merged = _merge_dicts(original_dict, new_dict)
    return original.__class__(**merged)


def _get_shallow_model_dict(model: BaseModel):
    return {field: getattr(model, field) for field in model.__fields__}


def _merge_dicts(original: Dict[Any, Any], new: Dict[Any, Any]) -> Dict[Any, Any]:
    merged_dict = original.copy()
    for new_key, new_value in new.items():
        if new_key in merged_dict:
            merged_dict[new_key] = _merge(merged_dict[new_key], new_value)
        else:
            merged_dict[new_key] = new_value

    return merged_dict
