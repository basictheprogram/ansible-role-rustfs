"""Probe tests for the realtime.rustfs Molecule scenario.

prepare.yml starts a stub S3 endpoint that refuses every request with 403, which
is what the role's probe expects of a healthy RustFS. A converge that got past
the probe has already proved the 403; these check the stub is still the thing
answering.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._data import S3_PORT

if TYPE_CHECKING:
    from testinfra.host import Host


def test_stub_s3_endpoint_is_running(host: Host) -> None:
    assert host.service("mock-s3").is_running


def test_stub_s3_endpoint_is_listening(host: Host) -> None:
    assert host.socket(f"tcp://0.0.0.0:{S3_PORT}").is_listening
