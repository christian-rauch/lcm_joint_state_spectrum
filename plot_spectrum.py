#!/usr/bin/env python
from lcm_extract_joint_position import *
from fft import get_spectrum

import matplotlib.pyplot as plt

import sys

joints = [
    "leftIndexFingerPitch1",
    "leftIndexFingerPitch2",
    "leftIndexFingerPitch3",
    "leftMiddleFingerPitch1",
    "leftMiddleFingerPitch2",
    "leftMiddleFingerPitch3",
    "leftPinkyPitch1",
    "leftPinkyPitch2",
    "leftPinkyPitch3",
    "leftThumbPitch1",
    "leftThumbPitch2",
    "leftThumbPitch3",
    "leftThumbRoll",
]

if __name__ == "__main__":

    logfile_path = sys.argv[1]

    # data, joint_names = read_log(logfile_path, joints, channel="CORE_ROBOT_STATE")
    data, joint_names = read_log(logfile_path, joints, channel="EST_ROBOT_STATE")

    print "filtered joints", joint_names

    spect = get_spectrum(data)

    print "spect shape", spect.shape

    for i in range(1, spect.shape[0]):
        plt.figure(joint_names[i-1])
        plt.grid()
        # plot spectrum without the offset (0Hz component)
        plt.stem(spect[0,1:], spect[i,1:])
        #plt.stem(spect[0, :], spect[i, :])
        plt.xlabel("frequency (Hz)")
        plt.ylabel("amplitude")
    plt.show()