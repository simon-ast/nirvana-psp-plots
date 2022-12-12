import sys
import numpy as np
import matplotlib.pyplot as plt

# NECESSARY GLOBALS
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS"


def theta_time_analysis(theta_list: list,
                        rel_time: list,
                        label: list) -> None:
    """
    Plots heliolatitude vs. time for specified arrays, to be used to
    analyse behaviour during one encounter phase
    """

    # Necessary parameters
    theta_full = np.concatenate(np.array(theta_list, dtype="object"))
    theta_mean = np.mean(theta_full)
    theta_stddev = np.std(theta_full)

    # Plot each theta_array individually
    fig, ax = plt.subplots(figsize=(7, 5))
    num_arr = len(theta_list)

    for i in range(num_arr):
        ax.scatter(rel_time[i], theta_list[i], label=label[i],
                   s=5, zorder=100)

    # Add median and stddev
    ax.axhline(theta_mean, ls="--", lw=2, color="black",
               label=f"MEAN = {theta_mean:.3f}",
               zorder=2)
    ax.axhspan(ymin=theta_mean - theta_stddev,
               ymax=theta_mean + theta_stddev,
               color="grey", alpha=0.5,
               zorder=1)

    # Plot cleanup
    ax.set(xlabel="$\\Delta$t [0: START - 1: END]",
           ylabel="Heliolatitude [deg]",
           title=f"STDDEV = {theta_stddev:.3f}")

    plt.legend()
    plt.savefig(f"{PLOT_SAVE_DIR}/HELIOLAT_eval.png", dpi=300)
