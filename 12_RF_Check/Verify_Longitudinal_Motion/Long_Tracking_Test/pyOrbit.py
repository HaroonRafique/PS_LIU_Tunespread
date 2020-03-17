import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import scipy.io as sio
from scipy.stats import moment
import os

# plotting 
import matplotlib
matplotlib.use('Agg')
import matplotlib.cm as cm

# Use switches in simulation_parameters.py in current folder
#-------------------------------------------------------------
from simulation_parameters import switches as s
from simulation_parameters import parameters as p

# utils
from orbit.utils.orbit_mpi_utils import bunch_orbit_to_pyorbit, bunch_pyorbit_to_orbit
from orbit.utils.consts import mass_proton, speed_of_light, pi

# bunch
from bunch import Bunch
from bunch import BunchTwissAnalysis, BunchTuneAnalysis
from orbit.bunch_utils import ParticleIdNumber

# diagnostics
from orbit.diagnostics import TeapotStatLatsNode, TeapotMomentsNode, TeapotTuneAnalysisNode
from orbit.diagnostics import addTeapotDiagnosticsNodeAsChild
from orbit.diagnostics import addTeapotMomentsNodeSet, addTeapotStatLatsNodeSet

# PTC lattice
from libptc_orbit import *
from ext.ptc_orbit import PTC_Lattice
from ext.ptc_orbit import PTC_Node
from ext.ptc_orbit.ptc_orbit import setBunchParamsPTC, readAccelTablePTC, readScriptPTC
from ext.ptc_orbit.ptc_orbit import updateParamsPTC, synchronousSetPTC, synchronousAfterPTC
from ext.ptc_orbit.ptc_orbit import trackBunchThroughLatticePTC, trackBunchInRangePTC
from orbit.aperture import TeapotApertureNode

# transverse space charge
from spacecharge import SpaceChargeCalcSliceBySlice2D

from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalcAnalyticGaussian
from spacecharge import InterpolatedLineDensityProfile

from lib.output_dictionary import *
from lib.save_bunch_as_matfile import *
from lib.suppress_stdout import suppress_STDOUT
from lib.pyOrbit_Bunch_Gather import *
from lib.pyOrbit_Tunespread_Calculator import *
from lib.pyOrbit_ParticleOutputDictionary import *
from lib.pyOrbit_GenerateInitialDistribution import *
from lib.pyOrbit_PrintLatticeFunctionsFromPTC import *
from lib.pyOrbit_PTCLatticeFunctionsDictionary import *
readScriptPTC_noSTDOUT = suppress_STDOUT(readScriptPTC)

# MPI stuff
#-----------------------------------------------------------------------
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)
print '\n\tStart PyORBIT simulation on MPI process: ', rank

# Function to check that a file isn't empty (common PTC file bug)
def is_non_zero_file(fpath):  
	print '\n\t\t\tis_non_zero_file:: Checking file ', fpath
	print '\n\t\t\tis_non_zero_file:: File exists = ', os.path.isfile(fpath)
	print '\n\t\t\tis_non_zero_file:: Size > 3 bytes = ', os.path.getsize(fpath)
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 3

# Function to check and read PTC file
def CheckAndReadPTCFile(f):
	if is_non_zero_file(f): 
		readScriptPTC_noSTDOUT(f)
	else:
		print '\n\t\t\CheckAndReadPTCFile:: ERROR: PTC file ', f, ' is empty or does not exist, exiting'
		exit(0)

# Function to open TWISS_PTC_table.OUT and return fractional tunes
def GetTunesFromPTC():
	readScriptPTC_noSTDOUT('../PTC/twiss_script.ptc')
	with open('TWISS_PTC_table.OUT') as f:
		first_line = f.readline()
		Qx = (float(first_line.split()[2]))
		Qy = (float(first_line.split()[3]))
	os.system('rm TWISS_PTC_table.OUT')
	return Qx, Qy

# simple sequence
def seq_start_to_end(n_vals, start, stop):
    n_mp = n_vals
    interval = (stop-start)/(n_mp-1) 

    print('seq_even_about_start::interval = ', interval)

    positions = np.arange(start, stop+interval, interval)
    
    return positions
    
def check_if_fig_exists(name):
    ret_val = False
    if os.path.isfile(name):
        print name, ' already exists, plotting skipped'
        ret_val = True
    return ret_val
    
def z_to_time(z, beta): 
    c = 299792458
    return z / (c * beta)

def dpp_from_dE(dE, E, beta):
    return (dE / (E * beta**2))

# Create folder structure
#-----------------------------------------------------------------------
print '\n\t\tmkdir on MPI process: ', rank
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('bunch_output')
mpi_mkdir_p('output')
mpi_mkdir_p('lost')

# Lattice function dictionary to print closed orbit
#-----------------------------------------------------------------------
if s['Update_Twiss']:
	ptc_dictionary_file = 'input/ptc_dictionary.pkl'
	if not os.path.exists(ptc_dictionary_file):        
		PTC_Twiss = PTCLatticeFunctionsDictionary()
	else:
		with open(ptc_dictionary_file) as sid:
			PTC_Twiss = pickle.load(sid)

# Dictionary for simulation status
#-----------------------------------------------------------------------
import pickle # HAVE TO CLEAN THIS FILE BEFORE RUNNING A NEW SIMULATION
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
	sts = {'turn': -1}
else:
	with open(status_file) as fid:
		sts = pickle.load(fid)

# Generate Lattice (MADX + PTC) - Use MPI to run on only one 'process'
#-----------------------------------------------------------------------
print '\nStart MADX on MPI process: ', rank
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
orbit_mpi.MPI_Barrier(comm)

# Generate PTC RF table
#-----------------------------------------------------------------------
print '\n\t\tCreate RF file on MPI process: ', rank
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF 
write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])

# Initialize a Teapot-Style PTC lattice
#-----------------------------------------------------------------------
print '\n\t\tRead PTC flat file: on MPI process: ', rank
PTC_File = 'PTC-PyORBIT_flat_file.flt'
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

print '\n\t\tRead PTC files on MPI process: ', rank
CheckAndReadPTCFile('PTC/fringe.ptc')
CheckAndReadPTCFile('PTC/time.ptc')
CheckAndReadPTCFile('PTC/ramp_cavities.ptc')

# Create a dictionary of parameters
#-----------------------------------------------------------------------
print '\n\t\tMake paramsDict on MPI process: ', rank
paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm

# Add apertures
#-----------------------------------------------------------------------
print '\n\t\tAdd apertures on MPI process: ', rank
position = 0
for node in Lattice.getNodes():
	myaperturenode = TeapotApertureNode(1, 10, 10, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()

# Import a bunch and relevant parameters for it
#-----------------------------------------------------------------------
if sts['turn'] < 0:
	print '\n\t\tCreate bunch on MPI process: ', rank
	bunch = Bunch()
	setBunchParamsPTC(bunch)

	p['harmonic_number'] = Lattice.nHarm 
	p['phi_s']           = 0
	p['gamma']           = bunch.getSyncParticle().gamma()
	p['beta']            = bunch.getSyncParticle().beta()
	p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
	# ~ p['bunch_length'] = p['sig_z']/speed_of_light/bunch.getSyncParticle().beta()*4
	p['bunch_length'] = p['bunch_length']
	kin_Energy = bunch.getSyncParticle().kinEnergy()

	print '\n\t\tOutput simulation_parameters on MPI process: ', rank
	for i in p:
		print '\t', i, '\t = \t', p[i]

	if s['CreateDistn']:
# Create the initial distribution 
#-----------------------------------------------------------------------
		print '\ngenerate_initial_distribution on MPI process: ', rank
		# ~ Particle_distribution_file = generate_initial_distribution_from_tomo(p, 1, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
		Particle_distribution_file = generate_initial_long_poincare_distribution(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

		print '\bunch_orbit_to_pyorbit on MPI process: ', rank
		bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.

	else:
# OR load bunch from file
#-----------------------------------------------------------------------
		print '\n\t\tLoad distribution from ', p['input_distn'] ,' on MPI process: ', rank
		path_to_distn = p['input_distn']
		bunch = bunch_from_matfile(path_to_distn)

# Add Macrosize to bunch
#-----------------------------------------------------------------------
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs

# Dump and save as Matfile
#-----------------------------------------------------------------------
	# ~ bunch.dumpBunch("input/mainbunch_start.dat")
	print '\n\t\tSave bunch in bunch_output/mainbunch_-000001.mat on MPI process: ', rank
	saveBunchAsMatfile(bunch, "bunch_output/mainbunch_-000001")
	print '\n\t\tSave bunch in input/mainbunch.mat on MPI process: ', rank
	saveBunchAsMatfile(bunch, "input/mainbunch")
	sts['mainbunch_file'] = "input/mainbunch"

# Create empty lost bunch
#-----------------------------------------------------------------------
	lostbunch = Bunch()
	bunch.copyEmptyBunchTo(lostbunch)
	lostbunch.addPartAttr('ParticlePhaseAttributes')
	lostbunch.addPartAttr("LostParticleAttributes")	
	saveBunchAsMatfile(lostbunch, "input/lostbunch")
	sts['lostbunch_file'] = "input/lostbunch"

# Add items to pickle parameters
#-----------------------------------------------------------------------
	sts['turns_max'] = p['turns_max']
	sts['turns_update'] = p['turns_update']
	sts['turns_print'] = p['turns_print']
	sts['circumference'] = p['circumference']

bunch = bunch_from_matfile(sts['mainbunch_file'])
lostbunch = bunch_from_matfile(sts['lostbunch_file'])
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch

#############################-------------------########################
#############################	SPACE CHARGE	########################
#############################-------------------########################

# Add space charge nodes
#----------------------------------------------------
if s['Space_Charge']:
	print '\n\t\tAdding slice-by-slice space charge nodes on MPI process: ', rank
	# Make a SC solver
	calcsbs = SpaceChargeCalcSliceBySlice2D(s['GridSizeX'], s['GridSizeY'], s['GridSizeZ'], useLongitudinalKick=True)
	sc_path_length_min = 1E-8
	# Add the space charge solver to the lattice as child nodes
	sc_nodes = scLatticeModifications.setSC2p5DAccNodes(Lattice, sc_path_length_min, calcsbs)
	print '\n\t\tInstalled', len(sc_nodes), 'space charge nodes ...'


# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")

tunes.assignTwiss(*[Twiss_at_parentnode_entrance[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

# Define twiss analysis and output dictionary
#-----------------------------------------------------------------------
print '\n\t\tbunchtwissanalysis on MPI process: ', rank
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

output_file = 'output/output.mat'
output = Output_dictionary()
output.addParameter('turn', lambda: turn)
output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
output.addParameter('D_x', lambda: bunchtwissanalysis.getDispersion(0))
output.addParameter('D_y', lambda: bunchtwissanalysis.getDispersion(1))
output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))
output.addParameter('beta_x', lambda: bunchtwissanalysis.getBeta(0))
output.addParameter('beta_y', lambda: bunchtwissanalysis.getBeta(1))
output.addParameter('alpha_x', lambda: bunchtwissanalysis.getAlpha(0))
output.addParameter('alpha_y', lambda: bunchtwissanalysis.getAlpha(1))
output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
output.addParameter('eff_beta_x', lambda: bunchtwissanalysis.getEffectiveBeta(0))
output.addParameter('eff_beta_y', lambda: bunchtwissanalysis.getEffectiveBeta(1))
output.addParameter('eff_epsn_x', lambda: bunchtwissanalysis.getEffectiveEmittance(0))
output.addParameter('eff_epsn_y', lambda: bunchtwissanalysis.getEffectiveEmittance(1))
output.addParameter('eff_alpha_x', lambda: bunchtwissanalysis.getEffectiveAlpha(0))
output.addParameter('eff_alpha_y', lambda: bunchtwissanalysis.getEffectiveAlpha(1))
output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())


# Pre Track Bunch Twiss Analysis & Add BunchGather outputs
#-----------------------------------------------------------------------
print '\n\t\tStart tracking on MPI process: ', rank
turn = -1
bunchtwissanalysis.analyzeBunch(bunch)
moments = BunchGather(bunch, turn, p) # Calculate bunch moments and kurtosis

# Add moments and kurtosis
output.addParameter('sig_x', lambda: moments['Sig_x'])
output.addParameter('sig_xp', lambda: moments['Sig_xp'])
output.addParameter('sig_y', lambda: moments['Sig_y'])
output.addParameter('sig_yp', lambda: moments['Sig_yp'])
output.addParameter('sig_z', lambda: moments['Sig_z'])
output.addParameter('sig_dE', lambda: moments['Sig_dE'])

output.addParameter('mu_x', lambda: moments['Mu_x'])
output.addParameter('mu_xp', lambda: moments['Mu_xp'])
output.addParameter('mu_y', lambda: moments['Mu_y'])
output.addParameter('mu_yp', lambda: moments['Mu_yp'])
output.addParameter('mu_z', lambda: moments['Mu_z'])
output.addParameter('mu_dE', lambda: moments['Mu_dE'])

output.addParameter('min_x', lambda: moments['Min_x'])
output.addParameter('min_xp', lambda: moments['Min_xp'])
output.addParameter('min_y', lambda: moments['Min_y'])
output.addParameter('min_yp', lambda: moments['Min_yp'])
output.addParameter('min_z', lambda: moments['Min_z'])
output.addParameter('min_dE', lambda: moments['Min_dE'])

output.addParameter('max_x', lambda: moments['Max_x'])
output.addParameter('max_xp', lambda: moments['Max_xp'])
output.addParameter('max_y', lambda: moments['Max_y'])
output.addParameter('max_yp', lambda: moments['Max_yp'])
output.addParameter('max_z', lambda: moments['Max_z'])
output.addParameter('max_dE', lambda: moments['Max_dE'])

output.addParameter('kurtosis_x', lambda: moments['Kurtosis_x'])
output.addParameter('kurtosis_xp', lambda: moments['Kurtosis_xp'])
output.addParameter('kurtosis_y', lambda: moments['Kurtosis_y'])
output.addParameter('kurtosis_yp', lambda: moments['Kurtosis_yp'])
output.addParameter('kurtosis_z', lambda: moments['Kurtosis_z'])
output.addParameter('kurtosis_dE', lambda: moments['Kurtosis_dE'])

output.addParameter('kurtosis_x_6sig', lambda: moments['Kurtosis_x_6sig'])
output.addParameter('kurtosis_xp_6sig', lambda: moments['Kurtosis_xp_6sig'])
output.addParameter('kurtosis_y_6sig', lambda: moments['Kurtosis_y_6sig'])
output.addParameter('kurtosis_yp_6sig', lambda: moments['Kurtosis_yp_6sig'])
output.addParameter('kurtosis_z_6sig', lambda: moments['Kurtosis_z_6sig'])
output.addParameter('kurtosis_dE_6sig', lambda: moments['Kurtosis_dE_6sig'])

start_time = time.time()
last_time = time.time()
output.addParameter('turn_time', lambda: time.strftime("%H:%M:%S"))
output.addParameter('turn_duration', lambda: (time.time() - last_time))
output.addParameter('cumulative_time', lambda: (time.time() - start_time))

# PTC_Twiss must be updated before updating output
if s['Update_Twiss']:
	PTC_Twiss.UpdatePTCTwiss(Lattice, turn)
	output.addParameter('orbit_x_min', lambda: PTC_Twiss.GetMinParameter('orbit_x', turn))
	output.addParameter('orbit_x_max', lambda: PTC_Twiss.GetMaxParameter('orbit_x', turn))
	output.addParameter('orbit_y_min', lambda: PTC_Twiss.GetMinParameter('orbit_y', turn))
	output.addParameter('orbit_y_max', lambda: PTC_Twiss.GetMaxParameter('orbit_y', turn))

output.update()

if os.path.exists(output_file):
	output.import_from_matfile(output_file)

# Define particle output dictionary - automatically adds first particle
#-----------------------------------------------------------------------
particle_output = Particle_output_dictionary()

for i in range(p['n_macroparticles']):
        if i is 0:
                pass
        else:
                particle_output.AddNewParticle(i)
                
# Track
#-----------------------------------------------------------------------
print '\n\t\tStart tracking on MPI process: ', rank
start_time = time.time()
last_time = time.time()

print '\n\t\tstart time = ', start_time

for turn in range(sts['turn']+1, sts['turns_max']):
	if not rank:	last_time = time.time()

	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance
	moments = BunchGather(bunch, turn, p)	# Calculate bunch moments and kurtosis
	if s['Update_Twiss']: 
		readScriptPTC_noSTDOUT("PTC/update-twiss.ptc") # this is needed to correclty update the twiss functions in all lattice nodes in updateParamsPTC
		updateParamsPTC(Lattice,bunch) 			# to update bunch energy and twiss functions

	if turn in sts['turns_update']:	sts['turn'] = turn

	output.update()
	particle_output.Update(bunch, turn)

	if turn in sts['turns_print']:
		saveBunchAsMatfile(bunch, "input/mainbunch")
		saveBunchAsMatfile(bunch, "bunch_output/mainbunch_%s"%(str(turn).zfill(6)))
		saveBunchAsMatfile(lostbunch, "lost/lostbunch_%s"%(str(turn).zfill(6)))
		output.save_to_matfile(output_file)
		if not rank:
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)



########################################################################
# Plots
########################################################################
plt.rcParams['figure.figsize'] = [8.0, 8.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 14

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 10

plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.markersize'] = 1

mpi_mkdir_p('Plots')
save_folder = 'Plots'  
main_label = 'LIU_2023_Long_Test'
if s['Space_Charge']:
        sc = 'SbS'
else:
        sc = 'NoSC'
        

########################################################################
# Simple Poincare Sections
########################################################################

particle_ids = seq_start_to_end(p['n_macroparticles'], 0, p['n_macroparticles']-1)
turn_ids = seq_start_to_end(p['turns_max'], 0, p['turns_max']-1)

for i in particle_ids:
        particle_output.PrintParticle(i)
        

print 'Particle IDS: ', particle_ids
print 'Turn IDS: ', turn_ids

turn_tot = p['turns_max']

LorentzBeta = p['beta']
LorentzGamma = p['gamma']
BeamEnergy = p['energy']
test_str = 'x'
test = particle_output.ReturnCoOrdinate(0, test_str, 9)
print '\ntest particle_output.ReturnCoOrdinate(0, \'x\', 0) = ', test

t_test = z_to_time(particle_output.ReturnCoOrdinate(0, 'z', 0), p['beta']) * 1E9
print '\nt_test = ', t_test

dpp_test = dpp_from_dE(particle_output.ReturnCoOrdinate(0, 'dE', 0), p['energy'], p['beta'] )
print '\ndpp_test = ', dpp_test

# X XP
########################################################################
param1 = 'x'
param2 = 'xp'
multi1 = 1E3
multi2 = 1E3

x_lab = 'x [mm]'
y_lab = 'xp [mrad]'

tit = main_label + ' ' + sc + ' ' + param1  + ' ' + param2
        
savename = save_folder + '/'+ main_label + '_Poincare_' + param1 + '_' + param2 + '.png'
file_exists = check_if_fig_exists(savename)

if not file_exists:
        fig1 = plt.figure(facecolor='w', edgecolor='k')
        ax1 = fig1.add_subplot(111)
        ax1.set_title(tit);

        ax1.set_ylabel(y_lab);
        ax1.set_xlabel(x_lab);

        colors = cm.rainbow(np.linspace(0, 1, len(turn_ids)))

        for t in turn_ids:
                for p in particle_ids:
                        ax1.scatter(particle_output.ReturnCoOrdinate(p, param1, t) *multi1, particle_output.ReturnCoOrdinate(p, param2, t) *multi2, color=colors[t]);

        ax1.grid(lw=1, ls=':');
        # ~ ax1.set_xlim(-1,turn_tot)
        plt.tight_layout()
        plt.savefig(savename, dpi = 200);

# X Y
########################################################################
param1 = 'x'
param2 = 'y'
multi1 = 1E3
multi2 = 1E3

x_lab = 'x [mm]'
y_lab = 'y [mm]'

tit = main_label + ' ' + sc + ' ' + param1  + ' ' + param2
        
savename = save_folder + '/'+ main_label + '_Poincare_' + param1 + '_' + param2 + '.png'
file_exists = check_if_fig_exists(savename)

if not file_exists:
        fig1 = plt.figure(facecolor='w', edgecolor='k')
        ax1 = fig1.add_subplot(111)
        ax1.set_title(tit);

        ax1.set_ylabel(y_lab);
        ax1.set_xlabel(x_lab);

        colors = cm.rainbow(np.linspace(0, 1, len(turn_ids)))

        for t in turn_ids:
                for p in particle_ids:
                        ax1.scatter(particle_output.ReturnCoOrdinate(p, param1, t) *multi1, particle_output.ReturnCoOrdinate(p, param2, t) *multi2, color=colors[t]);

        ax1.grid(lw=1, ls=':');
        # ~ ax1.set_xlim(-1,turn_tot)
        plt.tight_layout()
        plt.savefig(savename, dpi = 200);
        
# Y YP
########################################################################
param1 = 'y'
param2 = 'yp'
multi1 = 1E3
multi2 = 1E3

x_lab = 'y [mm]'
y_lab = 'yp [mrad]'

tit = main_label + ' ' + sc + ' ' + param1  + ' ' + param2
        
savename = save_folder + '/'+ main_label + '_Poincare_' + param1 + '_' + param2 + '.png'
file_exists = check_if_fig_exists(savename)

if not file_exists:
        fig1 = plt.figure(facecolor='w', edgecolor='k')
        ax1 = fig1.add_subplot(111)
        ax1.set_title(tit);

        ax1.set_ylabel(y_lab);
        ax1.set_xlabel(x_lab);

        colors = cm.rainbow(np.linspace(0, 1, len(turn_ids)))

        for t in turn_ids:
                for p in particle_ids:
                        ax1.scatter(particle_output.ReturnCoOrdinate(p, param1, t) *multi1, particle_output.ReturnCoOrdinate(p, param2, t) *multi2, color=colors[t]);

        ax1.grid(lw=1, ls=':');
        # ~ ax1.set_xlim(-1,turn_tot);
        plt.tight_layout();
        plt.savefig(savename, dpi = 200);

# Z dE
########################################################################
param1 = 'z'
param2 = 'dE'
multi1 = 1.
multi2 = 1E3

x_lab = 'z [m]'
y_lab = 'dE [MeV]'

tit = main_label + ' ' + sc + ' ' + param1  + ' ' + param2
        
savename = save_folder + '/'+ main_label + '_Poincare_' + param1 + '_' + param2 + '.png'
file_exists = check_if_fig_exists(savename)

if not file_exists:
        fig1 = plt.figure(facecolor='w', edgecolor='k')
        ax1 = fig1.add_subplot(111)
        ax1.set_title(tit);

        ax1.set_ylabel(y_lab);
        ax1.set_xlabel(x_lab);

        colors = cm.rainbow(np.linspace(0, 1, len(turn_ids)))

        for t in turn_ids:
                for p in particle_ids:
                        ax1.scatter(particle_output.ReturnCoOrdinate(p, param1, t)*multi1, particle_output.ReturnCoOrdinate(p, param2, t)*multi2, color=colors[t]);

        ax1.grid(lw=1, ls=':');
        # ~ ax1.set_xlim(-1,turn_tot)
        plt.tight_layout()
        plt.savefig(savename, dpi = 200);

# t dpp
########################################################################
param1 = 'z'
param2 = 'dE'
multi1 = 1E9
multi2 = 1E3

x_lab = 't [ns]'
y_lab = r'$\frac{\delta p}{p_0}$ $[10^{-3}]$'

tit = main_label + ' ' + sc + ' ' + 't'  + ' ' + 'dpp'
        
savename = save_folder + '/'+ main_label + '_Poincare_' + 't' + '_' + 'dpp' + '.png'
file_exists = check_if_fig_exists(savename)

if not file_exists:
        fig1 = plt.figure(facecolor='w', edgecolor='k')
        ax1 = fig1.add_subplot(111)
        ax1.set_title(tit);

        ax1.set_ylabel(y_lab);
        ax1.set_xlabel(x_lab);

        colors = cm.rainbow(np.linspace(0, 1, len(turn_ids)))

        for t in turn_ids:
                for pp in particle_ids:
                        ax1.scatter(z_to_time(particle_output.ReturnCoOrdinate(pp, param1, t), LorentzBeta)*multi1, dpp_from_dE(particle_output.ReturnCoOrdinate(pp, param2, t)*1E9, BeamEnergy, LorentzBeta)*multi2, color=colors[t]);

        ax1.grid(lw=1, ls=':');
        # ~ ax1.set_xlim(-1,turn_tot)
        plt.tight_layout()
        plt.savefig(savename, dpi = 200);
