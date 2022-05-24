import numpy as np
import typing as tp


def general_flag(general_flag_array: np.ndarray) -> np.ndarray:
    """
    This function reads out index locations where data general flag is
    set to 0 (see documentation for PSP data). This requires correct
    handling of CDF array keys

    :param general_flag_array: NDARRAY,
        cdf_data["general_flag"][...] - Only good when set to 0. The
        input here must specifically be this array!
    :return: NDARRAY,
        An array of the "faulty" indices. These indices correspond to
        the index m in the m x n GENERAL CDF array, not a measurement
        subarray!
    """
    # Notable indices are where values are set to non-zero
    # From the data user guide: 0 means no condition present
    index_list = np.where(general_flag_array != 0)[0]

    return index_list


def meas_failed(meas_array: np.ndarray) -> np.ndarray:
    """
    Takes a 1D array and returns indices of failed measurements (as
    indicated by a value of -1e30, SWEAP documentation)
    
    :param meas_array: NDARRAY,
        Measurement array
    :return: NDARRAY,
        Index array
    """
    index_array = np.where(meas_array <= -0.5e30)[0]
    
    return index_array


def full_meas_eval(data_dict: tp.Dict):
    """
    Assess additional failure indices by evaluating all desired
    measurement values.
    
    :param data_dict: DICT,
        Dictionary of PSP measurement data
    :return: LIST,
        List of "bad" indices
    """
    col_ind = []
    
    for key in data_dict.keys():
        
        # Skip unnecessary keys (maybe make this more dynamic?)
        if key in ["pos", "dqf", "epoch"]:
            continue
        
        col_ind.append(meas_failed(data_dict[key]))
    
    # Make an array of unique indices
    col_ind = np.unique(np.concatenate(col_ind))
    
    return col_ind
