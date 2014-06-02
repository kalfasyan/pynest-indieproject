import os, sys, inspect
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import nest
import numpy as np

# some parameter
n_nrns = 3      # number of neurons
dt = 0.1        # simulation time step
t_sim = 300.    # simulation time in [ms]
w_ss_nrn= 700.    # weight for spike source --> neuron
# naming convention: w_[SOURCE]_[TARGET]


# set file names
spike_fn_base = 'spike_output'  # the base of the name to which spikes will be stored (nest always adds some magic stuff)
output_folder = '/home/yannis/Desktop/OutputData/'
if not os.path.exists(output_folder):
    os.system('mkdir %s' % output_folder)
volt_fn_base = 'volt_'


# S E T U P 
nest.SetKernelStatus({'data_path': output_folder, 'overwrite_files': True, 'resolution' : dt })


# C R E A T E  
nrns = nest.Create('iaf_cond_exp', n_nrns) # iaf_cond_exp is the name of the neuron model
spike_source = nest.Create('spike_generator', n_nrns) # this is the container for input signals

print 'NEST params:', nest.GetStatus(nrns)

# D E F I N E    I N P U T 
spike_trains = [None for i_ in xrange(n_nrns)]
for i_ in xrange(n_nrns):
    spike_trains[i_] = np.linspace(10, t_sim, (i_ + 1), endpoint=False)
    spike_trains[i_] = np.round(spike_trains[i_], decimals=1)
    print 'Input spikes to cell %d:' % (i_), spike_trains[i_]
    nest.SetStatus([spike_source[i_]], {'spike_times' : spike_trains[i_]})

nest.Connect(spike_source, nrns, params={'weight': w_ss_nrn})

# R E C O R D    S P I K E S
spike_recorder = nest.Create('spike_detector', params={'to_file':True, 'label': spike_fn_base})
nest.ConvergentConnect(nrns, spike_recorder)


# R E C O R D    V O L T A G E S
voltmeter = nest.Create('multimeter', params={'record_from': ['V_m'], 'interval': dt})
nest.SetStatus(voltmeter, [{"to_file": True, "withtime": True, 'label' : volt_fn_base}])
nest.DivergentConnect(voltmeter, nrns)


# R U N 
nest.Simulate(t_sim)
