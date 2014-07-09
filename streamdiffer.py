"""
StreamDiffer
============

Compare and clusterize multiple data streams.

"""
# pylint: disable=I0011, W0212
from collections import deque


class Stream:
    """Stream of data.

    It has an internal deque object.

    """
    def __init__(self):
        self.data = deque()
        self._idx = 0
        self._dataset = set()

    def __hash__(self):
        return hash(id(self))

    def append(self, data):
        """Append new data to this stream."""
        self.data.append((self._idx, data))
        self._dataset.add(data)
        self._idx += 1

    def __eq__(self, other):
        """Equal if any of the streams is a subset of the other."""
        return (self._dataset <= other._dataset or
                other._dataset <= self._dataset)


class Cluster:
    """A cluster of streams."""
    def __init__(self, streams=None):
        if streams is None:
            self.streams = []
        elif not isinstance(streams, list):
            raise ValueError("streams attribute must be a list")
        elif not all(isinstance(s, Stream) for s in streams):
            raise ValueError("streams attribute must contain Stream objects")
        else:
            self.streams = streams

    def match(self, stream):
        """
        A stream match a cluster if it's a subset of al cluster's streams.
        """
        return all(s == stream for s in self.streams)


class Differ:
    """Find stream clusters."""
    def __init__(self, streams):
        cluster = Cluster(streams)
        self.clusters = [cluster]
        self.streams = {k:cluster for k in streams}

    def update_stream(self, stream, data):
        current_cluster = self.streams[stream]
        stream.append(data)
        if not current_cluster.match(stream):  # Stream differ
            current_cluster.streams.remove(stream)
            for other_cluster in self.streams.values():
                if other_cluster == current_cluster:
                    continue
                else:
                    # An existing cluster match. Add this stream.
                    if other_cluster.match(stream):
                        other_cluster.streams.append(stream)
                        new_cluster = other_cluster
                        break
            else:
                # If none of the existing clusters match create a new one
                new_cluster = Cluster([stream])
                self.clusters.append(new_cluster)

            self.streams[stream] = new_cluster
