import os
import sys
from unipath import Path
import numpy as np
import matplotlib.pyplot as plt
from spacepy import pycdf

# Append custom Python modules from parent directory
sys.path.append(Path(sys.path[0]).parent)
from PSPoperations import data_quality as dq
from PSPoperations import data_transformation as dt
from PSPoperations import plot_settings as ps
from PSPoperations import data_handling as dh


# Plot set up
ps.rc_setup()

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"

# open CDF file and generate faulty index array
cdf_data = pycdf.CDF("psp_swp_spc_l3i_20211117_v02.cdf")
data = dh.data_generation(cdf_data)

# Indices of non-usable data from general flag + reduction
bad_ind = dq.general_flag(data["dqf"])
data = dh.full_reduction(data, bad_ind)

# Additional reduction from failed measurement indices
mf_ind = dq.full_meas_eval(data)
data = dh.full_reduction(data, mf_ind)

# Add to data dictionary (spherical coordinates)
data["r"], data["theta"], data["phi"] = dt.pos_cart_to_sph(data["pos"])

# Add to data dictionary (temperature)
data["T"] = dt.wp_to_temp(data["wp"])
data["dThi"] = dt.wp_to_temp(data["dwphi"])
data["dTlo"] = dt.wp_to_temp(data["dwplo"])

# vr plot
ps.plot_r_vr(data["r"], data["vr"], data["dvrhi"], data["dvrlo"],
             save_ind="yes")
ps.plot_r_temp(data["r"], data["T"], data["dThi"], data["dTlo"],
               save_ind="yes")

plt.show()
