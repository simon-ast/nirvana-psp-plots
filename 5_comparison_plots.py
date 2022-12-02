import sys
from modules.stat import stats_dataread as dr
from modules.plotting import plotset_general as pg
from modules.plotting import plotset_comparison as pc

# Necessary global variables
PSP_STAT_DIR = f"{sys.path[0]}/STATISTICS"
ML_CONT = f"{sys.path[0]}/STATISTICS/MASSLOSS_CONTOURS"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ComparisonPlots"


def main():
    pg.rc_setup()

    # Read in the 2D curves from simulation data and the statistics file
    # generated from observations
    sim_data_eq = dr.SimMeshData(f"{PSP_STAT_DIR}/NIRwave_equatorial.csv")
    sim_data_pol = dr.SimMeshData(f"{PSP_STAT_DIR}/NIRwave_polar.csv")
    psp_stats = dr.PSPStatData(f"{PSP_STAT_DIR}/PSP_STATISTICS.json",
                               sim_data_eq)
    # Reduce the statistical data down to a maximum of 40 R_sol
    dr.cut_stat_data(psp_stats)

    # Generate individual plots for each parameter of interest
    for indicator in ["vr", "np", "T", "massloss", "rampressure"]:
        pc.comparison_plot(indicator, psp_stats, sim_data_eq, sim_data_pol,
                           PLOT_SAVE_DIR)

    # Use more specific plotting set-ups tailored to the paper
    # cp.bin_meas_numb(psp_stats, PLOT_SAVE_DIR)
    pc.paper_npT_com(psp_stats, sim_data_eq, sim_data_pol, PLOT_SAVE_DIR)

    # RP and ML, with integrated ML
    mli_dist, mli_ml = dr.massloss_interpolate(f"{ML_CONT}")
    pc.paper_plot_mlrp(psp_stats, sim_data_eq, sim_data_pol, mli_dist, mli_ml,
                       PLOT_SAVE_DIR)


# print(f"AT 40 Rs:\n\n"
#      f"\t\t EQ\t\t POL\t\t PSP\n\n"
#      f"VR\t\t {sim_data_eq.vr[-1]:.0f}\t\t "
#      f"{sim_data_pol.vr[-1]:.0f}\t\t {PSP_stats.vr.mean[-1]:.0f}\n\n"
#      f"NP\t\t {sim_data_eq.np[-1]:.1e}\t\t "
#      f"{sim_data_pol.np[-1]:.1e}\t\t {PSP_stats.np.mean[-1]:.1e}\n\n"
#      f"T\t\t {sim_data_eq.T[-1]:.1e}\t\t "
#      f"{sim_data_pol.T[-1]:.1e}\t\t {PSP_stats.T.mean[-1]:.1e}\n\n"
#      f"RP\t\t {sim_data_eq.rampressure[-1]:.1e}\t\t "
#      f"{sim_data_pol.rampressure[-1]:.1e}\t\t "
#      f"{PSP_stats.rampressure.mean[-1]:.1e}\n\n"
#      f"ML\t\t {sim_data_eq.massloss[-1]:.1e}\t\t "
#      f"{mli_ml[-1]:.1e}\t\t "
#      f"{PSP_stats.massloss.mean[-1]:.1e}\n\n")


if __name__ == "__main__":
    main()