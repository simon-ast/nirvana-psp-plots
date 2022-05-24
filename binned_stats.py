import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.constants import R_sun
from MODULES.Plotting import plot_settings as ps
from MODULES.Statistics import stats as st

# DESIGNATE BINNED DATA LOCATION
BIN_DATA_LOCATION = f"{sys.path[0]}/STATISTICS/BINNED_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(BIN_DATA_LOCATION):
	print(f"\n{BIN_DATA_LOCATION} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	
	test_r = test_v = np.array([])
	std_r = std_v = np.array([])
	
	# Loop over all files in the binned data directory
	for name in sorted(os.listdir(BIN_DATA_LOCATION)):
		
		# Generate correct pointer to data file
		file = BIN_DATA_LOCATION + f"/{name}"
		
		# Generate numpy array from data files (multi-dim)
		all_data = np.loadtxt(file, skiprows=1)
		
		# Generate sub-arrays from all data
		r = all_data[:, 0]
		vr = all_data[:, 1]
		
		stat_r = st.stat_ana(r * 1e3 / R_sun.value)
		stat_vr = st.stat_ana(vr)
		
		test_r = np.append(test_r, stat_r["median"])
		test_v = np.append(test_v, stat_vr["median"])
		
		std_r = np.append(std_r, stat_r["stddev"])
		std_v = np.append(std_v, stat_vr["stddev"])
		
	plt.plot(test_r, test_v, marker="x")
	plt.fill_between(test_r, test_v + std_v, test_v - std_v,
	                 color="grey", alpha=0.35, zorder=1)


if __name__ == "__main__":
	ps.rc_setup()
	
	main()
	
	plt.show()
