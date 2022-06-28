import numpy as np
import astropy.constants as c


class PSPStatData:
	def __init__(self, filename, sim_data):
		raw_data = np.loadtxt(filename, skiprows=1)
		
		# Correct for maximum distance of simulation data
		co_index = np.where(raw_data[:, 0] >= sim_data.dist[-1])[0][0]
		raw_data = raw_data[:co_index]
		
		# Positional data
		self.dist = raw_data[:, 0]
		
		# Create sub-classes which contain necessary stat data
		self.vr = StatDataSplit(raw_data, 1)
		self.np = StatDataSplit(raw_data, 6)
		self.T = StatDataSplit(raw_data, 11)


class StatDataSplit:
	"""DOC"""
	def __init__(self, raw_data_array, first_index):
		self.mean = raw_data_array[:, first_index]
		self.stddev = raw_data_array[:, first_index + 1]
		self.median = raw_data_array[:, first_index + 2]
		self.q1 = raw_data_array[:, first_index + 3]
		self.q3 = raw_data_array[:, first_index + 4]


class SimMeshData:
	def __init__(self, filename):
		# Get first valid index
		index = skip_nan_simdata(filename)
		
		# Handle simulation mesh data (skip rows integer is 1 more than index)
		raw_data = np.loadtxt(filename, skiprows=index + 1, delimiter=",")
		
		# Find out if any other indices correspond to nan-values in
		# distance and remove them
		more_nan = np.where(np.isnan(raw_data[:, 8]))[0]
		raw_data = np.delete(raw_data, more_nan, axis=0)
		
		# Assign necessary values
		self.dist = raw_data[:, 8] / c.R_sun.value
		self.vr = cart_to_rad_vel(raw_data) * 1e-3
		self.np = simrho_to_rho(raw_data)
		self.T = 10 ** raw_data[:, 3]
		

def skip_nan_simdata(filename):
	"""DOC"""
	# First always skipped because of header
	raw_data = np.loadtxt(filename, skiprows=1, delimiter=",")
	
	# Find first valid primary index
	first_value = 0
	while True:
		if np.isnan(raw_data[first_value][0]):
			first_value += 1
		else:
			return first_value


def cart_to_rad_vel(raw_data):
	"""DOCSTRING"""
	vx = raw_data[:, 12]
	vy = raw_data[:, 13]
	vz = raw_data[:, 14]
	theta = raw_data[:, 9]
	phi = raw_data[:, 10]
	
	vr = vx * np.sin(theta) * np.cos(phi) + \
	     vy * np.sin(theta) * np.sin(phi) + \
	     vz * np.cos(theta)
	
	return vr


def simrho_to_rho(raw_data):
	"""DOCSTRING"""
	lrho = raw_data[:, 6]
	rho = 10 ** lrho / c.m_p.value * 1e-6
	
	return rho
	