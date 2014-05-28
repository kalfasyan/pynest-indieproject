import numpy as np
import simulation_parameters
import os
import subprocess
import time


def prepare_simulation(ps, params):
    folder_name = params['folder_name']
    ps.set_filenames(folder_name)
    ps.create_folders()
    param_fn = ps.params['params_fn_json']
#    print 'Writing parameters to: %s' % param_fn
    print 'Debug.prepare_simulation folder written to file', ps.params['data_folder']
    print 'Ready for simulation:\n\t%s' % (param_fn)
    ps.write_parameters_to_file(fn=param_fn)
#    time.sleep(1.)


def run_simulation(script_name, folder, USE_MPI):
    # specify your run command (mpirun -np X, python, ...)
#    parameter_filename = params['params_fn_json']

    if USE_MPI:
        reply = subprocess.check_output(['grep', 'processor', '/proc/cpuinfo'])
        n_proc = reply.count('processor')
        print 'reply', n_proc
        run_command = 'mpirun -np %d python %s %s ' % (n_proc, script_name, folder)
    else:
        run_command = 'python %s %s ' % (script_name, folder)

    # TODO: change this to something more elegant in order to catch crashes
    print 'Running:\n\t%s' % (run_command)
    os.system(run_command)




if __name__ == '__main__':

    try:
        from mpi4py import MPI
        USE_MPI = True
        comm = MPI.COMM_WORLD
        pc_id, n_proc = comm.rank, comm.size
        print "USE_MPI:", USE_MPI, 'pc_id, n_proc:', pc_id, n_proc
    except:
        USE_MPI = False
        pc_id, n_proc, comm = 0, 1, None
        print "MPI not used"

    USE_MPI = False
    # set the name of your 'main script' that is to be run repeatedly
    script_name = '02_simulation_parameters.py'
    ps = simulation_parameters.global_parameters()
#    param_range_1 = [5., 10., 16.666, 20., 25.]
    param_range_1 = [5., 10.]
    param_name_1 = 'g_L'

    main_folder = 'ParameterSweepTest/' 
    if not os.path.exists(main_folder):
        os.system('mkdir %s' % main_folder)

    for i_, p1 in enumerate(param_range_1):
        params = ps.params
        params[param_name_1] = p1 
        folder_name = main_folder + 'Test_%s_%.2e/' % (param_name_1, p1)
        params['folder_name'] = folder_name
        print 'debug folder naem', folder_name
        prepare_simulation(ps, params)
        if comm != None:
            comm.barrier()

        run_simulation(script_name, folder_name, USE_MPI)
        if comm != None:
            comm.barrier()



