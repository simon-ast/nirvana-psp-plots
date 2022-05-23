import os
import sys
import numpy as np
from spacepy import pycdf
from PSPops import data_quality as dq
from PSPops import data_transformation as dt
from PSPops import plot_settings as ps
from PSPops import data_handling as dh
from Statistics import data_binning as db
from Statistics import stats as st
from astropy.constants import R_sun

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"

ENCOUNTER_NUM = "encounter_5"
DATA_LOCATION = sys.path[0]+"/DATA/"+ENCOUNTER_NUM

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(DATA_LOCATION):
	print(f"\n{DATA_LOCATION} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	# Total array setup
	epoch_tot = wp_tot = np.array([])
	r_tot = theta = phi = np.array([])
	vr_tot = dvhi = dvlo = np.array([])
	
	for file in sorted(os.listdir(DATA_LOCATION)):
		# Sanity check: print current file name
		print(f"CURRENTLY HANDLING {file}\n")
		
		# open CDF file and generate faulty index array
		cdf_data = pycdf.CDF(DATA_LOCATION+"/"+file)
		data = dh.data_generation(cdf_data)
		
		# Indices of non-usable data from general flag + reduction
		bad_ind = dq.general_flag(data["dqf"])
		data = dh.full_reduction(data, bad_ind)
		
		# Additional reduction from failed measurement indices
		mf_ind = dq.full_meas_eval(data)
		data = dh.full_reduction(data, mf_ind)
		
		# Transform necessary data
		data["r"], data["theta"], data["phi"] = dt.pos_cart_to_sph(data["pos"])
		
		# Append to total arrays
		r_tot = np.append(r_tot, data["r"])
		vr_tot = np.append(vr_tot, data["vr"])
	
	# Create distance bins and determine indices of data arrays that
	# correspond to the respective distance bins. Some of these
	# sub-arrays might be empty and have to be handled accordingly
	distance_bins = db.create_bins(0, 100, 1)
	bin_indices = db.sort_bins(distance_bins, r_tot * 1e3 / R_sun.value)
	
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
		
		binned_r = st.slice_index_list(r_tot, bin_indices[key])
		binned_vr = st.slice_index_list(vr_tot, bin_indices[key])
		
		###
		# EMPTY DIRECTORY BEFORE RUNNING
		###
		
		file_name = f"BINNED_DATA/PSP-RBIN-{name_append}.dat"
		with open(file_name, "w") as f:
			f.write("r [km] \t vr [km/s] \n")
			
			for i in range(sub_len):
				f.write(f"{binned_r[i]} \t {binned_vr[i]}\n")


if __name__ == "__main__":
	# Set-up plot parameters
	ps.rc_setup()
	
	# Call main function
	main()
