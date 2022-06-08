import os
import sys
import numpy as np
from spacepy import pycdf
from MODULES.PSPops import data_quality as dq
from MODULES.PSPops import data_transformation as dt
from MODULES.PSPops import data_handling as dh
from MODULES.Plotting import plot_settings as ps
from MODULES.Statistics import data_binning as db
from MODULES.Statistics import stats as st
from MODULES.Statistics import turn_around as ta
from astropy.constants import R_sun

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"

# Necessary global variables
ENCOUNTER_NUM = ["encounter_7", "encounter_8",
                 "encounter_9", "encounter_10"]
DATA_ROOT = f"{sys.path[0]}/DATA"
STAT_DIR = f"{sys.path[0]}/STATISTICS/BINNED_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(DATA_ROOT):
	print(f"\n{DATA_ROOT} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	# Total array initialization
	r_tot = vr_tot = temp_tot = np_tot = np.array([])
	
	# Loop over all files in the desired encounter folder(s), sorted
	# in ascending order of name (equal to date)
	for folder in ENCOUNTER_NUM:
		
		# Sanity check: print current folder name
		print(f"\nCURRENTLY HANDLING {folder}")
		
		# Variable for current folder
		data_location = f"{DATA_ROOT}/{folder}"
		
		# SANITY CHECK: Does the data directory even exist?
		if not os.path.isdir(data_location):
			print(f"\n{data_location} IS NOT A VALID DIRECTORY!\n")
			sys.exit(0)
		
		# Generate sub-total arrays for encounters individually
		r_file = vr_file = temp_file = np_file = np.array([])
		
		for file in sorted(os.listdir(data_location)):
			
			# Sanity check: print current file name
			print(f"CURRENTLY HANDLING {file}")
			
			# open CDF file and generate dictionary that stores data from
			# file
			cdf_data = pycdf.CDF(f"{data_location}/{file}")
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
			
			##
			# FIND TURN-AROUND AND SAVE APPROACH AND RECESSION DATA
			"""
			Save measurement data to encounter_X_STARTRs-ENDRs.dat
			"""
			##
			
			# Append to total arrays
			r_file = np.append(r_file, data["r"])
			vr_file = np.append(vr_file, data["vr"])
			np_file = np.append(np_file, data["np"])
			temp_file = np.append(temp_file, data["Temp"])
		
		# After all files of an individual encounter are handled,
		# generate the approach/recession divide and append to the
		# total arrays
		temp_data_dict = {"r": r_file, "vr": vr_file,
		                  "np": np_file, "Temp": temp_file}
		
		# Take in the total data from one encounter and save the values
		# for approach and recession independently
		# ta.approach_recession_slicing(folder, temp_data_dict)
		
		# Total value arrays
		r_tot = np.append(r_tot, r_file)
		vr_tot = np.append(vr_tot, vr_file)
		np_tot = np.append(np_tot, np_file)
		temp_tot = np.append(temp_tot, temp_file)
	
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
		name_append_list = "".join(key.strip("()").strip().split(",")).split()
		name_append = f"{name_append_list[0]}-{name_append_list[1]}"
		
		# Create nested arrays with binned data
		binned_r = st.slice_index_list(r_tot, bin_indices[key])
		binned_vr = st.slice_index_list(vr_tot, bin_indices[key])
		binned_np = st.slice_index_list(np_tot, bin_indices[key])
		binned_temp = st.slice_index_list(temp_tot, bin_indices[key])
		
		file_name = f"{STAT_DIR}/PSP-RBIN-{name_append}.dat"
		with open(file_name, "w") as f:
			f.write(f"START:\t {name_append_list[0]}\n"
			        f"END:\t {name_append_list[1]}\n\n")
			f.write("r [km]\t vr [km/s]\t np [cm-3]\t T [K]\n")
			
			for i in range(sub_len):
				f.write(f"{binned_r[i]}\t {binned_vr[i]}\t "
				        f"{binned_np[i]}\t {binned_temp[i]}\n")


if __name__ == "__main__":
	# Set-up plot parameters
	ps.rc_setup()
	
	# Call main function
	main()
