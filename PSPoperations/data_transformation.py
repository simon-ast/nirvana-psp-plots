import numpy as np
import typing as tp


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


def vel_cart_to_sph(vel_matrix, r, theta, phi):
	"""
	???
	
	:param vel_matrix:
	:param r:
	:param theta:
	:param phi:
	:return:
	"""
	# Sanity checks
	assert vel_matrix.shape[1] == 3, \
		"PLEASE CHECK POSITION MATRIX FOR COORDINATE CONVERSION!"
	assert r.shape[0] == theta.shape[0] == phi.shape[0] == vel_matrix.shape[0], \
		"PLEASE CHECK DIMENSIONS OF R, THETA, PHI AND VEL_MATRIX!"
	
	vx = vel_matrix[:, 0]
	vy = vel_matrix[:, 1]
	vz = vel_matrix[:, 2]
	
	vr = np.sin(theta) * np.cos(phi) * vx + \
	     np.sin(theta) * np.sin(phi) * vy + \
	     np.cos(theta) * vz
	
	return vr
	
	