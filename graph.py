from typing import List

class Graph:

    class Vertex:

        def __init__(self, payload: int) -> None:
            self.payload = payload

    class Edge:

        def __init__(self, start: "Graph.Vertex", end: "Graph.Vertex") -> None:
            self.start = start
            self.end = end

    def __init__(self) -> None:
        self.vertices: List[Graph.Vertex] = []
        self.edges: List[Graph.Edge] = [] 

    # ------------------------------------------------------------------ #
    # ✂️  IMPLEMENT THIS METHOD
    # Return a full deep copy of the graph:
    #   * Every Vertex and Edge object must be a *new* instance
    #   * Payload values and edge connectivity must be preserved
    # ------------------------------------------------------------------ #
    def deep_copy(self) -> "Graph":
        return None

    # ------------------------------------------------------------------ #
    # The rest of this file is *test infrastructure*; do not modify it.
    # ------------------------------------------------------------------ #
    def _test_valid(self) -> None:
        if self.vertices is None:
            raise Exception("vertices is None")
        if self.edges is None:
            raise Exception("edges is None")

        # -- Vertices ----------------------------------------------------
        for i, v in enumerate(self.vertices):
            if v is None:
                raise Exception(f"Vertex {i} is None")
            for j in range(i + 1, len(self.vertices)):
                if v is self.vertices[j]:
                    raise Exception(f"Duplicate vertices at {i} and {j}")

        # -- Edges -------------------------------------------------------
        for i, e in enumerate(self.edges):
            if e is None:
                raise Exception(f"Edge {i} is None")
            for j in range(i + 1, len(self.edges)):
                if e is self.edges[j]:
                    raise Exception(f"Duplicate edges at {i} and {j}")

            if e.start not in self.vertices:
                raise Exception(f"Start vertex for edge {i} not found")
            if e.end not in self.vertices:
                raise Exception(f"End vertex for edge {i} not found")
