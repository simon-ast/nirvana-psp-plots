import os
import numpy as np
import pandas as pd
from . import data_quality_spc as dqspc
from . import data_transformation as dt

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

    # Indices of non-usable data from general flag + reduction
    bad_ind = dqspc.general_flag(data.dqf.values)
    data.drop(bad_ind, inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Additional reduction from "-1e-30" meas. indices + reduction
    mf_ind = dqspc.full_meas_eval(data)
    data.drop(mf_ind, inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Transform necessary data
    data["posR"], data["posTH"], data["posPH"] = \
        dt.pos_cart_to_sph(data.posX, data.posY, data.posZ)
    data["Temp"] = dt.wp_to_temp(data["wp"])
    
    return data


def data_generation_span(cdf_file) -> pd.DataFrame:
    """
    Generate dictionary of measurement data from cdf file and turn into
    pandas DataFrame.

    :param cdf_file: CDF file
    :return: DataFrame,
        Data frame of measurements
    """
    data_dict = {
        "dqf": cdf_slice(cdf_file, key="QUALITY_FLAG"),
        "epoch": cdf_slice(cdf_file, key="Epoch"),
        "posX": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "posY": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "posZ": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "posR": cdf_slice(cdf_file, key="SUN_DIST"),

        # In the case of SPAN-I, the ion velocity has to be corrected
        # by the spacecraft velocity
        "vr": cdf_slice(cdf_file, key="VEL_RTN_SUN")[:, 0] -
              cdf_slice(cdf_file, key="SC_VEL_RTN_SUN")[:, 0],
        "np": cdf_slice(cdf_file, key="DENS"),
        "wp": np.zeros(len(cdf_slice(cdf_file, key="Epoch"))),
        "Temp": cdf_slice(cdf_file, key="TEMP")
    }   

    # Create pandas DataFrame Object
    data = pd.DataFrame(data_dict)

    # Make conversion of temperature
    data.Temp = dt.ev_to_kelvin(data.Temp)

    # TODO: Add data quality treatment
    # TODO: FOV of the instrument and influence on the distribution
    #       also needs to be considered

    return data
