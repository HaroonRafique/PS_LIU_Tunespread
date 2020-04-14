import os
import sys
import glob
import imageio
import numpy as np
import scipy.io as sio
import matplotlib.cm as cm
from math import log10, floor
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
from matplotlib.patches import Patch
import matplotlib.gridspec as gridspec
from scipy.stats import moment, kurtosis

main_label = 'LIU Standard 2021'
sc = 'SbS'
legend_label = 'Turn'

case = 'LIU Tunespread'
tune_tit = '(6.21, 6.245)'
tune_sav = '6p21_6p245' 
source_dir =  './bunch_output/'

# Plot parameters
#------------------------------------------------------------------------------

plt.rcParams['figure.figsize'] = [5.0, 4.5]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 14

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 10

plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.markersize'] = 5

# Function and class definitions
#------------------------------------------------------------------------------

class resonance_lines(object):
	
	def __init__(self, Qx_range, Qy_range, orders, periodicity):
		
		if np.std(Qx_range):
			self.Qx_min = np.min(Qx_range)
			self.Qx_max = np.max(Qx_range)
		else:
			self.Qx_min = np.floor(Qx_range)-0.05
			self.Qx_max = np.floor(Qx_range)+1.05
		if np.std(Qy_range):
			self.Qy_min = np.min(Qy_range)
			self.Qy_max = np.max(Qy_range)
		else:
			self.Qy_min = np.floor(Qy_range)-0.05
			self.Qy_max = np.floor(Qy_range)+1.05

		self.periodicity = periodicity
									
		nx, ny = [], []

		for order in np.nditer(np.array(orders)):
			t = np.array(range(-order, order+1))
			nx.extend(order - np.abs(t))
			ny.extend(t)
		nx = np.array(nx)
		ny = np.array(ny)
	
		cextr = np.array([nx*np.floor(self.Qx_min)+ny*np.floor(self.Qy_min), \
						  nx*np.ceil(self.Qx_max)+ny*np.floor(self.Qy_min), \
						  nx*np.floor(self.Qx_min)+ny*np.ceil(self.Qy_max), \
						  nx*np.ceil(self.Qx_max)+ny*np.ceil(self.Qy_max)], dtype='int')
		cmin = np.min(cextr, axis=0)
		cmax = np.max(cextr, axis=0)
		res_sum = [range(cmin[i], cmax[i]+1) for i in xrange(cextr.shape[1])]								
		self.resonance_list = zip(nx, ny, res_sum)
		
	def plot_resonance(self, figure_object = None):	
		plt.ion()
		if figure_object:
			fig = figure_object
			plt.figure(fig.number)
		else:
			fig = plt.figure()
		Qx_min = self.Qx_min
		Qx_max = self.Qx_max
		Qy_min = self.Qy_min
		Qy_max = self.Qy_max 
		plt.xlim(Qx_min, Qx_max)
		plt.ylim(Qy_min, Qy_max)
		plt.xlabel('Qx')
		plt.ylabel('Qy')
		for resonance in self.resonance_list:
			nx = resonance[0]
			ny = resonance[1]
			for res_sum in resonance[2]:
				if ny:
					line, = plt.plot([Qx_min, Qx_max], \
					    [(res_sum-nx*Qx_min)/ny, (res_sum-nx*Qx_max)/ny])
				else:
					line, = plt.plot([np.float(res_sum)/nx, np.float(res_sum)/nx],[Qy_min, Qy_max])
				if ny%2:
					plt.setp(line, linestyle='--') # for skew resonances
				if res_sum%self.periodicity:
					plt.setp(line, color='b')	# non-systematic resonances
				else:
					plt.setp(line, color='r', linewidth=2.0) # systematic resonances
		plt.draw()
		return fig
		
	def print_resonances(self):
		for resonance in self.resonance_list:
			for res_sum in resonance[2]:
				'''
				print str(resonance[0]).rjust(3), 'Qx ', ("+", "-")[resonance[1]<0], \
					  str(abs(resonance[1])).rjust(2), 'Qy = ', str(res_sum).rjust(3), \
					  '\t', ("(non-systematic)", "(systematic)")[res_sum%self.periodicity==0]
				'''
				print '%s %s%s = %s\t%s'%(str(resonance[0]).rjust(2), ("+", "-")[resonance[1]<0], \
						str(abs(resonance[1])).rjust(2), str(res_sum).rjust(4), \
						("(non-systematic)", "(systematic)")[res_sum%self.periodicity==0])

def gaussian(x, A, mu, sig):
    """gaussian_3_parameter(x, A, mu, sig)"""
    return A*np.exp(-(x-mu)**2/(2*sig**2))
    
def add_input_file(dd, filename, label):
	f = filename
	p = dict()
	sio.loadmat(f, mdict=p)
	dd[label] = p
	print '\tAdded output data from ', filename, '\t dictionary key: ', label
	return dd

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

print '\n\tPLOTTING SCRIPT: TUNE FOOTPRINTS FROM PTC-PYORBIT BUNCH OUTPUT FILES: STARTED'

# Find files
#------------------------------------------------------------------------------
plt.close('all')

filename = 'mainbunch'
files = glob.glob(source_dir + filename + '*.mat')
files.sort()

for i, file in enumerate(files):
    if 'mainbunch_-000001.mat' in file:
        files.remove(file)
for i, file in enumerate(files):        
    if '000000' in file:
        files.remove(file)

print '\n\tFount input files for turns: '
for f in files:
    print ' ', f.split('.')[1][-6:]

tune_gifs =[]
    
master_bins = 512
max_1d_hist = 10

min_tune = 5.75
max_tune = 6.25
q_fine = np.arange(5.5, 6.51, 0.01)

first_turn = True

# Loop over files
#------------------------------------------------------------------------------
for i, file in enumerate(files):
    
    folder = file.split('/')[0] + '/' + file.split('/')[1]
    try: 
        turn = int(file.split('mainbunch_')[-1][:-4])
        #turn = '%04d'%turn
    except:
        turn = ''
        
    print '\n\t Plotting ', case, ' scan tune =', tune_tit, ' turn = ', turn, ' with histograms'
    
    # Load data 
    #------------------------------------------------------------------------------
    particles = sio.loadmat(file, squeeze_me=True,  struct_as_record=False)['particles']
    #x  = particles.x
    #xp = particles.xp
    #y  = particles.y
    #yp = particles.yp
    #z  = particles.z
    #dE = particles.dE
    qx = particles.ParticlePhaseAttributes[2,:]
    qy = particles.ParticlePhaseAttributes[3,:]
    qx[np.where(qx>0.5)] -= 1
    qy[np.where((qy>0.6) & (qx<0.25))] -= 1 
     
    my_cmap = plt.cm.jet
    my_cmap.set_under('w',1)

    title = str( main_label + ' ' + tune_tit + ' Turn = ' + str(turn) )    
    
    fig = plt.figure(figsize=(7,7))
    gs = gridspec.GridSpec(nrows=3,ncols=3,figure=fig,width_ratios= [1, 1, 1],height_ratios=[1, 1, 1],wspace=0.0,hspace=0.0)
    r = resonance_lines((min_tune, max_tune),(min_tune, max_tune),(1,2,3,4),10)
 
    # Calculate RMS Qx and Qy
    #------------------------------------------------------------------------------
    Q_x_rms = np.sqrt(moment(6+qx,2))
    Q_y_rms = np.sqrt(moment(6+qy,2))
    Q_x_min = np.min(6+qx)
    Q_x_max = np.max(6+qx)
    Q_y_min = np.min(6+qy)
    Q_y_max = np.max(6+qy)
    Delta_q_x = Q_x_max - Q_x_min
    Delta_q_y = Q_y_max - Q_y_min    
    Delta_q_x_4sig = 4 * Q_x_rms
    Delta_q_y_4sig = 4 * Q_y_rms
    Delta_q_x_6sig = 6 * Q_x_rms
    Delta_q_y_6sig = 6 * Q_y_rms
    
    # TEXT BOX (top right)
    #------------------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[0, 2:3])
    ax4txt = str(
                #'q_x_min = ' + str(round_sig(Q_x_min)) + '\n' +
                #'q_x_max = ' + str(round_sig(Q_x_max)) + '\n' +
                #'q_y_min = ' + str(round_sig(Q_y_min)) + '\n' +
                #' Turn = ' + str(turn) + '\n' +
                '<q_x> = ' + str(round_sig(np.mean(6+qx),3)) + '\n' +
                '<q_y> = ' + str(round_sig(np.mean(6+qy),3)) + '\n' + '\n' +
                'q_x_RMS = ' + str(round_sig(Q_x_rms)) + '\n' +
                'q_y_RMS = ' +str(round_sig(Q_y_rms)) + '\n'  + '\n' +  
                'Dq_x (4*RMS) = ' + str(round_sig(Delta_q_x_4sig)) + '\n' +
                'Dq_y (4*RMS) = ' + str(round_sig(Delta_q_y_4sig)) + '\n' + '\n' +
                'Dq_x (6*RMS) = ' + str(round_sig(Delta_q_x_6sig)) + '\n' +
                'Dq_y (6*RMS) = ' + str(round_sig(Delta_q_y_6sig)) + '\n'
                )
    ax4.text(0.001, 0.001, ax4txt, fontsize=10)
    ax4.set_yticklabels([])
    ax4.set_xticklabels([])
    
    # FIRST SUBPLOT - x histogram
    #------------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0:2])
    ax1.set_title(title)    
    n_x, bins_x, patches_x = ax1.hist(6+qx, bins=master_bins, range=(r.Qx_min, r.Qx_max), density=True) #, norm=mcolors.PowerNorm(gamma))
    bins_x = bins_x[:-1] + (bins_x[1]-bins_x[0])/2 # centre bins

    if first_turn:
        if np.max(n_x) > max_1d_hist :
            max_1d_hist = round(np.max(n_x),2) + 2
            print '\n\t max_1d_hist set to ', max_1d_hist
            first_turn = False
            
    # fit Gaussian to histogram
    try:    
        amp_min_x = 0.99 * np.max(n_x)
        amp_max_x = 1.2 * np.max(n_x)
        mean_min_x = 0.9 * bins_x[np.argmax(n_x)]
        mean_max_x = 1.1 * bins_x[np.argmax(n_x)]
        sig_min_x = 0.5 * Q_x_rms
        sig_max_x = 1.5 * Q_x_rms
        popt, pcov = curve_fit(gaussian, bins_x, n_x, method = 'trf', bounds =((amp_min_x, mean_min_x, sig_min_x), (amp_max_x, mean_max_x, sig_max_x)))
        ax1.plot(q_fine, gaussian(q_fine, popt[0], popt[1], popt[2]), 'k--', lw=1, label='Gaussian Fit')
        ax1.plot(q_fine, gaussian(q_fine, popt[0], popt[1], Q_x_rms), 'r:', lw=1.5, label='Gaussian Fit (Sigma = RMS)')
        ax1.legend(loc=2)
    except RuntimeError:
        print '\n\t RuntimeError ', case, ' scan tune =', tune_tit, ' turn = ', turn, ' q_x Gaussian fit not found'
        
    # ~ ax1.set_ylabel('Frequency')
    ax1.set_ylabel('Density [arb.]')
    ax1.grid(which='both', ls=':', lw=0.5)
    ax1.set_ylim(0, max_1d_hist)
    ax1.set_xlim(min_tune, max_tune)
    
    # SECOND SUBPLOT - y histogram
    #------------------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1:3, 2])
    n_y, bins_y, patches_y = ax3.hist(6+qy, bins=master_bins, range=(r.Qy_min, r.Qy_max), orientation=u'horizontal', density=True) #, norm=mcolors.PowerNorm(gamma))
    bins_y = bins_y[:-1] + (bins_y[1]-bins_y[0])/2 # centre bins

    # fit Gaussian to histogram
    try:
        amp_min_y = 0.99 * np.max(n_y)
        amp_max_y = 1.2 * np.max(n_y)
        mean_min_y = 0.9 * bins_y[np.argmax(n_y)]
        mean_max_y = 1.1 * bins_y[np.argmax(n_y)]
        sig_min_y = 0.5 * Q_y_rms
        sig_max_y = 1.5 * Q_y_rms
        popt, pcov = curve_fit(gaussian, bins_y, n_y, method = 'trf', bounds =((amp_min_y, mean_min_y, sig_min_y), (amp_max_y, mean_max_y, sig_max_y)))
        ax3.plot(gaussian(q_fine, popt[0], popt[1], popt[2]), q_fine, 'k--', lw=1, label='Gaussian Fit')
        ax3.plot(gaussian(q_fine, popt[0], popt[1], Q_y_rms), q_fine, 'r:', lw=1.5, label='Gaussian Fit (Sigma = RMS)')    
    except RuntimeError:
        print '\n\t RuntimeError ', case, ' scan tune =', tune_tit, ' turn = ', turn, ' q_y Gaussian fit not found'
        
    # ~ ax3.set_xlabel('Frequency')    
    ax3.set_xlabel('Density [arb.]')    
    ax3.set_xlim(0, max_1d_hist)
    ax3.set_ylim(min_tune, max_tune)
    ax3.grid(which='both', ls=':', lw=0.5)
    
    # MAIN PLOT: TUNE FOOTPRINT
    #------------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[1:3, 0:2])
    r.plot_resonance(fig)
    ax2.hist2d(6+qx, 6+qy, bins=master_bins, cmap=my_cmap, vmin=1, range=[[r.Qx_min, r.Qx_max], [r.Qy_min, r.Qy_max]]) #, norm=mcolors.PowerNorm(gamma))
    ax2.set_xlabel(r'Q$_x$')
    ax2.set_ylabel(r'Q$_y$')
    ax2.set_ylim(min_tune, max_tune)
    ax2.grid(which='both', ls=':', lw=0.5)
 
    plt.tight_layout()
    savename = str(folder + '/Tune_Footprint_' + case + '_' + tune_sav + '_turn_' + str(turn) + '.png' )
    tune_gifs.append(savename)
    fig.savefig(savename, dpi=500)
    plt.close(fig)

print '\n\tPLOTTING SCRIPT: TUNE FOOTPRINTS FROM PTC-PYORBIT BUNCH OUTPUT FILES: COMPLETE'
