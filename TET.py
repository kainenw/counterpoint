import math

""" 
twelfthRootOfTwo = math.pow(2, 1 / 12)

# reference note of 49 (A4)
ref_num = 49
# reference frequency of 440 Hz
ref_freq = 440

def TTET_calculation(n):
  targetNum = n - ref_num
  proportion_from_ref_freq = math.pow(twelfthRootOfTwo, targetNum)
  freq = ref_freq * proportion_from_ref_freq
  return freq

def TTET_array():
  list = []
  for i in range(0, 88):
    Hz = TTET_calculation(i)
    list.append(Hz)
  return list

TTET = TTET_array() """

# twelve-tone equal temperament
# 49 = A4 = 440Hz
# frequency in hertz (Hz)
freq = [ 16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87, 32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.00, 58.27, 61.74, 65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98.00, 103.83, 110.0, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53, 2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07, 4186.00 ]

noteLetters = ["C", ["C#", "Db"], "D", ["D#", "Eb"], "E", "F", ["F#", "Gb"], "G", ["G#", "Ab"], "A", ["A#", "Bb"], "B"]

'''get the desired note by entering the pitch class and octave number (e.g. (9, 4) which is A4) this allows notes to be referenced intuitively but also for intervals to be retrieved easily. '''

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
