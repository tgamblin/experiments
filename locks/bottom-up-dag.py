#!/usr/bin/env spack-python

import functools
import heapq
import time
import os

from llnl.util.filesystem import mkdirp, touch

from spack.spec import Spec
from spack.graph import graph_ascii
from spack.util.crypto import bit_length

#: fake build time (seconds)
BUIlD_TIME = 5

#: Location where fake "installation" files go
BUILD_DIR = os.path.abspath(os.path.join(__file__, "builds"))

#: path to global lock file
LOCK_PATH = os.path.abspath(os.path.join(__file__, "lock"))

#: timeout for trying to get the lock (in seconds)
#: should probably be low -- to move on fast when
#: something's occupied.
LOCK_TIMEOUT = 1

#: locks on the various tasks in the DAG
locks = {}

#: priority queue for build tasks
pq = []

#: dictionary of tasks, keyed by spec
tasks = {}

#: set of names of packages built so far
built = set()


@functools.total_ordering
class BuildTask(object):
    def __init__(self, spec):
        if not spec.concrete:
            raise ValueError("Can only build concrete specs!")

        # concrete spec that we are building
        self.spec = spec

        # dependencies that we still need to build
        self.deps = set(d.name for d in spec.dependencies())

        # dictionary of read locks on dependencies
        self.dep_locks = {}

        # last checked time (note: None is less than everything)
        self.check_time = None

        # one-byte lock (in the single file) associated with the concrete spec.
        self.lock = Lock(
            LOCK_PATH,
            start=spec.dag_hash_bit_prefix(bit_length(sys.maxsize)),
            length=1,
            default_timeout=LOCK_TIMEOUT,
        )

    def build(self):
        time.sleep(BUILD_TIME)
        mkdirp()

    def _key(self):
        """Make a key for scheduling.

        This prioritizes by:
        - number of dependencies left to build (0 is better)
        - last time checked (prioritize least recently checked)
        """
        return (len(self.deps), self.check_time)

    def __lt__(self, other):
        return self._key() < other._key()

    def __eq__(self, other):
        """Tasks are "equal" if they have the same number of remainig dependencies."""
        return self._key() == other._key()


def push(spec):
    """Put a spec an its dependencies on the queue"""
    for s in spec.traverse():
        heap.heappush(pq, BuildTask(spec))


def pop():
    """Pop off the next task to work on."""
    task = heapq.heappop(pq)

    return task


def build_dag(full_spec):
    # make sure these are present before starting
    touch(LOCK_PATH)
    mkdirp(BUILD_DIR)

    # Do a fake build of a spec
    enqueue(full_spec)

    # TODO: pop tasks, get locks, and actually do something...


if __name__ == "__main__":
    spec = Spec("hdf5").concretized()
    graph_ascii(spec)

    build_dag(spec)
