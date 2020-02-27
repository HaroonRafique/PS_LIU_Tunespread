# Script to read multiple PTC twiss files and plot the closed orbit
# Expects a PTC twiss created with the following command:
# select, flag=ptc_twiss, column=name, s, betx, px, bety, py, disp3, disp3p, disp1, disp1p, x, y;
# 26.08.19 Haroon Rafique CERN BE-ABP-HSI 

import matplotlib
matplotlib.use('Agg')   # suppress opening of plots
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import numpy as np
import os
import scipy.io as sio

plt.rcParams['figure.figsize'] = [5.0, 4.5]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 14

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 8

plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.markersize'] = 5

ptc_extensions = ('.dat')		# All outputs are .ptc files
ptc_iterators = []				# Integers (turn) used to iterate over files

BSW40 = 471.002875
BSW42 = 484.409245
BSW43 = 490.47663
BSW44 = 497.016615

# Search from current directory
print '\nFind PTC Twiss files\n'
for subdir, dirs, files in os.walk('All_Twiss'):
	# Iterate over all files
    for file in files:
		# Find files with required extension
		ext = os.path.splitext(file)[-1].lower()
		if ext in ptc_extensions:
			# Print full file path
			print (os.path.join(subdir, file))		# full path to file
			fileno1 = (file.split('_')[3])
			fileno = int(fileno1.split('.')[0])	# use turn number as a key
			ptc_iterators.append(fileno)

ptc_data = dict()

# iterate over files (turns)
print '\nRead s, x ptc_data from files\n'
ptc_last_s = 0

for turn in sorted(ptc_iterators):
	s = []
	x = []

	# Open file
	infile = 'All_Twiss/PTC_Twiss_turn_' + str(turn) + '.dat'
	fin = open(infile,'r').readlines()[1:]

	# Save s, x
	for l in fin:
		if ptc_last_s == float(l.split()[0]):
			pass
		else:
			ptc_last_s =float(l.split()[0])
			s.append(float(l.split()[0]))
			x.append(float(l.split()[9])*1E3)

	# Add to dictionary as dict[turn] = (s, x)
	ptc_data[turn] = [s, x]
	ptc_last_s = 0

# Access turn 0, s column
# ptc_data[0][0]
# Access turn 25, x column, first value
# ~ print ptc_data[25][1][0]

print 'length of ptc_data = ', len(ptc_data[0][0])
print 'max x ptc_data = ', max(ptc_data[0][1])
print 'min x of ptc_data = ', min(ptc_data[0][1])


#-----------------------------------------------------------------------
#------------------------------PLOTTING---------------------------------
#-----------------------------------------------------------------------

case = '02_SbS_PreLIU_BCMS'

print '\n\tStart Plotting\n'

fig, ax1 = plt.subplots();
plt.title("PTC-PyORBIT Injection Closure Closed Orbit");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(ptc_iterators)))

# ~ ax1.set_xlim(470.0, 510.0)
ax1.set_ylim(-40, 30)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [mm]");

c_it = int(0)
for turn in sorted(ptc_iterators):
	print 'Plotting PTC turn ', turn
	plt.plot(ptc_data[turn][0], ptc_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

custom_lines = [Line2D([0], [0], color=colors[0], lw=2),
                Line2D([0], [0], color=colors[-1], lw=2)]

ax1.legend(custom_lines, ['Initial Turn', 'Final Turn'])

ax1.grid(lw=0.5, ls=':');

savename = 'PTC-PyORBIT_Closed_Orbit' + case + '.png'
plt.tight_layout()
plt.savefig(savename, dpi = 300);

print '\n\tPlot 1 done\n'

fig, ax1 = plt.subplots();
plt.title("PTC-PyORBIT Injection Closure Closed Orbit");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(ptc_iterators)))

ax1.set_xlim(470.0, 500.0)
ax1.set_ylim(-40, 30)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [mm]");

c_it = int(0)
for turn in sorted(ptc_iterators):
	print 'Plotting PTC turn ', turn
	plt.plot(ptc_data[turn][0], ptc_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

ax1.vlines(BSW40, -40, 0, colors='k', linestyles='solid', label='', lw=0.5, linestyle='--')
ax1.text(BSW40, -35, 'BSW40', rotation=90, verticalalignment='center', fontsize='small')

ax1.vlines(BSW42, -40, 0, colors='k', linestyles='solid', label='', lw=0.5, linestyle='--')
ax1.text(BSW42, -35, 'BSW42', rotation=90, verticalalignment='center', fontsize='small')

ax1.vlines(BSW43, 0, 30, colors='k', linestyles='solid', label='', lw=0.5, linestyle='--')
ax1.text(BSW43, 25, 'BSW43', rotation=90, verticalalignment='center', fontsize='small')

ax1.vlines(BSW44, -40, 0, colors='k', linestyles='solid', label='', lw=0.5, linestyle='--')
ax1.text(BSW44, -35, 'BSW44', rotation=90, verticalalignment='center', fontsize='small')

custom_lines = [Line2D([0], [0], color=colors[0], lw=2),
                Line2D([0], [0], color=colors[-1], lw=2)]

ax1.legend(custom_lines, ['Initial Turn', 'Final Turn'])

ax1.grid(lw=0.5, ls=':');

savename = 'PTC-PyORBIT_Closed_Orbit' + case + '_zoom.png'
plt.tight_layout()
plt.savefig(savename, dpi = 300);

print '\n\tPlot done\n'

