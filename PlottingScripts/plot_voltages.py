import pylab
import numpy as np
import utils
import sys

info_text = 'Please give the folder containing the voltage recordings after the script_name'
info_text += '\n USAGE:\n\t python plot_voltages.py [FOLDER_NAME]' 
assert (len(sys.argv) > 1), info_text
folder_name = sys.argv[1]

filenames = utils.find_files(folder_name, 'exc_volt_')
# since you can not decide on the final name your data files will have in NEST (it will depend on the number of processes, for example)
# you need to browse through the folder to retrieve all relevant files to be plotted
print 'Found filenames:', filenames


fig = pylab.figure()
ax = fig.add_subplot(111)

for fn in filenames:
    path = folder_name 
    d = np.loadtxt(fn)
    gids = np.unique(d[:, 0])
    for gid in gids:
        time_axis, volt_trace = utils.extract_trace(d, gid)
        ax.plot(time_axis, volt_trace)


pylab.show()
