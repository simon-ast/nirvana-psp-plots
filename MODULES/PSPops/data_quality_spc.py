import numpy as np
import pandas as pd


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
    index_list = np.asarray(general_flag_array != 0).nonzero()[0]

    # This is the previous call. The numpy documentation encourages
    # the use of .nonzero() over .where()
    # index_list = np.where(general_flag_array != 0)[0]

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
    index_list = np.asarray(meas_array <= -0.5e30).nonzero()[0]

    # Again, numpy documentation suggests using the above instead of
    # np.where()
    # index_array = np.where(meas_array <= -0.5e30)[0]
    
    return index_list


def full_meas_eval(data_dict: pd.DataFrame):
    """
    Assess additional failure indices by evaluating all desired
    measurement values.
    
    :param data_dict: DataFrame,
        Data Frame of PSP measurement data
    :return: LIST,
        List of "bad" indices
    """
    col_ind = []

    # This is very static, but should not make a problem as I am only
    # interested in these three parameters!
    for key in ["vr", "np", "wp"]:
        col_ind.append(meas_failed(data_dict[key]))
    
    # Make an array of unique indices
    col_ind = np.unique(np.concatenate(col_ind))
    
    return col_ind
