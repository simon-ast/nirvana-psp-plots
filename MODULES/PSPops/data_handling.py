import os
import numpy as np
import pandas as pd

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"


def cdf_slice(cdf_file, key: str):
    """
    Simple call to specific slice of cdf data.
    
    :param cdf_file: Name of cdf file
    :param key: Name of desired key from cdf file
    :return: Data slice
    """
    return cdf_file[key][...]


def data_generation_spc(cdf_file) -> pd.DataFrame:
    """
    Generate dictionary of measurement data from cdf file and turn into
    pandas DataFrame.
    
    :param cdf_file: CDF file
    :return: DataFrame,
        Data frame of measurements
    """
    data_dict = {
        "dqf": cdf_slice(cdf_file, key="general_flag"),
        "epoch": cdf_slice(cdf_file, key="Epoch"),
        "posX": cdf_slice(cdf_file, key="sc_pos_HCI")[:, 0],
        "posY": cdf_slice(cdf_file, key="sc_pos_HCI")[:, 1],
        "posZ": cdf_slice(cdf_file, key="sc_pos_HCI")[:, 2],
        "vr": cdf_slice(cdf_file, key="vp_moment_RTN")[:, 0],
        "np": cdf_slice(cdf_file, key="np_moment"),
        "wp": cdf_slice(cdf_file, key="wp_moment"),
    }

    # Create a pandas DataFrame Object
    data = pd.DataFrame(data_dict)
    
    return data


def data_generation_span(cdf_file) -> pd.DataFrame:
    """DOC"""
    data_dict = {
        "dqf": cdf_slice(cdf_file, key="QUALITY_FLAG"),
        "epoch": cdf_slice(cdf_file, key="Epoch"),
        "posX": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "posY": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "posZ": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "posR": cdf_slice(cdf_file, key="SUN_DIST"),
        "vr": cdf_slice(cdf_file, key="VEL_RTN_SUN")[:, 0],
        "np": cdf_slice(cdf_file, key="DENS"),
        "wp": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "Temp": cdf_slice(cdf_file, key="TEMP")
    }

    # Create pandas DataFrame Object
    data = pd.DataFrame(data_dict)

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
