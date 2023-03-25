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
  isInRange = prev2 - 12 <= next2 <= prev2 + 12
  isValid = isCons & isInRange & isNotParPerf
  return isValid

diatonic = {
    "1": [0,2,4,5,7,9,11],
    "2": [0,2,3,5,7,9,10],
    "3": [0,1,3,5,7,8,10],
    "4": [0,2,4,6,7,9,11],
    "5": [0,2,4,5,7,9,10],
    "6": [0,2,3,5,7,8,10]
  }

def detectMode(melody):
  firstPitch = melody[0]
  gamut = []
  for note in melody:
    adjusted = note - firstPitch
    if gamut.__contains__(adjusted):
      gamut.append(adjusted)
  if gamut.__contains__(6):
    return diatonic["4"]
  elif gamut.__contains__(1):
    return diatonic["3"]
  elif gamut.__contains__(8):
    return diatonic["6"]
  elif gamut.__contains__(3):
    return diatonic["2"]
  elif gamut.__contains__(10):
    return diatonic["5"]
  elif gamut.__contains__(11):
    return diatonic["1"]

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