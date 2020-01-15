import numpy as np

parameters = {}

parameters['Beam']				= 'Standard'
parameters['Machine']			= 'LIU'
# ~ parameters['Year']				= '2021'
# ~ parameters['Year']				= '2022'
parameters['Year']				= '2023'

parameters['tunex']				= '621'
parameters['tuney']				= '624'

parameters['lattice_start'] 	= 'BWSH65'
parameters['n_macroparticles']	= int(5E5)

# LIU parameters: 2GeV
parameters['gamma'] 			= 3.131540798
parameters['intensity']			= 325E10
parameters['epsn_x']		= 1.88E-6
parameters['epsn_y']		= 1.88E-6

if parameters['Year'] is '2021':
	parameters['bunch_length']	= 135E-9
	parameters['blength']		= 135E-9
	parameters['dpp_rms']		= 1.1E-03
	parameters['rf_voltage']	= 0.04225 # 42.25 kV
elif parameters['Year'] is '2022':
	parameters['bunch_length']	= 170E-9
	parameters['blength']		= 170E-9
	parameters['dpp_rms']		= 1.3E-03
	parameters['rf_voltage']	= 0.0426 # 42.6 kV
elif parameters['Year'] is '2023':
	parameters['bunch_length']	= 205E-9
	parameters['blength']		= 205E-9
	parameters['dpp_rms']		= 1.5E-03
	parameters['rf_voltage']	= 0.0418 # 41.8 kV

parameters['beta'] 		= np.sqrt(parameters['gamma']**2-1)/parameters['gamma']
parameters['LongitudinalJohoParameter'] = 1.2
parameters['LongitudinalCut'] 	= 2.4
parameters['TransverseCut']		= 5
parameters['circumference']		= 2*np.pi*100
parameters['phi_s']				= 0
parameters['macrosize']			= parameters['intensity']/float(parameters['n_macroparticles'])
parameters['tomo_file']			='Tomo_Files/PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_'+parameters['Year']+'.mat'

c 						= 299792458
parameters['sig_z'] 	= (parameters['beta'] * c * parameters['blength'])/4.

parameters['turns_max'] = int(5000)
tu1 = range(-1, parameters['turns_max'], 20)
tu2 = range(50, 100, 10) 
tu3 = range(0, 50)
tu = tu2 + tu1 + tu3 

parameters['turns_print'] = sorted(tu)
parameters['turns_update'] = sorted(tu)

switches = {
	'CreateDistn':		True,
	'Update_Twiss':		False,
	'Space_Charge': 	True,
	'GridSizeX': 128,
	'GridSizeY': 128,
	'GridSizeZ': 64
}

# PTC RF Table Parameters
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
