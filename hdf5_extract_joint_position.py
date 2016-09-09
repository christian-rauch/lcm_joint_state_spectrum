import h5py
import numpy as np

def read_log(path, jlist):
    log = h5py.File(path, 'r')

    data = []
    time = []

    for j in jlist:
        hdf_data = log[j]
        time.append(hdf_data.value[:,0]) # time
        data.append(hdf_data.value[:,1]) # joint position

    return np.asarray(data).transpose(), np.asarray(time).transpose()