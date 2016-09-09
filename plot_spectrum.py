#!/usr/bin/env python
import lcm_extract_joint_position as lcm
import hdf5_extract_joint_position as hdf5
from fft import get_spectrum

import matplotlib.pyplot as plt

import argparse

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

smt_channel = [
    "/left_arm/forearm_sensors/index/pitch_1",
    "/left_arm/forearm_sensors/index/pitch_2",
    "/left_arm/forearm_sensors/index/pitch_3",
    "/left_arm/forearm_sensors/middle/pitch_1",
    "/left_arm/forearm_sensors/middle/pitch_2",
    "/left_arm/forearm_sensors/middle/pitch_3",
    "/left_arm/forearm_sensors/pinky/pitch_1",
    "/left_arm/forearm_sensors/pinky/pitch_2",
    "/left_arm/forearm_sensors/pinky/pitch_3",
    "/left_arm/forearm_sensors/thumb/pitch_1",
    "/left_arm/forearm_sensors/thumb/pitch_2",
    "/left_arm/forearm_sensors/thumb/pitch_3",
    "/left_arm/forearm_sensors/thumb/roll",
]

if __name__ == "__main__":
    # parse and evaluate arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='type', choices=["lcm", "hdf5"], default="lcm",
                        help="type of log message")
    parser.add_argument('-c', dest='channel', default="EST_ROBOT_STATE",
                        choices=["CORE_ROBOT_STATE", "EST_ROBOT_STATE"],
                        help="LCM channel (only used for '-t lcm')")
    parser.add_argument('file', help="path to log file")
    parser.add_argument('-lb', type=float, dest='lb', help="start of time range")
    parser.add_argument('-ub', type=float, dest='ub', help="end of time range")
    args = parser.parse_args()

    file_type = args.type
    logfile_path = args.file

    if file_type=="lcm":
        data, time, joint_names = lcm.read_log(logfile_path, joints, channel=args.channel)

    if file_type=="hdf5":
        data, time = hdf5.read_log(logfile_path, smt_channel)
        joint_names = smt_channel

        print "data shape", data.shape

        if not (args.lb == None and args.ub == None):
            print "cropping data"
            # crop data to given time range
            t = time[:, 0]
            data = data[(args.lb <= t) & (t <= args.ub), :]
            time = time[(args.lb <= t) & (t <= args.ub), :]
            print "data shape", data.shape
            print "time shape", data.shape

    spect = get_spectrum(data, time)

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