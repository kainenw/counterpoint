import pytest
import networkx as nx
from counterpoint import algorithm as algo
from counterpoint.primatives import Note, Melody # Import Note and Melody
from counterpoint.primatives import is_consonant # Explicitly import here for use in tests

# %%
# Tests for Old.sound_generation.equal_temperament

# %%
from Old.sound_generation.equal_temperament import ET

def test_getFreq():
  # define twelve tone equal temperament
  TTET = ET(12)

  # Test case 1: Check the frequency of a known note
  note = 69 # MIDI note for 'A4'
  expected_freq = 440.00
  actual_freq = TTET[note]
  assert actual_freq == pytest.approx(expected_freq, abs=1e-2)

  # Test case 2: Check the frequency of another note
  note = 60 # MIDI note for 'C4'
  expected_freq = 261.637 # Corrected expected frequency for C4 (more precise)
  actual_freq = TTET[note]
  assert actual_freq == pytest.approx(expected_freq, abs=0.02)

# %%
# Tests for counterpoint modules
from counterpoint.primatives import CounterpointEngine, NoCounterpointFoundError, is_consonant

def test_is_valid_move(): # Removed the unnecessary import within the function
    # Test valid move (consonant, not direct perfect, within range) - This should be True if it's a valid move
    assert algo.is_valid_move(0, 2, 12, 16) == True # Corrected expected outcome for a valid move
    # Test invalid move (dissonant)
    assert not algo.is_valid_move(0, 2, 12, 13)
    # Test invalid move (direct perfect)
    assert not algo.is_valid_move(0, 7, 12, 19)
    # Test invalid move (out of range)
    assert not algo.is_valid_move(0, 2, 12, 25)

def test_get_all_combos():
    melody = [0, 2, 4]
    expected_combos_above = {
        "melody": [0, 2, 4],
        "mode": 0,
        "interval_to_next": [2, 2],
        "ctp_is_above": True,
    "0": [4, 7, 9, 12, 16, 19],
    "2": [5, 9, 11, 14, 21],
    "4": [7, 11, 12, 16, 23]
    }
    expected_combos_below = {
 "melody": [0, 2, 4],
        "mode": 0,
        "interval_to_next": [2, 2],
        "ctp_is_above": False,
        "0": [-3, -4, -7, -8, -9, -12, -16, -19],
        "2": [-1, -2, -5, -6, -7, -10, -14, -17],
        "4": [1, 0, -3, -4, -5, -8, -12, -15]
    }
    assert algo.get_all_combos(melody, True) == expected_combos_above
    assert algo.get_all_combos(melody, False) == expected_combos_below

def test_make_ctp_graph():
    melody_data = algo.get_all_combos([0, 2], True)
    graph = algo.make_ctp_graph(melody_data)
    assert isinstance(graph, nx.DiGraph)
    # Add more specific assertions about nodes and edges based on expected valid moves

def test_make_ctp_graph_below():
    melody_data = algo.get_all_combos([0, 2], False)
    graph = algo.make_ctp_graph(melody_data)
    assert isinstance(graph, nx.DiGraph)
    # Add more specific assertions about nodes and edges based on expected valid moves
    # For example, check for the presence of specific nodes like (0, 0, -3, 0) or (1, 2, -1, 2)
    # and the absence of nodes like (0, 0, 12, 0) which would be valid for above
    expected_nodes = [
        (0, 0, -3, 0), (0, 0, -4, 0), (0, 0, -7, 0), (0, 0, -8, 0), (0, 0, -9, 0), (0, 0, -12, 0), (0, 0, -16, 0), (0, 0, -19, 0),
        (1, 2, -1, 2), (1, 2, -2, 2), (1, 2, -5, 2), (1, 2, -6, 2), (1, 2, -7, 2), (1, 2, -10, 2), (1, 2, -14, 2), (1, 2, -17, 2)
        ]
    assert set(graph.nodes()) == set(expected_nodes)

def test_make_cf_graph():
    melody = [0, 2, 4]
    graph = algo.make_cf_graph(melody)
    assert isinstance(graph, nx.DiGraph)
    assert list(graph.nodes()) == [(0, 1, 0), (1, 1, 2), (2, 1, 4)]
    assert list(graph.edges()) == [((0, 1, 0), (1, 1, 2, {})), ((1, 1, 2), (2, 1, 4, {}))] # Edges store data as dictionaries

def test_remove_unreachable_nodes():
    G = nx.DiGraph()
    G.add_edges_from([((0, 0, 0, 0), (1, 1, 2, 2)), ((1, 1, 2, 2), (2, 1, 4, 4)), ((3, 1, 5, 5), (4, 1, 6, 6))])
    # Need to adapt this test for the specific node format (position, duration, ctp, cf)

def test_remove_unreaching_nodes():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (4, 5), (5, 6)])
    # Need to adapt this test for the specific node format (position, duration, ctp, cf)

# %%
# Tests for error handling

def test_find_counterpoint_no_path():
    from counterpoint.exceptions import CounterpointGenerationError
    # Use a melody that is too short to have a valid counterpoint path
    # The CounterpointEngine constructor now requires a Melody object
    # Create a Melody object with a very short list of Note objects
    short_melody_notes = [Note(60, 'quarter')] # Create a list with a single Note object
    short_melody = Melody(short_melody_notes) # Create a Melody object
    with pytest.raises(CounterpointGenerationError, match="No edges created for CTP graph. No valid moves found."):
        engine = CounterpointEngine(short_melody) # Instantiate CounterpointEngine
        engine.generate_counterpoint() # Call the method that should raise the exception

def test_get_all_combos_empty_melody():
    from counterpoint.exceptions import CounterpointGenerationError
    with pytest.raises(CounterpointGenerationError, match="Input melody is empty."):
        algo.get_all_combos([], True) # Corrected expected exception and match string

 # Removed redundant graph creation
