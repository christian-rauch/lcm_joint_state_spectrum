import numpy as np
from numpy.fft import rfft, rfftfreq

def get_spectrum(data, time):

    spectrum = []

    # get median sample time
    if time.ndim == 1:
        t = time
        dts = t[1:] - t[0:-1]
    else:
        dts = []
        for r in range(time.shape[1]):
            time_row = time[:,r]
            row_dts = time_row[1:] - time_row[0:-1]
            # print "median dt", np.median(row_dts), "s"
            dts.extend(row_dts)

    dt = np.median(dts)
    print "median dt", dt, "s"

    # downampling
    #dt *= 5

    # evenly spaced time stamps
    dt_interp = np.arange(np.min(time), np.max(time), dt)

    # frequencies
    fs = rfftfreq(len(dt_interp), dt).tolist()

    print "upper frequency:", max(fs), "Hz"

    spectrum.append(fs)

    for i in range(data.shape[1]):
        # print "mean: ", np.mean(data[:, i]) # amplitude of 0 Hz component
        # select common time base or individual time stamps
        if time.ndim == 1:
            x_interp = np.interp(dt_interp, time, data[:, i])
        else:
            x_interp = np.interp(dt_interp, time[:,i], data[:, i])

        # FFT
        # the magnitude of the spectrum is: m = A*(n/2)
        # with 'A' the original amplitude and 'n' the length of the input signal
        x_spect = np.absolute(rfft(x_interp))
        # convert to original amplitude units
        # A = 2 * (x_spect/n) for all frequencies except 0Hz and Nyquist frequency, otherwise A = x_spect/n
        x_spect /= len(x_interp)
        x_spect[1:] *= 2.0

        spectrum.append(x_spect.tolist())

    return np.asarray(spectrum)