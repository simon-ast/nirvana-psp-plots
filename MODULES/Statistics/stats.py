import numpy as np


def slice_index_list(value_array, index_list):
	"""
	DOC
	
	:param value_array:
	:param index_list:
	:return:
	"""
	sliced_array = np.array([
		value_array[i] for i in index_list
	])
	
	return sliced_array


def stat_ana(value_sample):
	"""
	DOC
	
	:param value_sample:
	:return:
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
	
	