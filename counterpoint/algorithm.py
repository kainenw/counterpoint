import networkx as nx

def node_label(position, cf, ctp):
  duration = 1
  return (position, duration, ctp, cf)

def make_cf_graph(melody):
  nodes = []
  edges = []
  for i in range(len(melody)):
    nodes.append((i, 1, melody[i]))
    if i > 0:
      edges.append(((i-1, 1, melody[i-1]), (i, 1, melody[i])))

  G = nx.DiGraph()
  G.add_nodes_from(nodes)
  G.add_edges_from(edges)

  return G

# only works with first species and ctp above
def make_ctp_graph(melody_data):
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
        if i == 0 or i == final_index:
            possible_ctps = [note, note + 7, note + 12, note + 19]
        elif i == final_index - 1:
            if note > 0:
              possible_ctps = [note + 9]
            elif note < 0:
              possible_ctps = [note + 3, note + 3 + 12]
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
                    valid = is_valid_move(note, next_note, possibility, next_possibility)
                    if valid:
                        next_label = node_label(next_index, next_note, next_possibility)
                        edge = (label, next_label)
                        edges.append(edge)
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    G = remove_unreachable_nodes(G)
    G = remove_unreaching_nodes(G,final_index)

    return G

def remove_unreachable_nodes(graph):
    """
    Remove nodes from a NetworkX graph that are not on a path to any of the specified nodes.

    Args:
        G (nx.Graph or nx.DiGraph): The input graph.
        specified_nodes (list): List of nodes that are considered reachable.

    Returns:
        nx.Graph or nx.DiGraph: The modified graph with unreachable nodes removed.
    """
    # find first nodes
    nodes = list(graph.nodes())
    first_nodes = []
    for node in nodes:
      position = node[0]
      if position == 0:
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

def remove_unreaching_nodes(graph, final_index):
  """Remove nodes from a NetworkX graph that do not have a path to any of the
  nodes in the input array.

  Args:
      G (nx.Graph or nx.DiGraph): The input graph.
      nodes (list): List of nodes that are considered reachable.

  Returns:
      nx.Graph or nx.DiGraph: The modified graph with unreachable nodes removed.
  """
  # Create a list of last nodes
  nodes = list(graph.nodes())
  final_nodes = []
  for node in nodes:
    position = node[0]
    if position == final_index:
      final_nodes.append(node)
  on_path = []

  # add all nodes on a path to the end to on_path.

  while nodes:
    node = nodes.pop()
    is_on_path = None
    for final_node in final_nodes:
      if final_nodes.__contains__(node):
        is_on_path = True
      elif not is_on_path:
        descendants = (nx.descendants(graph, node))
        if descendants.__contains__(final_node):
          is_on_path = True
    if is_on_path:
      on_path.append(node)

  # Create a set of all of the nodes that do not have
  # a path to any of the specified nodes.

  unreaching_nodes = set(graph.nodes()) - set(on_path)

  # Remove all of the unreaching nodes from the graph.
  for node in unreaching_nodes:
    graph.remove_node(node)

  return graph

from counterpoint.primatives import is_consonant, is_direct_perfect

def is_valid_move(prev1, next1, prev2, next2):
    is_cons = is_consonant(next1, next2)
    if is_cons:
        is_dir_perf = is_direct_perfect(prev1, next1, prev2, next2)
        if not is_dir_perf:
            is_in_range = prev2 - 8 <= next2 <= prev2 + 8
            if is_in_range:
                return True
    return False


def get_all_combos(melody, ctp_is_above):
    key = [0,2,4,5,7,9,11]
    mode = melody[0]
    combos = {
        "melody": melody,
        "mode": mode,
        "interval_to_next": [],
        "ctp_is_above": ctp_is_above,
    }
    pre_note = None
    intervals = [3, 4, 7, 8, 9, 12, 16, 19]
    for note in melody:
        possible_notes = []
        for interval in intervals:
            if ctp_is_above:
                possible_note = note + interval
            else:
                possible_note = note - interval
            is_in_key = key.__contains__(possible_note % 12)
            if is_in_key:
                possible_notes.append(possible_note)
        if pre_note != None:
            combos["interval_to_next"].append(note - pre_note)
        combos[str(note)] = possible_notes
        pre_note = note
    return combos

def findCounterpoint(melody):
  counterpoint = []
  # Your code to generate the counterpoint line goes here
  return counterpoint