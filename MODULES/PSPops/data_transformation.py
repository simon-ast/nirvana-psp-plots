import numpy as np
import typing as tp
# The warnings (for me) here don't seem to matter
from astropy.constants import k_B, m_p


def pos_cart_to_sph(position_matrix: np.ndarray) -> tp.Tuple:
	"""
	Transforms cartesian coordinates to spherical coordinates.
	
	:param position_matrix: NDARRAY,
		(n x 3) matrix of (x, y, z) coordinates
	:return: TUPLE,
		r = heliocentric distance in KM
		theta = inclination in RADIANS
		phi = azimuth in RADIANS
	"""
	# Sanity check: pos_mat MUST BE an (n x 3) matrix
	assert position_matrix.shape[1] == 3, \
		"PLEASE CHECK POSITION MATRIX FOR COORDINATE CONVERSION!"
	
	x = position_matrix[:, 0]
	y = position_matrix[:, 1]
	z = position_matrix[:, 2]
	
	r = np.sqrt(x * x + y * y + z * z)
	theta = np.arccos(z / r)
	phi = np.arctan2(y, x)
	
	return r, theta, phi


def wp_to_temp(thermal_speed: np.ndarray) -> np.ndarray:
	"""
	Calculate temperature from thermal speed of protons.
	
	:param thermal_speed: NDARRAY,
		Thermal speed (wp) of protons
	:return: NDARRAY,
		Temperature from wp = sqrt(2k_BT / m)
	"""
	wp_si = thermal_speed * 1e3
	
	return wp_si ** 2 * m_p.value / (2 * k_B.value)


def abs_to_rel_time(epoch_array: np.ndarray) -> np.ndarray:
	"""DOC"""
	start = epoch_array[0]
	end = epoch_array[-1]
	
	rel_array = (epoch_array - start) / (end - start)
	
	return rel_array
