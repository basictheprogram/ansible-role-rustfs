"""State tests for the realtime.rustfs Molecule scenario.

The role ran against a mock midclt, which writes what it was asked to create to a
JSON file. These tests read that file.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest

from ._data import APP_NAME, CONSOLE_PORT, DATASET_ID, FIXTURE_USER, S3_PORT, STATE_FILE

if TYPE_CHECKING:
    from testinfra.host import Host


@pytest.fixture
def state(host: Host) -> dict[str, Any]:
    return json.loads(host.file(STATE_FILE).content_string)


def test_state_file_exists(host: Host) -> None:
    assert host.file(STATE_FILE).is_file


def test_dataset_was_created(state: dict[str, Any]) -> None:
    assert DATASET_ID in state["datasets"]


def test_dataset_is_a_filesystem(state: dict[str, Any]) -> None:
    assert state["datasets"][DATASET_ID]["type"] == "FILESYSTEM"


def test_app_was_created(state: dict[str, Any]) -> None:
    assert APP_NAME in state["apps"]


def test_app_is_running(state: dict[str, Any]) -> None:
    assert state["apps"][APP_NAME]["state"] == "RUNNING"


def test_app_uses_the_community_train(state: dict[str, Any]) -> None:
    assert state["apps"][APP_NAME]["train"] == "community"


def test_app_uses_the_rustfs_catalog_app(state: dict[str, Any]) -> None:
    assert state["apps"][APP_NAME]["catalog_app"] == "rustfs"


def test_app_has_the_s3_port(state: dict[str, Any]) -> None:
    assert state["apps"][APP_NAME]["config"]["network"]["api_port"] == S3_PORT


def test_app_has_the_console_port(state: dict[str, Any]) -> None:
    assert state["apps"][APP_NAME]["config"]["network"]["console_port"] == CONSOLE_PORT


def test_app_has_the_fixture_values(state: dict[str, Any]) -> None:
    assert state["apps"][APP_NAME]["config"]["fixture"]["user"] == FIXTURE_USER


def test_only_the_one_app_exists(state: dict[str, Any]) -> None:
    assert list(state["apps"]) == [APP_NAME]
