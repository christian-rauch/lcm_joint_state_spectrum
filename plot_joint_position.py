#!/usr/bin/env python
import lcm_extract_joint_position as lcm
import hdf5_extract_joint_position as hdf5

import matplotlib.pyplot as plt

import sys

side = "left" # "right"
#side = "right" # "left"

joints = [
    side+"IndexFingerPitch1",
    side+"IndexFingerPitch2",
    side+"IndexFingerPitch3",
    side+"MiddleFingerPitch1",
    side+"MiddleFingerPitch2",
    side+"MiddleFingerPitch3",
    side+"PinkyPitch1",
    side+"PinkyPitch2",
    side+"PinkyPitch3",
    side+"ThumbPitch1",
    side+"ThumbPitch2",
    side+"ThumbPitch3",
    side+"ThumbRoll",
]

smt_channel = [
    "/"+side+"_arm/forearm_sensors/index/pitch_1",
    "/"+side+"_arm/forearm_sensors/index/pitch_2",
    "/"+side+"_arm/forearm_sensors/index/pitch_3",
    "/"+side+"_arm/forearm_sensors/middle/pitch_1",
    "/"+side+"_arm/forearm_sensors/middle/pitch_2",
    "/"+side+"_arm/forearm_sensors/middle/pitch_3",
    "/"+side+"_arm/forearm_sensors/pinky/pitch_1",
    "/"+side+"_arm/forearm_sensors/pinky/pitch_2",
    "/"+side+"_arm/forearm_sensors/pinky/pitch_3",
    "/"+side+"_arm/forearm_sensors/thumb/pitch_1",
    "/"+side+"_arm/forearm_sensors/thumb/pitch_2",
    "/"+side+"_arm/forearm_sensors/thumb/pitch_3",
    "/"+side+"_arm/forearm_sensors/thumb/roll",
]

fingers = {"index"  : [0,1,2],
           "middle" : [3,4,5],
           "pinky"  : [6,7,8],
           "thumb"  : [9,10,11,12]}

if __name__ == "__main__":

    lcm_log_path = sys.argv[1]
    hdf5_log_path = sys.argv[2]

    lcm_data, lcm_time, joint_names = lcm.read_log(lcm_log_path, joints, channel="CORE_ROBOT_STATE")

    #print "joints", joint_names
    print "data shape", lcm_data.shape
    print "time shape", lcm_time.shape
    print "time range", min(lcm_time), max(lcm_time), "s"

    min_time = min(lcm_time)
    max_time = max(lcm_time)

    smt_data, smt_time = hdf5.read_log(hdf5_log_path, smt_channel)

    print "data shape", smt_data.shape
    print "time shape", smt_time.shape
    print "time range", min(smt_time[:, 0]), max(smt_time[:, 0]), "s"

    t = smt_time[:, 0]
    smt_data = smt_data[(min_time <= t) & (t <= max_time), :]
    smt_time = smt_time[(min_time <= t) & (t <= max_time), :]

    for f in sorted(fingers.keys()):
        plt.figure(f)
        plt.title(f)
        for fi in fingers[f]:
            finger_name = f+str(fi-fingers[f][0]+1)
            # plot lcm
            plt.plot(lcm_time - lcm_time[0], lcm_data[:, fi], label=finger_name+" lcm")
            # plot smt
            plt.plot(smt_time[:, fi] - smt_time[0, fi], smt_data[:, fi], label=finger_name+" smt")

        plt.xlabel("time (s)")
        plt.ylabel("joint position (rad)")
        plt.legend(ncol = 3, fancybox=True, framealpha=0.5)
        plt.grid()

    plt.show()