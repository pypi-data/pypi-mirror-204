import os
from ethraid import _ROOT

# CONSTANTS
# Mass of the Sun in grams
M_sun = 1.988409870698051e+33
# Mass of Jupiter in grams
M_jup = 1.8981245973360504e+30
# 1 parsec in AU
pc_in_au = 206264.80624548031 # (c.pc.cgs/c.au.cgs).value
# Conversion factor between solar masses and Jupiter masses
Ms2Mj = M_sun/M_jup

# GENERAL PARAMS
# Number of orbital models to simulate
num_points = 1e6
# Dimension of grid over which model probabilities will be spread.
# Higher grid_num gives greater resolution, but fewer models per grid box.
# When using CLI, grid_num should be supplied at the command line rather than config file (default grid_num=100).
# Include grid_num in config file for API usage.
grid_num = 100
# Whether to save raw arrays (1d, unbinned), processed arrays (2d, binned), or both
save = ['raw', 'proc']
# Output directory. Destination of folder containing saved products
outdir = ''
# Minimum and maximum semi-major axes to sample (AU)
min_a = 1.6489
max_a = 1e2
# Minimum and maximum masses to sample (M_Jup)
min_m = 0.769
max_m = 1e3


# STELLAR PARAMS
# Star name for file labeling. Need not be official.
star_name = '191939'
# Mass of star in Jupiter masses
m_star = 0.807*Ms2Mj
# Distance from Earth to star in AU
d_star = 53.8*pc_in_au


# RV PARAMS
# Whether to use RV data. Assign run_rv=False to omit RVs from the calculation entirely.
run_rv = True
# Linear RV trend term (m/s/day).
gammadot = 0.114
# Error on gammadot
gammadot_err = 0.006
# Quadratic RV curvature term (m/s/day/day)
gammaddot = -6e-5
# Error on gammaddot
gammaddot_err = 1.9e-5
# Epoch at which gammadot and gammaddot are measured. Typically about 1/2 way through the observing baseline.
rv_epoch = 2458847.780463


# ASTROMETRY PARAMS
# Whether to use astrometry data. Assign run_astro=False to omit astrometry from the calculation entirely.
run_astro = True
# Difference between the average Gaia proper motion and the position-based average proper motion between the Hipparcos and Gaia missions (milli-arcseconds/year)
# Set dmu/dmu_err to None to provide Hipparcos or Gaia ID instead
delta_mu = None
# Error on delta_mu
delta_mu_err = 1e8
# Target Hipparcos identifier. Alternative to supplying delta_mu
hip_id = '99175'
# Target Gaia DR3 identifier. Alternative to supplying delta_mu
gaia_id = None


# IMAGING PARAMS
# Whether to use imaging data. Assign run_imag=False to omit imaging from the calculation entirely.
run_imag = True
# How to calculate imaging posterior. If 'exact', forward model companions as with RVs and astrometry.
# If 'approx', then for the imaging calculations only, approximate all orbits to be face-on and circular regardless of sampled parameters, and rule out any model with a mass/angular separation combo that was detectable by imaging.
imag_calc = 'exact'
# Host star visual magnitude. Used to estimate the magnitude at the imaging wavelength
vmag = 8.97
# Wavelength at which contrast curve was acquired (micrometers)
imag_wavelength = 2.2
# Path to contrast curve
contrast_str = os.path.join(_ROOT, 'data/test_K_band.csv')
# Epoch of imaging observations (BJD).
imag_epoch = 24593300


# PLOTTING PARAMS
# Coordinates at which to plot a gold star. Usually corresponds to a known companion which could be the source of an observed trend.
scatter_plot = [3.8, 3.0]