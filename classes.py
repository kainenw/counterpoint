# %% [markdown]
# # Analyze cf notes and features
#

# %% [markdown]
# ## Pitch Class (a single note)


# %%
# pitch class from 0 to 12
def pitchClass(num):
    return num % 12


# %% [markdown]
# ## Interval Class (between two simultaneous notes)


# %%
# interval class (negative or positive)
def interval_class(num1, num2):
    num1 = pitchClass(num1)
    num2 = pitchClass(num2)
    interval = num2 - num1
    return interval


# interval categories
consonance = {"perfect": [0, 5, 7], "imperfect": [3, 4, 8, 9]}
dissonance = [1, 2, 6, 10, 11]


def isConsonant(num1, num2):
    interval = interval_class(num1, num2)
    print(interval)
    # perfect 4ths (categorized as positive 5) are not counted as consonants by Fux in 1st species
    if consonance["perfect"].__contains__(interval) and interval != 5:
        return "perfect"
    elif consonance["imperfect"].__contains__(interval):
        return "imperfect"
    else:
        return False


print(isConsonant(2, 11))

# %% [markdown]
# #### Motion Types (from the transition from two simultaneous notes to two other simultaneous notes)
# - Parallel: 2
# - Direct: 1
# - Oblique: 0
# - Contrary: -1


# %%
def motion(prev1, next1, prev2, next2):
    interval1 = interval_class(prev1, next1)
    interval2 = interval_class(prev2, next2)
    if interval1 == interval2:
        return 2
    motion = interval1 * interval2 / abs(interval1 * interval2)
    return motion


def isDirectPerfect(prev1, next1, prev2, next2):
    next_interval = interval_class(next1, next2)
    isDirect = motion(prev1, next1, prev2, next2) > 0
    isPerfect = consonance["perfect"].__contains__(next_interval)
    return isDirect and isPerfect


""" 


def isParallelPerfect(prev1, next1, prev2, next2):
    int1 = int(prev1, prev2)
    isPerfect = consonance["perfect"].__contains__(int1)
    if isPerfect:
      motion = motion(prev1, next1, prev2, next2)
      return motion == 2
    else:
      return False """
