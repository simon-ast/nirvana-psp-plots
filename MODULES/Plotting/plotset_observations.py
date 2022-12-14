import matplotlib.pyplot as plt
import numpy as np
import astropy.constants as c
import pandas as pd


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
            ylim=(10 ** 4, 5 * 10 ** 6), yscale="log"
        )
    return fig, ax


def plot_histogram(save_dir, data, filename, identifier):
    """Specified plot settings for histogram data."""
    # SANITY CHECK
    pos_ident = ["vr", "np", "Temp"]
    assert identifier in pos_ident, \
        f"IDENTIFIER {identifier} UNKNOWN!"

    # MISC. INFORMATION
    num_points = len(data[identifier])  # Number of meas. in binned sample
    mean = np.mean(data[identifier])  # Mean of data
    stddev = np.std(data[identifier])  # Stddev of data
    median = np.median(data[identifier])  # Median of data

    # OVERALL FIGURE INITIALIZATION
    fig, ax = plt.subplots()

    # Histogram of all data points, binned automatically by plt.hist()
    _, bins, _ = ax.hist(x=data[identifier], bins="auto", histtype="step",
                         color="grey", lw=2.5,
                         label=f"comb. ({num_points})")

    # Plot SPC and SPAN-I bins separate
    data_spc = data[data["Inst"] == "SPC"]
    ax.hist(x=data_spc[identifier], bins=bins, histtype="step",
            color="black", lw=1.5, ls="--",
            label=f"SPC ({data_spc.shape[0]})")

    data_span = data[data["Inst"] == "SPAN"]
    ax.hist(x=data_span[identifier], bins=bins, histtype="step",
            color="tab:blue", lw=1.5, ls="--",
            label=f"SPAN-I ({data_span.shape[0]})")

    # Mean and standard deviation
    ax.axvline(
        mean, ls="--", lw=2, color="darkgreen",
        label=f"MEAN = {mean:.3f}"
    )
    ax.axvspan(
        xmin=mean - stddev, xmax=mean + stddev,
        color="tab:green", alpha=0.5
    )

    # Median and quantiles
    ax.axvline(
        median, ls="--", lw=2, color="maroon",
        label=f"MEDIAN = {median:.3f}"
    )
    ax.axvspan(
        xmin=np.percentile(data[identifier], 25),
        xmax=np.percentile(data[identifier], 75),
        color="lightcoral", alpha=0.5
    )

    # General Plot adjustments
    plt.legend(framealpha=1., frameon=True)
    ax.set(
        ylabel="Frequency",
        title=f"{filename}\n # Data Points = {num_points}"
    )

    # ADJUST GRID BY HAND TO MAKE SURE IMPLEMENTATION IS CORRECT
    ax.grid(alpha=0.5, axis="y")
    ax.grid(alpha=0, axis="x")

    # THIS IS CALLED WHEN RADIAL VELOCITY IS DESIRED
    if identifier == "vr":

        # MAKE CORRECT ADJUSTMENTS TO PLOTS
        ax.set(xlabel="Radial velocity [kms$^{-1}$]")
        plt.savefig(f"{save_dir}/{filename}_RadVel_HIST.png")

    # THIS IS CALLED WHEN NUMBER DENSITY IS DESIRED
    elif identifier == "np":

        # MAKE CORRECT ADJUSTMENTS TO PLOTS
        ax.set(xlabel="Number density [cm$^{-3}$]")
        plt.savefig(f"{save_dir}/{filename}_Density_HIST.png")

    # THIS IS CALLED WHEN TEMPERATURE IS DESIRED
    elif identifier == "Temp":

        # MAKE CORRECT ADJUSTMENTS TO PLOTS
        ax.set(xlabel="Temperature [K]")
        plt.savefig(f"{save_dir}/{filename}_Temperature_HIST.png")

    # CLOSE FIGURE TO SAVE MEMORY
    plt.close()


def plot_finals(stat_data, key_name, save_dir):
    """Specified final plotting attributes for measurement data."""
    # Sub-slices of data frame
    data_mean = stat_data[stat_data["Type"] == "mean"]
    data_std = stat_data[stat_data["Type"] == "std"]
    data_median = stat_data[stat_data["Type"] == "median"]
    data_q1 = stat_data[stat_data["Type"] == "q1"]
    data_q3 = stat_data[stat_data["Type"] == "q3"]
    
    # Adjusted position parameter
    distance = data_mean.posR * 1e3 / c.R_sun

    # PLOTTING MEAN AND STDDEV OF DATA
    fig, ax = None, None

    if key_name == "vr":
        fig, ax = plot_setup("Radial velocity")

    elif key_name == "np":
        fig, ax = plot_setup("Density")

    elif key_name == "Temp":
        fig, ax = plot_setup("Temperature")

    ax.plot(
        distance, data_mean.__getattr__(key_name).values,
        lw=2, color="tab:blue", label="Mean"
    )

    ax.fill_between(
        x=distance,
        y1=data_mean.__getattr__(key_name).values -
           data_std.__getattr__(key_name).values,
        y2=data_mean.__getattr__(key_name).values +
           data_std.__getattr__(key_name).values,
        color="lightblue", label="1$\\sigma$")

    plt.legend()
    ax.set_zorder(3000)

    if key_name == "vr":
        plt.savefig(f"{save_dir}/RadialVelocity_MEAN.eps")

    elif key_name == "np":
        plt.savefig(f"{save_dir}/NumberDensity_MEAN.eps")

    elif key_name == "Temp":
        plt.savefig(f"{save_dir}/Temperature_MEAN.eps")

    plt.close()

    # PLOTTING MEDIAN AND Q1/Q3 OF DATA
    fig, ax = None, None

    if key_name == "vr":
        fig, ax = plot_setup("Radial velocity")

    elif key_name == "np":
        fig, ax = plot_setup("Density")

    elif key_name == "Temp":
        fig, ax = plot_setup("Temperature")

    ax.plot(
        distance,
        data_median.__getattr__(key_name).values,
        lw=2, color="maroon", label="median"
    )

    ax.fill_between(
        x=distance,
        y1=data_q1.__getattr__(key_name).values,
        y2=data_q3.__getattr__(key_name).values,
        color="lightcoral", alpha=0.5,
        label="q1/q3"
    )

    plt.legend()

    if key_name == "vr":
        plt.savefig(f"{save_dir}/RadialVelocity_MEDIAN.png")

    elif key_name == "np":
        plt.savefig(f"{save_dir}/NumberDensity_MEDIAN.png")

    elif key_name == "Temp":
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
            ylim=(10 ** 4, 5 * 10 ** 6), yscale="log"
        )

    return fig, ax_vr, ax_np, ax_t


def plot_setup_obs_epoch():
    """Setup for epoch plots"""
    fig, (ax_r, ax_vr, ax_np) = plt.subplots(3, 1, figsize=(15, 9))

    ax_r.set(ylabel="Distance [R$_\\odot$]")

    ax_vr.set(ylabel="v$_r$ [km s$^{-1}$]",
              ylim=(0, 700))

    ax_np.set(xlabel="Epoch", ylabel="n$_p$ [cm$^{-3}$]",
              yscale="log", ylim=(10, 10 ** 4))

    return fig, ax_r, ax_vr, ax_np


def plot_fill_epoch(label, ax_r, ax_vr, ax_np, spc_data, span_data, save_dir):
    """Filling epoch plots"""
    spc_color = "black"
    span_color = "tab:red"

    # Create more readable epoch values
    spc_epoch = pd.to_datetime(spc_data.epoch / 86400,
                               unit="D", origin="julian")
    span_epoch = pd.to_datetime(span_data.epoch / 86400,
                                unit="D", origin="julian")

    # Fill distance plot
    ax_r.plot(span_epoch, span_data.posR * 1e3 / c.R_sun,
              c=span_color, label="SPAN",
              lw=2.5)
    ax_r.plot(spc_epoch, spc_data.posR * 1e3 / c.R_sun,
              c=spc_color, label="SPC",
              lw=2.5)

    ax_vr.plot(span_epoch, span_data.vr, c=span_color, label="SPAN",
    lw=2.5)
    ax_vr.plot(spc_epoch, spc_data.vr, c=spc_color, label="SPC",
    lw=2.5)

    ax_np.plot(span_epoch, span_data.np, c=span_color, label="SPAN",
    lw=2.5)
    ax_np.plot(spc_epoch, spc_data.np, c=spc_color, label="SPC",
    lw=2.5)

    # Finish up the plots
    plt.setp(ax_r.get_xticklabels(), visible=False)
    plt.setp(ax_vr.get_xticklabels(), visible=False)
    ax_r.legend()

    plt.tight_layout()
    plt.savefig(f"{save_dir}/{label}.eps")
