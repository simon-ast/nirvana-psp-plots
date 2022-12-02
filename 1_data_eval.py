from modules.pspdata import data_turnaround as ta
from modules.pspdata import data_handling as dh
from modules.plotting import plotset_general as pg
from modules.stat import stats_databin as db
from astropy.constants import R_sun
# from MODULES.misc import write_log

# NECESSARY GLOBAL VARIABLES
from modules.config import *
# CDF library (is needed to interface with the measurement data files)
# see https://cdf.gsfc.nasa.gov/
os.environ["CDF_LIB"] = "/data/home/simons97/LocalApplications/cdf/lib"
from spacepy import pycdf

# SIZE OF DISTANCE BINS IN R_SOL
DISTANCE_BIN_SIZE = float(sys.argv[1])
DATA_ROOT = f"{sys.path[0]}/DATA"
PLOT_ROOT = f"{sys.path[0]}/PLOTS"
STAT_DIR = f"{sys.path[0]}/STATISTICS"
STAT_DIR_BIN = f"{sys.path[0]}/STATISTICS/BINNED_DATA"

# SANITY CHECK: Does the data directory even exist?
if not os.path.isdir(DATA_ROOT):
    print(f"\n{DATA_ROOT} IS NOT A VALID DIRECTORY!\n")
    sys.exit(0)


def main():
    # Start the logging file
    # write_log.start_log()

    # Pandas empty DataFrame for ALL data
    total_data = pd.DataFrame()

    # Loop over all files in the desired encounter folder(s), sorted
    # in ascending order of name (equal to date)
    for folder in ENCOUNTER_NUM:

        # Sanity check: print current folder name
        print(f"\nCURRENTLY HANDLING {folder}")

        # Variable for current folder, SPC data location and SPAN-I data
        # location
        encounter_folder = f"{DATA_ROOT}/{folder}"
        spc_folder = f"{encounter_folder}/SPC"
        span_folder = f"{encounter_folder}/SPAN-I"

        # SANITY CHECK: Do all the data directories exist?
        for data_location in [encounter_folder, span_folder, span_folder]:
            if not os.path.isdir(data_location):
                print(f"\n{data_location} IS NOT A VALID DIRECTORY!\n")
                sys.exit(0)

        # Initialize data frames for encounter data
        data_enc_spc = pd.DataFrame()
        data_enc_span = pd.DataFrame()

        # FIRST SPC DATA
        print("\nEVALUATION OF SPC MEASUREMENTS")
        data_enc_spc = dh.encounter_data(spc_folder, data_enc_spc,
                                         inst="SPC")

        # SECOND SPAN-I DATA
        print("\nEVALUATION OF SPAN-I MEASUREMENTS")
        data_enc_span = dh.encounter_data(span_folder, data_enc_span,
                                          inst="SPAN-I")

        # Concatenate SPC and SPAN measurements to total data frame
        data_encounter_total = pd.concat(
            objs=[
                data_enc_spc.assign(Inst="SPC"),
                data_enc_span.assign(Inst="SPAN")
            ],
            ignore_index=True
        )

        # After looping through one full encounter, generate the
        # approach/recession divide and append and then extend the FULL
        # DataFrame
        data_encounter_total.reset_index(drop=True, inplace=True)

        # Take in the total data from one encounter and save the values
        # for approach and recession independently
        ta.approach_recession_slicing(folder, data_encounter_total)

        # Log the total amount of measurements per encounter for future
        # reference
        # write_log.append_raw_data(folder, logging_raw_array)
        # write_log.append_encounter_data(folder, data_encounter_total.posR)

        # Total data frame
        total_data = pd.concat([data_encounter_total, total_data])
        total_data.reset_index(drop=True, inplace=True)

    # Create distance bins and group the data frame according to
    # determined indices of data arrays that correspond to the
    # respective distance bins. The object 'dist_groups' is an index
    # array for the total data frame
    distance_bins = np.arange(0, 100, DISTANCE_BIN_SIZE)
    dist_groups = total_data.groupby(
        np.digitize(total_data.posR * 1e3 / R_sun.value, distance_bins)
    )

    # Make sure to empty the directory containing the data files for
    # binned data values before starting to save files from a new run.
    for file in sorted(os.listdir(STAT_DIR_BIN)):
        os.remove(f"{STAT_DIR_BIN}/{file}")

    # Loop over all created bins to sort the total data. Also log number
    # of data points and the corresponding distance bin index (see
    # empty arrays below)
    spc_numpts = []
    span_numpts = []
    dist_index = []

    # Compute and save data frame for total stats (mean, median, std,
    # q1, g3). It is of note here that "pd.assign(name=value)" creates a
    # new column in the data frame filled with "value"
    total_stats = pd.concat(
        objs=[
            dist_groups.mean(numeric_only=True).assign(Type="mean"),
            dist_groups.std(numeric_only=True).assign(Type="std"),
            dist_groups.median(numeric_only=True).assign(Type="median"),
            dist_groups.quantile(q=0.25, numeric_only=True).assign(Type="q1"),
            dist_groups.quantile(q=0.75, numeric_only=True).assign(Type="q3")
        ],
        ignore_index=True
    )
    total_stats.to_json(f"{STAT_DIR}/PSP_STATISTICS.json")

    # Save bins individually for posterity (not necessary to read in
    # separately anymore after change to pandas). Get the number of
    # decimal points used in bin size for file naming purposes.
    dec_pts = db.decimal_length(DISTANCE_BIN_SIZE)
    for r_bin, grp in dist_groups:

        # Generalized necessary variables
        # TODO: Is "Hashable" a problem here?
        bin_name = r_bin * DISTANCE_BIN_SIZE
        file_name = f"PSP_BIN_{bin_name:.{dec_pts}f}-" \
                    f"{bin_name + DISTANCE_BIN_SIZE:.{dec_pts}f}.json"

        # SANITY CHECK:
        # Stop if the distance bins exceed the simulation domain size of 40 Rs
        if bin_name > 40.0:
            print(
                f"\n\nSTOPPING AT {file_name},"
                f"OUTSIDE SIMULATION DOMAIN SIZE!\n\n"
            )
            break

        # Save Data Frames of distance bins to JSON file
        grp.to_json(f"{STAT_DIR_BIN}/{file_name}")

        # Evaluate Number of data points for each instrument!
        split_datapts = grp["Inst"].value_counts()

        # For each instrument
        try:
            spc_numpts += [split_datapts["SPC"]]
        except KeyError:
            spc_numpts += [0]

        try:
            span_numpts += [split_datapts["SPAN"]]
        except KeyError:
            span_numpts += [0]

        # Append to parameters for plot below
        dist_index += [bin_name]

    # THIS RUNS AFTER THE BIN LOOP!
    # Plot a simple scatter plot with # of data points per bin
    # TODO: Add # of data points from SPAN-i here individually
    pg.bin_analysis(PLOT_ROOT, spc_numpts, span_numpts, dist_index)


if __name__ == "__main__":
    # Set-up plot parameters
    pg.rc_setup()

    # Call main function
    main()
