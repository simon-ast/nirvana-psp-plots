import os
import typing as tp
import numpy as np

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"


def cdf_slice(cdf_file, key: str):
    """
    Simple call to specific slice of cdf data.
    
    :param cdf_file: Name of cdf file
    :param key: Name of desired key from cdf file
    :return: Datta slice
    """
    return cdf_file[key][...]


def data_generation(cdf_file) -> tp.Dict:
    """
    Generate dictionary of measurement data from cdf file
    
    :param cdf_file: CDF file
    :return: DICT,
        Data dictionary
    """
    data = {
        "dqf": cdf_slice(cdf_file, key="general_flag"),
        "epoch": cdf_slice(cdf_file, key="Epoch"),
        "pos": cdf_slice(cdf_file, key="sc_pos_HCI"),
        "vr": cdf_slice(cdf_file, key="vp_moment_RTN")[:, 0],
        "dvrhi": cdf_slice(cdf_file, key="vp_moment_RTN_deltahigh")[:, 0],
        "dvrlo": cdf_slice(cdf_file, key="vp_moment_RTN_deltalow")[:, 0],
        "np": cdf_slice(cdf_file, key="np_moment"),
        "wp": cdf_slice(cdf_file, key="wp_moment"),
        "dwphi": cdf_slice(cdf_file, key="wp_moment_deltahigh"),
        "dwplo": cdf_slice(cdf_file, key="wp_moment_deltalow")
    }
    
    return data


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


def full_reduction(data_dict: tp.Dict,
                   bad_indices: np.array) -> tp.Dict:
    """
    Fully reduce data dictionary by all determined "bad" indices
    
    :param data_dict: DICT;
        Data dictionary (for PSP data)
    :param bad_indices: NDARRAY,
        Array of "bad" indices
    :return: DICT,
        Same as input, but with reduced value arrays
    """
    for key in data_dict.keys():
        data_dict[key] = array_reduction(data_dict[key], bad_indices)
    
    return data_dict
