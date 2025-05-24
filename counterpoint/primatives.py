import networkx as nx

from counterpoint.exceptions import NoCounterpointFoundError
class Note: # type: ignore
    """
    Represents a musical note with a pitch and duration.
    """
    def __init__(self, pitch, duration):
        """
        Initializes a Note object.

        Args:
            pitch: The pitch of the note. Can be a string (e.g., 'C4', 'D#5')
                   or a MIDI number (integer).
            duration: The duration of the note (e.g., 'quarter', 'half', in beats).
        """
        self.pitch = pitch  # e.g., 'C4', 'D#5', MIDI number
        self.duration = duration  # e.g., 'quarter', 'half', in beats

    def __repr__(self):
        return f"Note(pitch='{self.pitch}', duration='{self.duration}')"

class Interval:
    def __init__(self, note1, note2):
        self.note1 = note1
        self.note2 = note2
        # Calculate interval based on pitches (simplified)
        """
        Represents a musical interval between two notes.

        Args:
            note1 (Note): The first note.
            note2 (Note): The second note.
        """
        # This is a placeholder and would need actual musical interval calculation logic
        self.semitones = abs(note1.pitch - note2.pitch) if isinstance(note1.pitch, int) and isinstance(note2.pitch, int) else None

    def __repr__(self):
        return f"Interval(note1={self.note1.pitch}, note2={self.note2.pitch}, semitones={self.semitones})"

class Melody:
    def __init__(self, notes):
        """
        Represents a sequence of musical notes.

        Args:
            notes (list[Note]): A list of Note objects forming the melody.
        Raises:
            TypeError: If any element in the input list is not a Note object.
        """
        if not all(isinstance(note, Note) for note in notes):
            raise TypeError("Melody must consist of Note objects")
        self.notes = notes

    def __repr__(self):
        return f"Melody(notes={self.notes})"

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, index):
        return self.notes[index]

def is_consonant(note1, note2):
    """Checks if the interval between two notes is consonant."""
    # Simplified check for consonance based on semitone difference
    # This should be expanded to include all consonant intervals
    interval = abs(note1 - note2) % 12
    print(f"is_consonant interval: {interval}")
    if note1 == 2 and note2 == 13:
        print(f"is_consonant(2, 13) - note1: {note1}, note2: {note2}, interval: {interval}")
    return interval in [0, 3, 4, 7, 8, 9] # Unison, minor 3rd, major 3rd, perfect 5th, minor 6th, major 6th (and their octaves)

def is_direct_perfect(prev1, next1, prev2, next2):
    """
    Checks for direct perfect intervals (unisons, fifths, or octaves) where
    both voices move in the same direction.
    Checks for direct perfect fifths or octaves.

    Args:
        prev1: The previous note in the first voice.
        next1: The current note in the first voice.
        prev2: The previous note in the second voice.
        next2: The current note in the second voice.

    Returns:
        bool: True if there is a direct perfect fifth or octave, False otherwise.
    """
    interval_prev = abs(prev1 - prev2) % 12
    interval_next = (next2 - next1) % 12 # Calculate interval from first voice to second voice
    # Check if the destination interval is a perfect fifth or octave (or unison)
    is_perfect_next = interval_next % 12 in [0, 7]
    # Check if voices move in the same direction
    same_direction = (next1 - prev1 > 0 and next2 - prev2 > 0) or (next1 - prev1 < 0 and next2 - prev2 < 0)

    if prev1 == 0 and next1 == 7 and prev2 == 12 and next2 == 19:
        print(f"is_direct_perfect(0, 7, 12, 19) - is_perfect_next: {is_perfect_next}, same_direction: {same_direction}, result: {is_perfect_next and same_direction}")

    return is_perfect_next and same_direction

class CounterpointEngine:
    def __init__(self, melody):
        """
        Args:
            melody (Melody): The cantus firmus melody as a Melody object.
        Raises:
            TypeError: If the input is not a Melody object.
        """
        if not isinstance(melody, Melody):
            raise TypeError("CounterpointEngine requires a Melody object")
        self.melody = melody

    def generate_counterpoint(self) -> Melody or None:
        """
        Generates a counterpoint melody for the engine's cantus firmus.

        Returns:
            Melody: A Melody object representing the generated counterpoint.
        """
        from counterpoint.algorithm import get_all_combos, make_ctp_graph
        print(f"Generating counterpoint for melody: {self.melody}")
        # Extract pitches from the input melody
        melody_pitches = [note.pitch for note in self.melody.notes]

        # 1. Get all possible combinations
        melody_data = get_all_combos(melody_pitches, True) # Assuming ctp_is_above is True for now

        # 2. Make the counterpoint graph
        ctp_graph = make_ctp_graph(melody_data)

        # Find start and end nodes
        start_nodes = [n for n in ctp_graph.nodes() if n[0] == 0]
        end_nodes = [n for n in ctp_graph.nodes() if n[0] == len(melody_pitches) - 1]

        counterpoint_pitches = []
        shortest_path = None
        shortest_path_length = float('inf')

        # Iterate through all possible start and end nodes to find the overall shortest path
        for start_node in start_nodes:
            for end_node in end_nodes:
                try:
                    path = nx.dijkstra_path(ctp_graph, source=start_node, target=end_node, weight='weight')
                    path_length = nx.dijkstra_path_length(ctp_graph, source=start_node, target=end_node, weight='weight')
                    if path_length < shortest_path_length:
                        shortest_path_length = path_length
                        shortest_path = path
                except nx.NetworkXNoPath:
                    # No path exists between this start and end node
                    pass

        if shortest_path:
            counterpoint_pitches = [node[2] for node in shortest_path]
            counterpoint_notes = [Note(pitch, self.melody.notes[i].duration) for i, pitch in enumerate(counterpoint_pitches)]
            return Melody(counterpoint_notes)
        else:
            raise NoCounterpointFoundError("No valid counterpoint could be generated for the given melody.")

if __name__ == '__main__':
    # Example Usage:
    note1 = Note(60, 'quarter') # MIDI number for C4
    note2 = Note(62, 'quarter') # MIDI number for D4
    note3 = Note(64, 'half')    # MIDI number for E4

    interval = Interval(note1, note2)
    print(interval)

    melody = Melody([note1, note2, note3])
    print(melody)

    engine = CounterpointEngine(melody)
    counterpoint_melody = engine.generate_counterpoint()
    print(f"Generated counterpoint: {counterpoint_melody}") # This will likely be an empty melody until the findCounterpoint logic is fully implemented and tested

    # Example with simple integer pitches for testing
    melody_pitches_example = [60, 62, 64, 65, 67, 69, 71, 72] # C4 to C5 scale
    melody_notes_example = [Note(p, 'quarter') for p in melody_pitches_example]
    melody_example = Melody(melody_notes_example)

    engine_example = CounterpointEngine(melody_example)
    counterpoint_example = engine_example.generate_counterpoint()
    print(f"Generated counterpoint example: {counterpoint_example}")