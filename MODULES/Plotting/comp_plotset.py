import matplotlib.pyplot as plt


def plot_setup(indicator: str):
	"""General plot setup (x-label and size)"""
	valid_ind = ["vr", "np", "T"]
	assert indicator in valid_ind, f"{indicator} NOT RECOGNIZED!"
	
	# General values
	fig, ax = plt.subplots(figsize=(6, 4))
	ax.set(xlabel="Distance [R$_\\odot$]")
	
	if indicator == "vr":
		ax.set(
			ylabel="$v_r$ [km s$^{-1}$]"
		)
	
	elif indicator == "np":
		ax.set(
			ylabel="$n_p$ [cm$^{-3}$]",
			yscale="log"
		)
	
	elif indicator == "T":
		ax.set(
			ylabel="T [K]",
			yscale="log",
			ylim=(1e4, 1e7)
		)
	return fig, ax


def comparison_plot(indicator: str, obs_data,
                    sim_data_eq, sim_data_polar,
                    save_dir):
	"""
	Combine simulation radial profile and observational data into
	one plot
	"""
	# Set-up plots
	fig, ax = plot_setup(indicator)
	
	# GENERALIZED PLOTTING ROUTINE
	# This is a nested class!
	y_data = getattr(getattr(obs_data, indicator), "mean")
	y_area = getattr(getattr(obs_data, indicator), "stddev")
	
	# Observational data (central)
	ax.plot(obs_data.dist,
	        y_data,
	        label="PSP",
	        lw=1.5,
	        zorder=4)
	
	# Observational data (shaded area)
	ax.fill_between(obs_data.dist,
	                y1=y_data - y_area,
	                y2=y_data + y_area,
	                alpha=0.5,
	                zorder=3)
	
	# Simulated data (equatorial)
	ax.plot(sim_data_eq.dist,
	        getattr(sim_data_eq, indicator),
	        label="Equatorial",
	        lw=2.5,
	        c="tab:green",
	        zorder=5)
	
	# Simulated data (polar)
	ax.plot(sim_data_polar.dist,
	        getattr(sim_data_polar, indicator),
	        label="Polar",
	        lw=2.5,
	        ls="--",
	        c="tab:red",
	        zorder=5)
	
	ax.legend()
	plt.tight_layout()
	plt.savefig(f"{save_dir}/{indicator}_comparison.jpg", dpi=300)
	plt.close()
	