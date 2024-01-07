import math


# frequency in hertz (Hz)

import math


def ET(octave_divisions):
    # ratio between semitones
    semitone = math.pow(2, 1 / octave_divisions)

    def hz(num):
        ref_hz = 440  # (A4 = 440Hz) reference pitch
        ref_num = 49  # (A4) reference number
        # ratio from base frequency
        distance = num - ref_num

        ratio = math.pow(semitone, distance)

        # return frequency
        return ref_hz * ratio

    tones = list()
    for i in range(0, 88):
        pitch = hz(i)
        tones.append(pitch)

    return tones


# twelve-tone equal temperament
# 49 = A4 = 440Hz
TTET = ET(12)


noteLetters = [
    "C",
    ["C#", "Db"],
    "D",
    ["D#", "Eb"],
    "E",
    "F",
    ["F#", "Gb"],
    "G",
    ["G#", "Ab"],
    "A",
    ["A#", "Bb"],
    "B",
]

"""get the desired note by entering the pitch class and octave number (e.g. (9, 4) which is A4) this allows notes to be referenced intuitively but also for intervals to be retrieved easily. """


def getNoteNum(pitchClass, octave):
    octShift = octave * 12
    noteNum = pitchClass + octShift
    return noteNum


def getOctave(noteNum):
    return math.floor(noteNum / 12)


def getFreq(noteNum):
    noteFreq = freq[noteNum]
    return noteFreq


def getNoteLetter(noteNum):
    mod12 = noteNum % 12
    noteLetter = noteLetters[mod12]
    return noteLetter


print(getFreq(49))
