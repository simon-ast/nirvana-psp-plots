import os
import sys
import numpy as np
import pandas as pd
from spacepy import pycdf
from MODULES.PSPops import data_quality as dq, data_turnaround as ta
from MODULES.PSPops import data_transformation as dt
from MODULES.PSPops import data_handling as dh
from MODULES.PSPops import miscellaneous as misc
from MODULES.Plotting import plotset_general as gp
from MODULES.Statistics import stats_databin as db
from MODULES.Statistics import stats_general as st
from MODULES.Miscellaneous import write_log
from astropy.constants import R_sun

# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/usr/local/cdf/lib"

# NECESSARY GLOBAL VARIABLES
ENCOUNTER_NUM = ["encounter_7", "encounter_8", "encounter_9"]
# SIZE OF DISTANCE BINS IN RSOL
DISTANCE_BIN_SIZE = float(sys.argv[1])
DATA_ROOT = f"{sys.path[0]}/DATA"
PLOT_ROOT = f"{sys.path[0]}/PLOTS"
STAT_DIR = f"{sys.path[0]}/STATISTICS"
STAT_DIR_BIN = f"{sys.path[0]}/STATISTICS/BINNED_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(DATA_ROOT):
	print(f"\n{DATA_ROOT} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	# Start the logging file
	write_log.start_log()

	# Pandas empty DataFrame for ALL data
	total_data = pd.DataFrame()
	
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
		
		# Empty DataFrame for Encounter
		data_encounter = pd.DataFrame()
		
		# Instantiate total, non-reduced array for logging
		logging_raw_array = np.array([])
		
		for file in sorted(os.listdir(data_location)):
			
			# Sanity check: print current file name
			print(f"CURRENTLY HANDLING {file}")
			
			# open CDF file and generate pandas DataFrame that stores
			# data from file
			cdf_data = pycdf.CDF(f"{data_location}/{file}")
			data = dh.data_generation(cdf_data)

			# Log the number of data points before reduction
			logging_raw_array = np.append(logging_raw_array, len(data.columns))
			
			# Indices of non-usable data from general flag + reduction
			bad_ind = dq.general_flag(data.dqf.values)
			data.drop(bad_ind, inplace=True)
			data.reset_index(drop=True, inplace=True)
			
			# Additional reduction from "-1e-30" meas. indices + reduction
			mf_ind = dq.full_meas_eval(data)
			data.drop(mf_ind, inplace=True)
			data.reset_index(drop=True, inplace=True)
			
			# Transform necessary data
			data["posR"], data["posTH"], data["posPH"] = dt.pos_cart_to_sph(
				data.posX, data.posY, data.posZ
			)
			data["Temp"] = dt.wp_to_temp(data["wp"])

			# Add the DataFrame of one encounter to the total array
			data_encounter = pd.concat([data_encounter, data])

		# After looping through one full encounter, generate the
		# approach/recession divide and append and then extend the FULL
		# DataFrame
		data_encounter.reset_index(drop=True, inplace=True)
		
		# Take in the total data from one encounter and save the values
		# for approach and recession independently
		ta.approach_recession_slicing(folder, data_encounter)
		
		# Log the total amount of measurements per encounter for future
		# reference
		write_log.append_raw_data(folder, logging_raw_array)
		write_log.append_encounter_data(folder, data_encounter.posR)
		
		# Total data frame
		total_data = pd.concat([data_encounter, total_data])
		total_data.reset_index(drop=True, inplace=True)

	# Create distance bins and group the data frame according to
	# determined indices of data arrays that correspond to the
	# respective distance bins. The object 'dist_groups' is an index
	# array for the total data frame
	distance_bins = np.arange(0, 100, DISTANCE_BIN_SIZE)
	dist_groups = total_data.groupby(
		np.digitize(total_data.posR * 1e3 / R_sun.value, distance_bins)
	)

	# Make sure to empty the directory containing the data files for
	# binned data values before starting to save files from a new run.
	for file in sorted(os.listdir(STAT_DIR_BIN)):
		os.remove(f"{STAT_DIR_BIN}/{file}")
	
	# Loop over all created bins to sort the total data. Also log number
	# of data points and the corresponding distance bin index (see
	# empty arrays below)
	num_points = []
	dist_index = []

	# Compute and save data frame for total stats (mean, median, std,
	# q1, g3). It is of note here that "pd.assign(name=value)" creates a
	# new column in the data frame filled with "value"
	total_stats = pd.concat(
		objs=[
			dist_groups.mean(numeric_only=True).assign(Type="mean"),
			dist_groups.std(numeric_only=True).assign(Type="std"),
			dist_groups.median(numeric_only=True).assign(Type="median"),
			dist_groups.quantile(q=0.25, numeric_only=True).assign(Type="q1"),
			dist_groups.quantile(q=0.75, numeric_only=True).assign(Type="q3")
		],
		ignore_index=True
	)
	total_stats.to_json(f"{STAT_DIR}/PSP_STATISTICS.json")

	# Save bins individually for posterity (not necessary to read in
	# separately anymore after change to pandas). Get the number of
	# decimal points used in bin size for file naming purposes.
	dec_pts = db.decimal_length(DISTANCE_BIN_SIZE)
	for r_bin, grp in dist_groups:

		# Generalized necessary variables
		# TODO: Is "Hashable" a problem here?
		bin_name = r_bin * DISTANCE_BIN_SIZE
		file_name = f"PSP_BIN_{bin_name:.{dec_pts}f}-" \
					f"{bin_name + DISTANCE_BIN_SIZE:.{dec_pts}f}.json"

		# SANITY CHECK:
		# Stop if the distance bins exceed the simulation domain size of 40 Rs
		if bin_name > 40.0:
			print(
				f"\n\nSTOPPING AT {file_name},"
				f"OUTSIDE SIMULATION DOMAIN SIZE!\n\n"
			)
			break

		# Save Data Frames of distance bins to JSON file
		grp.to_json(f"{STAT_DIR_BIN}/{file_name}")
		
		# Append to parameters for plot below
		num_points += [grp.shape[0]]
		dist_index += [bin_name]
		
	# THIS RUNS AFTER THE BIN LOOP!
	# Plot a simple scatter plot with # of data points per bin
	# TODO: Add # of data points from SPAN-i here individually
	gp.bin_analysis(PLOT_ROOT, num_points, dist_index)


if __name__ == "__main__":
	# Set-up plot parameters
	gp.rc_setup()
	
	# Call main function
	main()
