# %%
import networkx as nx
import matplotlib.pyplot as plt

# %%
def node_label(position, cf, ctp):
  duration = 1
  return (position, duration, ctp, cf)

# change to position, note, duration

# %%
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


# %%
# only works with first species and ctp above
def make_ctp_graph(melody_data, ctp_above=True):
    melody = melody_data["melody_notes"]
    num_positions = len(melody)
    final_index = num_positions - 1

    G = nx.DiGraph()

    # Generate nodes and potential edges in a single pass
    for i in range(num_positions):
        note = melody[i]
 
        if i == 0 or i == final_index:
            if ctp_above:
                possible_ctps = [note + 12, note + 19] # Octave and 12th above
            else:
                possible_ctps = [note - 12, note - 19] # Octave and 12th below
        elif i == final_index - 1:
            if ctp_above:
                possible_ctps = [note + 9] # Leading tone above (major 7th)
            else:
                possible_ctps = [note - 3, note - 3 - 12] # Leading tone below (minor 3rd and 10th)
        else:
            if ctp_above:
                possible_ctps = melody_data[str(note)]["above"]
            else:
                possible_ctps = melody_data[str(note)]["below"]
        for ctp in possible_ctps:
            current_node = node_label(i, note, ctp)
            G.add_node(current_node)


            if i < final_index:
                next_index = i + 1
                next_note = melody[next_index]
                next_possible_ctps = melody_data[str(next_note)]["above"] if ctp_above else melody_data[str(next_note)]["below"]

                for next_ctp in next_possible_ctps:
                    valid = first.is_valid_move(note, next_note, ctp, next_ctp, ctp_above=ctp_above)
                    if valid:
                        next_node = node_label(next_index, next_note, next_ctp)
                        G.add_edge(current_node, next_node)

    G = prune_graph(G, final_index)
    
    return G


# %% [markdown]
# ## Pruning Functons

# %%
def prune_graph(graph, final_index):
    """Prunes the graph by removing nodes unreachable from the start and nodes that don't have a path to the end."""
    # Remove nodes unreachable from the start
    first_nodes = [node for node in graph.nodes() if node[0] == 0]
    reachable_from_start = set(first_nodes)
    for node in first_nodes:
        reachable_from_start.update(nx.descendants(graph, node))
    unreachable_nodes = set(graph.nodes()) - reachable_from_start
    graph.remove_nodes_from(unreachable_nodes)

    # Remove nodes that don't have a path to the end
    final_nodes = [node for node in graph.nodes() if node[0] == final_index]
    reachable_to_end = set(final_nodes)
    for node in final_nodes:
        reachable_to_end.update(nx.ancestors(graph, node))
    unreaching_nodes = set(graph.nodes()) - reachable_to_end
    graph.remove_nodes_from(unreaching_nodes)

    return graph


# %%
def visualize_network(G, solution_path=None):
    pos = {}
    cf_notes_pos = {}
    cf_notes_labels = {}

    for node in G.nodes():
        position, duration, ctp, cf_note = node
        pos[node] = (position, ctp) # X=position, Y=counterpoint pitch
        cf_notes_pos[(position, cf_note)] = (position, cf_note)
        cf_notes_labels[(position, cf_note)] = str(cf_note)

    plt.figure(figsize=(12, 6)) # Adjust figure size as needed

    # Draw all nodes and edges (greyed out)
    nx.draw(G, pos, with_labels=False, node_size=100, node_color='lightgray', edge_color='lightgray', arrows=False)

    # Draw cantus firmus notes
    nx.draw_networkx_nodes(G, cf_notes_pos, node_size=200, node_color='skyblue', marker='s')
    nx.draw_networkx_labels(G, cf_notes_pos, cf_notes_labels, font_size=8)

    # If a solution path is provided, highlight it
    if solution_path:
        solution_edges = [(solution_path[i], solution_path[i+1]) for i in range(len(solution_path)-1)]
        nx.draw_networkx_nodes(G, pos, nodelist=solution_path, node_color='red', node_size=200)
        nx.draw_networkx_edges(G, pos, edgelist=solution_edges, edge_color='red', width=2, arrows=True)

    plt.title("Counterpoint Graph and Solution")
    plt.xlabel("Position")
    plt.ylabel("Pitch")
    plt.grid(True)

# %%
import first

melody = [0,4,9,7,4,2,0]
melody_data = first.get_all_combos(melody)
# print("melody data:", melody_data)

ctp_graph = make_ctp_graph(melody_data)
# print("network:", ctp_graph)
visualize_network(ctp_graph)

cf_graph = make_cf_graph(melody)
# print("network:", cf_graph)
visualize_network(cf_graph)

