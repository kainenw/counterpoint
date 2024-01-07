""" # %%
pip install -r requirements.txt """

import classes as c
import scales as s


def isValidMove(prev1, next1, prev2, next2):
    if prev2 - 8 <= next2 <= prev2 + 8:
        next_is_consonant = c.isConsonant(next1, next2)
        if next_is_consonant != False:  # the function will return a string if true
            if c.isParallelPerfect(prev1, next1, prev2, next2):
                return True
    return False


def getAllCombos(melody, ctpIsAbove):
    mode = s.detectMode(melody)
    combos = {
        "melody": melody,
        "mode": mode,
        "intervalToNext": [],
        "ctpIsAbove": ctpIsAbove,
    }
    prevNote = None
    intervals = [3, 4, 7, 8, 9, 12, 16, 19]
    for note in melody:
        possibleNotes = []
        for interval in intervals:
            if ctpIsAbove:
                possibleNote = note + interval
            else:
                possibleNote = note - interval
            if s.isInGamut(possibleNote, mode):
                possibleNotes.append(possibleNote)
        if prevNote != None:
            combos["intervalToNext"].append(note - prevNote)
        combos[str(note)] = possibleNotes
        prevNote = note
    return combos


# todo: see trello
def justifiableLeap(graph, edge):
    outNode = edge[0]
    inNode = edge[1]


# %%
import random


def randomMelody(length, mode):
    melody = []
    for i in range(length):
        melody.append(random.choice(mode))
    return melody
