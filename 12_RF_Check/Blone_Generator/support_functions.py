import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib import animation, rc


def plotPhaseSpace(distribution, figname=None,
                   xbins=50, ybins=50,
                   alpha=0.2, markersize=1,
                   marker='.',
                   xlim=None, ylim=None,
                   xunits='ns', yunits='MeV'):

    plt.figure(figname, figsize=(8,8))
    plt.clf()
    # Definitions for placing the axes
    left, width = 0.115, 0.63
    bottom, height = 0.115, 0.63
    bottom_h = left_h = left+width+0.03

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    rect_txtBox= [left_h, bottom_h, 0.2, 0.2]

    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    axScatter = plt.axes(rect_scatter)

#     global txtBox
#     txtBox = plt.axes(rect_txtBox)
#     txtBox.axes.get_xaxis().set_ticklabels([])
#     txtBox.axes.get_yaxis().set_ticklabels([])
    
    hist_phase = np.histogram(distribution[0], xbins, range=xlim)
    global line_phase
    line_phase, = axHistx.plot(hist_phase[1][0:-1]+(hist_phase[1][1]-hist_phase[1][0])/2, hist_phase[0]/np.max(hist_phase[0]))    
    axHistx.axes.get_xaxis().set_ticklabels([])      
    axHistx.axes.get_yaxis().set_ticklabels([])  
    axHistx.set_ylabel('Bunch profile $\\lambda_{\\tau}$')
        
    hist_energy = np.histogram(distribution[1], ybins, range=ylim)
    global line_energy
    line_energy, = axHisty.plot(hist_energy[0]/np.max(hist_energy[0]), hist_energy[1][0:-1]+(hist_energy[1][1]-hist_energy[1][0])/2)    
    axHisty.axes.get_xaxis().set_ticklabels([])  
    axHisty.axes.get_yaxis().set_ticklabels([])  
    axHisty.set_xlabel('Energy spread $\\lambda_{\\Delta E}$')
    
    global distri_plot
    distri_plot, = axScatter.plot(*distribution, marker, alpha=alpha,
                                 markersize=markersize)
    axScatter.set_xlabel('Time $\\tau$ [%s]'%(xunits))
    axScatter.set_ylabel('Energy $\\Delta E$ [%s]'%(yunits))
    plt.xlim(xlim)
    plt.ylim(ylim)


