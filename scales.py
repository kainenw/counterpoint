import classes
import random

keys = []


def add(num1, num2):
    return int(num1 + num2)


key = [0, 2, 4, 5, 7, 9, 11]
circle_of_fifths = [
    0,
    7,
    2,
    9,
    4,
    11,
    6,
    1,
    8,
    3,
    10,
    5,
]


def generate_key(position):
    center = circle_of_fifths[position]
    scale = []
    for note in key:
        scale.append((center + note) % 12)
    return scale


print(generate_key(4))

scales = {
    "dia": {
        "i": [0, 2, 4, 5, 7, 9, 11],
        "d": [0, 2, 3, 5, 7, 9, 10],
        "p": [0, 1, 3, 5, 7, 8, 10],
        "ly": [0, 2, 4, 6, 7, 9, 11],
        "m": [0, 2, 4, 5, 7, 9, 10],
        "a": [0, 2, 3, 5, 7, 8, 10],
    },
    "pent": {"0": {0, 2, 4, 6, 8, 10}, "1": {1, 3, 5, 7, 9, 11}},
    "oct": {
        "0,1": {0, 1, 3, 4, 6, 7, 9, 10},
        "0,2": {0, 2, 3, 5, 6, 8, 9, 11},
        "1,2": {1, 2, 4, 5, 7, 8, 10, 11},
    },
}


def getGamut(melody):
    # detects mode of a diatonic melody, arbitrarily selects compatible modes when mode is ambiguous, will return incorrect results for non-diatonic melodies
    firstPitch = melody[0]
    gamut = []
    for note in melody:
        # transpose down so pitch center is 0
        adjusted = (note - firstPitch) % 12

        # add adjusted pitch-class to gamut unless it is already there
        if not gamut.__contains__(adjusted):
            gamut.append(adjusted)
    return gamut


def isInGamut(note, mode):
    contains = mode.__contains__(classes.pitchClass(note))
    return contains


# chat gpt generated
def matching_modes(input_arr):
    """
    Returns a list of keys for the lists in diatonic_modes which contain input_arr.
    """
    matching_keys = []
    # diatonic dictionary containing the six diatonic modes
    for key, arr in scales["dia"].items():
        if arr == input_arr or all(elem in arr for elem in input_arr):
            matching_keys.append(key)
    if matching_keys == []:
        raise ValueError(
            "The mode is not diatonic. Only diatonic modes are allowed for now."
        )
    return matching_keys


def detectMode(melody):
    gamut = getGamut(melody)
    mode = matching_modes(gamut)
    if len(mode) == 1:
        mode = mode[0]
    elif len(mode) > 1:
        # arbitrarily pick a compatible mode
        index_length = len(mode) - 1
        num = round(random.random() * index_length)
        mode = mode[num]
    return scales['dia'][mode]


def isInGamut(note, mode):
    contains = mode.__contains__(classes.pitchClass(note))
    return contains
