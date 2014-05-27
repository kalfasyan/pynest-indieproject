import nest
import numpy as np
import os
import sys
import simulation_parameters
import utils

class Simulation(object):
    def __init__(self, params):
        self.params = params

    def setup(self):
        # S E T U P 
        nest.SetKernelStatus({'data_path': self.params['spiketimes_folder'], 'overwrite_files': True, 'resolution' : self.params['dt'] })

    def create_cells(self):
        # C R E A T E  
        self.nrns = nest.Create('iaf_cond_exp', self.params['n_nrns']) # iaf_cond_exp is the name of the neuron model
        self.spike_source = nest.Create('spike_generator', self.params['n_nrns']) # this is the container for input signals

    def create_input_spiketrains(self):
        # D E F I N E    I N P U T 
        self.spike_trains = [None for i_ in xrange(self.params['n_nrns'])]
        for i_ in xrange(self.params['n_nrns']):
            self.spike_trains[i_] = np.linspace(10, self.params['t_sim'], (i_ + 1), endpoint=False)
            self.spike_trains[i_] = np.round(self.spike_trains[i_], decimals=1) # required because of limited simulation time step resolution
            print 'Input spikes to cell %d:' % (i_), self.spike_trains[i_]
            nest.SetStatus([self.spike_source[i_]], {'spike_times' : self.spike_trains[i_]})

    def record(self):

        # R E C O R D    S P I K E S
        spike_recorder = nest.Create('spike_detector', params={'to_file':True, 'label': self.params['exc_spikes_fn']})
        nest.Connect(self.spike_source, self.nrns, params={'weight': 1.})

        # R E C O R D    V O L T A G E S
        voltmeter = nest.Create('multimeter', params={'record_from': ['V_m'], 'interval': self.params['dt_volt']})
        nest.SetStatus(voltmeter, [{"to_file": True, "withtime": True, 'label' : self.params['exc_volt_fn']}])
        nest.DivergentConnect(voltmeter, self.nrns)


    def run(self):
        # R U N 
        nest.Simulate(self.params['t_sim'])


if __name__ == '__main__':

        
    if len(sys.argv) == 2:
        params = utils.load_params(os.path.abspath(sys.argv[1]))
        # load existing parameters
    else:
        GP = simulation_parameters.global_parameters()
        params = GP.params
        GP.write_parameters_to_file() # write_parameters_to_file MUST be called before every simulation

    sim = Simulation(params) 
    sim.setup()
    sim.create_cells()
    sim.create_input_spiketrains()
    sim.record()
    sim.run()

