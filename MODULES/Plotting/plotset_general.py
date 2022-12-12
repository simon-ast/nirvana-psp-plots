import matplotlib as mpl
import matplotlib.pyplot as plt


def rc_setup():
    """Generalized plot attributes"""
    mpl.rcParams["xtick.direction"] = "in"
    mpl.rcParams["xtick.labelsize"] = "large"
    mpl.rcParams["xtick.major.width"] = 1.5
    mpl.rcParams["xtick.minor.width"] = 1.5
    mpl.rcParams["xtick.minor.visible"] = "True"
    mpl.rcParams["xtick.top"] = "True"

    mpl.rcParams["ytick.direction"] = "in"
    mpl.rcParams["ytick.labelsize"] = "large"
    mpl.rcParams["ytick.major.width"] = 1.5
    mpl.rcParams["ytick.minor.width"] = 1.5
    mpl.rcParams["ytick.minor.visible"] = "True"
    mpl.rcParams["ytick.right"] = "True"

    mpl.rcParams["axes.grid"] = "False"
    mpl.rcParams["axes.linewidth"] = 1.5
    mpl.rcParams["axes.labelsize"] = "large"

    mpl.rcParams["legend.frameon"] = "False"


def bin_analysis(save_dir, spc_pts, span_pts, dist_index):
    """Simple plot of bin distance index and number of data points"""
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(dist_index, spc_pts,
               color="black",
               s=6, label="SPC")

    ax.scatter(dist_index, span_pts,
               color="tab:blue", marker="^",
               s=6, label="SPAN-I")

    ax.set(xlabel="Distance [R$_\\odot$]",
           ylabel="Number of measurements",
           yscale="log")

    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{save_dir}/datapoints.eps")
    plt.savefig(f"{save_dir}/datapoints.svg")
