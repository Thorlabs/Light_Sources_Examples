"""
CHROLIS_Example.py
=================
This examples shows basic use of the CHROIS light source in python using Ctypes to call the Thorlabs dll
"""
import time
import os
import sys
from ctypes import *


def main():
    """
    main():
    ------
    Performs all actions of the CHROLIS
    :return: None
    """

    if sys.version_info < (3, 8):
        os.chdir("C:\\Program Files\\IVI Foundation\\VISA\\Win64\\Bin")
    else:
        os.add_dll_directory("C:\\Program Files\\IVI Foundation\\VISA\\Win64\\Bin")

    lib: CDLL = cdll.LoadLibrary("TL6WL_64.dll")

    num_devices = c_uint()
    lib.TL6WL_findRsrc(None, byref(num_devices))
    
    if num_devices.value == 0:
        print("No devices connected. Closing...")
        return None

    #loop through and print out info for all found devices
    print("Found instruments: ", num_devices.value)

    manufacturer = create_string_buffer(1024)
    resource_name = create_string_buffer(1024)
    model_name = create_string_buffer(1024)
    serial_number = create_string_buffer(1024)

    k = 0
    for k in range(0, num_devices.value):
        print("Device index: ", k)
        lib.TL6WL_getRsrcName(None, c_uint32(k), resource_name)
        available = c_int16() 
        lib.TL6WL_getRsrcInfo(None, c_uint32(k), model_name, serial_number, manufacturer, byref(available))
        print("Model name: ", model_name.value.decode('utf_8'))
        print("Serial number: ", serial_number.value.decode('utf_8'))
        print("Resource Name: ", resource_name.value.decode('utf_8'))
        if(available.value):
            break

    if(k >= num_devices.value):
        print("No eligable instruments available. Close other programs that might have corrupted a device.")
        return
    
    #get the resource name for the first device and connect
    print("Connecting to the first available device.")
    lib.TL6WL_getRsrcName(None, c_uint32(0), resource_name)

    instr_handle = c_long() #handle to the connected device
    err = lib.TL6WL_init(resource_name, c_bool(False), c_bool(False), byref(instr_handle))
    if err != 0:
        print("Could not connect to device. closing...")
        return None
    
    # lists to store the states of the led's
    #brightness values are 0-1000 for percentage of max brightness.
    power_states_list = [c_bool(False), c_bool(True), c_bool(False), c_bool(False), c_bool(False), c_bool(False)]
    brightness_list = [c_ushort(0), c_ushort(500), c_ushort(0), c_ushort(0), c_ushort(0), c_ushort(0)]

    #Only enable after enter is pressed
    input("press enter to enable light source")

    # use the lists to set the led states
    lib.TL6WL_setLED_HeadPowerStates(instr_handle, power_states_list[0], power_states_list[1], power_states_list[2], 
                                    power_states_list[3], power_states_list[4], power_states_list[5])
    lib.TL6WL_setLED_HeadBrightness(instr_handle, brightness_list[0], brightness_list[1], brightness_list[2], 
                                    brightness_list[3], brightness_list[4], brightness_list[5])
    
    input("press enter to disable light source")
    #disable all led's
    lib.TL6WL_setLED_HeadPowerStates(instr_handle, c_bool(False), c_bool(False), c_bool(False), 
                                    c_bool(False), c_bool(False), c_bool(False))

    #close the device
    lib.TL6WL_close(instr_handle)
    print("Device closed...")
    return None


if __name__ == "__main__":
    main()