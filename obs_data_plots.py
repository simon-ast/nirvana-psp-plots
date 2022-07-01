import sys
from MODULES.PSPops import data_handling as dh
from MODULES.Plotting import general_plotset as gp
from MODULES.Plotting import obs_plotset as op


# GLOBAL: STAT FILE NAME
STAT_FILE = f"{sys.path[0]}/STATISTICS/PSP_STATISTICS.dat"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ObsDataPlots"


def main():
	# Read in statistics file
	main_parameters = ["vr", "rho", "temp"]
	stat_data = dh.stat_data_dict(STAT_FILE)
	
	# Plot setup
	gp.rc_setup()
	
	# Plotting all three major parameters
	for parameter in main_parameters:
		op.plot_finals(stat_data, parameter, PLOT_SAVE_DIR)
	

if __name__ == "__main__":
	main()
