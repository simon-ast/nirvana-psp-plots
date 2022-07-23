import sys
import os

# GLOBALS
FILE_NAME = f"{sys.path[0]}/EXECUTE_LOG.dat"


def start_log():
	"""Start the log-file"""
	with open(FILE_NAME, "w") as f:
		f.write("Logging execution of calculation routine.\n\n")


def append_raw_data(enc_numb, raw_array):
	"""Append length before reduction for reference"""
	data_points = len(raw_array)
	
	with open(FILE_NAME, "a") as f:
		f.write(f"For {enc_numb}: \n"
		        f"Total number before reduction = {data_points:.5e}\n\n")
	

def append_encounter_data(enc_numb, measurement_array):
	"""Write length of the array as # of data points"""
	data_points = len(measurement_array)
	
	with open(FILE_NAME, "a") as f:
		f.write(f"For {enc_numb}: \n"
		        f"Total number of data points = {data_points:.5e}\n\n")
	