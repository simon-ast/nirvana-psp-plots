import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import typing as tp
from MODULES.Plotting import plot_settings as ps

DATA_ROOT = f"{sys.path[0]}/STATISTICS/SPLIT_DATA"


def main():
	
	for file in sorted(os.listdir(DATA_ROOT)):
		file_name = f"{DATA_ROOT}/{file}"
		
		data = read_in(file_name)
		
		plt.plot(data["r"], data["vr"], label=file)
	
	plt.legend()
	plt.show()


def read_in(file_name: str) -> tp.Dict:
	""""""
	# Initialize result dictionary
	data = {}
	
	# Raw data from individual files
	data_raw = np.loadtxt(file_name, skiprows=2)
	
	# Split raw data into dictionary
	data["r"] = data_raw[:, 0]
	data["vr"] = data_raw[:, 1]
	data["np"] = data_raw[:, 2]
	data["Temp"] = data_raw[:, 3]
	
	return data


if __name__ == "__main__":
	# General rcParam setup
	ps.rc_setup()
	
	# Call of main function
	main()
