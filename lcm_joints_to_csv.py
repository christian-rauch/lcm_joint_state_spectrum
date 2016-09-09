#!/usr/bin/env python
from lcm_extract_joint_position import *
import sys
import numpy as np

if __name__ == "__main__":
    joints = [
        "leftIndexFingerPitch1", "leftIndexFingerPitch2", "leftIndexFingerPitch3",
        "leftMiddleFingerPitch1", "leftMiddleFingerPitch2", "leftMiddleFingerPitch3",
        "leftPinkyPitch1", "leftPinkyPitch2", "leftPinkyPitch3",
        "leftThumbPitch1", "leftThumbPitch2", "leftThumbPitch3",
        "leftThumbRoll",
    ]

    data, time, jnames = read_log(sys.argv[1], joints, "CORE_ROBOT_STATE")

    merged = np.concatenate((np.atleast_2d(time).T, data), axis=1)

    np.savetxt("finger_joints.csv", merged, header="time_s " + " ".join(jnames), comments='')
