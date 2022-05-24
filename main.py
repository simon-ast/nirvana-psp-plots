import os
import sys
import numpy as np
from spacepy import pycdf
from MODULES.PSPops import data_quality as dq
from MODULES.PSPops import data_transformation as dt
from MODULES.Plotting import plot_settings as ps
from MODULES.PSPops import data_handling as dh
from MODULES.Statistics import data_binning as db
from MODULES.Statistics import stats as st
from astropy.constants import R_sun

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"

# Necessary global variables
ENCOUNTER_NUM = "encounter_5"
DATA_LOCATION = f"{sys.path[0]}/DATA/{ENCOUNTER_NUM}"
STAT_DIR = f"{sys.path[0]}/STATISTICS/BINNED_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(DATA_LOCATION):
	print(f"\n{DATA_LOCATION} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	# Total array initialization
	r_tot = vr_tot = temp_tot = np_tot = np.array([])
	
	# Loop over all files in the desired encounter folder(s), sorted
	# in ascending order of name (equal to date)
	for file in sorted(os.listdir(DATA_LOCATION)):
		
		# Sanity check: print current file name
		print(f"CURRENTLY HANDLING {file}")
		
		# open CDF file and generate dictionary that stores data from
		# file
		cdf_data = pycdf.CDF(f"{DATA_LOCATION}/{file}")
		data = dh.data_generation(cdf_data)
		
		# Indices of non-usable data from general flag + reduction
		bad_ind = dq.general_flag(data["dqf"])
		data = dh.full_reduction(data, bad_ind)
		
		# Additional reduction from "1e-30" meas. indices + reduction
		mf_ind = dq.full_meas_eval(data)
		data = dh.full_reduction(data, mf_ind)
		
		# Transform necessary data
		data["r"], data["theta"], data["phi"] = dt.pos_cart_to_sph(data["pos"])
		data["Temp"] = dt.wp_to_temp(data["wp"])
		
		# Append to total arrays
		r_tot = np.append(r_tot, data["r"])
		vr_tot = np.append(vr_tot, data["vr"])
		np_tot = np.append(np_tot, data["np"])
		temp_tot = np.append(temp_tot, data["Temp"])
	
	# Create distance bins and determine indices of data arrays that
	# correspond to the respective distance bins. Some of these
	# sub-arrays might be empty and have to be handled accordingly
	distance_bins = db.create_bins(0, 100, .5)
	bin_indices = db.sort_bins(distance_bins, r_tot * 1e3 / R_sun.value)
	
	# Make sure to empty the directory containing the data files for
	# binned data values before starting to save files from a new run.
	for file in sorted(os.listdir(STAT_DIR)):
		os.remove(f"{STAT_DIR}/{file}")
	
	# Create a loop for all sub-arrays, and "continue" if the index
	# array is empty
	for key in bin_indices:
		# Skip if the index array is empty
		if not np.size(bin_indices[key]):
			continue
	
		# Determine length of index array and set naming variable for
		# individual file
		sub_len = len(bin_indices[key])
		name_append = "".join(key.strip("()").strip().split(","))
		
		# Create nested arrays with binned data
		binned_r = st.slice_index_list(r_tot, bin_indices[key])
		binned_vr = st.slice_index_list(vr_tot, bin_indices[key])
		binned_np = st.slice_index_list(np_tot, bin_indices[key])
		binned_temp = st.slice_index_list(temp_tot, bin_indices[key])
		
		file_name = f"{STAT_DIR}]/PSP-RBIN-{name_append}.dat"
		with open(file_name, "w") as f:
			f.write("r [km]\t vr [km/s]\t np [cm-3]\t T [K]\n")
			
			for i in range(sub_len):
				f.write(f"{binned_r[i]}\t {binned_vr[i]}\t "
				        f"{binned_np[i]}\t {binned_temp[i]}\n")


if __name__ == "__main__":
	# Set-up plot parameters
	ps.rc_setup()
	
	# Call main function
	main()
