# %%
import unittest

from first import allPossibleMoves, getAllNextMoves, getAllPossibleCpts

testLowerCf = {
  "a": [0, 4, 9, 5, 7, 0],
  "b": [0, 2, 5, 4, 0, 2, 7, 5, 0],
  "c": [0, 5, 4, 9, 7, 12, 11, 7, 5, 0, 2, 0],
  "d": [0, 4, 2, 5, 4, 7, 5, 9, 7, 11, 9, 12, 11, 12],
  "e": [0, 2, 4, 5, 7, 9, 11, 12, 11, 9, 7, 5, 4, 2, 0],
  "f": [0, 2, 7, 5, 7, 11, 9, 4, 5, 2, 4, 5, 5, 2, 4, 0],
}

testHigherCf = {
  "a": [12, 9, 4, 7, 5, 12],
  "b": [12, 11, 7, 9, 11, 12],
  "c": [12, 11, 9, 7, 5, 4, 2, 0],
  "d": [12, 11, 7, 9, 12, 11, 5, 7, 12],
  "e": [12, 9, 11, 12, 7, 9, 5, 7, 9, 11, 12],
  "f": [12, 7, 9, 4, 5, 0, 2, 5, 7, 12, 11, 12],
  "g": [12, 9, 11, 7, 9, 5, 7, 4, 5, 2, 4, 0, 2, 0],
  "h": [12, 11, 9, 7, 5, 4, 2, 0, 2, 4, 5, 7, 9, 11, 12],
  "i": [12, 11, 5, 7, 5, 2, 4, 9, 7, 11, 9, 7, 7, 11, 9, 12],
}

moves = allPossibleMoves([])

class nextDict(unittest.TestCase):
  def test_nextDict(self):
    input = {
      'moves': [[0,12]],
      '[0, 12]': [[[0,12]]],
    }

    expected = {
      'moves': [[2, 11],[2, 9],[2, 17],[2, 5]],
      '[2, 11]': [[[0, 12],[2, 11]]],
      '[2, 17]': [[[0, 12],[2, 17]]],
      '[2, 9]': [[[0, 12], [2, 9]]],
      '[2, 5]': [[[0, 12], [2, 5]]]
    }
    actual = getAllNextMoves(input, 2)
    self.assertEqual(expected, actual)



if __name__ == '__main__':
  unittest.main()




# %%
import classes as c
import first as f
import graph as g

melody_data = c.getAllCombos(testLowerCf["f"], True)
ctp_nodes_and_edges = f.find_nodes_and_edges(melody_data)
cf_nodes_and_edges = f.cf_make_nodes_and_edges(testLowerCf["f"])
print(ctp_nodes_and_edges)
ctp_graph = g.make_network(ctp_nodes_and_edges["nodes"], ctp_nodes_and_edges["edges"], ctp_nodes_and_edges["final_index"])
cf_graph = g.make_network(cf_nodes_and_edges["nodes"], cf_nodes_and_edges["edges"], cf_nodes_and_edges["final_index"])
g.visualize_graph(cf_graph, ctp_graph)


# %%
import sys
from equal_temperament import ET

class MyTest(unittest.TestCase):
  def test_getFreq(self):
    # define twelve tone equal temperament
    TTET = ET(12)

    # Test case 1: Check the frequency of a known note
    note = 49 # 'A4'
    expected_freq = 440.00
    actual_freq = TTET[note]
    self.assertAlmostEqual(actual_freq, expected_freq, places=2)

    # Test case 2: Check the frequency of another note
    note = 52 # 'C4'
    expected_freq = 261.63
    actual_freq = TTET[note]
    self.assertAlmostEqual(actual_freq, expected_freq, places=2)

if __name__ == '__main__':
  unittest.main()
  sys.path.append('../sound_generation/equal_temperament.py')



# %% [markdown]
# equal_temperament test

# %%
import equal_temperament

ttet = equal_temperament.TTET()


# %%
import unittest
import sys
sys.path.append('../sound_generation/equal_temperament.py')
from equal_temperament import ET

class MyTest(unittest.TestCase):
  def test_getFreq(self):
    # define twelve tone equal temperament
    TTET = ET(12)

    # Test case 1: Check the frequency of a known note
    note = 49 # 'A4'
    expected_freq = 440.00
    actual_freq = TTET[note]
    self.assertAlmostEqual(actual_freq, expected_freq, places=2)

    # Test case 2: Check the frequency of another note
    note = 52 # 'C4'
    expected_freq = 261.63
    actual_freq = TTET[note]
    self.assertAlmostEqual(actual_freq, expected_freq, places=2)

# %%
import unittest

def transform_array_to_dict(arr):
  # Transform the array into a dictionary
  # Your implementation here
  pass

class ArrayToDictTest(unittest.TestCase):
  def test_transform_array_to_dict(self):
    arr = [1, 2, 3, 4]
    expected_dict = {1: 1, 2: 2, 3: 3, 4: 4}
    actual_dict = transform_array_to_dict(arr)
    self.assertEqual(expected_dict, actual_dict)

if __name__ == '__main__':
  unittest.main()



