#!/usr/bin/env python3

# load modules:
from boutdata.data import BoutOutputs, BoutOptionsFile # container class for outputs collected from BOUT.dmp.* files
from boututils.showdata import showdata # function that produces matplotlib animations
import numpy
from matplotlib import pyplot
from IPython.display import HTML
from sys import exit

# Output is 2d with one point in the y-direction
# Slicing with these indices eliminates the y-dimension from the arrays
inds = numpy.index_exp[:,:,0,:]

# path to directory with simulation output
path = '.'

# fraction of amplitude above background to use as minimum when finding centre-of-mass
threshold = 0.

# container object for BOUT++ simulation output
data = BoutOutputs(path=path, xguards=False, caching=True)

# grid sizes
nt, nx, nz = data['n'][inds].shape

# object to interact with options from BOUT++ input file
#options = BoutOptionsFile(path+'/BOUT.inp') # read input file
# BOUT.settings file contains options actually used by the simulation, including command line options and defaults
options = BoutOptionsFile(path+'/BOUT.settings')

# get some parameters
A = max(options['blob']['A'], options['blob2']['A']) # amplitude of the largest filament
Lx = options['mesh']['Lx'] # radial width of domain, in units of rho_s
Lz = options['mesh']['Lz'] # binormal width of domain, in units of rho_s

# x-coordinate in units of rho_s
# make coordinates 2d arrays so that they broadcast correctly with data arrays
x = numpy.linspace(0.5/nx*Lx, Lx*(1.-0.5/nx), nx)[:, numpy.newaxis]

# z-coordinate in units of rho_s
z = numpy.linspace(0., Lz, nz, endpoint=False)[numpy.newaxis, :]

# make a movie of the density
showdata(data['n'][inds], t_array=data['t_array'], x=x[:,0], y=z[0,:])


# find the centre-of-mass position of the filaments

# take 'filament' to be the density above this level
nmin = 1. + threshold*A

nFilament = data['n'][inds] - nmin
# zero all negative entries, which represent density below the threshold
nFilament[nFilament<0.] = 0.

# calculate centre-of-mass
# sum over x- and z-dimensions
# don't need area element dx*dz because we only want ratios of integrals
nTotal = numpy.sum(nFilament, axis=(1,2))
xCoM = numpy.sum(x*nFilament, axis=(1,2))/nTotal
zCoM = numpy.sum(z*nFilament, axis=(1,2))/nTotal


# find the centre-of-mass velocity

dt = data['t_array'][1] - data['t_array'][0]

# will take simple finite-difference time derivative with output half way between data time points
tArrayVelocity = 0.5*(data['t_array'][:-1] + data['t_array'][1:])

# calculate velocities
vxCoM = 0.5 * (xCoM[1:] - xCoM[:-1]) / dt
vzCoM = 0.5 * (zCoM[1:] - zCoM[:-1]) / dt


# plot centre-of-mass positions
pyplot.figure('X')
pyplot.plot(data['t_array'], xCoM)
pyplot.xlabel('t / Omega_i^-1')
pyplot.ylabel('xCoM / rho_s')
pyplot.tight_layout()

pyplot.figure('Z')
pyplot.plot(data['t_array'], zCoM)
pyplot.xlabel('t / Omega_i^-1')
pyplot.ylabel('zCoM / rho_s')
pyplot.tight_layout()

# plot centre-of-mass velocities
pyplot.figure('Vx')
pyplot.plot(tArrayVelocity, vxCoM)
pyplot.xlabel('t / Omega_i^-1')
pyplot.ylabel('vxCoM / c_s')
pyplot.tight_layout()

pyplot.figure('Vz')
pyplot.plot(tArrayVelocity, vzCoM)
pyplot.xlabel('t / Omega_i^-1')
pyplot.ylabel('vzCoM / c_s')
pyplot.tight_layout()

pyplot.show()

exit(0)
