from scales import scales

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
intervals = {
  'consonances': {
    'perfect': [0, 5],
    'imperfect': [3, 4]
  },
  'dissonances': {1, 2, 6},
}

def isConsonant(num1, num2):
  mod = intervalClassModTwelve(num1, num2)
  absVal = abs(mod)
  # perfect 4ths (categorized as positive 5) are not counted as consonants by Fux in 1st species
  if (intervals["consonances"]["perfect"].__contains__(absVal) and mod != 5):
    return "perfect"
  elif intervals["consonances"]["imperfect"].__contains__(absVal):
    return "imperfect"
  else:
    return False

def isDirect(prev1,next1, prev2,next2):
  interval1 = prev1 - next1
  interval2 = prev2 - next2
  isDirect = interval1 * interval2  > 0
  return isDirect

# rewrite to only care about parallel perfect intervals
# return what kind of motion is occuring between two notes
def isDirectPerfect(prev1,next1, prev2,next2):
  interval1 = prev1 - prev2
  interval2 = next1 - next2
  isDirect = interval1 * interval2 > 0
  isCons = isConsonant(next1, next2)
  isPerfect = isCons == "perfect"
  return isDirect and isPerfect

def isInGamut(note, gamutType = "dia", mode = "i"):
  gamut = scales[gamutType][mode]
  contains = gamut.__contains__(pitchClass(note))
  return contains

def isValidMove(prevCf, nextCf, prevCtp, nextCtp):
  isCons = isConsonant(nextCf, nextCtp) != False
  isDirPerf = isDirectPerfect(prevCf, nextCf, prevCtp, nextCtp)
  isNotDirPerf = not isDirPerf
  isInRange = prevCtp - 12 <= nextCtp <= prevCtp + 12
  """ print("isCons: " + str(isCons) + "isInRange: " + str(isInRange) + "isNotDirPerf: " + str(isNotDirPerf)) """
  isValid = isCons & isInRange & isNotDirPerf
  """ print("isValid" + str(isValid)) """
  return isValid

from classes import intervalClassModTwelve

# todo detect gamut type and mode
def getAllCombos(melody, ctpAbove, gamutType = "dia", mode = "i"):
  combos = {
    'melody': melody,
    'intervalToNext': [],
    'ctpIsAbove': ctpAbove
  }
  prevNote = None
  intervals = [3,4,7,8,9,12,16,19]
  for note in melody:
    possibleNotes = []
    for interval in intervals:
      if ctpAbove:
        possibleNote = note + interval
      else:
        possibleNote = note - interval
      if isInGamut(possibleNote, gamutType, mode):
        possibleNotes.append(possibleNote)
    if(prevNote != None):
      combos["intervalToNext"].append(note - prevNote)
    combos[str(note)] = possibleNotes
    """ print("note: " + str(note) + "\n" + "prevNote: " + str(prevNote)) """
    prevNote = note
  return combos