import nest
import numpy as np
import os
import simulation_parameters_MN as sp
import pylab as pl
import nest.raster_plot
PS = sp.global_parameters()
params = PS.params

nest.ResetKernel()

# CREATE MINICOLUMNS WITHIN HYPERCOLUMNS
hcs = [ [] for i in xrange(params['n_hc'])]
mcs = [ None for i in xrange(params['n_mc'])]
for i_hc in xrange(params['n_hc']):
	for i_mc in xrange(params['n_mc_per_hc']):
	    mcs[params['n_mc_per_hc']*i_hc+i_mc] = nest.Create(params['neuron_type'], params['n_exc_per_mc'])
	    hcs[i_hc].append(mcs[params['n_mc_per_hc']*i_hc+i_mc])


# CREATE INHIBITORY NEURONS FOR CROSS INHIBITION
inh_pops = [ None for i in xrange(params['n_hc'])]
for i_hc in xrange(params['n_hc']):
    inh_pops[i_hc] = nest.Create(params['neuron_type'], params['n_inh_per_hc'])

""" AUXILARY STUFF """
# CREATING SPIKE DETECTOR
spikerec = nest.Create('spike_detector', params['n_mc'])
# CREATING POISSON GENERATOR FOR INPUT
poiss = nest.Create('poisson_generator', params['n_mc'],{'rate': 4000.})
"""                """

# CONNECT CELLS WITHIN MINICOLUMNS + 
n_tgt = int(np.round(params['p_ee_local'] * params['n_exc_per_mc']))
for i_mc in xrange(params['n_mc']):
	nest.RandomConvergentConnect(mcs[i_mc], mcs[i_mc], n_tgt, \
			weight=params['w_ee_local'], delay=params['delay_ee_local'], \
			options={'allow_autapses': False, 'allow_multapses': False})
			
			
for i_hc in xrange(params['n_hc']):	
	for i_mc in xrange(params['n_mc_per_hc']):
		# CONNECT INHIBITORY POPULATION WITH MINICOLUMS		
		nest.RandomConvergentConnect(hcs[i_hc][i_mc], inh_pops[i_hc], n_tgt, \
				weight=params['w_ee_local'], delay=params['delay_ee_local'], \
				options={'allow_autapses': False, 'allow_multapses': False})
		nest.RandomConvergentConnect(inh_pops[i_hc],hcs[i_hc][i_mc], 10, weight=-5., delay=params['delay_ee_local'], options={'allow_autapses': False, 'allow_multapses': False}) #10 to trito orisma
		# FINALLY CONNECT MINICOLUMN NEURONS WITH SPIKE RECORDER
		nest.ConvergentConnect(mcs[params['n_mc_per_hc']*i_hc+i_mc], [spikerec[params['n_mc_per_hc']*i_hc+i_mc]])

# CONNECT HYPERCOLUMNS TOGETHER 
nest.RandomConvergentConnect(hcs[0][0], hcs[1][0], n_tgt, \
					weight=params['w_ee_local'], delay=params['delay_ee_local'], \
					options={'allow_autapses': False, 'allow_multapses': False})
nest.RandomConvergentConnect(hcs[0][0], hcs[1][1], n_tgt, \
					weight=params['w_ee_local'], delay=params['delay_ee_local'], \
					options={'allow_autapses': False, 'allow_multapses': False})
nest.RandomConvergentConnect(hcs[0][1], hcs[1][0], n_tgt, \
					weight=params['w_ee_local'], delay=params['delay_ee_local'], \
					options={'allow_autapses': False, 'allow_multapses': False})
nest.RandomConvergentConnect(hcs[0][1], hcs[1][1], n_tgt, \
					weight=params['w_ee_local'], delay=params['delay_ee_local'], \
					options={'allow_autapses': False, 'allow_multapses': False})
										
# CONNECT INPUT TO FIRST HYPERCOLUMN's first minicolumn
nest.DivergentConnect([poiss[0]], hcs[0][0], params['w_ee_local'],params['delay_ee_global'])
nest.DivergentConnect([poiss[0]], hcs[0][1], params['w_ee_local'],params['delay_ee_global'])

# check the connectivity
connections = nest.GetConnections()
conn_list = np.zeros((len(connections), 3)) # 3 columns for src, tgt, weight
"""
print 'example connections:'
for i in connections:
	print i
print 'information from nest.GetStatus', nest.GetStatus([connections[0]])
"""

for i_ in xrange(len(connections)):
    info = nest.GetStatus([connections[i_]])
    weight = info[0]['weight']
    conn_list[i_, 0] = connections[i_][0]
    conn_list[i_, 1] = connections[i_][1]
    conn_list[i_, 2] = weight


np.savetxt('debug_connectivity.txt', conn_list)

nest.Simulate(500.0)

data = nest.GetStatus(spikerec)

kolor=['k','b','y','g','c','m']
for i in xrange(len(spikerec)):
	a,b = data[i]['events']['times'],data[i]['events']['senders']
	pl.subplot(211)
	pl.scatter(a,b,marker='.',color=kolor[i])
#nest.raster_plot.from_device(spikerec, hist=True)
#nest.raster_plot.show()


pl.ylabel('Neuron ID')
pl.title('\"Minicolumn Neurons Spiking\"')


pl.subplot(223)
pl.ylabel('Rate(Hz)')
pl.xlabel('Time')
pl.hist(a,20)

pl.show()


