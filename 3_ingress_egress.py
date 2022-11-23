import os
import sys
import typing as tp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.constants import R_sun
from modules.plotting import plotset_general as pg
from modules.plotting import plotset_observations as po

# DISTANCE BIN SIZE IN R_SOL
DISTANCE_BIN_SIZE = float(sys.argv[1])

# DATA LOCATION OF SPLIT DATA AND PLOTS
SPLIT_DATA_LOCATION = f"{sys.path[0]}/STATISTICS/SPLIT_DATA"
STAT_DATA_FILE = f"{sys.path[0]}/STATISTICS/PSP_STATISTICS.json"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/IngressEgressPlots"

# CUSTOM COLOUR LIST FOR PLOTTING [NESTED 10 x 2]
# TODO: This is very jank, there might be a nicer-looking solution
COLOUR_LIST = [[], [], [], [], [], [],
               ["red", "orange"],
               ["darkgreen", "lime"],
               ["blue", "cyan"],
               ["darkviolet", "fuchsia"]]


def main_orbit_plots(folder: str) -> None:
    """DOC"""

    # Instantiate three plots: vr, np and T
    fig_vr, ax_vr = po.plot_setup("Radial velocity")
    fig_np, ax_np = po.plot_setup("Density")
    fig_t, ax_t = po.plot_setup("Temperature")

    # Instantiate combined plots
    fig_com, ax_vr_com, ax_np_com, ax_t_com = po.plot_setup_obs_comb()

    # Create (archaic) sorted list of files by asc. encounter number
    # varying ingress - egress
    raw_file_list = sorted(os.listdir(folder))
    file_list = raw_file_list

    # Loop over all split files in the directory
    for file in file_list:
        print(f"CURRENTLY HANDLING {file}")

        # Generate total file name (and very rough label)
        file_name = f"{folder}/{file}"
        label = file[10:13]

        # Read in (1) and append (2) to total data
        data, label, pcolour, ls = orbit_readin(file_name, label)
        median_df = data_orbit_analysis(data)

        # Generate general position values for orbit (in R_sol)
        position = median_df.posR * 1e3 / R_sun

        # Add to existing plots
        for vr_axis in (ax_vr, ax_vr_com[0]):
            vr_axis.plot(
                position, median_df.vr,
                label=label, color=pcolour,
                ls=ls, lw=2
            )

        for np_axis in (ax_np, ax_np_com[0]):
            np_axis.plot(
                position, median_df.np,
                label=label, color=pcolour,
                ls=ls, lw=2
            )

        for tem_axis in (ax_t, ax_t_com[0]):
            tem_axis.plot(
                position, median_df.Temp,
                label=label, color=pcolour,
                ls=ls, lw=2
            )

    # Fill in mean (or median) plots
    # Read in the .json file and split by value type
    stat_data = pd.read_json(STAT_DATA_FILE)
    plot_stats(ax_vr_com[1], stat_data, "vr")
    plot_stats(ax_np_com[1], stat_data, "np")
    plot_stats(ax_t_com[1], stat_data, "Temp")

    # Finalize and save individual plots
    ax_vr.legend(ncol=3)
    plt.tight_layout()
    fig_vr.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_RadialVelocity.eps")

    ax_np.legend()
    plt.tight_layout()
    fig_np.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_Density.eps")

    ax_t.legend()
    plt.tight_layout()
    fig_t.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_Temperature.eps")

    # Finalize and save total plot
    ax_vr_com[0].legend(ncol=3)
    ax_vr_com[1].legend()
    fig_com.tight_layout()
    fig_com.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_measurements.eps")
    fig_com.savefig(f"{PLOT_SAVE_DIR}/PSP_I-E_measurements.svg")


def orbit_readin(filename: str, label) -> tp.Tuple:
    """Read in file data and create dictionary"""
    # Read in data frame
    data = pd.read_json(filename)

    # Extract individual necessary designation keys
    enc_numb = int(label[0])  # Encounter number
    enc_type = label[-1].lower()  # Encounter type (in/eg)

    # Assign more appropriate label formatting
    enc_lab = f"E{enc_numb}-{enc_type}"

    # Set a plot color index based on approach or recession
    if enc_type[0] == "i":
        plot_colour = COLOUR_LIST[enc_numb - 1][0]
        linestyle = "-"
    else:
        plot_colour = COLOUR_LIST[enc_numb - 1][1]
        linestyle = "--"

    return data, enc_lab, plot_colour, linestyle


def data_orbit_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """Update data dictionary with "plottable" values"""
    # Create distance bins and zip indices
    distance_bins = np.arange(0, 100, DISTANCE_BIN_SIZE)
    dist_groups = data.groupby(
        np.digitize(data.posR * 1e3 / R_sun.value, distance_bins)
    )

    mean_df = dist_groups.mean(numeric_only=True)

    return mean_df


def plot_stats(ax, stat_data, key_name):
    """DOC"""
    data_mean = stat_data[stat_data["Type"] == "mean"]
    data_std = stat_data[stat_data["Type"] == "std"]

    # Not used for now!
    # data_median = stat_data[stat_data["Type"] == "median"]
    # data_q1 = stat_data[stat_data["Type"] == "q1"]
    # data_q3 = stat_data[stat_data["Type"] == "q3"]

    # Generalized position parameter in R_sol
    position = data_mean.posR * 1e3 / R_sun.value

    ax.plot(
        position, data_mean.__getattr__(key_name),
        lw=2, color="tab:blue",
        label="mean", zorder=5)

    ax.fill_between(
        x=position,
        y1=data_mean.__getattr__(key_name).values - data_std.__getattr__(
            key_name).values,
        y2=data_mean.__getattr__(key_name).values + data_std.__getattr__(
            key_name).values,
        color="lightblue", label="1$\\sigma$", zorder=4)


if __name__ == "__main__":
    # GENERAL PLOTTING PARAMETERS
    pg.rc_setup()

    # CALL ALL NESTED FUNCTIONS
    main_orbit_plots(SPLIT_DATA_LOCATION)
