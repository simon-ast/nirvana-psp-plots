import os
import typing as tp
import numpy as np

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"


def cdf_slice(cdf_file, key: str):
    """
    DOC
    
    :param cdf_file:
    :param key:
    :return:
    """
    return cdf_file[key][...]


def data_generation(cdf_file) -> tp.Dict:
    """
    DOC
    
    :param cdf_file:
    :return:
    """
    data = {
        "dqf": cdf_slice(cdf_file, key="general_flag"),
        "epoch": cdf_slice(cdf_file, key="Epoch"),
        "pos": cdf_slice(cdf_file, key="sc_pos_HCI"),
        "vr": cdf_slice(cdf_file, key="vp_moment_RTN")[:, 0],
        "dvrhi": cdf_slice(cdf_file, key="vp_moment_RTN_deltahigh")[:, 0],
        "dvrlo": cdf_slice(cdf_file, key="vp_moment_RTN_deltalow")[:, 0],
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
    DOC
    
    :param data_dict:
    :param bad_indices:
    :return:
    """
    for key in data_dict.keys():
        data_dict[key] = array_reduction(data_dict[key], bad_indices)
    
    return data_dict
