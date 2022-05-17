"""
PSEUDOCODE

BACKGROUND
- Collect data for one Encounter in folder
	-- Variable name of folder to handle different encounters
	
- SWEAP provides (all with uncertainties)
	-- Date and time of observation
	-- Cartesian position (x, y, z)
	-- RTN frame velocity
	-- Thermal velocity w
	-- Density of protons (majority of wind)

- Collect all measurements (after reduction) into singular arrays?
	-- Could then be split by minimum distance for perihelion


OPERATIONS
- Sort through "general flag" (only use where set to 0)
- Calculate spherical heliocentric coordinates (HIC)
- Transform to usable data parameters (vr, log_T, log_rho)
"""

DATA_LOCATION = 
