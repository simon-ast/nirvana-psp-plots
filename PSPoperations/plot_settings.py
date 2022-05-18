import matplotlib as mpl
import matplotlib.pyplot as plt


def rc_setup():
	"""Generalized plot attributes"""
	mpl.rcParams["xtick.direction"] = "in"
	mpl.rcParams["ytick.direction"] = "in"
	mpl.rcParams["xtick.minor.visible"] = "True"
	mpl.rcParams["ytick.minor.visible"] = "True"


def plot_r_vr(r, vr, v_ulim, v_lolim, save_ind: str = "no"):
	"""
	Plots radial velocity wrt heliocentric distance
	
	:param r: NDARRAY,
		Distance (must be in km)
	:param vr: NDARRAY,
		Radial velocity (must be in km/s)
	:param v_ulim, v_lolim: NDARRAY,
		Upper (lower) uncertainty of vr
	:param save_ind: STR,
		"yes" if plot should be saved (default: no)
	"""
	fig, ax = plt.subplots(figsize=(10, 6))
	plt.plot(r / 6.957e5, vr)
	plt.fill_between(r / 6.957e5, vr + v_ulim, vr - v_lolim, color="grey",
	                 alpha=0.25)
	ax.set(
		xlabel="r [R$_\\odot$]", ylabel="v$_r$ [km s$^{-1}$]",
		ylim=(0, 800)
	)
	ax.grid(True, alpha=0.5)
	
	if save_ind.lower() == "yes":
		plt.savefig("plot_vr.png")


def plot_r_temp(r, T, T_ulim, T_lolim, save_ind: str = "no"):
	"""
	Plots logarithmic temperature wrt heliocentric distance
	
	:param r: NDARRAY,
		Heliocentric distance (mst be in km)
	:param T: NDARRAY,
		logarithmic Temperature (Kelvin)
	:param T_ulim, T_lolim: NDARRAY,
		Upper (lower) uncertainty of logT
	:param save_ind: STR,
		"yes" if plot should be saved (default: no)
	"""
	fig, ax = plt.subplots(figsize=(10, 6))
	plt.plot(r / 6.957e5, T)
	plt.fill_between(r / 6.957e5, T_ulim, T - T_lolim,
	                 color="grey", alpha=0.25)
	ax.set(
		xlabel="r [R$_\\odot$]", ylabel="T [K]", yscale="log"
	)
	ax.grid(True, alpha=0.5)
	
	if save_ind.lower() == "yes":
		plt.savefig("plot_logT.png")
