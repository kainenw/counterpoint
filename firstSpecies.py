from classes import isConsonant, isDirect
from firstSpecies import allPossibleMoves, getAllNextMoves, getAllPossibleCpts
from tests import testLowerCf, testHigherCf

from scales import scales

def allPossibleMoves(prevCf, nextCf, prevCtp, type = "dia", mode = "i"):
  scale = scales[type][mode]
  ctpIsAbove = prevCf < prevCtp
  possibilities = []
  for i in range(0,9):
    up = prevCtp + i
    down = prevCtp - i
    possibleCtpNotes = [up, down]
    for nextCtp in possibleCtpNotes:
      if(scale.__contains__(nextCtp % 12)):
        isCons = isConsonant(nextCf, nextCtp)
        if(isCons):
          isDir = isDirect(prevCf, nextCf, prevCtp, nextCtp)
          isPerfect = isCons == 'perfect'
          isDirectPerfect = isDir and isPerfect
          if(not isDirectPerfect):
            notCrossing = nextCtp > nextCf if ctpIsAbove else nextCtp < nextCf
            if(notCrossing):
              if(nextCf - 16 <= nextCtp <= nextCf + 16):
                possibilities.append([nextCf, nextCtp])
  return possibilities

def getAllNextMoves(dict, nextCf):
  newDict = {
    'moves': []
  }
  for prevMove in dict['moves']:
    prevKey = str(prevMove)
    nextMoves = allPossibleMoves(prevMove[0], nextCf, prevMove[1])
    for move in nextMoves:
      for cumulativeLine in dict[prevKey]:
        if(not newDict['moves'].__contains__(move)):
          newDict[str(move)] = [[*cumulativeLine, move]]
          newDict['moves'].append(move)
        else:
          newDict[str(move)].append([*cumulativeLine, move])
  print(newDict)
  return newDict

def getAllPossibleCpts(cf, direction):
  currentDict = {}
  for note in cf:
    if not currentDict:
      if(direction == "+"):
        firstCtp = note + 12
      elif(direction == "-"):
        firstCtp = note - 12
      currentDict['moves'] = [[note, firstCtp]]
      currentDict[str([note, firstCtp])] = [[[note, firstCtp]]]
    else:
      nextDict = getAllNextMoves(currentDict, note)
      currentDict = nextDict
  possibleCtps = []
  for item in currentDict['moves']:
    for j in currentDict[str(item)]:
      possibleCtps.append(j)
