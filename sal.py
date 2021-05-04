from itertools import chain
import random
from collections import defaultdict

import libpysal
from cytoolz import sliding_window


def square_at(pt):
    (x, y) = pt
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def lattice(w, h):
    return [
        square_at((i, j))
        for i in range(0, w)
        for j in range(0, h)
    ]


def normalize_edge(edge):
    return tuple(sorted(tuple(v) for v in edge))


def polygon_edges(polygon):
    return sliding_window(2, polygon)


def weights(polygons):
    closed_polygons = (
        polygon + [polygon[-1], polygon[0]]
        for polygon in polygons
    )
    labeled_edges = chain.from_iterable(
        (
            (i, normalize_edge(edge))
            for edge in polygon_edges(polygon)
        )
        for (i, polygon) in enumerate(closed_polygons)
    )

    nbhds = defaultdict(set)
    for (poly, edge) in labeled_edges:
        nbhds[edge].add(poly)

    graph_edges = [tuple(edge) for edge in nbhds.values() if len(edge) == 2]
    return graph_edges
