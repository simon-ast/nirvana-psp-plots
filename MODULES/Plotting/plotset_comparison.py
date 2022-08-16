import matplotlib.pyplot as plt

# GLOBALS (FOR PLOT UNITY)
COLOR_EQ = "black"
COLOR_POL = "darkred"
COLOR_OBS = "tab:blue"
COLOR_STDDEV = "lightblue"
EQ_LABEL = "Slow wind"
POL_LABEL = "Fast wind"


def plot_setup(indicator: str):
	"""General plot setup (x-label and size)"""
	valid_ind = ["vr", "np", "T", "massloss", "rampressure"]
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
	elif indicator == "massloss":
		ax.set(
			ylabel="$\dot{M}$ [M$_\\odot$ yr$^{-1}$]",
			yscale="log"
		)
	elif indicator == "rampressure":
		ax.set(
			ylabel="P$_{ram}$ [Pa]",
			yscale="log"
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
	        c=COLOR_OBS,
	        zorder=4)
	
	# Observational data (shaded area)
	ax.fill_between(obs_data.dist,
	                y1=y_data - y_area,
	                y2=y_data + y_area,
	                color=COLOR_STDDEV,
	                zorder=3)
	
	# Simulated data (equatorial)
	ax.plot(sim_data_eq.dist,
	        getattr(sim_data_eq, indicator),
	        label=EQ_LABEL,
	        lw=2.5,
	        c=COLOR_EQ,
	        zorder=5)
	
	# Simulated data (polar)
	ax.plot(sim_data_polar.dist,
	        getattr(sim_data_polar, indicator),
	        label="Fast wind",
	        lw=2.5,
	        ls="--",
	        c=COLOR_POL,
	        zorder=5)
	
	ax.legend()
	plt.tight_layout()
	plt.savefig(f"{save_dir}/{indicator}_comparison.eps")
	plt.savefig(f"{save_dir}/{indicator}_comparison.svg")
	plt.close()


def paper_plot_mlrp(obs_data, simdata_eq, simdata_pol, mli_dist, mli_ml,
                    save_dir):
	"""Specific plotting setup for paper"""
	fig, (ax_ml, ax_rp) = plt.subplots(2, 1, figsize=(6, 8))
	
	# MASS LOSS RATE
	ax_ml.set(ylabel="$\dot{M}$ [M$_\\odot$ yr$^{-1}$]",
	          yscale="log", ylim=(1e-15, 4e-13))
	plt.setp(ax_ml.get_xticklabels(), visible=False)
	
	# OBSERVATIONAL DATA
	ml_data = obs_data.massloss.mean
	ml_unce = obs_data.massloss.stddev
	
	# Central line
	ax_ml.plot(obs_data.dist, ml_data,
	           label="PSP",
	           lw=1.5,
	           zorder=4,
	           c=COLOR_OBS)
	# Shaded area
	ax_ml.fill_between(obs_data.dist,
	                   y1=ml_data - ml_unce,
	                   y2=ml_data + ml_unce,
	                   color=COLOR_STDDEV,
	                   zorder=3)
	
	# Simulated data (equatorial)
	ax_ml.plot(simdata_eq.dist, simdata_eq.massloss,
	           label=EQ_LABEL,
	           lw=2.5,
	           c=COLOR_EQ,
	           zorder=5)
	
	# Simulated data (surface integral)
	ax_ml.plot(mli_dist, mli_ml,
	           label="Surface integral",
	           lw=2.5,
	           ls="-.",
	           c="darkgreen",
	           zorder=5)
	
	ax_ml.legend()
	
	###################################################################
	# RAM PRESSURE
	ax_rp.set(xlabel="Distance [R$_\\odot$]",
	          ylabel="P$_{ram}$ [Pa]",
	          yscale="log", ylim=(1e-8, 4e-5))
	
	# OBSERVATIONAL DATA
	rp_data = obs_data.rampressure.mean
	rp_unce = obs_data.rampressure.stddev
	
	# Central line
	ax_rp.plot(obs_data.dist, rp_data,
	           label="PSP",
	           lw=1.5,
	           zorder=4,
	           c=COLOR_OBS)
	# Shaded area
	ax_rp.fill_between(obs_data.dist,
	                   y1=rp_data - rp_unce,
	                   y2=rp_data + rp_unce,
	                   color=COLOR_STDDEV,
	                   zorder=3)
	
	# Simulated data (equatorial)
	ax_rp.plot(simdata_eq.dist, simdata_eq.rampressure,
	           label=EQ_LABEL,
	           lw=2.5,
	           c=COLOR_EQ,
	           zorder=5)
	
	# Simulated data (polar)
	ax_rp.plot(simdata_pol.dist, simdata_pol.rampressure,
	           label=EQ_LABEL,
	           lw=2.5,
	           ls="--",
	           c=COLOR_POL,
	           zorder=5)
	
	ax_rp.legend()
	plt.tight_layout()
	plt.savefig(f"{save_dir}/MLRP_comparison.eps")
	plt.close()


def bin_meas_numb(psp_data, save_dir):
	"""Simple plot comparing data point number in each bin"""
	fig, ax = plt.subplots(figsize=(4, 3))
	
	ax.scatter(psp_data.dist, psp_data.num_meas,
	           c="black", s=5)
	ax.set(xlabel="Distance [R$_\\odot$]",
	       ylabel="Number of measurements",
	       yscale="log")
	
	plt.tight_layout()
	plt.savefig(f"{save_dir}/bin_meas_comp.eps")


def paper_npT_com(obs_data, simdata_eq, simdata_pol, save_dir):
	fig, (ax_np, ax_T) = plt.subplots(2, 1, figsize=(6, 8))
	
	# NUMBER DENSITY
	ax_np.set(ylabel="n$_p$ [cm$^{-3}$]",
	          yscale="log")
	plt.setp(ax_np.get_xticklabels(), visible=False)
	
	# OBSERVATIONAL DATA
	np_data = obs_data.np.mean
	np_unce = obs_data.np.stddev
	
	# Central line
	ax_np.plot(obs_data.dist, np_data,
	           label="PSP",
	           lw=1.5,
	           zorder=4,
	           c=COLOR_OBS)
	# Shaded area
	ax_np.fill_between(obs_data.dist,
	                   y1=np_data - np_unce,
	                   y2=np_data + np_unce,
	                   color=COLOR_STDDEV,
	                   zorder=3)
	
	# Simulated data (equatorial)
	ax_np.plot(simdata_eq.dist, simdata_eq.np,
	           label=EQ_LABEL,
	           lw=2.5,
	           c=COLOR_EQ,
	           zorder=5)
	
	# Simulated data (polar)
	ax_np.plot(simdata_pol.dist, simdata_pol.np,
	           label=EQ_LABEL,
	           lw=2.5,
	           ls="--",
	           c=COLOR_POL,
	           zorder=5)
	
	ax_np.legend()
	
	###################################################################
	# TEMPERATURE
	ax_T.set(xlabel="Distance [R$_\\odot$]",
	         ylabel="T [K]",
	         yscale="log")
	
	# OBSERVATIONAL DATA
	T_data = obs_data.T.mean
	T_unce = obs_data.T.stddev
	
	# Central line
	ax_T.plot(obs_data.dist, T_data,
	          label="PSP",
	          lw=1.5,
	          zorder=4,
	          c=COLOR_OBS)
	# Shaded area
	ax_T.fill_between(obs_data.dist,
	                  y1=T_data - T_unce,
	                  y2=T_data + T_unce,
	                  color=COLOR_STDDEV,
	                  zorder=3)
	
	# Simulated data (equatorial)
	ax_T.plot(simdata_eq.dist, simdata_eq.T,
	          label=EQ_LABEL,
	          lw=2.5,
	          c=COLOR_EQ,
	          zorder=5)
	
	# Simulated data (polar)
	ax_T.plot(simdata_pol.dist, simdata_pol.T,
	          label=EQ_LABEL,
	          lw=2.5,
	          ls="--",
	          c=COLOR_POL,
	          zorder=5)
	
	ax_T.legend()
	plt.tight_layout()
	plt.savefig(f"{save_dir}/npT_comparison.eps")
	plt.close()
