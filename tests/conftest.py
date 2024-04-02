import subprocess
import time

import pytest
from pytest import MonkeyPatch


@pytest.fixture(scope="session")
def postgres_test_db():
    start = subprocess.run(
        ["docker-compose", "-f", "tests/docker-compose-test.yaml", "up", "-d"],
        capture_output=True,
        text=True,
    )
    print(start.stdout)
    if start.stderr:
        print(start.stderr)
    time.sleep(5)

    # Run Alembic migrations
    alembic_result = subprocess.run(
        ["alembic", "upgrade", "head"], capture_output=True, text=True
    )
    print(alembic_result.stdout)
    if alembic_result.stderr:
        print(alembic_result.stderr)

    yield

    down = subprocess.run(
        ["docker-compose", "-f", "tests/docker-compose-test.yaml", "down"],
        capture_output=True,
        text=True,
    )
    print(down.stdout)
    if down.stderr:
        print(down.stderr)
