import numpy as np
import typing as tp
import logging

# Logging functionality. Comment out first line to enable logging.
logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format="%(message)s")


def create_bins(lower_bound, upper_bound, bin_size):
	"""
	Returns an equal-width (distance) partitioning. as an ascending list
	of tuples.
	
	:param lower_bound:
	:param upper_bound:
	:param bin_size:
	:return:
	"""
	# Sanity check
	assert (upper_bound - lower_bound) % bin_size == 0, \
		f"RANGE {lower_bound} TO {upper_bound} WITH BIN SIZE {bin_size}" \
		f" CANNOT BE EQUALLY DIVIDED INTO BINS (MIGHT BE INCORRECT?)!"
	
	# Create bins as list
	bins = []
	bin_lo = lower_bound
	bin_up = 0
	
	while bin_up <= upper_bound:
		bin_up = bin_lo + bin_size
		bins.append((bin_lo, bin_up))
		
		bin_lo = bin_up
		bin_up += bin_size
	
	logging.debug("Calling create_bin(lower_bound=%d, "
	              "upper_bound=%d, bin_size=%d)",
	              lower_bound, upper_bound, bin_size)
	logging.debug("FIRST BIN = (%f, %f)", bins[0][0], bins[0][1])
	logging.debug("LAST BIN = (%f, %f)", bins[-1][0], bins[-1][1])
		
	return bins


def find_bin(value, bins):
	"""
	Takes a value and tries to assign an index of a list of bins in an
	effort to sort it into the list. If that fails, the call exits.
	
	:param value:
	:param bins:
	:return:
	"""
	for i in range(len(bins)):
		if bins[i][0] <= value < bins[i][1]:
			return i
	
	print(f"VALUE {value} COULD NOT BE ASSIGNED!")
	exit()


def sort_bins(bins: tp.List[tp.Tuple],
              input_array: np.ndarray
              ) -> tp.Dict:
	"""
	Returns a dictionary, assigning index lists of the input_array to
	dictionary keys representing the bin designations.
	
	:param bins:
	:param input_array:
	:return:
	"""
	num_bins = len(bins)
	
	bin_dict_keys = [str(bins[i]) for i in range(num_bins)]
	bin_indices = [[] for _ in range(num_bins)]
	
	for i in range(len(input_array)):
		bin_index = find_bin(input_array[i], bins)
		bin_indices[bin_index].append(i)
	
	bin_dict = dict(zip(bin_dict_keys, bin_indices))
	
	return bin_dict
