import os
import typing as tp
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


def data_generation(cdf_file) -> pd.DataFrame:
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
        # "dvrhi": cdf_slice(cdf_file, key="vp_moment_RTN_deltahigh")[:, 0],
        # "dvrlo": cdf_slice(cdf_file, key="vp_moment_RTN_deltalow")[:, 0],
        "np": cdf_slice(cdf_file, key="np_moment"),
        "wp": cdf_slice(cdf_file, key="wp_moment"),
        # "dwphi": cdf_slice(cdf_file, key="wp_moment_deltahigh"),
        # "dwplo": cdf_slice(cdf_file, key="wp_moment_deltalow")
    }

    # Create a pandas DataFrame Object
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


def stat_data_dict(file_name):
    """Generates dictionaries of statistical data from file read-in."""
    raw_data = np.loadtxt(file_name, skiprows=1)
    
    return {
        "r"   : raw_data[:, 0],
        "vr"  : {
            "mean"  : raw_data[:, 1],
            "stddev": raw_data[:, 2],
            "median": raw_data[:, 3],
            "q1"    : raw_data[:, 4],
            "q3"    : raw_data[:, 5]
        },
        "rho" : {
            "mean"  : raw_data[:, 6],
            "stddev": raw_data[:, 7],
            "median": raw_data[:, 8],
            "q1"    : raw_data[:, 9],
            "q3"    : raw_data[:, 10]
        },
        "temp": {
            "mean"  : raw_data[:, 11],
            "stddev": raw_data[:, 12],
            "median": raw_data[:, 13],
            "q1"    : raw_data[:, 14],
            "q3"    : raw_data[:, 15]
        }
    }
