import matplotlib.pyplot as plt
import numpy as np


def plot_setup(indicator: str):
	"""General plot setup (x-label and size)"""
	# Make sure that oly valid indicators are used
	valid_ind = ["Radial velocity", "Density", "Temperature"]
	assert indicator in valid_ind, f"{indicator} NOT RECOGNIZED!"
	
	# General values
	fig, ax = plt.subplots(figsize=(6, 4))
	ax.set(xlabel="Distance [R$_\\odot$]")
	
	if indicator == "Radial velocity":
		ax.set(
			ylabel="v$_r$ [km s$^{-1}$]",
			ylim=(0, 700)
		)
		
	elif indicator == "Density":
		ax.set(
			ylabel="n$_p$ [cm$^{-3}$]",
			ylim=(10, 10 ** 4), yscale="log"
		)
		
	elif indicator == "Temperature":
		ax.set(
			ylabel="T [K]",
			ylim=(10 ** 4, 10 ** 6), yscale="log"
		)
	return fig, ax


def plot_histogram(save_dir, data, bin_lo, bin_hi, identifier):
	"""Specified plot settings for histogram data."""
	# SANITY CHECK
	pos_ident = ["vr", "rho", "temp"]
	assert identifier.lower() in pos_ident, \
		f"IDENTIFIER {identifier} UNKNOWN!"
	
	# MISC. INFORMATION
	num_points = len(data)  # Number of measurements in binned sample
	mean = np.mean(data)        # Mean of data
	stddev = np.std(data)       # Stddev of data
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
	"""Specified final plotting attributes for measurement data."""
	# PLOTTING MEAN AND STDDEV OF DATA
	fig, ax = None, None
	
	if key_name == "vr":
		fig, ax = plot_setup("Radial velocity")
	
	elif key_name == "rho":
		fig, ax = plot_setup("Density")
	
	elif key_name == "temp":
		fig, ax = plot_setup("Temperature")
	
	ax.plot(stat_data["r"], stat_data[key_name]["mean"],
	        lw=2, color="tab:blue", label="Mean")
	
	ax.fill_between(
		x=stat_data["r"],
		y1=stat_data[key_name]["mean"] - stat_data[key_name]["stddev"],
		y2=stat_data[key_name]["mean"] + stat_data[key_name]["stddev"],
		color="lightblue", label="1$\sigma$")
	
	plt.legend()
	
	if key_name == "vr":
		plt.savefig(f"{save_dir}/RadialVelocity_MEAN.eps")
	
	elif key_name == "rho":
		plt.savefig(f"{save_dir}/NumberDensity_MEAN.eps")

	elif key_name == "temp":
		plt.savefig(f"{save_dir}/Temperature_MEAN.eps")
	
	plt.close()
	
	# PLOTTING MEDIAN AND Q1/Q3 OF DATA
	fig, ax = None, None
	
	if key_name == "vr":
		fig, ax = plot_setup("Radial velocity")
	
	elif key_name == "rho":
		fig, ax = plot_setup("Density")
	
	elif key_name == "temp":
		fig, ax = plot_setup("Temperature")

	ax.plot(stat_data["r"], stat_data[key_name]["median"],
	        lw=2, color="maroon")

	ax.fill_between(x=stat_data["r"],
	                y1=stat_data[key_name]["q1"],
	                y2=stat_data[key_name]["q3"],
	                color="lightcoral", alpha=0.5)
	
	if key_name == "vr":
		plt.savefig(f"{save_dir}/RadialVelocity_MEDIAN.png")
	
	elif key_name == "rho":
		plt.savefig(f"{save_dir}/NumberDensity_MEDIAN.png")
	
	elif key_name == "temp":
		plt.savefig(f"{save_dir}/Temperature_MEDIAN.png")
	
	plt.close()


def plot_setup_obs_comb():
	"""Setup for combined plots of observational data"""
	fig, (ax_top, ax_bot) = plt.subplots(2, 3, figsize=(15, 9))
	
	for axis in ax_bot:
		axis.set(xlabel="Distance [R$_\\odot$]")
	
	# Split axis objects by parameter
	ax_vr = (ax_top[0], ax_bot[0])
	ax_np = (ax_top[1], ax_bot[1])
	ax_t = (ax_top[2], ax_bot[2])
	
	for axis in ax_vr:
		axis.set(
			ylabel="v$_r$ [km s$^{-1}$]",
			ylim=(0, 700)
		)
		
	for axis in ax_np:
		axis.set(
			ylabel="n$_p$ [cm$^{-3}$]",
			ylim=(10, 10 ** 4), yscale="log"
		)
	for axis in ax_t:
		axis.set(
			ylabel="T [K]",
			ylim=(10 ** 4, 10 ** 6), yscale="log"
		)
	
	return fig, ax_vr, ax_np, ax_t
	
