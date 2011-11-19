#!/usr/bin/env python

import pypm

num_of_devices = pypm.CountDevices()

def dev_info():
    """
    Parse devices
    """

    for i in range(num_of_devices):
        print(pypm.GetDeviceInfo(i))

if __name__ == "__main__":
    dev_info()
