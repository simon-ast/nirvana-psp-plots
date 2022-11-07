import sys
import pandas as pd
from MODULES.PSPops import data_handling as dh
from MODULES.Plotting import plotset_general as gp
from MODULES.Plotting import plotset_observations as op


# GLOBAL: STAT FILE NAME
STAT_DATA_FILE = f"{sys.path[0]}/STATISTICS/PSP_STATISTICS.json"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ObsDataPlots"


def main():
	# Read in statistics file
	main_parameters = ["vr", "np", "Temp"]
	stat_data = pd.read_json(STAT_DATA_FILE)

	# Plot setup
	gp.rc_setup()
	
	# Plotting all three major parameters
	for parameter in main_parameters:
		op.plot_finals(stat_data, parameter, PLOT_SAVE_DIR)
	

if __name__ == "__main__":
	main()
