import math

# frequency in hertz (Hz)
def ET(octave_divisions):
    # ratio between semitones
    class EqualTemperament:
        def __init__(self, octave_divisions):
            self.semitone = math.pow(2, 1 / octave_divisions)
            self.ref_hz = 440  # (A4 = 440Hz) reference pitch
            self.ref_num = 69  # (A4) reference number

        def __getitem__(self, note_num):
            distance = note_num - self.ref_num
            ratio = math.pow(self.semitone, distance)
            return self.ref_hz * ratio
    semitone = math.pow(2, 1 / octave_divisions)

    def hz(num):
        ref_hz = 440  # (A4 = 440Hz) reference pitch
        ref_num = 69  # (A4) reference number
        # ratio from base frequency
        distance = num - ref_num

        ratio = math.pow(semitone, distance)

        # return frequency
        return ref_hz * ratio

    return EqualTemperament(octave_divisions)
# twelve-tone equal temperament
# 49 = A4 = 440Hz
TTET = ET(12)


noteLetters = [
    ["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"], ["F"],
    ["F#", "Gb"], ["G"], ["G#", "Ab"], ["A"], ["A#", "Bb"], ["B"]
]

"""get the desired note by entering the pitch class and octave number (e.g. (9, 4) which is A4) this allows notes to be referenced intuitively but also for intervals to be retrieved easily. """


def getNoteNum(pitch_class, octave):
    if not (0 <= pitch_class <= 11):
        raise ValueError("pitch_class must be between 0 and 11")
    return pitch_class + octave * 12


def getOctave(noteNum):
    return math.floor(noteNum / 12)


def getNoteLetter(noteNum):
    mod12 = noteNum % 12
    noteLetter = noteLetters[mod12]
    return noteLetter


