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
  # perfect 4ths (categorized as positive 5) are not counted as consonants by Fux
  if (intervals["consonances"]["perfect"].__contains__(absVal) and mod != 5):
    return "perfect"
  if intervals["consonances"]["imperfect"].__contains__(absVal):
    return "imperfect"
  else:
    return False

def isDirect(prev1,next1, prev2,next2):
  interval1 = prev1 - next1
  interval2 = prev2 - next2
  isDirect = interval1 * interval2  > 0
  return isDirect

# return what kind of motion is occuring between two notes
def isDirectPerfect(prev1,next1, prev2,next2, isCons):
  interval1 = prev1 - prev2
  interval2 = next1 - next2
  isDirect = interval1 * interval2  > 0
  isPerfect = isCons == "perfect"
  return isDirect and isPerfect