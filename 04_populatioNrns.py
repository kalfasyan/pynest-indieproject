import nest
import numpy as np
import os
import pylab as pl
#import simulation_parameters
#import utils

nest.ResetKernel()
dt = 1.
w_ss_nrn = 5.0
nrns =  9

neurons = nest.Create('iaf_cond_exp',nrns)
#populationPoisson = nest.Create('poisson_generator',2)

#nest.SetStatus([populationPoisson[0]], {'rate' : 5000.0})
#nest.SetStatus([populationPoisson[1]], {'rate' : 5000.0})
nest.SetStatus([neurons[0]], {'I_e': 555.0})
nest.SetStatus([neurons[nrns/2]], {'I_e': 10.})
print nest.GetDefaults('iaf_cond_exp')
#nest.Connect([populationPoisson[0]], [neurons[0]], params={'weight': 1*w_ss_nrn})
#nest.Connect([populationPoisson[1]], [neurons[1]], params={'weight': -1*w_ss_nrn})


#print nest.GetDefaults('stdp_synapse')
nest.CopyModel('stdp_synapse', 'excitatory', {'weight': 100*w_ss_nrn, 
                                              'delay': 1.})
nest.CopyModel('stdp_synapse', 'inhibitory', {'weight': 10*w_ss_nrn, 
                                              'delay': 1.})

#nest.help('Connect')
for i in range(nrns):
	if i != (nrns)-1 and i < (nrns/2):
		nest.Connect([neurons[i]],[neurons[i+1]], model = 'excitatory')
	elif i!= (nrns)-1:
		nest.Connect([neurons[i]],[neurons[i+1]], model = 'inhibitory')

#nest.Connect([neurons[nrns/2]],[neurons[nrns/2+1]], model = 'inhibitory')
#nest.help('stdp_synapse')
#nest.help('iaf_cond_exp')

voltmeter = nest.Create('multimeter', 3, params={'record_from': ['V_m']})
nest.SetStatus(voltmeter,{"withtime": True})
nest.Connect(voltmeter, [neurons[0]])

voltmeter2 = nest.Create('multimeter', params={'record_from': ['V_m']})
nest.SetStatus(voltmeter2,{"withtime": True})
nest.Connect(voltmeter2, [neurons[nrns/2]])

voltmeter3 = nest.Create('multimeter', params={'record_from': ['V_m']})
nest.SetStatus(voltmeter2,{"withtime": True})
nest.Connect(voltmeter3, [neurons[nrns/2+1]])

spike_recorder = nest.Create('spike_detector')
nest.ConvergentConnect(neurons, spike_recorder)

nest.Simulate(1000.0)

data = nest.GetStatus(voltmeter)
data2 = nest.GetStatus(voltmeter2)
data3 = nest.GetStatus(voltmeter3)

pl.subplot(311)
pl.plot(data[0]['events']['times'], data[0]['events']['V_m'])
pl.subplot(312)
pl.plot(data2[0]['events']['times'], data2[0]['events']['V_m'])
pl.subplot(313)
pl.plot(data3[0]['events']['times'], data3[0]['events']['V_m'])
pl.show()
