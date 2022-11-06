import os
import sys
import typing as tp

import matplotlib.pyplot as plt
import numpy as np
from astropy.constants import R_sun
from astropy import units as u
from MODULES.PSPops import data_handling as dh
from MODULES.Plotting import plotset_general as gp
from MODULES.Plotting import plotset_observations as op
from MODULES.Statistics import stats_databin as db
from MODULES.Statistics import stats_general as st

# DISTANCE BIN SIZE IN RSOL
DISTANCE_BIN_SIZE = float(sys.argv[1])

# DATA LOCATION OF SPLIT DATA AND PLOTS
SPLIT_DATA_LOCATION = f"{sys.path[0]}/STATISTICS/SPLIT_DATA"
STAT_DATA_FILE = f"{sys.path[0]}/STATISTICS/PSP_STATISTICS.dat"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ApproachRecessionPlots"

# CUSTOM COLOUR LIST FOR PLOTTING [NESTED 10 x 2]
COLOUR_LIST = [[], [], [], [], [], [],
               ["red", "orange"],
               ["darkgreen", "lime"],
               ["blue", "cyan"],
               ["darkviolet", "fuchsia"]]


def orbit_readin(filename: str) -> tp.Dict:
	"""Read in file data and create dictionary"""
	# Generate label and colour designation from header of file
	with open(filename, "r") as f:
		header = f.readline().strip().split()
	
	# Extract individual necessary designation keys
	enc_numb = int(header[0][:-1].split("_")[1])    # Encounter number
	enc_type = header[1].lower()[:2]                # Encounter type (in/eg)
	
	# Assign more appropriate label formatting
	enc_lab = f"E{enc_numb}-{enc_type}"
	
	# Set a plot color index based on approach or recession
	if enc_type[0] == "i":
		plot_colour = COLOUR_LIST[enc_numb - 1][0]
		linestyle = "-"
	else:
		plot_colour = COLOUR_LIST[enc_numb - 1][1]
		linestyle = "--"
	
	# Read in stored data
	data = np.loadtxt(filename, skiprows=2)
	
	# Generate a result dictionary
	result = {
		"label"  : enc_lab,
		"pcolour": plot_colour,
		"ls"     : linestyle,
		"r"      : data[:, 0] / R_sun.to(u.km).value,
		"vr"     : data[:, 1],
		"np"     : data[:, 2],
		"T"      : data[:, 3]
	}
	
	return result


def data_orbit_analysis(data_dict: tp.Dict) -> None:
	"""Update data dictionary with "plottable" values"""
	# Instantiate empty arrays to be filled
	distance = rad_vel = num_den = temp = np.array([])
	
	# Create distance bins and zip indices
	distance_bins = db.create_bins(0, 100, DISTANCE_BIN_SIZE)
	bin_indices = db.sort_bins(distance_bins, data_dict["r"])
	
	# Loop over all index bins and sort data individually
	for key in bin_indices:
		# Skip if the index array is empty
		if not np.size(bin_indices[key]):
			continue
		
		# Radial plot values should be bin centres
		name_append_list = "".join(key.strip("()").strip().split(",")).split()
		bin_lo = float(name_append_list[0])
		bin_hi = float(name_append_list[1])
		bin_mid = bin_lo + (bin_hi - bin_lo) / 2
		
		# Sort radial velocity into bins and determine medians
		vr_temp = st.slice_index_list(data_dict["vr"], bin_indices[key])
		vr_median = np.median(vr_temp)
		
		# Sort number density into bins and determine medians
		np_temp = st.slice_index_list(data_dict["np"], bin_indices[key])
		np_median = np.median(np_temp)
		
		# Sort temperature into bins and determine medians
		t_temp = st.slice_index_list(data_dict["T"], bin_indices[key])
		t_median = np.median(t_temp)
		
		# Update total arrays
		distance = np.append(distance, bin_mid)
		rad_vel = np.append(rad_vel, vr_median)
		num_den = np.append(num_den, np_median)
		temp = np.append(temp, t_median)

	# Modify existing data dictionary
	data_dict["r_bin"] = distance
	data_dict["vr_med"] = rad_vel
	data_dict["np_med"] = num_den
	data_dict["T_med"] = temp
	
	return None


def orbit_plots(folder: str) -> None:
	"""Plot and save the three major parameters"""
	# Instantiate three plots: vr, np and T
	fig_vr, ax_vr = op.plot_setup("Radial velocity")
	fig_np, ax_np = op.plot_setup("Density")
	fig_t, ax_t = op.plot_setup("Temperature")
	
	# Instantiate combined plots
	fig_com, ax_vr_com, ax_np_com, ax_t_com = op.plot_setup_obs_comb()
	
	# Create (archaic) sorted list of files by asc. encounter number
	# varying ingress - egress
	raw_file_list = sorted(os.listdir(folder))
	# file_list = raw_file_list[1:] + [raw_file_list[0]]
	file_list = raw_file_list
	
	# Loop over all split files in the directory
	for file in file_list:
		print(f"CURRENTLY HANDLING {file}")
		
		# Generate total file name
		file_name = f"{folder}/{file}"
		
		# Read in (1) and append (2) to total data
		file_data = orbit_readin(file_name)
		data_orbit_analysis(file_data)
		
		# Add to existing plots
		for vr_axis in (ax_vr, ax_vr_com[0]):
			vr_axis.plot(file_data["r_bin"], file_data["vr_med"],
			             label=file_data["label"], color=file_data["pcolour"],
			             ls=file_data["ls"], lw=2)
		
		for np_axis in (ax_np, ax_np_com[0]):
			np_axis.plot(file_data["r_bin"], file_data["np_med"],
			             label=file_data["label"], color=file_data["pcolour"],
			             ls=file_data["ls"], lw=2)
		for tem_axis in (ax_t, ax_t_com[0]):
			tem_axis.plot(file_data["r_bin"], file_data["T_med"],
			              label=file_data["label"], color=file_data["pcolour"],
			              ls=file_data["ls"], lw=2)
	
	# Fill in mean (or median) plots
	stat_data = dh.stat_data_dict(STAT_DATA_FILE)
	plot_stats(ax_vr_com[1], stat_data, "vr")
	plot_stats(ax_np_com[1], stat_data, "rho")
	plot_stats(ax_t_com[1], stat_data, "temp")
	
	# Finalize and save individual plots
	ax_vr.legend(ncol=3)
	plt.tight_layout()
	fig_vr.savefig(f"{PLOT_SAVE_DIR}/PSP_AR_RadialVelocity.eps")
	
	ax_np.legend()
	plt.tight_layout()
	fig_np.savefig(f"{PLOT_SAVE_DIR}/PSP_AR_Density.eps")
	
	ax_t.legend()
	plt.tight_layout()
	fig_t.savefig(f"{PLOT_SAVE_DIR}/PSP_AR_Temperature.eps")
	
	# Finalize and save total plot
	ax_vr_com[0].legend(ncol=3)
	ax_vr_com[1].legend()
	fig_com.tight_layout()
	fig_com.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_measurements.eps")
	fig_com.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_measurements.svg")


def plot_stats(ax, stat_data, key_name):
	"""DOC"""
	ax.plot(stat_data["r"], stat_data[key_name]["mean"],
	        lw=2, color="tab:blue",
	        label="mean", zorder=5)
	
	ax.fill_between(
		x=stat_data["r"],
		y1=stat_data[key_name]["mean"] - stat_data[key_name]["stddev"],
		y2=stat_data[key_name]["mean"] + stat_data[key_name]["stddev"],
		color="lightblue", label="1$\\sigma$", zorder=4)
	

if __name__ == "__main__":
	# GENERAL PLOTTING PARAMETERS
	gp.rc_setup()
	
	# CALL ALL NESTED FUNCTIONS
	orbit_plots(SPLIT_DATA_LOCATION)
