"""Shared test constants for the realtime.rustfs Molecule scenario.

They mirror the variables in converge.yml; the mock midclt records everything the
role does in STATE_FILE.
"""

from __future__ import annotations

STATE_FILE = "/var/lib/mock-midclt/state.json"

APP_NAME = "rustfs-test"
DATASET_ID = "tank/apps/rustfs-test"
S3_PORT = 40292
CONSOLE_PORT = 40293
FIXTURE_USER = "testuser1"
