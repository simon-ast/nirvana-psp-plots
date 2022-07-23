import numpy as np
import typing as tp


def slice_index_list(value_array: np.ndarray,
                     index_list: np.ndarray) -> np.ndarray:
	"""
	Extracts a given set of values from a total array.
	
	:param value_array: NDARRAY,
		Value array
	:param index_list: NDARRAY,
		List of indices to be extracted
	:return: NDARRAY,
		Subarray containing index_list values
	"""
	sliced_array = np.array([
		value_array[i] for i in index_list
	])
	
	return sliced_array


def stat_ana(value_sample: np.ndarray) -> tp.Dict:
	"""
	For a given array of data, this function returns a dictionary
	storing statistical data.
	
	:param value_sample: NDARRAY,
		Value array
	:return: DICT,
		Dictionary containing mean, median, standard deviation and
		percentiles 25 and 75.
	"""
	mean = np.mean(value_sample)
	median = np.median(value_sample)
	std = np.std(value_sample)
	q1 = np.percentile(value_sample, 25)
	q3 = np.percentile(value_sample, 75)
	
	return {
		"mean": mean,
		"stddev": std,
		"median": median,
		"q1": q1,
		"q3": q3
	}
	
	