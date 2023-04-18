import sys
print(sys.path)

import networkx as nx
import matplotlib.pyplot as plt


def node_label(position, cf, ctp):
  return str(position) + ':' + str(cf) + ',' + str(ctp)


## Pruning Functons


"""Remove all nodes with no path from any first node."""
def remove_unreachable_nodes(graph):
  # find first nodes
  nodes = list(graph.nodes())
  first_nodes = []
  for node in nodes:
    index = int(node.split(':')[0])
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
    index = int(node.split(':')[0])
    if index == final_index:
      final_nodes.append(node)
  on_path = []

  # add all nodes on a path to the end to on_path.
  while nodes:
    node = nodes.pop()
    is_on_path = None
    for final_node in final_nodes:
      if final_node.__contains__(node):
        is_on_path = True
      elif not is_on_path:
        descendants = (nx.descendants(graph, node))
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


def make_network(nodes, edges, final_index, willPrint=True):
  """
  input:
    1. nodes array ( form: [a,b,c] )
    2. edges array ( form: [(a,b),(b,c)] )
  """
  
  graph = nx.DiGraph()
  graph.add_nodes_from(nodes)
  graph.add_edges_from(edges)
  
  graph = remove_unreachable_nodes(graph)
  graph = remove_unreaching_nodes(graph,final_index)
  
  # display nodes and edges unless otherwise specified
  if willPrint:
    print(graph.nodes)
    print(graph.edges)
  
  return graph


def visualize_graph(G):
  # Set the spring layout with custom node positions
  pos = nx.spring_layout(G, seed=42)

  #create dictionary of nodes with (x,y) coordinates
  pos_nodes = G.nodes
  pos_coords = {}
  for node in pos_nodes.items():
    node = node[0]
    index = node.split(':')[0]
    ctp = node.split(',')[1]
    pos_coords[node] = (int(index), int(ctp))

  # Set custom positions for nodes
  for node, coords in pos_coords.items():
    pos[node] = coords
  
  nx.draw(G, pos, with_labels=True, arrows=True)
  plt.figure(figsize = (2^16,2^16))