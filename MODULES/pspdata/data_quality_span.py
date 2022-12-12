import numpy as np


def fov_restriction(peak_idx):
    """
    As suggested by R. Livi, the SPAN-I data is conservatively sorted by
    determining the azimuth bin of the flux peak, and then only accepted
    when the peak bin is approx. 150 degrees (where 180 would be the
    heat shield)
    """
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
    """Get peak indices for nested array"""
    num_meas = len(array)
    peak_idx = np.array([np.argmax(array[i]) for i in range(num_meas)])

    return peak_idx
