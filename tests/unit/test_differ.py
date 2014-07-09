"""
Test the `Differ` class.

"""
# pylint: disable=I0011, E1101, W0612, C0111, C0103
import pytest


def test_import():
    try:
        from streamdiffer import Differ
    except ImportError:
        assert False


def test_differ_update_stream(stream_x, stream_y, stream_z):
    from streamdiffer import Differ
    differ = Differ([stream_x, stream_y, stream_z])
    assert len(differ.streams) == 3
    assert len(differ.clusters) == 1

    # Same input, three streams
    differ.update_stream(stream_x, "a")
    assert len(differ.clusters) == 1
    differ.update_stream(stream_y, "a")
    assert len(differ.clusters) == 1
    differ.update_stream(stream_z, "a")
    assert len(differ.clusters) == 1

    # X go ahead...
    differ.update_stream(stream_x, "b")
    differ.update_stream(stream_x, "c")
    assert len(differ.clusters) == 1

    # Y start differing
    differ.update_stream(stream_y, "2")
    assert len(differ.clusters) == 2

    # Z follow Y
    differ.update_stream(stream_z, "2")
    assert len(differ.clusters) == 2

    assert stream_x in differ.clusters[0].streams
    assert stream_y in differ.clusters[1].streams
    assert stream_z in differ.clusters[1].streams
