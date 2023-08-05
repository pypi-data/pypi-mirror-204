from __future__ import annotations

import base64
import gzip
import json
from typing import Callable, Union
from uuid import uuid4

import networkx as nx

from .execution import Execution
from .factory import Factory
from .types import Runners
from .utils import generate_id


class Graph:
    nodes: list[Node]
    edges: list[Edge]

    def __init__(self, *, nodes: list[Node], edges: list[Edge]):
        self.nodes = nodes
        self.edges = edges

    @classmethod
    def empty(cls):
        return cls(nodes=[], edges=[])

    @classmethod
    def start(cls, node: Node, initializer=None, use: Runners = Runners.Lambda):
        graph = cls.empty()
        start_node = Node(graph=graph)
        graph.nodes = [start_node, node]
        graph.edges = [Single.connect(start_node, node, method=initializer, use=use)]
        return graph

    def end(self):
        end_node = Node.end()
        self.edges.append(Edge.connect(self.nodes[-1], end_node, override_type="end"))
        self.nodes.append(end_node)

    def copy(self):
        return self.__class__(nodes=self.nodes, edges=self.edges)

    def join_edge(self, edge: Edge, node: Node):
        edge.target = node
        self.nodes.append(node)
        self.edges.append(edge)


class Node:
    id: str
    graph: Graph
    requirements: list[str]

    def __init__(self, initializer=None, graph=None):
        self.id = str(uuid4())
        self.graph = graph or Graph.start(self, initializer=initializer)
        self.requirements = []

    @classmethod
    def end(cls):
        return cls()

    def _extend(self, entity: Union[Scalar, Vector], edge: Edge):
        graph_copy = self.graph.copy()
        graph_copy.join_edge(edge, entity)
        entity.graph = graph_copy
        return entity

    def _map_to_scalar(self, edge: Edge) -> Scalar:
        scalar = Scalar()
        return self._extend(scalar, edge)

    def _map_to_vector(self, edge: Edge) -> Vector:
        vector = Vector()
        return self._extend(vector, edge)

    def apply(self, method: Callable, use: Runners = Runners.Lambda) -> Scalar:
        return self._map_to_scalar(Single(self, method=method, use=use))

    def map(self, predicate: Callable, use: Runners = Runners.Lambda) -> Vector:
        return self._map_to_vector(Map(self, method=predicate, use=use))

    def filter(self, predicate: Callable, use: Runners = Runners.Lambda) -> Vector:
        return self._map_to_vector(Filter(self, method=predicate, use=use))

    def get_graph(self):
        graph = nx.DiGraph()
        for node in self.graph.nodes:
            graph.add_node(node.id, **node.serialize())
        for edge in self.graph.edges:
            graph.add_edge(edge.source.id, edge.target.id, **edge.serialize())
        return graph

    def get_line_graph(self):
        graph = self.get_graph()
        line_graph = nx.line_graph(graph)
        line_graph.add_nodes_from((node, graph.edges[node]) for node in line_graph)
        return line_graph

    def serialize_line_graph(self):
        line_graph = self.get_line_graph()
        line_graph_nodes = line_graph.nodes(data=True)
        line_graph_edges = line_graph.edges

        node_id_map = {
            "".join(node_id_tuple): node_data["id"]
            for node_id_tuple, node_data in line_graph_nodes
        }

        nodes = [
            {
                "id": node_data["id"],
                "type": node_data["type"],
                "use": node_data["use"],
                "method": node_data["method"],
            }
            for _, node_data in line_graph_nodes
        ]

        edges = [
            {
                "id": generate_id(),
                "target": node_id_map["".join(source_pair)],
                "source": node_id_map["".join(target_pair)],
            }
            for source_pair, target_pair in line_graph_edges
        ]

        return {"nodes": nodes, "edges": edges}

    def serialize(self):
        return {"id": self.id}

    def json(self, compress=False):
        ret = json.dumps(
            {
                "id": self.id,
                "graph": self.serialize_line_graph(),
                "requirements": self.requirements,
            },
            separators=(",", ":"),
        )
        if compress:
            ret_compressed = gzip.compress(ret.encode("utf-8"))
            return base64.b64encode(ret_compressed).decode("utf-8")
        return ret

    def evaluate(self, *, api_key: str, requirements: list[str] = None):
        self.graph.end()
        self.requirements = requirements or []
        execution = Execution.submit(self.json(compress=True), api_key=api_key)
        execution.poll_for_completion()
        return execution.get_results()


class Edge:
    id: str
    source: Node
    target: Node
    type: str = "noop"

    def __init__(
        self,
        source: Node,
        target: Node = None,
        method: Callable = None,
        use: Runners = None,
        override_type: str = None,
    ):
        self.id = generate_id()
        self.source = source
        self.target = target
        self.method = Factory(method)
        self.use = use

        if override_type is not None:
            self.type = override_type

    @classmethod
    def connect(
        cls,
        source: Node,
        target: Node,
        method: Callable = None,
        use: Runners = None,
        override_type: str = None,
    ):
        return cls(
            source,
            target=target,
            method=method,
            use=use,
            override_type=override_type,
        )

    def serialize(self):
        return {
            "id": self.id,
            "source": self.source.id,
            "target": self.target.id,
            "type": self.type,
            "use": self.use.value if self.use is not None else None,
            "method": self.method.serialize() if self.method is not None else None,
        }


class Single(Edge):
    type = "single"


class Map(Edge):
    type = "map"


class Filter(Edge):
    type = "filter"


class Scalar(Node):
    """
    Represents a single, non-proxy, data object.
    """

    pass


class Vector(Node):
    """
    Represents a proxy data object with many children.
    """

    pass
