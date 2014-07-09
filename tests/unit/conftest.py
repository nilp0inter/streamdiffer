"""
pytest fixtures

"""
# pylint: disable=I0011, E1101, C0111
import pytest


@pytest.fixture
def stream():
    from streamdiffer import Stream
    return Stream()


@pytest.fixture
def cluster():
    from streamdiffer import Cluster
    return Cluster()


@pytest.fixture
def stream_x():
    return stream()


@pytest.fixture
def stream_y():
    return stream()


@pytest.fixture
def stream_z():
    return stream()
