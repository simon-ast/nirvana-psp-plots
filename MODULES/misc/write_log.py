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
