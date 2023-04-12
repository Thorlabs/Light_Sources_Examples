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
        os.chdir(os.getcwd())
    else:
        os.add_dll_directory(os.getcwd())

    lib: CDLL = cdll.LoadLibrary("S5FC_COMMAND_LIB_win64.dll")

    #Get the connected devices
    serial_numbers_string = create_string_buffer(1024)
    num_devices = lib.List(serial_numbers_string)
    
    if num_devices == 0:
        print("No devices found. Closing...")   
        return None 
    elif num_devices == -1:
        print("Error with library. Closing...")    
        return None
    
    # Print out the list and ask user for index of device to connect
    device_list = str(serial_numbers_string.value.decode('utf_8')).split(',')
    print("Serial numbers found: ", device_list)

    index = int(input("Please enter index of list to open (Use 0 index)..."))
    #Open the device
    instrument_handle = lib.Open(c_char_p(device_list[index].encode('utf_8')), c_int(115200), c_int(2))

    if instrument_handle == -1:
        print("Error opening device. Closing...")    
        return None
    
    #set the operating temperature
    lib.SetTargetTemperature(instrument_handle, c_double(25.0))

    #set the operating current in mA
    lib.SetCurrent(instrument_handle, c_double(100.0))

    #Only enable after enter is pressed
    input("press enter to enable light source")
    lib.SetEnable(instrument_handle, c_bool(True))

    
    #disable the source
    input("press enter to disable light source")
    lib.SetEnable(instrument_handle, c_bool(False))

    #close the device
    lib.Close(instrument_handle)
    print("Device closed...")
    return None


if __name__ == "__main__":
    main()