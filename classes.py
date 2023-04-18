import random

# pitch class from 0 to 12
def pitchClass(num):
  return num % 12

# interval class from -6 to 6
def intervalClassModTwelve(num1, num2):
  interval = num1 - num2
  intervalClass = abs(interval) % 12
  if(intervalClass > 6):
    mod6 = intervalClass % 6
    return -6 + mod6
  else:
    return intervalClass

# interval categories
consonance = {
  'perfect': [0, 5],
  'imperfect': [3, 4]
}
dissonance = [1, 2, 6]

def isConsonant(num1,num2):
  mod = intervalClassModTwelve(num1,num2)
  absVal = abs(mod)
  # perfect 4ths (categorized as positive 5) are not counted as consonants by Fux in 1st species
  if (consonance["perfect"].__contains__(absVal) and mod != 5):
    return "perfect"
  elif (consonance["imperfect"].__contains__(absVal)):
    return "imperfect"
  else:
    return False

# Direct: > 0
# Oblique: == 0
# Contrary: < 0
def motion(prev1,next1,prev2,next2):
  interval1 = prev1 - prev2
  interval2 = next1 - next2
  motion = interval1 * interval2
  return motion

def isParallelPerfect(prev1,next1,prev2,next2):
  interval1 = prev1 - next1
  interval2 = prev2 - next2
  isDirect = motion(prev1,next1,prev2,next2) > 0
  isParallel = isDirect and interval1 == interval2
  mod = intervalClassModTwelve(prev1,prev2)
  isPerfect = consonance["perfect"].__contains__(abs(mod))
  return isParallel and isPerfect

def isInGamut(note, mode):
  contains = mode.__contains__(pitchClass(note))
  return contains

def isValidMove(prev1,next1,prev2,next2):
  isCons = isConsonant(next1,next2) != False
  isParPerf = isParallelPerfect(prev1,next1,prev2,next2)
  isNotParPerf = not isParPerf
  isInRange = prev2 - 8 <= next2 <= prev2 + 8
  isValid = isCons & isInRange & isNotParPerf
  return isValid

diatonic_modes = {
  "ionian": [0,2,4,5,7,9,11],
  "lydian": [0,2,4,6,7,9,11],
  "mixolydian": [0,2,4,5,7,9,10],
  "dorian": [0,2,3,5,7,9,10],
  "phrygian": [0,1,3,5,7,8,10],
  "aeolean": [0,2,3,5,7,8,10]
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

#chat gpt generated
def matching_modes(input_arr):
    """
    Returns a list of keys for the lists in diatonic_modes which contain input_arr.
    """
    matching_keys = []
    # diatonic dictionary containing the six diatonic modes
    for key, arr in diatonic_modes.items():
        if arr == input_arr or all(elem in arr for elem in input_arr):
            matching_keys.append(key)
    if matching_keys == []:
      raise ValueError("The mode is not diatonic. Only diatonic modes are allowed for now.")
    return matching_keys

def detectMode(melody):
  gamut = getGamut(melody)
  mode = matching_modes(gamut)
  if len(mode) == 1:
    mode = mode[0]
  elif len(mode) > 1:
    #arbitrarily pick a compatible mode
    index_length = len(mode) -1
    num = round(random.random() * index_length)
    mode = mode[num]
  return diatonic_modes[mode]

def getAllCombos(melody, ctpIsAbove):
  mode = detectMode(melody)
  combos = {
    'melody': melody,
    'mode': mode,
    'intervalToNext': [],
    'ctpIsAbove': ctpIsAbove
  }
  prevNote = None
  intervals = [3,4,7,8,9,12,16,19]
  for note in melody:
    possibleNotes = []
    for interval in intervals:
      if ctpIsAbove:
        possibleNote = note + interval
      else:
        possibleNote = note - interval
      if isInGamut(possibleNote, mode):
        possibleNotes.append(possibleNote)
    if(prevNote != None):
      combos["intervalToNext"].append(note - prevNote)
    combos[str(note)] = possibleNotes
    prevNote = note
  return combos