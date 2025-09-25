# Example python code that uses ctypes to interface to the dlls for USB operations for the MX/TLX devices
# Simple code to connect to the dll, open a hid to uart connection to the MX/TLX and then exchange scpi messages
# This is meant to be run on a windows x86 or x64 PC. Tested with Python 3.8 and 3.12. It is expected to work on Python version 3.8 and greater. 
# any imported libraries in this example code are part of the standard python library - sys, time, ctypes
# dll files for the USB HID device are included in the separate folders that are part of this project - both the x86 and x64 versions of the dlls are provided.
import sys
import SLABHIDtoUART_drv as hidToUart
import mx_scpi
import time

if __name__ == "__main__":
    
    errorlevel = 1
    opened = False
    hu = hidToUart.HidUartDevice()

    ndx = 0
    if len(sys.argv) > 1:
        ndx = int(sys.argv[1])

    # Get information related to the dlls
    print('')
    print("SLABHIDtoUART Library:", hidToUart.GetLibraryVersion())
    print("SLABHIDDevice Library:", hidToUart.GetHidLibraryVersion())
    print('')

    # Note: this example will only work with a single Thorlabs device. Theoretically we could open multiple devices and keep track of them
    # via the values returned by silabs_cp2110.Open().
    # Thorlabs VID = 0x1313. The range of PIDs for MX/TLX devices is 0x5000 - 0x503f and depends on the model.

    print("Available MX Device:")
    vid = 0x1313
    pid_start = 0x5000
    pid_end = 0x503f
    for pid in range(pid_start, pid_end):
        devices_for_pid = hidToUart.GetNumDevices(vid, pid)
        if devices_for_pid > 0:
            print(f"Found: VID = {vid:x} PID = {pid:x}")
            break

    if devices_for_pid != 1:
        print( "This example will only work with one Thorlabs MX/TLX/MBX family device (found {} eligible devices).".format( str( devices_for_pid ) ) )
        exit(0)

    # Initialize the class for the MX/TLX USB
    mx = mx_scpi.mx_usb(baudrate= 115200, vid=vid, pid=pid)
    # Connect to the USB using the driver
    if mx.Connect(0, vid, pid) is False:
        print("Could not set connection")
        exit(0)


    # Note - all responses will be returned as a string 
    # It is the responsibility of the calling program to convert from a string to the expected type as necessary ex. int, float ...
 
    fw = mx.get_sys_app_ver()
    print(f"Firmware: {fw}")

    hw = mx.get_sys_hw()
    print(f"Hardware: {hw}")

    # get laser power On = 1 or Off = 0
    laser_status = mx.get_laser_power()
    print(f"Laser Power is {laser_status}. On = 1, Off = 0")

    # get RGB LED strip mode 0 = Off, 1 = RGB, 2 = White
    rgb_mode = mx.get_rgb_mode()
    
    if rgb_mode == '0':
        mx.set_rgb_mode(1)
        mx.set_rgb_red(100)
        time.sleep(2)
        mx.set_rgb_red(0)
        time.sleep(2)
        mx.set_rgb_mode(0)
    elif rgb_mode == '1':
        mx.set_rgb_red(100)
        time.sleep(2)
        mx.set_rgb_red(0)
    elif rgb_mode == '2':
        mx.set_rgb_white(100)
        time.sleep(2)
        mx.set_rgb_white(50)
        time.sleep(2)
        mx.set_rgb_white(0)


    mx.Disconnect()