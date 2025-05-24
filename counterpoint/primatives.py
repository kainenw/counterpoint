class Note:
    def __init__(self, pitch, duration):
        self.pitch = pitch  # e.g., 'C4', 'D#5', MIDI number
        self.duration = duration # e.g., 'quarter', 'half', in beats

    def __repr__(self):
        return f"Note(pitch='{self.pitch}', duration='{self.duration}')"

class Interval:
    def __init__(self, note1, note2):
        self.note1 = note1
        self.note2 = note2
        # Calculate interval based on pitches (simplified)
        # This is a placeholder and would need actual musical interval calculation logic
        self.semitones = abs(note1.pitch - note2.pitch) if isinstance(note1.pitch, int) and isinstance(note2.pitch, int) else None

    def __repr__(self):
        return f"Interval(note1={self.note1.pitch}, note2={self.note2.pitch}, semitones={self.semitones})"

class Melody:
    def __init__(self, notes):
        if not all(isinstance(note, Note) for note in notes):
            raise TypeError("Melody must consist of Note objects")
        self.notes = notes

    def __repr__(self):
        return f"Melody(notes={self.notes})"

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, index):
        return self.notes[index]

class CounterpointEngine:
    def __init__(self, melody):
        if not isinstance(melody, Melody):
            raise TypeError("CounterpointEngine requires a Melody object")
        self.melody = melody

    def generate_counterpoint(self):
        # This is a placeholder for counterpoint generation logic
        # It would involve analyzing the melody and applying counterpoint rules
        print(f"Generating counterpoint for melody: {self.melody}")
        # Return a new Melody object representing the generated counterpoint
        return Melody([]) # Return an empty melody as a placeholder

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
    print(f"Generated counterpoint: {counterpoint_melody}")