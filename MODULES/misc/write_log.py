import sys

# GLOBALS
FILE_NAME = f"{sys.path[0]}/EXECUTE_LOG.dat"


def start_log():
    """Start the log-file"""
    with open(FILE_NAME, "w") as f:
        f.write("# Logging execution of calculation routine.\n\n")


def log_encounter(enc_number):
    """Log encounter number"""
    with open(FILE_NAME, "a") as f:
        f.write(f"## CURRENTLY HANDLING {enc_number}\n\n")


def log_inst(name):
    """Log encounter number"""
    with open(FILE_NAME, "a") as f:
        f.write(f"### INSTRUMENT: {name}\n\n")


def append_numpts(num_pts, case):
    """Append length of different reduction steps"""

    with open(FILE_NAME, "a") as f:
        if case == "raw":
            f.write(f"RAW DATA:\t {num_pts:.5e}\n")
        if case == "dqf":
            f.write(f"DQF DATA:\t {num_pts:.5e}\n")
        if case == "time_avg":
            f.write(f"TIME AVG DATA:\t {num_pts:.5e}\n\n")


def eof_comparison(out_filename, sim_eq, sim_pol, mli_ml, psp):
    """
    Write the EOF (outer boundary) values of simulation and
    observational data to file for rough comparison.
    'mli_ml' is the interpolated mass loss as calculated.
    """
    with open(out_filename, "w") as f:
        f.write(
            f"AT 40 Rs:\n\n"
            f"\t\t EQ\t\t POL\t\t PSP\n\n"
            f"VR\t\t {sim_eq.vr[-1]:.0f}\t\t "
            f"{sim_pol.vr[-1]:.0f}\t\t {psp.vr.mean.values[-1]:.0f}\n\n"
            f"NP\t\t {sim_eq.np[-1]:.1e}\t\t "
            f"{sim_pol.np[-1]:.1e}\t\t {psp.np.mean.values[-1]:.1e}\n\n"
            f"T\t\t {sim_eq.T[-1]:.1e}\t\t "
            f"{sim_pol.T[-1]:.1e}\t\t {psp.T.mean.values[-1]:.1e}\n\n"
            f"RP\t\t {sim_eq.rampressure[-1]:.1e}\t\t "
            f"{sim_pol.rampressure[-1]:.1e}\t\t "
            f"{psp.rampressure.mean.values[-1]:.1e}\n\n"
            f"ML\t\t {sim_eq.massloss[-1]:.1e}\t\t "
            f"{mli_ml[-1]:.1e}\t\t "
            f"{psp.massloss.mean.values[-1]:.1e}\n\n"
        )

    pass
