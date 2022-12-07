"""
As Dr. Livi pointed out, EFLUX peaks should be below 150° (or 30° from
the heat shield) to be confident about a full distribution.

PSEUDOCODE:
Take the argmax of EFLUX_VS_PHI
    - 8 entries per measurement
    - Output will be between 0 and 7

Correlate the output as index for Theta value (can be hardcoded)
    - Drop all measurements where the index is <= 1 (maybe 2?)
    - 0 and 1 correspond to ~175 and ~160°, 2 would be almost 150°

"""
import numpy as np


def fov_restriction(peak_idx):
    """DOC!"""
    # Hard-code the critical index here. There are 8 PHI-bins for SPAN
    # between (roughly) 180 and 100 degrees. According to Dr. Livi,
    # peaks above 150 degrees mean the full distribution is NOT in the
    # FOV of the instrument. The indices of the PHI-bins start at 180,
    # so the first two indices (0, 1) are definitely too high, index 2
    # might be arguable (~152 degrees)
    crit_index = 1
    fov_idx = np.where(peak_idx <= crit_index)[0]

    return fov_idx


def array_peak(array):
    """DOC!"""
    num_meas = len(array)
    peak_idx = np.array([np.argmax(array[i]) for i in range(num_meas)])

    return peak_idx
