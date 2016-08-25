import numpy as np
from numpy.fft import rfft, rfftfreq

def get_spectrum(data):

    spectrum = []

    print "data shape", data.shape
    t = data[:,0]
    dts = t[1:] - t[0:-1]

    dt = np.median(dts)
    print "median dt", dt

    # downampling
    #dt *= 5

    # evenly spaced time stamps
    dt_interp = np.arange(t[0], t[-1], dt)

    # frequencies
    fs = rfftfreq(len(dt_interp), dt).tolist()

    spectrum.append(fs)

    for i in range(1,data.shape[1]):
        x_interp = np.interp(dt_interp, t, data[:,i])
        x_spect = np.absolute(rfft(x_interp)).tolist()
        spectrum.append(x_spect)

    return np.asarray(spectrum)