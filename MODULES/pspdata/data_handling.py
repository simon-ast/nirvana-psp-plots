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
        "vr": cdf_slice(cdf_file, key="vp_fit_RTN")[:, 0],
        "np": cdf_slice(cdf_file, key="np_fit"),
        "wp": cdf_slice(cdf_file, key="wp_fit")
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

    if not data.empty:
        data["epoch"] = data["epoch"].apply(pd.Timestamp.to_julian_date) \
                        * 86400     # In Seconds

    # TODO: Time averaging should go in here
    # data_tavg = data
    data_tavg = time_averaging(data)

    return data_tavg


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

    # Prepare data quality assessment through FOV
    dq_eflux = cdf_slice(cdf_file, key="EFLUX_VS_PHI")
    fov_idx = dqspan.fov_restriction(dq_eflux)

    # Reduce data by FOV coverage and overall spacecraft distance
    data.drop(index=fov_idx, inplace=True)
    distance_restriction(data)

    # Make conversion of temperature
    data.Temp = dt.ev_to_kelvin(data.Temp)

    if not data.empty:
        data["epoch"] = data["epoch"].apply(pd.Timestamp.to_julian_date) \
                        * 86400  # In Seconds

    # TODO: DOCUMENT THIS!
    # data_tavg = data
    data_tavg = time_averaging(data)

    return data_tavg


def distance_restriction(data_frame):
    """
    Restrict evaluated data to distances below 40 R_sol, which is the
    boundary of the simulation domain
    """
    idx = data_frame.index[data_frame["posR"] > 40 * R_sun / 1e3].tolist()
    data_frame.drop(index=idx, inplace=True)


def time_averaging(data):
    """DOC!"""
    # Generate empty data frame with same column headers as data
    averaged_frame = pd.DataFrame(columns=data.columns)

    # Store the length of frame (number of measurements) for later
    # reference
    size = data.shape[0]

    # Start index and end index for time window initialization
    start_idx = 0
    end_idx = 0

    # Desired time window in seconds
    time_window = 10

    # The loop can last until the start_idx reaches the end of the data
    # array (size - 1 translates length to index number!)
    while start_idx < size - 1:

        # Initialize time delta variable
        time_delta = 0

        # Loop can last while time_delta stays below window size
        while time_delta < time_window:

            # Iteratively increase end_idx to size the window
            end_idx += 1

            # If end_idx hits the end of the array, stop (again,
            # size - 1 translates length to index number)
            if end_idx == size - 1:
                break

            # Determine time delta size (this loops back to the top if
            # the time_delta is smaller than the window)
            time_delta = data.epoch.iloc[end_idx] - data.epoch.iloc[start_idx]

        # Once window size is reached or surpassed, slice out the window
        # of the data set (excluding end_idx, which would bring the time
        # window above the threshold and is given by iloc[a:b])
        data_window = data.iloc[start_idx:end_idx]
        avg = data_window.mean(numeric_only=True).to_frame().T

        # Extend the averaged_frame with the new result
        averaged_frame = pd.concat(objs=[averaged_frame, avg])

        # Set the old end_idx as the new start_idx (making them equal again)
        # This is done here so the loop exits correctly.
        start_idx = end_idx

    return averaged_frame
