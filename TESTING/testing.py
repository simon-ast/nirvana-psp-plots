import os
import sys
from unipath import Path
import numpy as np
import matplotlib.pyplot as plt
from spacepy import pycdf
from astropy.constants import R_sun

# Append custom Python modules from parent directory
sys.path.append(Path(sys.path[0]).parent)
from MODULES.PSPops import data_quality as dq
from MODULES.PSPops import data_transformation as dt
from MODULES.Plotting import obs_plotset as ps
from MODULES.PSPops import data_handling as dh
from MODULES.Statistics import data_binning as db
from MODULES.Statistics import stats as st


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

# Testing binning into radial bins
distance_bins = db.create_bins(0, 100, .5)
bin_indices = db.sort_bins(distance_bins, data["r"] * 1e3 / R_sun.value)

test_r = st.slice_index_list(data["r"], bin_indices["(46.5, 47.0)"]) * 1e3 / R_sun.value
test_v = st.slice_index_list(data["vr"], bin_indices["(46.5, 47.0)"])

plt.plot(test_r, test_v, zorder=2)
plt.hlines(np.mean(test_v), np.min(test_r), np.max(test_r), color="black",
           zorder=3, lw=2, ls="--")
plt.fill_between(test_r, np.mean(test_v) + np.std(test_v),
                 np.mean(test_v) - np.std(test_v),
                 color="grey", alpha=0.35, zorder=1)
plt.show()
