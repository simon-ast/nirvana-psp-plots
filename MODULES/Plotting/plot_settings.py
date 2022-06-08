import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def rc_setup():
	"""Generalized plot attributes"""
	mpl.rcParams["xtick.direction"] = "in"
	mpl.rcParams["ytick.direction"] = "in"
	mpl.rcParams["xtick.minor.visible"] = "True"
	mpl.rcParams["ytick.minor.visible"] = "True"
	mpl.rcParams["xtick.top"] = "True"
	mpl.rcParams["ytick.right"] = "True"
	mpl.rcParams["axes.grid"] = "True"


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


def plot_histogram(save_dir, data, bin_lo, bin_hi, identifier):
	"""
	DOC
	"""
	# SANITY CHECK
	pos_ident = ["vr", "rho", "temp"]
	assert identifier.lower() in pos_ident, \
		f"IDENTIFIER {identifier} UNKNOWN!"
	
	# MISC. INFORMATION
	num_points = len(data)  # Number of measurements in binned sample
	mean = np.mean(data)        # Mean of data
	stddev = np.std(data)
	median = np.median(data)    # Median of data
	
	# OVERALL FIGURE INITIALIZATION
	fig, ax = plt.subplots()
	
	# Histogram of all data points, binned automatically by plt.hist()
	ax.hist(x=data, bins="auto", histtype="step", color="black", lw=2)
	
	# Mean and standard deviation
	ax.axvline(mean, ls="--", lw=2, color="darkgreen",
	           label=f"MEAN = {mean:.3f}")
	ax.axvspan(xmin=mean - stddev, xmax=mean + stddev,
	           color="tab:green", alpha=0.5)
	
	# Median and quantiles
	ax.axvline(median, ls="--", lw=2, color="maroon",
	           label=f"MEDIAN = {median:.3f}")
	ax.axvspan(xmin=np.percentile(data, 25), xmax=np.percentile(data, 75),
	           color="lightcoral", alpha=0.5)
	
	# General Plot adjustments
	plt.legend()
	ax.set(
		ylabel="Frequency",
		title=f"{bin_lo} - {bin_hi} R$_\\odot$\n"
		      f"# Data Points = {num_points}"
	)
	
	# ADJUST GRID BY HAND TO MAKE SURE IMPLEMENTATION IS CORRECT
	ax.grid(alpha=0.5, axis="y")
	ax.grid(alpha=0, axis="x")
	
	# THIS IS CALLED WHEN RADIAL VELOCITY IS DESIRED
	if identifier.lower() == "vr":
		
		# MAKE CORRECT ADJUSTMENTS TO PLOTS
		ax.set(xlabel="Radial velocity [kms$^{-1}$]")
		plt.savefig(f"{save_dir}/PSP_BIN{bin_lo}-{bin_hi}_RadVel_HIST.png")
	
	# THIS IS CALLED WHEN NUMBER DENSITY IS DESIRED
	elif identifier.lower() == "rho":
		
		# MAKE CORRECT ADJUSTMENTS TO PLOTS
		ax.set(xlabel="Number density [cm$^{-3}$]")
		plt.savefig(f"{save_dir}/PSP_BIN{bin_lo}-{bin_hi}_Density_HIST.png")
		
	# THIS IS CALLED WHEN TEMPERATURE IS DESIRED
	elif identifier.lower() == "temp":
	
		# MAKE CORRECT ADJUSTMENTS TO PLOTS
		ax.set(xlabel="Temperature [K]")
		plt.savefig(f"{save_dir}/PSP_BIN{bin_lo}-{bin_hi}_"
		            f"Temperature_HIST.png")
		
	# CLOSE FIGURE TO SAVE MEMORY
	plt.close()


def plot_finals(stat_data, key_name, save_dir):
	"""DOC"""
	# PLOTTING MEAN AND STDDEV OF DATA
	fig, ax = plt.subplots(figsize=(10, 7))
	ax.set(xlabel="Distance [R$_\\odot$]")
	
	ax.plot(stat_data["r"], stat_data[key_name]["mean"],
	        lw=2, color="darkgreen")
	
	ax.fill_between(
		x=stat_data["r"],
		y1=stat_data[key_name]["mean"] - stat_data[key_name]["stddev"],
		y2=stat_data[key_name]["mean"] + stat_data[key_name]["stddev"],
		color="tab:green", alpha=0.5)
	
	if key_name == "vr":
		ax.set(ylabel="Radial velocity [km s$^{-1}$]",
		       title=f"MEAN and STDDEV of RADIAL VELOCITY")
		plt.savefig(f"{save_dir}/RadialVelocity_MEAN.png")
	
	elif key_name == "rho":
		ax.set(ylabel="Number Density [cm$^{-3}$]", yscale="log",
		       title=f"MEAN and STDDEV of NUMBER DENSITY")
		plt.savefig(f"{save_dir}/NumberDensity_MEAN.png")

	elif key_name == "temp":
		ax.set(ylabel="Temperature [K]", yscale="log",
		       title=f"MEAN and STDDEV of TEMPERATURE")
		plt.savefig(f"{save_dir}/Temperature_MEAN.png")
	
	plt.close()
	
	# PLOTTING MEDIAN AND Q1/Q3 OF DATA
	fig, ax = plt.subplots(figsize=(10, 7))
	ax.set(xlabel="Distance [R$_\\odot$]")

	ax.plot(stat_data["r"], stat_data[key_name]["median"],
	        lw=2, color="maroon")

	ax.fill_between(x=stat_data["r"],
	                y1=stat_data[key_name]["q1"],
	                y2=stat_data[key_name]["q3"],
	                color="lightcoral", alpha=0.5)
	
	if key_name == "vr":
		ax.set(ylabel="Radial velocity [km s$^{-1}$]",
		       title=f"MEDIAN and Q1/Q3 of RADIAL VELOCITY")
		plt.savefig(f"{save_dir}/RadialVelocity_MEDIAN.png")
	
	elif key_name == "rho":
		ax.set(ylabel="Number Density [cm$^{-3}$]", yscale="log",
		       title=f"MEDIAN and Q1/Q3 of NUMBER DENSITY")
		plt.savefig(f"{save_dir}/NumberDensity_MEDIAN.png")
	
	elif key_name == "temp":
		ax.set(ylabel="Temperature [K]", yscale="log",
		       title=f"MEDIAN and Q1/Q3 of TEMPERATURE")
		plt.savefig(f"{save_dir}/Temperature_MEDIAN.png")
	
	plt.close()
	
