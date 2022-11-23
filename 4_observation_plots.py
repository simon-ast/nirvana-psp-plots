import sys
import pandas as pd
from modules.plotting import plotset_general as pg
from modules.plotting import plotset_observations as po


# GLOBAL: STAT FILE NAME
STAT_DATA_FILE = f"{sys.path[0]}/STATISTICS/PSP_STATISTICS.json"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ObsDataPlots"


def main():
	# Read in statistics file
	main_parameters = ["vr", "np", "Temp"]
	stat_data = pd.read_json(STAT_DATA_FILE)

	# Plot setup
	pg.rc_setup()
	
	# Plotting all three major parameters
	for parameter in main_parameters:
		po.plot_finals(stat_data, parameter, PLOT_SAVE_DIR)
	

if __name__ == "__main__":
	main()
