import os
import numpy as np
import matplotlib.pyplot as plt
from spacepy import pycdf
from PSPoperations import data_quality as dq
from PSPoperations import data_transformation as dt

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"

# open CDF file and generate faulty index array
cdf_data = pycdf.CDF("psp_swp_spc_l3i_20211117_v02.cdf")
dqf = cdf_data["general_flag"][...]
bad_ind = dq.general_flag(dqf)

# generate reduced epoch array
time = dq.array_reduction(cdf_data["Epoch"][...], bad_ind)

# generate reduced position array and spherical coordinates
pos = dq.array_reduction(cdf_data["sc_pos_HCI"][...], bad_ind)
r, theta, phi = dt.pos_cart_to_sph(pos)

# generate (prelim.) velocity array (is [0] in RTN right?)
vr = dq.array_reduction(cdf_data["vp_moment_RTN"][...][:, 0], bad_ind)
del_vr_lo = dq.array_reduction(cdf_data["vp_moment_RTN_deltalow"][...][:, 0],
                               bad_ind)
del_vr_hi = dq.array_reduction(cdf_data["vp_moment_RTN_deltahigh"][...][:, 0],
                               bad_ind)

plt.figure()
plt.plot(r / 1.49e8, vr)
plt.fill_between(r / 1.49e8, vr + del_vr_hi, vr - del_vr_lo, color="grey",
                 alpha=0.15)
plt.ylim(0, 1000)

plt.figure()
plt.scatter(time, r / 1.49e8)

plt.show()
