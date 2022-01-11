import pytest


@pytest.fixture(scope="module")
def test_fixture():
    return 1
