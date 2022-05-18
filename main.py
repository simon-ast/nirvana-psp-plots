import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from spacepy import pycdf
from PSPoperations import data_quality as dq
from PSPoperations import data_transformation as dt
from PSPoperations import plot_settings as ps

# Plot parameters
ps.rc_setup()

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"


"""
PSEUDOCODE

BACKGROUND
- Collect data for one Encounter in folder
	-- Variable name of folder to handle different encounters
	
- SWEAP provides (all with uncertainties)
	-- Date and time of observation
	-- Cartesian position (x, y, z)
	-- RTN frame velocity
	-- Thermal velocity w
	-- Density of protons (majority of wind)

- Collect all measurements (after reduction) into singular arrays?
	-- Could then be split by minimum distance for perihelion


OPERATIONS
- Sort through "general flag" (only use where set to 0)
	-- Also sort through each array to find entries with -1e30, which
	   marks failed measurements
- Calculate spherical heliocentric coordinates (HIC)
- Transform to usable data parameters (vr, log_T, log_rho)
- Generate log-file with important information
	-- Total number of data points
	-- Reduced number of data points
	-- Epoch from start to finish
"""
ENCOUNTER_NUM = "encounter_5"
DATA_LOCATION = sys.path[0]+"/DATA/"+ENCOUNTER_NUM

# SANITY CHECK IF DATA LOCATION EXISTS
if not os.path.isdir(DATA_LOCATION):
	print(f"\n{DATA_LOCATION} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	# Total array setup
	r = theta = phi = np.array([])
	vr = dvhi = dvlo = np.array([])
	
	for file in os.listdir(DATA_LOCATION):
		cdf_data = pycdf.CDF(DATA_LOCATION+"/"+file)
		
		dqf = cdf_data["general_flag"][...]
		bad_ind = dq.general_flag(dqf)
		
		# generate reduced epoch array
		time_file = dq.array_reduction(cdf_data["Epoch"][...], bad_ind)
		
		# Position
		pos_file = dq.array_reduction(cdf_data["sc_pos_HCI"][...], bad_ind)
		r_file, theta_file, phi_file = dt.pos_cart_to_sph(pos_file)
		
		# Velocity
		vr_file = dq.array_reduction(
			cdf_data["vp_moment_RTN"][...][:, 0],
			bad_ind)
		dvhi_file = dq.array_reduction(
			cdf_data["vp_moment_RTN_deltalow"][...][:, 0],
			bad_ind)
		dvlo_file = dq.array_reduction(
			cdf_data["vp_moment_RTN_deltahigh"][...][:, 0],
			bad_ind)
		
		# Update total arrays
		r = np.append(r, r_file)
		vr = np.append(vr, vr_file)
	
	plt.figure()
	plt.plot(r, vr)
	plt.ylim(0, 1000)
	
	plt.show()


def plot_setup():
	fig_vr, ax_vr = plt.subplots()
	ax_vr.set(
		xlabel="r [R$_\\odot$]", ylabel="v$_r$ [km/s$^{-1}$]",
		ylim=(0, 800)
	)


if __name__ == "__main__":
	main()
