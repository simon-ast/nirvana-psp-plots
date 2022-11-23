import numpy as np
# The warnings (for me) here don't seem to matter
from astropy.constants import k_B, m_p


def pos_cart_to_sph(x, y, z):
	"""
	r = heliocentric distance in KM
	theta = inclination in RADIANS
	phi = azimuth in RADIANS
	"""
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


def ev_to_kelvin(electron_volts: np.ndarray) -> np.ndarray:
	"""DOC"""

	return electron_volts * 1.60217653e-19 / k_B


def abs_to_rel_time(epoch_array: np.ndarray) -> np.ndarray:
	"""
	Transforms absolute time (datetime.datetime) into relative time
	between 0 = start and 1 = finish
	"""
	start = epoch_array[0]
	end = epoch_array[-1]
	
	if len(epoch_array) == 1:
		print("Oi oi, what's goin' on 'ere?")
		return np.array([0])
	
	rel_array = (epoch_array - start) / (end - start)
	
	return rel_array
