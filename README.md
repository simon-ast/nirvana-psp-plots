# SWEAP/SPC data evaluation

The GitHub repository of this code does not provide the  [measurement data](http://sweap.cfa.harvard.edu/Data.html "SWEAP data") that is evaluated. For the purposes of the connected paper ([Kasper et al., 2016](https://link.springer.com/article/10.1007/s11214-015-0206-3 "Kasper et al., 2016")), several encounter phases of PSP
are evaluated:
- **ENCOUNTER 07:** 01-12-2021 to 01-23-2021, Perihelion ~ 0.090 Rs
- **ENCOUNTER 08:** 04-24-2021 to 05-04-2021, Perihelion ~ 0.076 Rs
- **ENCOUNTER 09:** 08-04-2021 to 08-15-2021, Perihelion ~ 0.076 Rs

The data is reduced according to 
- **SPC:** The conservative boundaries of the [SWEAP User Guide](http://sweap.cfa.harvard.edu/sweap_data_user_guide.pdf "SWEAP User Guide") (`general_flag=0`)
- **SPAN-I**: The `EFLUX_VS_PHI` variable (where a flux peak above 150° shows that the solar wind is not fully in the FOV of the instrument)

Additionally, both data sets are averaged over a ten-second time frame to account for different measurement cadences, and then sorted into radial distance bins congruent with the radial cell size of the connected NIRVANA simulations (`dr = 0.1 R_s`), treated with a mean/stddev and median/quartiles evaluation and compared to a radial outline of the simulation results.

## Structure
The code execution routine can be read in the bash-script `evaluation_run.sh`. It sets the size of the radial bins as a global variable and then:
1. `1_data_eval.py`: Reads in the observational data files, sorts ALL data into distance bins and writes data file for each distance bin into `STATISTICS/BINNED_DATA`
2. `2_binnded_stats.py`: Takes all files in previously mentioned folder and creates a new file, `psp_statistics.dat`, with mean+stddev and median+q1/q3 for each major parameter and distance bin. Also creates bar charts for each major parameter and distance bin
3. `3_ingress_egress.py`: Similar as above, but the data is split between ingress and egress phase for each encounter
4. `4_observation_plots.py`: Creates median+stddev and mean+q1/q3 plots for all three major parameters
5. `5_comparison_plots.py`: Collects the evaluated measurement data and creates plots together with a radial profile of the simulation results.
6. `6_nirwave_poly_comparison.py`: Generates plots as a comparison between NIRwave and polytropic wind simulations (not directly related to PSP data evaluation)

Be aware that the `binned_stats.py` routine creates three (3) histograms per distance bin, which can result in a large number of files. These plots are generated in `PLOTS/BinHistrograms` but are not included in this repository

## Selected Results
This first plot below illustrates the measurements by SPC (black) and SPAN-I (red) during the ingress phase of encounter 8, after the quality flag and FOV data reduction (but before time-averaging!). The first panel shows the corresponding radial distance (where SPC stops long before the perihelion), the second panel shows the radial velocity component and the third panel shows the number density of protons.
![SPC Measurement Evaluation](PLOTS/IngressEgressPlots/encounters/8_I.svg)

The second plot below illustrates the evaluated SPC and SPAN-I measurements from Encounters 7, 8 and 9, both for individual ingress and egress phases (top row) as well as mean and standard deviation parameters (bottom row).
![SPC Measurement Evaluation](PLOTS/IngressEgressPlots/PSP_I-E_measurements.svg)

Comparing the measurement data to the simulated solar wind results, the bimodal structure of the simulations becomes visible.

![SPC Measurement Evaluation](PLOTS/ComparisonPlots/vr_comparison.svg)
