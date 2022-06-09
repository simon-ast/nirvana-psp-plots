import sys
import numpy as np
from MODULES.Plotting import plot_settings as ps


# GLOBAL: STAT FILE NAME
STAT_FILE = f"{sys.path[0]}/STATISTICS/PSP_STATISTICS.dat"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/FinalPlots"


def main():
	# Read in statistics file
	main_parameters = ["vr", "rho", "temp"]
	stat_data = stat_data_dict(STAT_FILE)
	
	# Plot setup
	ps.rc_setup()
	
	# Plotting all three major parameters
	for parameter in main_parameters:
		ps.plot_finals(stat_data, parameter, PLOT_SAVE_DIR)


def stat_data_dict(file_name):
	"""Generates dictionaries of statistical data from file read-in."""
	raw_data = np.loadtxt(file_name, skiprows=1)
	
	return {
		"r": raw_data[:, 0],
		"vr": {
			"mean"  : raw_data[:, 1],
			"stddev": raw_data[:, 2],
			"median": raw_data[:, 3],
			"q1"    : raw_data[:, 4],
			"q3"    : raw_data[:, 5]
		},
		"rho": {
			"mean"  : raw_data[:, 6],
			"stddev": raw_data[:, 7],
			"median": raw_data[:, 8],
			"q1"    : raw_data[:, 9],
			"q3"    : raw_data[:, 10]
		},
		"temp": {
			"mean"  : raw_data[:, 11],
			"stddev": raw_data[:, 12],
			"median": raw_data[:, 13],
			"q1"    : raw_data[:, 14],
			"q3"    : raw_data[:, 15]
		}
	}
	

if __name__ == "__main__":
	main()
