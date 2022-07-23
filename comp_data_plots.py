import sys
from MODULES.Statistics import data_read
from MODULES.Plotting import general_plotset as gp
from MODULES.Plotting import comp_plotset as cp


# Necessary global variables
PSP_STAT_DIR = f"{sys.path[0]}/STATISTICS"
ML_CONT = f"{sys.path[0]}/STATISTICS/MASSLOSS_CONTOURS"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ComparisonPlots"


def main():
	gp.rc_setup()
	
	sim_data_eq = data_read.SimMeshData(f"{PSP_STAT_DIR}/sim_data_eq.csv")
	sim_data_pol = data_read.SimMeshData(f"{PSP_STAT_DIR}/sim_data_polar.csv")
	PSP_stats = data_read.PSPStatData(f"{PSP_STAT_DIR}/PSP_STATISTICS.dat",
	                                  sim_data_eq)
	
	# Generate individual plots for each parameter of interest
	for indicator in ["vr", "np", "T", "massloss", "rampressure"]:
		cp.comparison_plot(indicator, PSP_stats, sim_data_eq, sim_data_pol,
		                   PLOT_SAVE_DIR)
	
	# Use more specific plotting set-ups tailored to the paper
	cp.bin_meas_numb(PSP_stats, PLOT_SAVE_DIR)
	cp.paper_npT_com(PSP_stats, sim_data_eq, sim_data_pol, PLOT_SAVE_DIR)
	
	# RP and ML, with integrated ML
	mli_dist, mli_ml = data_read.massloss_interpolate(f"{ML_CONT}")
	cp.paper_plot_mlrp(PSP_stats, sim_data_eq, sim_data_pol, mli_dist, mli_ml,
	                   PLOT_SAVE_DIR)


if __name__ == "__main__":
	main()
