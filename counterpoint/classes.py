# %% [markdown]
# # Analyze cf notes and features
# 

# %% [markdown]
# ## Pitch Class (a single note)

# %%
# pitch class from 0 to 12
def pitch_class(num):
  return num % 12

# %% [markdown]
# ## Interval Class (between two simultaneous notes)

# %%
def interval_class(num1, num2):
    interval = (num2 - num1)
    return interval

consonance = {
    'perfect': [0, 5, 7],
    'imperfect': [3, 4, 8, 9]
}

dissonance = [1, 2, 6, 10, 11]

def is_consonant(num1, num2):
    interval = interval_class(num1, num2) % 12
    if interval in consonance['perfect'] and interval != 5:
        return 'perfect'
    elif interval in consonance['imperfect']:
        return 'imperfect'
    else:
        return False

print(is_consonant(2, 11))
print(interval_class(0, 7))
print(interval_class(7, 0))
print(is_consonant(7, 26))

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
    motion_value = interval1 * interval2
    if interval1 == interval2:
      return 2
    elif motion_value > 0:
      return 1
    elif motion_value < 0:
      return -1
    elif motion_value == 0:
      return 0


def is_direct_perfect(prev1, next1, prev2, next2):
    next_interval = interval_class(next1, next2)
    is_direct = motion(prev1, next1, prev2, next2) > 0
    is_perfect = consonance["perfect"].__contains__(next_interval)
    return is_direct and is_perfect


print(is_direct_perfect(2, 0, 11, 12))



