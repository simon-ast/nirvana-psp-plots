import sys
import os
import pandas as pd

from MODULES.Plotting import plotset_general as gp
from MODULES.Plotting import plotset_observations as op
from MODULES.Statistics import stats_databin as db

# DESIGNATE BINNED DATA LOCATION
BIN_DATA_LOCATION = f"{sys.path[0]}/STATISTICS/BINNED_DATA"
# DESIGNATE LOCATION TO SAVE HISTOGRAM PLOTS
HIST_SAVE_DIR = f"{sys.path[0]}/PLOTS/BinHistograms"
# DESIGNATE LOCATION TO SAVE STATISTICAL ANALYSIS OF PARAMETERS
STAT_SAVE_DIR = f"{sys.path[0]}/STATISTICS"
# BIN SIZE DECIMAL POINTS FOR NAMING CONVENTION
BIN_SIZE = db.decimal_length(float(sys.argv[1]))


# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(BIN_DATA_LOCATION):
	print(f"\n{BIN_DATA_LOCATION} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)
if not os.path.isdir(HIST_SAVE_DIR):
	print(f"\n{HIST_SAVE_DIR} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)
if not os.path.isdir(STAT_SAVE_DIR):
	print(f"\n{STAT_SAVE_DIR} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def main():
	# Make sure to empty the directory containing the bin plots for
	# before starting to save files from a new run.
	for file in sorted(os.listdir(HIST_SAVE_DIR)):
		os.remove(f"{HIST_SAVE_DIR}/{file}")
	
	# Loop over all files in the binned data directory
	for name in sorted(os.listdir(BIN_DATA_LOCATION)):
		
		# SANITY CHECK: print current file name
		print(f"CURRENTLY HANDLING {name}")
		
		# Generate correct pointer to data file
		file = BIN_DATA_LOCATION + f"/{name}"
		data_frame = pd.read_json(file)

		# Create bin plots and save them correctly. "plt_nm" cuts off
		# the file extension
		index_ext_rev = name[::-1].find(".") + 1
		plt_nm = name[:-index_ext_rev]
		op.plot_histogram(HIST_SAVE_DIR, data_frame.vr, plt_nm, "vr")
		op.plot_histogram(HIST_SAVE_DIR, data_frame.np, plt_nm, "rho")
		op.plot_histogram(HIST_SAVE_DIR, data_frame.Temp, plt_nm, "temp")
			

if __name__ == "__main__":
	gp.rc_setup()
	
	main()
