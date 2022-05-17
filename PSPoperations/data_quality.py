import numpy as np


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


def array_reduction(data_array: np.ndarray,
                    index_list: np.ndarray) -> np.ndarray:
    """
    Reduction of an array by a list of indices.

    :param data_array: NDARRAY,
        Array that is to be reduced
    :param index_list: NDARRAY,
        List of indices that should be deleted
    :return: NDARRAY,
        The reduced array
    """
    # Choose axis=0 to delete rows and not flatten the array
    reduced_array = np.delete(data_array, index_list, axis=0)

    return reduced_array
