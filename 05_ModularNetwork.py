import nest
import numpy as np
import os
import simulation_parameters_MN as sp

PS = sp.global_parameters()
params = PS.params


# create the minicolumns
mcs = [ None for i in xrange(params['n_mc'])]
for i_mc in xrange(params['n_mc']):
   mcs[i_mc] = nest.Create(params['neuron_type'], params['n_exc_per_mc'])


# create inhibitory neurons for cross inhibition
inh_pops = [ None for i in xrange(params['n_hc'])]
for i_hc in xrange(params['n_hc']):
    inh_pops[i_hc] = nest.Create(params['neuron_type'], params['n_inh_per_hc'])


# connect cells within a minicolumns
n_tgt = int(np.round(params['p_ee_local'] * params['n_exc_per_mc']))
for i_mc in xrange(params['n_mc']):
    nest.RandomConvergentConnect(mcs[i_mc], mcs[i_mc], n_tgt, \
            weight=params['w_ee_local'], delay=params['delay_ee_local'], \
            options={'allow_autapses': False, 'allow_multapses': False})

# check the connectivity
connections = nest.GetConnections()
conn_list = np.zeros((len(connections), 3)) # 3 columns for src, tgt, weight
print 'example connection:', connections[0]
print 'information from nest.GetStatus', nest.GetStatus([connections[0]])

for i_ in xrange(len(connections)):
    info = nest.GetStatus([connections[i_]])
    weight = info[0]['weight']
    conn_list[i_, 0] = connections[i_][0]
    conn_list[i_, 1] = connections[i_][1]
    conn_list[i_, 2] = weight


np.savetxt('debug_connectivity.txt', conn_list)

