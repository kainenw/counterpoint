# %%
from classes import is_consonant, is_direct_perfect


def is_valid_move(prev1, next1, prev2, next2):
    is_cons = is_consonant(next1, next2)
    if is_cons:
        is_dir_perf = is_direct_perfect(prev1, next1, prev2, next2)
        if not is_dir_perf:
            is_in_range = prev2 - 8 <= next2 <= prev2 + 8
            if is_in_range:
                return True
    return False


print(is_valid_move(0, 2, 12, 11))

# %% [markdown]
# mini-test

# %%
import classes

def get_all_combos(melody, ctp_is_above):
    key = [0,2,4,5,7,9,11]
    mode = melody[0]
    combos = {
        "melody": melody,
        "mode": mode,
        "interval_to_next": [],
        "ctp_is_above": ctp_is_above,
    }
    pre_note = None
    intervals = [3, 4, 7, 8, 9, 12, 16, 19]
    for note in melody:
        possible_notes = []
        for interval in intervals:
            if ctp_is_above:
                possible_note = note + interval
            else:
                possible_note = note - interval
            is_in_key = key.__contains__(possible_note % 12)
            if is_in_key:
                possible_notes.append(possible_note)
        if pre_note != None:
            combos["interval_to_next"].append(note - pre_note)
        combos[str(note)] = possible_notes
        pre_note = note
    return combos
  
print(get_all_combos([0, 2, 4, 5, 7, 9, 11, 12], True))

# %%


# %%
def findCounterpoint(melody):
  counterpoint = []
  # Your code to generate the counterpoint line goes here
  return counterpoint



