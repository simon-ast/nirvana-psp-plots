import sys
import os
import numpy as np
import pandas as pd
from astropy.constants import R_sun

# Global variables (save directory for individual data)
SAVE_DIR = f"{sys.path[0]}/STATISTICS/SPLIT_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(SAVE_DIR):
	print(f"\n{SAVE_DIR} IS NOT A VALID DIRECTORY!\n")
	sys.exit(0)


def approach_recession_slicing(encounter_num, encounter_data):
	"""DOC"""
	# Initialize designation
	designation = "unclear"

	# I need to handle SPAN and SPC separately before slicing
	spc_data = encounter_data[encounter_data["Inst"] == "SPC"]
	span_data = encounter_data[encounter_data["Inst"] == "SPAN"]

	# SPC handling
	tap_spc = find_turn_around(spc_data.posR)
	spc_in = spc_data.iloc[:tap_spc, :]
	spc_out = spc_data.iloc[tap_spc + 1:, :]

	# SPAN handling
	tap_span = find_turn_around(span_data.posR)
	span_in = span_data.iloc[:tap_span, :]
	span_out = span_data.iloc[tap_span + 1:, :]

	# Combine again
	data_part1 = pd.concat(objs=[span_in, spc_in], ignore_index=True)
	data_part2 = pd.concat(objs=[span_out, spc_out], ignore_index=True)
	
	# Save the data from both dictionary
	for df in [data_part1, data_part2]:

		# Skip if there are now entries in the ingress/egress data
		if len(df.columns) == 1:
			continue
		
		# Some definitions for correct file naming
		df.reset_index(drop=True, inplace=True)
		r_start = df.posR.iloc[0] * 1e3 / R_sun.value
		r_end = df.posR.iloc[-1] * 1e3 / R_sun.value
		
		if r_start - r_end >= 0:
			designation = "INGRESS"
		elif r_start - r_end < 0:
			designation = "EGRESS"
		
		save_append_r = f"{r_start:.1f}-{r_end:.1f}"
		
		# Write to files
		file_name = f"{SAVE_DIR}/{encounter_num}_{designation}"
		df.to_json(f"{file_name}.json")


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
