import pandas as pd
import numpy as np
import random
from math import floor

# Trial schedule dataframe
ts = pd.DataFrame()

# Trial numbers
n_baseline = 0
start = n_baseline + 4
n_exposure = 60
n_trials = n_baseline + n_exposure

# Init trial arrays
trials_string = ["B" for i in range(n_baseline)]
trials_numeric = np.zeros(n_trials)

# Init rot values 
rotations = [-2, -1, 1, 2]

n_trials_per_pert = floor(n_exposure / (3 * len(rotations)))

# Init trial type permutations
trial_type_1 = ["NXP", "NPX", "XNP", "XPN"]
trial_type_2 = ["NPX", "XPN", "PXN", "PNX"]
start_perm = random.choice(["PXN", "PNX"])
trials_string[n_baseline:n_baseline+3] = [str(val) for val in start_perm]
triplet_prev = start_perm

# Init no FB flag

np_fb_flag = []

# Populate trial types

for i in range(start, n_trials, 3):
    if (triplet_prev == "NXP") or (triplet_prev == "XNP"):
        triplet = random.choice(trial_type_1)
    else:
        triplet = random.choice(trial_type_2)
    
    trials_string.extend([triplet[0], triplet[1], triplet[2]])

    triplet_prev = triplet



# Find indices where trials_str == "P"
P_indices = [i for i, val in enumerate(trials_string) if val == "P"]
perturbations = np.tile(rotations, int(np.ceil(len(P_indices) / len(rotations))))
np.random.shuffle(perturbations)

for i, p in enumerate(P_indices):
    trials_numeric[p] = perturbations[i]

ts["trial"] = [i+1 for i in range(n_trials)]
ts['trial type'] = trials_string
ts["rotation"] = trials_numeric

ts.to_csv("tgt.csv", index=False)
