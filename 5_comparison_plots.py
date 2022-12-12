import sys
from modules.stat import stats_dataread as dr
from modules.plotting import plotset_general as pg
from modules.plotting import plotset_comparison as pc
from modules.misc import write_log

# Necessary global variables
PSP_STAT_DIR = f"{sys.path[0]}/STATISTICS"
ML_CONT = f"{sys.path[0]}/STATISTICS/MASSLOSS_CONTOURS"
PLOT_SAVE_DIR = f"{sys.path[0]}/PLOTS/ComparisonPlots"
ROUGH_EVAL = "OUTER_BOUNDARY_COMPARISON.dat"


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

    # Write EOF values for data and simulation to roughly compare
    write_log.eof_comparison(ROUGH_EVAL, sim_data_eq, sim_data_pol, mli_ml,
                             psp_stats)


if __name__ == "__main__":
    main()
