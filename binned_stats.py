import sys
import os
import numpy as np
from MODULES.Plotting import plot_settings as ps
from MODULES.Statistics import stats as st

# DESIGNATE BINNED DATA LOCATION
BIN_DATA_LOCATION = f"{sys.path[0]}/STATISTICS/BINNED_DATA"
# DESIGNATE LOCATION TO SAVE HISTOGRAM PLOTS
HIST_SAVE_DIR = f"{sys.path[0]}/PLOTS/BinHistograms"
# DESIGNATE LOCATION TO SAVE STATISTICAL ANALYSIS OF PARAMETERS
STAT_SAVE_DIR = f"{sys.path[0]}/STATISTICS"


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
	# DEFINE A NAME FOR THE STATISTICAL DATA FILES (WITH FUTURE
	# ADJUSTMENT NECESSARY) AND MAKE FIRST ENTRIES
	stat_file_name = "PSP_STATISTICS.dat"
	with open(f"{STAT_SAVE_DIR}/{stat_file_name}", "w") as f:
		# File Header
		f.write("r [Rsol]\t "
		        "vr_mean [km/s]\t vr_stddev [km/s]\t "
		        "vr_median [km/s]\t vr_q1 [km/s]\t vr_q3 [km/s]\t "
		        "rho_mean [cm-3]\t rho_stddev [cm-3]\t "
		        "rho_median [cm-3]\t rho_q1 [cm-3]\t rho_q3 [cm-3]\t "
		        "T_mean [K]\t T_stddev [K]\t "
		        "T_median [K]\t T_q1 [K]\t T_q3 [K]\n")
	
	# Make sure to empty the directory containing the bin plots for
	# before starting to save files from a new run.
	for file in sorted(os.listdir(HIST_SAVE_DIR)):
		os.remove(f"{HIST_SAVE_DIR}/{file}")
	
	# Loop over all files in the binned data directory
	for name in sorted(os.listdir(BIN_DATA_LOCATION)):
		
		# Generate correct pointer to data file
		file = BIN_DATA_LOCATION + f"/{name}"
		
		# Read out lower and upper end of the individual bins
		header = np.genfromtxt(file, max_rows=2)
		bin_lo = header[0][1]
		bin_hi = header[1][1]
		dist_ind = bin_lo + (bin_hi - bin_lo) / 2
		
		# Generate numpy array from data files (multi-dim)
		all_data = np.loadtxt(file, skiprows=4)
		
		# Generate sub-arrays from all data
		vr = all_data[:, 1]
		rho = all_data[:, 2]
		temp = all_data[:, 3]
		
		# Sets of statistical data for each parameter
		stat_vr = st.stat_ana(vr)
		stat_rho = st.stat_ana(rho)
		stat_temp = st.stat_ana(temp)
		
		# Create bin plots and save them correctly
		ps.plot_histogram(HIST_SAVE_DIR, vr, bin_lo, bin_hi, "vr")
		ps.plot_histogram(HIST_SAVE_DIR, rho, bin_lo, bin_hi, "rho")
		ps.plot_histogram(HIST_SAVE_DIR, temp, bin_lo, bin_hi, "temp")
		
		# Fill in data file values
		with open(f"{STAT_SAVE_DIR}/{stat_file_name}", "a") as f:
			f.write(f"{dist_ind}\t "
			        f"{stat_vr['mean']:.3f}\t {stat_vr['stddev']:.3f}\t "
			        f"{stat_vr['median']:.3f}\t {stat_vr['q1']:.3f}\t "
			        f"{stat_vr['q3']:.3f}\t "
			        f"{stat_rho['mean']:.3f}\t {stat_rho['stddev']:.3f}\t "
			        f"{stat_rho['median']:.3f}\t {stat_rho['q1']:.3f}\t "
			        f"{stat_rho['q3']:.3f}\t "
			        f"{stat_temp['mean']:.3f}\t {stat_temp['stddev']:.3f}\t "
			        f"{stat_temp['median']:.3f}\t {stat_temp['q1']:.3f}\t "
			        f"{stat_temp['q3']:.3f}\n")
		

if __name__ == "__main__":
	ps.rc_setup()
	
	main()
