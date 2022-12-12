import matplotlib as mpl
import matplotlib.pyplot as plt

# PLOTTING PARAMS
LS_EQ = "-"
LS_POL = "--"
C_NIR = "black"
C_POLY = "tab:green"
LW_NIR = 2.5
LW_POLY = 2
LAB_EQ = "Slow wind"
LAB_POL = "Fast wind"


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


def plot_comparison(peq, ppol, neq, npol, stat_data, indicator,
                    savedir, save_type):
    """Plotting setup and saving"""
    fig, ax = general_setup()

    comparison_profiles(ax, peq, ppol, neq, npol, stat_data, indicator)

    plot_finish(ax, indicator)
    plt.tight_layout()

    for ext in save_type:
        plt.savefig(f"{savedir}/{indicator}_comparison.{ext}")

    return None


def general_setup():
    """General axis labels"""
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.set(
        xlabel="Distance [R$_\\odot$]"
    )

    return fig, ax


def comparison_profiles(ax, peq, ppol, neq, npol, stats, indicator):
    """Plotting profiles of EQ and POL for NIRwave and Polytrope"""
    plot_profile(ax, peq, "peq", indicator)
    plot_profile(ax, ppol, "ppol", indicator)
    plot_profile(ax, neq, "neq", indicator)
    plot_profile(ax, npol, "npol", indicator)

    plot_psp_stat(ax, stats, indicator)

    custom_legend(ax)

    return None


def plot_profile(ax, data, prof_type, indicator):
    """Plotting individual radial parameter profile"""
    ls = None
    color = None
    lw = None
    lab = None

    if prof_type == "neq":
        ls = LS_EQ
        color = C_NIR
        lw = LW_NIR
        lab = LAB_EQ

    elif prof_type == "npol":
        ls = LS_POL
        color = C_NIR
        lw = LW_NIR
        lab = LAB_POL

    elif prof_type == "peq":
        ls = LS_EQ
        color = C_POLY
        lw = LW_POLY
        lab = LAB_EQ

    elif prof_type == "ppol":
        ls = LS_POL
        color = C_POLY
        lw = LW_POLY
        lab = LAB_POL

    ax.plot(
        data.dist, getattr(data, indicator),
        ls=ls, color=color, lw=lw,
        label=lab
    )

    return None


def plot_finish(ax, indicator):
    """Plot clean-up"""
    if indicator == "vr":
        ax.set(
            ylabel="v$_r$ [km s$^{-1}$]",
            ylim=(0, 700)
        )

    elif indicator == "np":
        ax.set(
            ylabel="n$_p$ [cm$^{-3}$]",
            ylim=(1e1, 1e7), yscale="log"
        )

    elif indicator == "T":
        ax.set(
            ylabel="T [K]",
            ylim=(5e4, 1e7), yscale="log"
        )

    return None


def plot_combination(peq, ppol, neq, npol, stats, save_dir, save_type):
    """Plot profile comparison for all three parameters"""
    fig, (ax_vr, ax_np, ax_T) = plt.subplots(3, 1, figsize=(6, 12))

    comparison_profiles(ax_vr, peq, ppol, neq, npol, stats, "vr")
    comparison_profiles(ax_np, peq, ppol, neq, npol, stats, "np")
    comparison_profiles(ax_T, peq, ppol, neq, npol, stats, "T")

    ax_vr.set(
        ylabel="v$_r$ [km s$^{-1}$]",
        ylim=(0, 700)
    )

    ax_np.set(
        ylabel="n$_p$ [cm$^{-3}$]",
        ylim=(1e1, 1e7), yscale="log"
    )

    ax_T.set(
        xlabel="Distance [R$_\\odot$]",
        ylabel="T [K]",
        ylim=(5e4, 1e7), yscale="log"
    )

    # HIDE THE LABELS FOR THE FIRST TWO SUB FIGURES
    ax_vr.set_xticklabels([])
    ax_np.set_xticklabels([])

    # DESCRIBE
    custom_legend(ax_vr)

    plt.tight_layout()

    for ext in save_type:
        plt.savefig(f"{save_dir}/comparison_comb.{ext}")


def custom_legend(axis):
    """
    Reformatting the legend of a comparison plot to a visually more
    appealing format.

    The layout should look something like this in the end, with 3
    columns for the legend.
    % ---------------------------------------------------------------- %
    % |           NIRwave         Polytrope                          | %
    % |   (solid bl) Slow wind  (solid gr) Slow wind                 | %
    % |   (dash. bl) Fast wind  (dash. gr) Fast wind                 | %
    % ---------------------------------------------------------------- %
    """
    handles_old, labels_old = axis.get_legend_handles_labels()
    header = [plt.plot([], marker="", ls="")[0]] * 2
    handles = header[:1] + handles_old[2:] + \
              header[1:] + handles_old[:2]
    labels = ["NIRwave"] + labels_old[2:] + \
             ["Polytrope"] + labels_old[:2]
    leg = axis.legend(handles, labels, ncol=2)

    for vpack in leg._legend_handle_box.get_children():
        for hpack in vpack.get_children()[:1]:
            hpack.get_children()[0].set_width(0)

    return handles


def plot_psp_stat(ax, stats, indicator):
    """Insert PSP paramter profile into plot"""
    stat_data = getattr(getattr(stats, indicator), "mean")
    ax.plot(stats.dist, stat_data,
            color="grey", ls=":", lw=1.5,
            # label="PSP", # SKIP LABEL (DOES NOT FIT RIGHT)
            zorder=0)
