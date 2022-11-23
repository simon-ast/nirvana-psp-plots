from modules.eoscomparison import data_read, plotting


# GLOBALS
POLY_EQ = "STATISTICS/poly_equatorial.csv"
POLY_POL = "STATISTICS/poly_polar.csv"
NIR_EQ = "STATISTICS/NIRwave_equatorial.csv"
NIR_POL = "STATISTICS/NIRwave_polar.csv"

# SAVING FIGURES
SAVE_DIR = "PLOTS/eos-comparison"
SAVE_TYPE = ["eps"]


def main():
    # GENERATE USABLE DATA FROM OUTLINES
    poly_eq = data_read.SimMeshData(POLY_EQ)
    poly_pol = data_read.SimMeshData(POLY_POL)
    nir_eq = data_read.SimMeshData(NIR_EQ)
    nir_pol = data_read.SimMeshData(NIR_POL)

    # PLOT DESIRED RADIAL PROFILES
    plotting.rc_setup()

    for indicator in ["vr", "T", "np"]:
        plotting.plot_comparison(poly_eq, poly_pol, nir_eq, nir_pol,
                                 indicator, SAVE_DIR, SAVE_TYPE)

    plotting.plot_combination(poly_eq, poly_pol, nir_eq, nir_pol,
                              SAVE_DIR, SAVE_TYPE)


if __name__ == "__main__":
    main()
