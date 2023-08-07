from pathlib import Path
import json

import matplotlib.pyplot as plt
import networkx as nx


def __get_data(json_abs_path: str) -> dict[str, list[dict]]:
    """
    Loads a JSON file as dict object.

    :param json_abs_path:  The absolute path to the .json file to load
    :return: a Python dict object
    """
    with open(json_abs_path) as json_file:
        return json.load(json_file)


def visualize_using_networkx(json_abs_path: str) -> None:
    """
    Generate a NetworkX graph in a new window using the data defined in a specified JSON file whose data format complies
    with `knowledge graph specification <https://qubitpi.github.io/knowledge-graph-spec/draft/>`_. An example data file
    in this format could be::

    {
        "nodes":[
            {
                "id":"node1-id",
                "fields": {
                    "name":"Pride and Prejudice",
                    "type": "Book"
                }
            },
            {
                "id":"node2-id",
                "fields":{
                    "name":"Jane Austen",
                    "type":"Person"
                }
            }
        ],
        "links":[
            {
                "source":"node2-id",
                "target":"node1-id",
                "fields": {
                    "label":"wrote"
                }
            }
        ]
    }

    .. NOTE::
       The following "fields" must present in data:

       - (node) "name" for node label
       - (link) "label" for link label

    :param json_abs_path:  The absolute path to the data file
    """
    data: dict[str, list[dict]] = __get_data(json_abs_path)

    edges: list = [[link["source"], link["target"]] for link in data["links"]]

    graph = nx.DiGraph()

    graph.add_edges_from(edges)

    pos = nx.spring_layout(graph)
    plt.figure()
    nx.draw(
        graph,
        pos,
        edge_color='black',
        width=1,
        linewidths=1,
        node_size=500,
        node_color='pink',
        alpha=0.9,
        with_labels=True,
        labels={node["id"]: node["fields"]["name"] for node in data["nodes"]}
    )
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels={(link["source"], link["target"]): link["fields"]["label"] for link in data["links"]},
        font_color='red'
    )
    plt.axis('off')

    filename: str = Path(json_abs_path).stem

    plt.savefig(filename + ".png", format="PNG")
    plt.show()


if __name__ == "__main__":
    pass
