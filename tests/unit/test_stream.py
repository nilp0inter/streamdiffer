"""
Test the `Stream` class.

"""
# pylint: disable=I0011, E1101, W0612, C0111, C0103
import pytest


def test_import():
    try:
        from streamdiffer import Stream
    except ImportError:
        assert False


def test_append(stream):
    stream.append('a')
    assert 'a' in stream.data[0]  # <- [(0, 'a')]

    stream.append('b')
    assert 'b' in stream.data[1]  # <- [(0, 'a'), (1, 'b')]


def test_stream_equality():
    from streamdiffer import Stream
    x=Stream()
    y=Stream()

    x.append("a")
    assert x == y

    y.append("a")
    assert x == y

    y.append("b")
    assert x == y

    x.append("c")
    assert x != y
