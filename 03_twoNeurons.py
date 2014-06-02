import nest
import numpy as np
import os
import sys
import pylab as pl
#import simulation_parameters
#import utils

nest.ResetKernel()
dt = 1.
w_ss_nrn = 7.0

neurons = nest.Create('iaf_cond_exp',2)
populationPoisson = nest.Create('poisson_generator',2)

nest.SetStatus([populationPoisson[0]], {'rate' : 4500.0})
nest.SetStatus([populationPoisson[1]], {'rate' : 4500.0})

nest.SetStatus([neurons[0]], {'V_reset': -70.0},{'t_ref': 500.0})
#print nest.GetDefaults('iaf_cond_exp')

nest.Connect([populationPoisson[0]], [neurons[0]], params={'weight': w_ss_nrn})
nest.Connect([populationPoisson[1]], [neurons[1]], params={'weight': w_ss_nrn})

#nest.Connect([neurons[0]],[neurons[1]], model = 'stdp_synapse')

voltmeter = nest.Create('multimeter', params={'record_from': ['V_m']})
nest.SetStatus(voltmeter,{"withtime": True})
nest.DivergentConnect(voltmeter, [neurons[0]])

voltmeter2 = nest.Create('multimeter', params={'record_from': ['V_m']})
nest.SetStatus(voltmeter2,{"withtime": True})
nest.DivergentConnect(voltmeter2, [neurons[1]])

spike_recorder = nest.Create('spike_detector')
nest.ConvergentConnect(neurons, spike_recorder)


nest.Simulate(1000.0)

data = nest.GetStatus(voltmeter)
data2 = nest.GetStatus(voltmeter2)

pl.subplot(211)
pl.plot(data[0]['events']['times'], data[0]['events']['V_m'])
pl.subplot(212)
pl.plot(data2[0]['events']['times'], data2[0]['events']['V_m'])
pl.show()

