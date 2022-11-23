import os
import numpy as np
import pandas as pd
from . import data_quality_spc as dqspc
from . import data_quality_span as dqspan
from . import data_transformation as dt
from astropy.constants import R_sun

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/data/home/simons97/LocalApplications/cdf/lib"
from spacepy import pycdf


def encounter_data(folder, data_frame, inst):
    """DOC!"""
    # SANITY CHECK: only SPC and SPAN-I allowed
    legal_inst = ["SPC", "SPAN-I"]
    assert inst in legal_inst, \
        "Only SPC and SPAN-I allowed!"

    for file in sorted(os.listdir(folder)):
        # Sanity check: print current file name
        print(f"CURRENTLY HANDLING {file}")

        # Initialize empty data frame
        data = pd.DataFrame()

        # open CDF file and generate pandas DataFrame that stores
        # data from file
        cdf_data = pycdf.CDF(f"{folder}/{file}")

        # Either SPC or SPAN
        if inst == "SPC":
            data = data_generation_spc(cdf_data)

        if inst == "SPAN-I":
            data = data_generation_span(cdf_data)

        # Add the DataFrame of one encounter to the total array
        data_frame = pd.concat([data_frame, data])

    return data_frame


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
        "wp": cdf_slice(cdf_file, key="wp_moment")
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

    distance_restriction(data)
    
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
    distance_restriction(data)

    # Make conversion of temperature
    data.Temp = dt.ev_to_kelvin(data.Temp)

    # TODO: Add data quality treatment
    # TODO: FOV of the instrument and influence on the distribution
    #       also needs to be considered
    dqspan.dqf_conversion(data["dqf"])

    # TODO: This is only a very rough sorting argument for now
    # Drop all entries where the distance is larger than 25 Rs
    idx = data.index[data["posR"] > 27 * R_sun / 1e3].tolist()
    data.drop(index=idx, inplace=True)

    return data


def distance_restriction(data_frame):
    """
    Restrict evaluated data to distances below 40 R_sol, which is the
    boundary of the simulation domain
    """
    idx = data_frame.index[data_frame["posR"] > 40 * R_sun / 1e3].tolist()
    data_frame.drop(index=idx, inplace=True)
