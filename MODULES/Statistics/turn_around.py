import sys
import os
import numpy as np
import typing as tp
from astropy.constants import R_sun

# Global variables (save directory for individual data)
SAVE_DIR = f"{sys.path[0]}/STATISTICS/SPLIT_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(SAVE_DIR):
	print(f"\n{SAVE_DIR} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def find_turn_around(distance_array: np.ndarray) -> int:
	"""
	Finds the turn-around point of a distance array. This requires a
	sorted read-in of all encounter data (otherwise the distance values
	will not show a sin-like variation)
	
	:param distance_array: NDARRAY,
		Array of radial distance values
	:return: INT,
		Index of turn-around point of the array
	"""
	tap = np.argmin(distance_array)
	return int(tap)


def approach_recession_slicing(encounter_num, data: tp.Dict):
	""""""
	# Initialize empty temporary dictionaries
	data_1 = {}
	data_2 = {}
	
	# Determine the index of the turn-around point
	tap = find_turn_around(data["r"])
	
	# Fill the temporary arrays
	for key in data.keys():
		data_1[key] = data[key][:tap + 1]   # Slicing def. needs + 1
		data_2[key] = data[key][tap:]
	
	# Save the data from both dictionary
	for data_dict in [data_1, data_2]:
		
		# Some definitions for correct file naming
		r_start = data_dict["r"][0] * 1e3 / R_sun.value
		r_end = data_dict["r"][-1] * 1e3 / R_sun.value
		
		if r_start - r_end >= 0:
			designation = "APPROACH"
		elif r_start - r_end < 0:
			designation = "RECESSION"
		
		save_append_r = f"{r_start:.1f}-{r_end:.1f}"
		
		# Write to files
		file_name = f"{SAVE_DIR}/{encounter_num}_{designation}" \
		            f"_{save_append_r}Rs.dat"
		with open(file_name, "w") as f:
			f.write(f"{encounter_num}:\t {designation}\n")
			f.write("r [km]\t vr [km/s]\t np [cm-3]\t T [K]\n")
			
			for i in range(len(data_dict["r"])):
				f.write(f'{data_dict["r"][i]}\t {data_dict["vr"][i]}\t '
				        f'{data_dict["np"][i]}\t {data_dict["Temp"][i]}\n')
