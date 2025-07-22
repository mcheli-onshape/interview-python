"""
Run with:
    pytest -q          # functional checks + perf log to stdout
or:
    pytest -q -s       # keep the log even if tests fail
"""
import random
import time
import logging
import pytest

from graph import Graph

# Configure a lightweight logger
_log = logging.getLogger("deepcopy_bench")
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("%(message)s"))
_log.addHandler(_handler)
_log.setLevel(logging.INFO)

def _log_perf(label: str, vertices: int, edges: int, elapsed_ns: int) -> None:
    """Pretty-print timing information."""
    _log.info(
        f"{label:20s} | {vertices:6d} V | {edges:7d} E | "
        f"{elapsed_ns / 1_000_000:.3f} ms"
    )

# Helper that wraps functional assertions *and* measures copy duration
def _exercise_copy(graph: Graph, label: str):
    graph._test_valid()

    # snapshot payloads so we can ensure immutability later
    v_payloads = [v.payload for v in graph.vertices]
    s_payloads = [e.start.payload for e in graph.edges]
    e_payloads = [e.end.payload for e in graph.edges]

    # performance timing
    t0 = time.perf_counter_ns()
    clone = graph.deep_copy()
    elapsed = time.perf_counter_ns() - t0
    _log_perf(label, len(graph.vertices), len(graph.edges), elapsed)

    # functional assertions (same as before)
    _compare_payloads(graph, v_payloads, s_payloads, e_payloads)

    clone._test_valid()
    _compare_payloads(clone, v_payloads, s_payloads, e_payloads)

    # deep-copy guarantees
    assert clone is not graph
    assert clone.vertices is not graph.vertices
    assert clone.edges is not graph.edges

    for v_orig in graph.vertices:
        for v_copy in clone.vertices:
            assert v_orig is not v_copy
    for e_orig in graph.edges:
        for e_copy in clone.edges:
            assert e_orig is not e_copy


def _compare_payloads(graph, v_payloads, s_payloads, e_payloads):
    """Verify payload values and edge connectivity match the snapshot."""
    assert len(graph.vertices) == len(v_payloads)
    assert len(graph.edges) == len(s_payloads)

    for i, v in enumerate(graph.vertices):
        assert v.payload == v_payloads[i]
    for i, e in enumerate(graph.edges):
        assert e.start.payload == s_payloads[i]
        assert e.end.payload == e_payloads[i]

# Individual test cases
def test_empty():
    _exercise_copy(Graph(), "empty")

def test_one_vertex_one_edge():
    g = Graph()
    v = Graph.Vertex(5)
    g.vertices.append(v)
    g.edges.append(Graph.Edge(v, v))
    _exercise_copy(g, "self-loop")

def test_two_vertices_one_edge():
    g = Graph()
    v1, v2 = Graph.Vertex(5), Graph.Vertex(15)
    g.vertices.extend([v1, v2])
    g.edges.append(Graph.Edge(v1, v2))
    _exercise_copy(g, "2V-1E")

@pytest.mark.performance
def test_large_random():
    random.seed(0)
    V, E = 5_000, 20_000

    g = Graph()
    for _ in range(V):
        g.vertices.append(Graph.Vertex(random.randint(-2**31, 2**31 - 1)))

    for _ in range(E):
        start = g.vertices[random.randrange(V)]
        end = g.vertices[random.randrange(V)]
        g.edges.append(Graph.Edge(start, end))

    _exercise_copy(g, "large-random")
