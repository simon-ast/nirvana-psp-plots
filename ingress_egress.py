import os
import sys
import typing as tp
import numpy as np
from astropy.constants import R_sun
from astropy import units as u
from MODULES.Plotting import general_plotset as  gp
from MODULES.Plotting import obs_plotset as op
from MODULES.Statistics import data_binning as db
from MODULES.Statistics import stats as st

# DISTANCE BIN SIZE IN RSOL
DISTANCE_BIN_SIZE = float(sys.argv[1])

# DATA LOCATION OF SPLIT DATA AND PLOTS
SPLIT_DATA_LOCATION = f"{sys.path[0]}/STATISTICS/SPLIT_DATA"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ApproachRecessionPlots"

# CUSTOM COLOUR LIST FOR PLOTTING [NESTED 10 x 2]
COLOUR_LIST = [[], [], [], [], [], [],
               ["maroon", "tomato"],
               ["darkgreen", "springgreen"],
               ["teal", "darkturquoise"],
               ["darkblue", "royalblue"]]


def orbit_readin(filename: str) -> tp.Dict:
	"""Read in file data and create dictionary"""
	# Generate label and colour designation from header of file
	with open(filename, "r") as f:
		header = f.readline().strip().split()
	
	# Extract individual necessary designation keys
	enc_numb = int(header[0][:-1].split("_")[1])    # Encounter number
	enc_type = header[1].lower()                    # Encounter type
	
	# Assign more appropriate label formatting
	enc_lab = f"Encounter {enc_numb} ({enc_type})"
	
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
	
	# Loop over all split files in the directory
	for file in sorted(os.listdir(folder)):
		print(f"CURRENTLY HANDLING {file}")
		
		# Generate total file name
		file_name = f"{folder}/{file}"
		
		# Read in (1) and append (2) to total data
		file_data = orbit_readin(file_name)
		data_orbit_analysis(file_data)
		
		# Add to existing plots
		ax_vr.plot(file_data["r_bin"], file_data["vr_med"],
		           label=file_data["label"], color=file_data["pcolour"],
		           ls=file_data["ls"], lw=2)
		ax_np.plot(file_data["r_bin"], file_data["np_med"],
		           label=file_data["label"], color=file_data["pcolour"],
		           ls=file_data["ls"], lw=2)
		ax_t.plot(file_data["r_bin"], file_data["T_med"],
		          label=file_data["label"], color=file_data["pcolour"],
		          ls=file_data["ls"], lw=2)
	
	# Finalize and save plots
	ax_vr.legend()
	fig_vr.savefig(f"{PLOT_SAVE_DIR}/PSP_AR_RadialVelocity.png")
	
	ax_np.legend()
	fig_np.savefig(f"{PLOT_SAVE_DIR}/PSP_AR_Density.png")
	
	ax_t.legend()
	fig_t.savefig(f"{PLOT_SAVE_DIR}/PSP_AR_Temperature.png")
	

if __name__ == "__main__":
	# GENERAL PLOTTING PARAMETERS
	gp.rc_setup()
	
	# CALL ALL NESTED FUNCTIONS
	orbit_plots(SPLIT_DATA_LOCATION)
