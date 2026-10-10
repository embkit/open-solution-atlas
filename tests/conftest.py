"""Shared test helpers: load the hyphenated tool scripts as modules."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def _load(name: str) -> ModuleType:
    path = TOOLS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    assert spec and spec.loader, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
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
