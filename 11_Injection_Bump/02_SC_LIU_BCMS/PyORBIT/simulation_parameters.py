import numpy as np

parameters = {}

parameters['Machine']			= 'LIU' #'PreLIU' 
parameters['Beam']			= 'BCMS'#'Standard'

parameters['tunex']			= '621'
parameters['tuney']			= '624'

parameters['lattice_start'] 		= 'BWSH65'
parameters['n_macroparticles']		= int(5E5)

# PS Injection 1.4 GeV
if parameters['Machine'] is 'PreLIU':
	parameters['gamma'] 	                = 2.49038064
	if parameters['Beam'] is 'Standard':
		parameters['intensity']		= 16.84E+11
		parameters['epsn_x']		= 2.25E-6
		parameters['epsn_y']		= 2.25E-6
		parameters['bunch_length']	= 180e-9
		parameters['blength']		= 180e-9
		parameters['dpp_rms']		= 0.9E-03
		parameters['rf_voltage']	= 0.0251 # 25.1 kV
	elif parameters['Beam'] is 'BCMS':
		parameters['intensity']		= 8.05E+11
		parameters['epsn_x']		= 1.2E-6
		parameters['epsn_y']		= 1.2E-6
		parameters['bunch_length']	= 150e-9
		parameters['blength']		= 150e-9
		parameters['dpp_rms']		= 0.8E-03
		parameters['rf_voltage']	= 0.0212 # 21.2 kV
# PS Injection 2 GeV
elif parameters['Machine'] is 'LIU':
	parameters['gamma'] 	                = 3.131540798
	if parameters['Beam'] is 'Standard':
		parameters['intensity']		= 32.5E+11
		parameters['epsn_x']		= 1.8E-6
		parameters['epsn_y']		= 1.8E-6
		parameters['bunch_length']	= 205e-9
		parameters['blength']		= 205e-9
		parameters['dpp_rms']		= 1.5E-03
		parameters['rf_voltage']	= 0.0418 # 41.8 kV
	elif parameters['Beam'] is 'BCMS':
		parameters['intensity']		= 16.25E+11
		parameters['epsn_x']		= 1.43E-6
		parameters['epsn_y']		= 1.43E-6
		parameters['bunch_length']	= 135e-9
		parameters['blength']		= 135e-9
		parameters['dpp_rms']		= 1.1E-03
		parameters['rf_voltage']	= 0.03655 # 36.55 kV

c 					= 299792458
parameters['circumference']		= 2*np.pi*100
parameters['beta'] 		        = np.sqrt(parameters['gamma']**2-1)/parameters['gamma']
parameters['TransverseCut']		= 5
parameters['macrosize']			= parameters['intensity']/float(parameters['n_macroparticles'])
parameters['tomo_file']			='Tomo_Files/PyORBIT_Tomo_file_'+parameters['Beam']+'_'+parameters['Machine']+'.mat'
parameters['sig_z'] 	                = (parameters['beta'] * c * parameters['blength'])/4.

# Only used with parabolic distn
#parameters['LongitudinalJohoParameter']= 1.2   
#parameters['LongitudinalCut'] 	        = 2.4
#parameters['phi_s']			= 0

parameters['turns_max'] = int(2200)
tu1                     = range(-1, parameters['turns_max'], 50)
tu2                     = range(50, 100, 10) 
tu3                     = range(1, 50)
tu                      = tu2 + tu1 + tu3 

parameters['turns_print']  = sorted(tu)
parameters['turns_update'] = sorted(tu)

switches = {
	'CreateDistn':	True,
	'Update_Twiss':	True,
	'Space_Charge': True,
	'GridSizeX':    128,
	'GridSizeY':    128,
	'GridSizeZ':    64
}

# PTC RF Table Parameters
harmonic_factors        = [1] # this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
time                    = np.array([0,1,2])
ones                    = np.ones_like(time)
if parameters['Machine'] is 'PreLIU':
	Ekin_GeV        = 1.4*ones
elif parameters['Machine'] is 'LIU':
	Ekin_GeV        = 2.0*ones
RF_voltage_MV           = np.array([parameters['rf_voltage']*ones]).T # in MV
RF_phase                = np.array([np.pi*ones]).T

RFparameters = {
	'harmonic_factors':     harmonic_factors,
	'time':                 time,
	'Ekin_GeV':             Ekin_GeV,
	'voltage_MV':           RF_voltage_MV,
	'phase':                RF_phase
}
