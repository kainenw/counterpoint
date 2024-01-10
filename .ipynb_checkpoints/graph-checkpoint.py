import networkx as nx
import matplotlib.pyplot as plt
import classes as c


def node_label(position, cf, ctp):
    return str(position) + ":" + str(cf) + "," + str(ctp)


## Pruning Functons
"""Remove all nodes with no path from any first node."""
def remove_unreachable_nodes(graph):
    # find first nodes
    nodes = list(graph.nodes())
    first_nodes = []
    print(nodes)
    for node in nodes:
        print(node)
        print(node.split(":"))
        index = int(node.split(":")[0])
        if index == 0:
            first_nodes.append(node)

    # Create a set of reachable nodes
    reachable_nodes = set(first_nodes)

    # Perform a breadth-first search from each specified node and add all reachable nodes to the set
    for node in first_nodes:
        reachable_nodes.update(nx.descendants(graph, node))

    # Get the set of nodes that are not reachable
    unreachable_nodes = set(graph.nodes()) - reachable_nodes

    # Remove the unreachable nodes from the graph
    graph.remove_nodes_from(unreachable_nodes)

    # Return the modified graph with unreachable nodes removed
    return graph


"""Remove nodes that have no path to any final node."""


def remove_unreaching_nodes(graph, final_index):
    # Create a list of last nodes
    nodes = list(graph.nodes())
    final_nodes = []
    for node in nodes:
        index = int(node.split(":")[0])
        if index == final_index:
            final_nodes.append(node)
    on_path = []

    # add all nodes on a path to the end to on_path.
    while len(nodes) != 0:
        node = nodes.pop()
        is_on_path = None
        if final_nodes.__contains__(node):
            is_on_path = True
        else:
            num_edges = len(list(graph.successors(node)))
            if num_edges != 0:
                # check if node is in graph (avoids error somehow)
                if node in graph:
                    for final_node in final_nodes:
                        if not is_on_path:
                            descendants = nx.descendants(graph, node)
                            if descendants.__contains__(final_node):
                                is_on_path = True
        if is_on_path:
            on_path.append(node)

    # Create a set of all of the nodes that do not have a path to any of the specified nodes.
    unreachable_nodes = set(graph.nodes()) - set(on_path)

    # Remove all of the unreachable nodes from the graph.
    for node in unreachable_nodes:
        graph.remove_node(node)

    return graph

# only works with first species and ctp above
def find_nodes_and_edges(melody_data):
    melody = melody_data["melody"]
    final_index = len(melody) - 1

    all_possibilities = dict()

    nodes = list()
    final_nodes = list()
    first_nodes = list()
    edges = list()

    # find all possible nodes
    for i in range(0, len(melody)):
        note = melody[i]
        current = all_possibilities[i] = []

        # get possible counterpoint notes
        if i == 0:
            possible_ctps = [note, note + 12]
        elif i == final_index:
            possible_ctps = [note, note + 12]
        else:
            possible_ctps = melody_data[str(note)]

        # add nodes for each possible ctp
        for ctp in possible_ctps:
            label = node_label(
                i, note, ctp
            )  # create label: "index, melody note, ctp note"
            current.append(ctp)  # add label to possibilities dictionary
            nodes.append(label)  # add label to nodes list
            if i == 0:
                first_nodes.append(label)
            if i == final_index:
                final_nodes.append(label)

    # find all possible edges
    for key, possibilities in all_possibilities.items():
        if key != final_index:
            note = melody[key]
            index = int(key)

            next_index = index + 1
            next_note = melody[next_index]
            next_possibilities = all_possibilities[next_index]

            for possibility in possibilities:
                label = node_label(index, note, possibility)
                for next_possibility in next_possibilities:
                    # check if move is valid, if so add edge
                    valid = c.isValidMove(
                        note, next_note, possibility, next_possibility
                    )
                    if valid:
                        next_label = node_label(
                            next_index, next_note, next_possibility
                        )
                        edge = (label, next_label)
                        edges.append(edge)
    
    return {"nodes": nodes, "edges": edges, "final_index": final_index}


def make_network(nodes, edges, final_index=None, willPrint=True):
    """
    input:
      1. nodes array ( form: [a,b,c] )
      2. edges array ( form: [(a,b),(b,c)] )
    """

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    if final_index:
        graph = remove_unreachable_nodes(graph)
        graph = remove_unreaching_nodes(graph, final_index)

    # display nodes and edges unless otherwise specified
    if willPrint:
        print(graph.nodes)
        print(graph.edges)
    return graph


def visualize_graph(cf_graph, ctp_graph):
    # Set the spring layout
    cf_pos = nx.spring_layout(cf_graph, seed=42)
    ctp_pos = nx.spring_layout(ctp_graph, seed=42)

    # create dictionary of nodes with (x,y) coordinates
    # cf
    cf_pos_notes = cf_graph.nodes
    cf_pos_coords = {}
    for node in cf_pos_notes.items():
        node = node[0]
        print(node)
        cf = node[1]
        index = node[0]
        print(cf)
        """ print(int(index)) """
        cf_pos_coords[node] = (int(index), int(cf))
    # ctp
    ctp_pos_nodes = ctp_graph.nodes
    ctp_pos_coords = {}
    for node in ctp_pos_nodes.items():
        node = node[0]
        index = node.split(":")[0]
        ctp = node.split(",")[1]
        ctp_pos_coords[node] = (int(index), int(ctp))

    # Set custom positions for nodes
    # cf
    for node, coords in cf_pos_coords.items():
        cf_pos[node] = coords
    # ctp
    for node, coords in ctp_pos_coords.items():
        ctp_pos[node] = coords

    plt.figure(figsize=(2 ^ 16, 2 ^ 16))
    nx.draw(
        ctp_graph,
        cf_pos,
        with_labels=True,
        arrows=True,
        node_size=1200,
        node_shape="s",
        node_color="#3dbbff",
    )
    nx.draw(
        ctp_graph,
        ctp_pos,
        with_labels=True,
        arrows=True,
        node_size=1200,
        node_shape="s",
        node_color="#3dbbff",
    )
