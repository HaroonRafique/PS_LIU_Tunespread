import os
import numpy as np
from math import log10, floor

# Functions
########################################################################
def round_sig(x, sig=3):
        return round(x, sig-int(floor(log10(abs(x))))-1)

def replace_point_with_p(input_str):
        return input_str.replace(".", "p")
    
def is_non_zero_file(fpath):  
        print '\n\t\t\tis_non_zero_file:: Checking file ', fpath
        print '\n\t\t\tis_non_zero_file:: File exists = ', os.path.isfile(fpath)
        print '\n\t\t\tis_non_zero_file:: Size > 3 bytes = ', os.path.getsize(fpath)
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 3

# Folder flags
########################################################################
cwd = os.getcwd() # Get the present directory
folder = cwd.split('/')[-1] # Last part of cwd is folder name
run = folder.split('_')[0] # First word is Run
beam = folder.split('_')[1] # Second word is beam selection
if (run is 'Run3') and (beam is 'Standard'):
        year = folder.split('_')[2] # for Run3 Standard we also require the year
    
# parameters
########################################################################        
parameters = {}

parameters['Beam']			= beam
parameters['Run']			= run

if (parameters['Run'] is 'Run3') and (parameters['Beam'] is 'Standard'):
        parameters['Year']			= year
        parameters['BLonD_file']        = '../BLonD_Longitudinal_Distributions/BLonD_Longitudinal_Distn_'+parameters['Run']+'_'+parameters['Beam']+'_'+parameters['Year']+'.npz'
else:                
        parameters['BLonD_file']        = '../BLonD_Longitudinal_Distributions/BLonD_Longitudinal_Distn_'+parameters['Run']+'_'+parameters['Beam']+'.npz'

parameters['tunex']			= '621'
parameters['tuney']			= '624'

parameters['lattice_start'] 	= 'BWSH65'
parameters['n_macroparticles']	= int(5E5)


# LIU parameters: 2GeV
if parameters['Run'] is 'Run3': 
        parameters['gamma'] 		= 3.131540798
        
        if parameters['Beam'] is 'Standard':                
                parameters['intensity']		= 32.5E11
                parameters['epsn_x']		= 1.88E-6
                parameters['epsn_y']		= 1.88E-6
                if parameters['Year'] is '2021':
                        parameters['bunch_length']	= 135E-9
                        parameters['blength']		= 135E-9
                        parameters['dpp_rms']		= 1.1E-03
                        parameters['rf_voltage']	= 0.04954 # SC adjusted 0.04225 # 42.25 kV
                elif parameters['Year'] is '2022':
                        parameters['bunch_length']	= 170E-9
                        parameters['blength']		= 170E-9
                        parameters['dpp_rms']		= 1.3E-03
                        parameters['rf_voltage']	= 0.04505 # SC adjusted 0.0426 # 42.6 kV
                elif parameters['Year'] is '2023':
                        parameters['bunch_length']	= 205E-9
                        parameters['blength']		= 205E-9
                        parameters['dpp_rms']		= 1.5E-03
                        parameters['rf_voltage']	= 0.04379 # SC adjusted 0.0418 # 41.8 kV

        elif parameters['Beam'] is 'BCMS':
		parameters['intensity']		= 16.25E+11
		parameters['epsn_x']		= 1.43E-6
		parameters['epsn_y']		= 1.43E-6
		parameters['blength']		= 135e-9
		parameters['bunch_length']	= 135e-9
		parameters['dpp_rms']		= 1.1E-03
		parameters['rf_voltage']	= 0.03819 # SC adjusted 0.03655 # 36.55 kV

# Run2 parameters: 1.4GeV
elif parameters['Run'] is 'Run2':
	parameters['gamma'] 	= 2.49038064
	if parameters['Beam'] is 'Standard':
		parameters['intensity']			= 16.84E+11
		parameters['epsn_x']			= 2.25E-6
		parameters['epsn_y']			= 2.25E-6
		parameters['blength']			= 180e-9
		parameters['bunch_length']		= 180e-9
		parameters['dpp_rms']			= 0.9E-03
		parameters['rf_voltage']		= 0.02746 # SC adjusted 0.0251 # 25.1 kV
	elif parameters['Beam'] is 'BCMS':
		parameters['intensity']			= 8.05E+11
		parameters['epsn_x']			= 1.2E-6
		parameters['epsn_y']			= 1.2E-6
		parameters['blength']			= 150e-9
		parameters['bunch_length']		= 150e-9
		parameters['dpp_rms']			= 0.8E-03
		parameters['rf_voltage']		= 0.02273 # SC adjusted 0.0212 # 21.2 kV
                
                

parameters['rf_voltage']        = 0.0418

parameters['beta'] 		= np.sqrt(parameters['gamma']**2-1)/parameters['gamma']
parameters['LongitudinalJohoParameter'] = 1.2
parameters['LongitudinalCut'] 	= 2.4
parameters['TransverseCut']	= 5
parameters['circumference']	= 2*np.pi*100
parameters['phi_s']		= 0
parameters['macrosize']		= parameters['intensity']/float(parameters['n_macroparticles'])

c 				= 299792458
parameters['sig_z'] 	= (parameters['beta'] * c * parameters['blength'])/4.

parameters['turns_max'] = int(2.2E3)
tu1 = range(-1, parameters['turns_max'], 100)
tu2 = range(50, 100, 10) 
tu3 = range(1, 50)
tu = tu2 + tu1 + tu3 
tu.append(874) # WS 172s
tu.append(2185)# WS 175s

parameters['turns_print'] = sorted(tu)
parameters['turns_update'] = sorted(tu)

# switches
########################################################################  
switches = {
        'Space_Charge': True
	'CreateDistn':	True,
	'Update_Twiss':	False,
	'GridSizeX':    128,
	'GridSizeY':    128,
	'GridSizeZ':    64
}

# PTC RF Table Parameters
########################################################################  
harmonic_factors = [1] # this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
time = np.array([0,1,2])
ones = np.ones_like(time)
if parameters['Machine'] is 'PreLIU':
	Ekin_GeV = 1.4*ones
elif parameters['Machine'] is 'LIU':
	Ekin_GeV = 2.0*ones
RF_voltage_MV = np.array([parameters['rf_voltage']*ones]).T # in MV
RF_phase = np.array([np.pi*ones]).T

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
