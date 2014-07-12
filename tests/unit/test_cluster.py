"""
Test the `Cluster` class.

"""
# pylint: disable=I0011, E1101, W0612, C0111
import pytest


def test_import():
    try:
        from streamdiffer import Cluster
    except ImportError:
        assert False


def test_instantiate_empty():
    from streamdiffer import Cluster
    cluster = Cluster()
    assert cluster.streams == set()


def test_instantiate_nolist():
    from streamdiffer import Cluster
    with pytest.raises(ValueError):
        Cluster(streams="abcd")


def test_instantiate_invalid_list():
    from streamdiffer import Cluster
    with pytest.raises(ValueError):
        Cluster(streams=["a", "b", "c", "d"])


def test_match(cluster, stream_x, stream_y, stream_z):

    # Empty cluster match all ...
    assert cluster.match(stream_x)  # [] == ()
    assert cluster.match(stream_y)  # [] == ()

    # .. ALL
    stream_x.append("a")  # ["a"]
    assert cluster.match(stream_x)  # ["a"] == ()

    # If it's not empty only match if math all streams
    cluster.streams.add(stream_x)  # (["a"])
    assert cluster.match(stream_y)  # [] == (["a"])

    stream_y.append("b")  # ["b"]
    assert not cluster.match(stream_y)  # ["b"] != (["a"])

    stream_z.append("a")  # ["a"]
    assert cluster.match(stream_z)  # ["a"] == (["a"])

    cluster.streams.add(stream_z)  # (["a"], ["a"])
    assert not cluster.match(stream_y)  # ["b"] != (["a"], ["a"])

    # If any of the cluster's stream changes the cluster must be updated
    stream_x.append("b")  # ["a", "b"]
    assert cluster.match(stream_x)  # ["a", "b"] == (["a", "b"], ["a"])
    stream_z.append("c")  # ["a", "c"]
    assert not cluster.match(stream_x)  # ["a", "b"] == (["a", "b"], ["a", "c"])
    assert not cluster.match(stream_z)  # ["a", "c"] == (["a", "b"], ["a", "c"])
    cluster.streams.remove(stream_x)  # (["a", "c"])
    assert cluster.match(stream_z)  # ["a", "c"] == (["a", "c"])
