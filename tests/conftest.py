"""Shared test helpers: load the hyphenated tool scripts as modules."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def _load(name: str) -> ModuleType:
    path = TOOLS / f"{name}.py"
    mod_name = name.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    assert spec and spec.loader, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolving annotations looks the module up in sys.modules,
    # so register it before executing.
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def validate_packs() -> ModuleType:
    return _load("validate-packs")


@pytest.fixture(scope="session")
def check_links() -> ModuleType:
    return _load("check-links")


@pytest.fixture(scope="session")
def check_ids() -> ModuleType:
    return _load("check-ids")


@pytest.fixture(scope="session")
def build_site() -> ModuleType:
    return _load("build-site")
