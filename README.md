# PSP SWEAP (and FIELDS?) data analysis

## Data Usage
The github repository of this code does not provide the measurement data that is evaluated 
here. For the purposes of the connected paper (HYPERLINK), several encounter phases of PSP
are evaluated:
- **ENCOUNTER 08:** 04-24-2021 to 05-04-2021, Perihelion ~ 0.076 Rs
- **ENCOUNTER 09:** 08-04-2021 to 08-15-2021, Perihelion ~ 0.076 Rs
- **ENCOUNTER 10:** 11-16-2021 to 11-26-2021, Perihelion ~ 0.062 Rs

PSEUDOCODE

BACKGROUND
- Collect data for one Encounter in folder
	- Variable name of folder to handle different encounters
In total, evaluate the last few encounters
	- Perihelia of ~0.064 au (ENCOUNTER 10)
	- Perihelia of ~0.074 au (ENCOUNTER 8 and 9)
	- Perihelia of ~0.090 au (ENCOUNTER 6 and 7)
	
- SWEAP provides (all with uncertainties)
	- Date and time of observation
	- Cartesian position (x, y, z)
	- RTN frame velocity
	- Thermal velocity w
	- Density of protons (majority of wind)

- Collect all measurements (after reduction) into singular arrays?
	- Could then be split by minimum distance for perihelion


OPERATIONS
- Sort through "general flag" (only use where set to 0)
	- Also sort through each array to find entries with -1e30, which
	   marks failed measurements
- Calculate spherical heliocentric coordinates (HIC)
- Transform to usable data parameters (vr, log_T, log_rho)
- Generate log-file with important information
	- Total number of data points
	- Reduced number of data points
	- Epoch from start to finish
- If mean/median + std is desired, I need to bin the data appropriately
	- Loop over multiple files, collect data in bins, do evaluation at
	   end.
	- Generate a plot (Bar Chart) displaying each bin at the end, to
	   have quick reference.
- Radial data binning: Find appropriate bin size (maybe 0.5 R_sol)
- After radial sorting is done:
	- Take all indices for each bin and treat the data bin by bin

SINGLE ENCOUNTER SEQUENCE
-For File in encounter
	- Fill encounter dictionary with reduced values
- Find index of minimum distance-value
	- Split total data into approach and recession

## Files
- test.py: Testing data operations on data files.


## NIROperations
Python modules necessary in the processing of measurement data.