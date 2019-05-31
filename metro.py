import itertools
import json
from typing import List, Dict, Iterable
from collections import Counter
import matplotlib.pyplot as plt

import networkx as nx
from unidecode import unidecode


def main():
    lines = load_lines()
    g = build_graph(lines)
    plot_graph(g)

    trips = load_trips()
    shortest_paths = get_shortest_paths(g, trips)
    most_visited = get_most_visited(shortest_paths, 4)
    print(most_visited)


def load_lines() -> List[Dict]:
    with open('metro_lines.json') as file:
        lines = json.load(file)
    return lines


def build_graph(lines: List[Dict]) -> nx.Graph:
    g = nx.Graph()
    for line in lines:
        for prev, next_ in pairwise(line['stations']):
            g.add_node(prev['name'], name=prev['name'])
            g.add_node(next_['name'], name=next_['name'])
            g.add_edge(
                prev['name'],
                next_['name'],
                weight=next_['time'] - prev['time']
            )
    return g


def pairwise(iterable: Iterable) -> Iterable:
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def plot_graph(g: nx.Graph):
    nx.draw(g, with_labels=True)
    plt.savefig("graph.png")


def load_trips() -> List[Dict]:
    with open('trip_records.jsonl') as file:
        trips = [json.loads(line) for line in file]
    return trips


def get_shortest_paths(g: nx.Graph, trips: List[Dict]) -> List[List[str]]:
    return [
        get_alphabetical_shortest_path(
            list(nx.all_shortest_paths(g, trip['origin'], trip['destination'], weight='weight'))
        )
        for trip in trips
    ]


def get_alphabetical_shortest_path(shortest_paths: List[List[str]]) -> List[str]:
    candidate_indices = list(range(len(shortest_paths)))
    for group in itertools.zip_longest(*shortest_paths, fillvalue='ZZZ'):
        sanitized = [unidecode(item.upper()) for item in group]
        minimum = min(item for i, item in enumerate(sanitized) if i in candidate_indices)
        candidate_indices = [i for i, item in enumerate(sanitized) if item == minimum and i in candidate_indices]
        if len(candidate_indices) == 1:
            break

    shortest_index, = candidate_indices
    return shortest_paths[shortest_index]


def get_most_visited(shortest_paths: List[List[str]], maximum: int = 10) -> List[str]:
    counter = Counter(itertools.chain.from_iterable(shortest_paths))
    return [name for name, count in counter.most_common(maximum)]


if __name__ == '__main__':
    main()
