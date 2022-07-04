import sys
from MODULES.Statistics import data_read
from MODULES.Plotting import general_plotset as gp
from MODULES.Plotting import comp_plotset as cp


# Necessary global variables
PSP_STAT_DIR = f"{sys.path[0]}/STATISTICS"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ComparisonPlots"


def main():
	gp.rc_setup()
	
	sim_data_eq = data_read.SimMeshData(f"{PSP_STAT_DIR}/sim_data_eq.csv")
	sim_data_pol = data_read.SimMeshData(f"{PSP_STAT_DIR}/sim_data_polar.csv")
	PSP_stats = data_read.PSPStatData(f"{PSP_STAT_DIR}/PSP_STATISTICS.dat",
	                                  sim_data_eq)
	
	for indicator in ["vr", "np", "T"]:
		cp.comparison_plot(indicator, PSP_stats, sim_data_eq, sim_data_pol,
		                   PLOT_SAVE_DIR)


if __name__ == "__main__":
	main()
