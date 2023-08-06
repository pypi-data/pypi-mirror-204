"""
Documentar.
"""

from typing import Any, List, Dict
import importlib


def get_class(full_class_name: str) -> Any:
    module_name, class_name = full_class_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def instantiate_class(full_class_name: str, *args: List, **kwargs: Dict[str, Any]) -> object:
    Klass = get_class(full_class_name)
    return Klass(*args, **kwargs)


def get_variable_by_pathname(full_class_name: str) -> Any:
    module_name, class_name = full_class_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)
