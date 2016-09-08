from bot_core import joint_state_t, robot_state_t
import lcm
import numpy as np


def read_log(path, jlist, channel):
    # store boolean mask of target joint names
    joint_mask = []
    joint_names = []

    # matrix containing joint position values of target joints and time stamps
    data = []

    log = lcm.EventLog(path)
    for event in log:

        if event.channel == channel:
            # decode message based on channel
            if channel == "CORE_ROBOT_STATE":
                msg = joint_state_t.decode(event.data)
            if channel == "EST_ROBOT_STATE":
                msg = robot_state_t.decode(event.data)

            sample = []

            # find target joints indices once
            if not joint_mask:
                for n in msg.joint_name:
                    joint_mask.append(n in jlist)
                #print "mask", joint_mask
                #print "joints", np.asarray(msg.joint_name)[np.where(joint_mask)[0]]
                joint_names = np.asarray(msg.joint_name)[np.where(joint_mask)[0]]

            # store values from current message
            sample.append([msg.utime / 1000000.0])
            sample.append(np.asarray(msg.joint_position)[np.where(joint_mask)[0]].tolist())
            sample = [item for sublist in sample for item in sublist]

            # add sample
            data.append(sample)

    return np.asarray(data), joint_names