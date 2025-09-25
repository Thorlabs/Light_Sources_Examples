## Copyright (c) 2013-2015 by Silicon Laboratories Inc.
## All rights reserved. This program and the accompanying materials
## are made available under the terms of the Silicon Laboratories End User
## License Agreement which accompanies this distribution, and is available at
## http://developer.silabs.com/legal/version/v10/License_Agreement_v10.htm
## Original content and implementation provided by Silicon Laboratories.

## Edited for use with MX/TLX instruments - Thorlabs

"""
Python wrapper for Silabs CP211x library (SLABHIDtoUART.dll).

Documentation for the library is provided by HID_to_UART_API_Specification.doc.
"""

import sys

import ctypes as ct

__all__ = ['HID_UART', 'HID_UART_STATUS_DESC',
    'HidUartDevice', 'HidUartError', 'IsOpened', 
    'GetNumDevices', 'GetAttributes', 'GetString', 
    'GetLibraryVersion', 'GetHidLibraryVersion']

#==============================================================================
# Constants
#==============================================================================

class HID_UART:
    VID = 0x10C4
    PID = 0xEA80

    VID_STR = 0x01
    PID_STR = 0x02
    PATH_STR = 0x03
    SERIAL_STR = 0x04
    MANUFACTURER_STR = 0x05
    PRODUCT_STR = 0x06

    FIVE_DATA_BITS = 0x00
    SIX_DATA_BITS = 0x01
    SEVEN_DATA_BITS = 0x02
    EIGHT_DATA_BITS = 0x03
    NO_PARITY = 0x00
    ODD_PARITY = 0x01
    EVEN_PARITY = 0x02
    MARK_PARITY = 0x03
    SPACE_PARITY = 0x04
    SHORT_STOP_BIT = 0x00
    LONG_STOP_BIT = 0x01
    NO_FLOW_CONTROL = 0x00
    RTS_CTS_FLOW_CONTROL = 0x01


#==============================================================================
# Error Handling
#==============================================================================

HID_UART_STATUS_DESC = {
    0x00 : "HID_UART_SUCCESS",
    0x01 : "HID_UART_DEVICE_NOT_FOUND",
    0x02 : "HID_UART_INVALID_HANDLE",
    0x03 : "HID_UART_INVALID_DEVICE_OBJECT",
    0x04 : "HID_UART_INVALID_PARAMETER",
    0x05 : "HID_UART_INVALID_REQUEST_LENGTH",
    0x10 : "HID_UART_READ_ERROR",
    0x11 : "HID_UART_WRITE_ERROR",
    0x12 : "HID_UART_READ_TIMED_OUT",
    0x13 : "HID_UART_WRITE_TIMED_OUT",
    0x14 : "HID_UART_DEVICE_IO_FAILED",
    0x15 : "HID_UART_DEVICE_ACCESS_ERROR",
    0x16 : "HID_UART_DEVICE_NOT_SUPPORTED",
    0xFF : "HID_UART_UNKNOWN_ERROR",
}

#-------------------------------------------------------------------------------
# Constant definitions copied from the public DLL header
HID_UART_SUCCESS         = 0x00
HID_UART_DEVICE_NOT_FOUND = 0x01
HID_UART_READ_TIMED_OUT  = 0x12
HID_UART_WRITE_TIMED_OUT = 0x13

HID_UART_SHORT_STOP_BIT = 0
HID_UART_LONG_STOP_BIT  = 1
HID_UART_NO_PARITY    = 0
HID_UART_ODD_PARITY   = 1
HID_UART_EVEN_PARITY  = 2
HID_UART_MARK_PARITY  = 3
HID_UART_SPACE_PARITY = 4
HID_UART_NO_FLOW_CONTROL      = 0
HID_UART_RTS_CTS_FLOW_CONTROL = 1
HID_UART_FIVE_DATA_BITS    = 0
HID_UART_SIX_DATA_BITS	   = 1
HID_UART_SEVEN_DATA_BITS   = 2
HID_UART_EIGHT_DATA_BITS   = 3

class HidUartError(Exception):
    def __init__(self, status):
        self.status = status
        try:
            self.name = HID_UART_STATUS_DESC[status]
        except:
            self.name = "HID_UART_STATUS_UNKNOWN: " + hex(status)
    def __str__(self):
        return self.name

def hiduart_errcheck(result, func, args):
    if result != HID_UART_SUCCESS:
        raise HidUartError(result)


#==============================================================================
# CP211x HIDtoUART DLL
#==============================================================================

if sys.platform == 'win32':
    if sys.maxsize > 2**32:
        print("Running on a 64 bit platform")
        _DLL = ct.windll.LoadLibrary("x64/SLABHIDtoUART.dll")
    else:
        print("Running on a 32 bit platform")
        _DLL = ct.windll.LoadLibrary("x86/SLABHIDtoUART.dll")
else:
    print(f"Not running on a windows platform. sys.platform: {sys.platform}")
    exit(0)

# for win_function in ["HidUart_GetHidGuid", 
    # "HidUart_GetIndexedString", "HidUart_GetOpenedIndexedString"]:
    # fnc = getattr(_DLL, win_function)
    # fnc.restype = ct.c_int
    # fnc.errcheck = hiduart_errcheck

for hiduart_function in ["HidUart_GetNumDevices", 
    "HidUart_GetAttributes", "HidUart_GetString", 
    "HidUart_GetLibraryVersion", "HidUart_GetHidLibraryVersion",
    "HidUart_Open", "HidUart_Close", 
    "HidUart_IsOpened", "HidUart_GetPartNumber", 
    "HidUart_GetOpenedAttributes", "HidUart_GetOpenedString",
    "HidUart_SetUartEnable", "HidUart_GetUartEnable", 
    "HidUart_FlushBuffers", "HidUart_CancelIo",
    "HidUart_SetTimeouts", "HidUart_GetTimeouts", 
    "HidUart_SetUartConfig", "HidUart_GetUartConfig", 
    "HidUart_GetUartStatus", "HidUart_Reset", 
    "HidUart_StartBreak", "HidUart_StopBreak", 
    "HidUart_ReadLatch", "HidUart_WriteLatch"]:
    fnc = getattr(_DLL, hiduart_function)
    fnc.restype = ct.c_int
    fnc.errcheck = hiduart_errcheck

# Don't want hiduart_errcheck for these functions
getattr(_DLL, "HidUart_Read").restype = ct.c_int
getattr(_DLL, "HidUart_Write").restype = ct.c_int

#==============================================================================
# Library Functions
#==============================================================================
# Methods Not Implemented
#  HidUart_GetIndexedString(DWORD deviceNum, WORD vid, WORD pid, DWORD stringIndex, char* deviceString);
#  HidUart_GetHidGuid(void* guid);

# HidUart_GetNumDevices(DWORD* numDevices, WORD vid, WORD pid);
def GetNumDevices(vid=HID_UART.VID, pid=HID_UART.PID):
    """Returns the number of devices connected to the host with matching VID/PID."""
    ndev = ct.c_ulong()
    _DLL.HidUart_GetNumDevices(ct.byref(ndev), vid, pid)
    return ndev.value

# HidUart_GetAttributes(DWORD deviceNum, WORD vid, WORD pid, WORD* deviceVid, WORD* devicePid, WORD* deviceReleaseNumber);
def GetAttributes(index=0, vid=HID_UART.VID, pid=HID_UART.PID):
    """Returns VID, PID and release number for the indexed device with matching VID/PID."""
    dev_vid = ct.c_ushort()
    dev_pid = ct.c_ushort()
    dev_rel = ct.c_ushort()
    _DLL.HidUart_GetAttributes(index, vid, pid, ct.byref(dev_vid), ct.byref(dev_pid), ct.byref(dev_rel))
    return (dev_vid.value, dev_pid.value, dev_rel.value)

# HidUart_GetString(DWORD deviceNum, WORD vid, WORD pid, char* deviceString, DWORD options);
def GetString(index=0, vid=HID_UART.VID, pid=HID_UART.PID, opt=HID_UART.SERIAL_STR):
    """Returns the selected string for the indexed device with matching VID/PID."""
    buf = ct.create_string_buffer(512)
    _DLL.HidUart_GetString(index, vid, pid, buf, opt)
    return buf.value.decode()

# HidUart_GetLibraryVersion(BYTE* major, BYTE* minor, BOOL* release);
def GetLibraryVersion():
    """Returns the SLABHIDtoUART library version number as a string."""
    major = ct.c_byte()
    minor = ct.c_byte()
    release = ct.c_long()
    _DLL.HidUart_GetLibraryVersion(ct.byref(major), ct.byref(minor), ct.byref(release))
    return "{}.{}.{}".format(major.value, minor.value, release.value)

# HidUart_GetHidLibraryVersion(BYTE* major, BYTE* minor, BOOL* release);
def GetHidLibraryVersion():
    """Returns the SLABHIDDevice library version number as a string."""
    major = ct.c_byte()
    minor = ct.c_byte()
    release = ct.c_long()
    _DLL.HidUart_GetHidLibraryVersion(ct.byref(major), ct.byref(minor), ct.byref(release))
    return "{}.{}.{}".format(major.value, minor.value, release.value)

def IsOpened(index=0, vid=HID_UART.VID, pid=HID_UART.PID):
    """Checks if the indexed device with matching VID/PID is already open."""
    status = 0
    try:
        GetAttributes(index, vid, pid)
    except HidUartError as e:
        status = e.status
    # 0x15 : "HID_UART_DEVICE_ACCESS_ERROR"
    return bool(status == 0x15)


#==============================================================================
# HidUart Class
#==============================================================================
# Methods Not Implemented:
#  HidUart_GetOpenedIndexedString(HID_UART_DEVICE device, DWORD stringIndex, char* deviceString);
#
#  Device customization functions:
#  HidUart_SetLock(HID_UART_DEVICE device, WORD lock);
#  HidUart_GetLock(HID_UART_DEVICE device, WORD* lock);
#  HidUart_SetUsbConfig(HID_UART_DEVICE device, WORD vid, WORD pid, BYTE power, BYTE powerMode, WORD releaseVersion, BYTE flushBuffers, BYTE mask);
#  HidUart_GetUsbConfig(HID_UART_DEVICE device, WORD* vid, WORD* pid, BYTE* power, BYTE* powerMode, WORD* releaseVersion, BYTE* flushBuffers);
#  HidUart_SetManufacturingString(HID_UART_DEVICE device, char* manufacturingString, BYTE strlen);
#  HidUart_GetManufacturingString(HID_UART_DEVICE device, char* manufacturingString, BYTE* strlen);
#  HidUart_SetProductString(HID_UART_DEVICE device, char* productString, BYTE strlen);
#  HidUart_GetProductString(HID_UART_DEVICE device, char* productString, BYTE* strlen);
#  HidUart_SetSerialString(HID_UART_DEVICE device, char* serialString, BYTE strlen);
#  HidUart_GetSerialString(HID_UART_DEVICE device, char* serialString, BYTE* strlen);

class HidUartDevice(object):
    """
    HidUartDevice instances are used to work with a specific CP211x device.

    For help on the wrapped functions, refer to HID_to_UART_API_Specification.doc.
    """

    def __init__(self):
        self.handle = ct.c_void_p(0)

    # HidUart_Open(HID_UART_DEVICE* device, DWORD deviceNum, WORD vid, WORD pid);
    def Open(self, DevIndex, vid=HID_UART.VID, pid=HID_UART.PID):
        GetNumDevices(vid, pid)
        _DLL.HidUart_Open(ct.byref(self.handle), DevIndex, vid, pid)

    # HidUart_Close(HID_UART_DEVICE device);
    def Close(self):
        if self.handle.value:
            _DLL.HidUart_Close(self.handle)
            self.handle.value = 0

    # HidUart_IsOpened(HID_UART_DEVICE device, BOOL* opened);
    def IsOpened(self):
        opened = ct.c_long(0)
        if self.handle:
            _DLL.HidUart_IsOpened(self.handle, ct.byref(opened))
        return bool(opened.value)

    # HidUart_GetOpenedAttributes(HID_UART_DEVICE device, WORD* deviceVid, WORD* devicePid, WORD* deviceReleaseNumber);
    def GetAttributes(self):
        vid = ct.c_ushort(0)
        pid = ct.c_ushort(0)
        rel = ct.c_ushort(0)
        _DLL.HidUart_GetOpenedAttributes(self.handle, ct.byref(vid), ct.byref(pid), ct.byref(rel))
        return (vid.value, pid.value, rel.value)

    # HidUart_GetPartNumber(HID_UART_DEVICE device, BYTE* partNumber, BYTE* version);
    def GetPartNumber(self):
        pno = ct.c_byte(0)
        ver = ct.c_byte(0)
        _DLL.HidUart_GetPartNumber(self.handle, ct.byref(pno), ct.byref(ver))
        return (pno.value, ver.value)

    # HidUart_GetOpenedString(HID_UART_DEVICE device, char* deviceString, DWORD options);
    def GetString(self, opt=HID_UART.SERIAL_STR):
        buf = ct.create_string_buffer(512)
        _DLL.HidUart_GetOpenedString(self.handle, buf, opt)
        return buf.value.decode()

    # HidUart_SetUartEnable(HID_UART_DEVICE device, BOOL enable);
    def SetUartEnable(self, enable=True):
        _DLL.HidUart_SetUartEnable(self.handle, enable)

    # HidUart_GetUartEnable(HID_UART_DEVICE device, BOOL* enable);
    def GetUartEnable(self):
        enable = ct.c_long(0)
        _DLL.HidUart_GetUartEnable(self.handle, ct.byref(enable))
        return bool(enable.value)

    # HidUart_FlushBuffers(HID_UART_DEVICE device, BOOL flushTransmit, BOOL flushReceive);
    def FlushBuffers(self, flushTransmit=True, flushReceive=True):
        _DLL.HidUart_FlushBuffers(self.handle, flushTransmit, flushReceive)

    # HidUart_CancelIo(HID_UART_DEVICE device);
    def CancelIo(self):
        _DLL.HidUart_CancelIo(self.handle)

    # HidUart_Read(HID_UART_DEVICE device, BYTE* buffer, DWORD numBytesToRead, DWORD* numBytesRead);
    def Read(self, size=256):
        buf = ct.create_string_buffer(size)
        cnt = ct.c_ulong(0)
        status = _DLL.HidUart_Read(self.handle, buf, size, ct.byref(cnt))
        if status == HID_UART_SUCCESS or status == HID_UART_READ_TIMED_OUT:
            return buf.value
        else:
            raise

    def ReadString(self, size=256):
        return self.Read(size).decode('ascii', 'ignore')

    # HidUart_Write(HID_UART_DEVICE device, BYTE* buffer, DWORD numBytesToWrite, DWORD* numBytesWritten);
    def Write(self, buffer):
        cnt = ct.c_ulong(0)
        status = _DLL.HidUart_Write(self.handle, buffer, len(buffer), ct.byref(cnt))
        if status == HID_UART_SUCCESS or status == HID_UART_WRITE_TIMED_OUT:
            return cnt.value
        else:
            raise

    def WriteString(self, string):
        return self.Write(string.encode('ascii', 'ignore'))

    # HidUart_SetTimeouts(HID_UART_DEVICE device, DWORD readTimeout, DWORD writeTimeout);
    def SetTimeouts(self, rto=1000, wto=1000):
        _DLL.HidUart_SetTimeouts(self.handle, rto, wto)

    # HidUart_GetTimeouts(HID_UART_DEVICE device, DWORD* readTimeout, DWORD* writeTimeout);
    def GetTimeouts(self):
        rto = ct.c_ulong(0)
        wto = ct.c_ulong(0)
        _DLL.HidUart_GetTimeouts(self.handle, ct.byref(rto), ct.byref(wto))
        return (rto.value, wto.value)

    # HidUart_GetUartStatus(HID_UART_DEVICE device, WORD* transmitFifoSize, WORD* receiveFifoSize, BYTE* errorStatus, BYTE* lineBreakStatus);
    def GetUartStatus(self):
        tx_fifo = ct.c_ushort(0)
        rx_fifo = ct.c_ushort(0)
        err_stat = ct.c_byte(0)
        lbr_stat = ct.c_byte(0)
        _DLL.HidUart_GetUartStatus(self.handle, ct.byref(tx_fifo), ct.byref(rx_fifo), ct.byref(err_stat), ct.byref(lbr_stat))
        return (tx_fifo.value, rx_fifo.value, err_stat.value, lbr_stat.value)

    # HidUart_SetUartConfig(HID_UART_DEVICE device, DWORD baudRate, BYTE dataBits, BYTE parity, BYTE stopBits, BYTE flowControl);
    def SetUartConfig(self, baud=115200, data=HID_UART.EIGHT_DATA_BITS,
            parity=HID_UART.NO_PARITY, stop=HID_UART.SHORT_STOP_BIT, flow=HID_UART.NO_FLOW_CONTROL):
        _DLL.HidUart_SetUartConfig(self.handle, baud, data, parity, stop, flow)

    # HidUart_GetUartConfig(HID_UART_DEVICE device, DWORD* baudRate, BYTE* dataBits, BYTE* parity, BYTE* stopBits, BYTE* flowControl);
    def GetUartConfig(self):
        baud = ct.c_ulong()
        data = ct.c_ulong()
        parity = ct.c_ulong()
        stop = ct.c_ulong()
        flow = ct.c_ulong()
        _DLL.HidUart_GetUartConfig(self.handle, ct.byref(baud),
            ct.byref(data), ct.byref(parity), ct.byref(stop), ct.byref(flow))
        return (baud.value, data.value, parity.value, stop.value, flow.value)

    # HidUart_StartBreak(HID_UART_DEVICE device, BYTE duration);
    def StartBreak(self, duration=0):
        _DLL.HidUart_StartBreak(self.handle, duration)

    # HidUart_StopBreak(HID_UART_DEVICE device);
    def StopBreak(self):
        _DLL.HidUart_StopBreak(self.handle)

    # HidUart_Reset(HID_UART_DEVICE device);
    def Reset(self):
        _DLL.HidUart_Reset(self.handle)
        _DLL.HidUart_Close(self.handle)
        self.handle.value = 0

    #----------------------------------------------------------
    def Connect( self, DevIndex, vid=HID_UART.VID, pid=HID_UART.PID):
        self.Open( DevIndex, vid, pid)
        if self.IsOpened() is True:
            print("COM is Opened")
 
            self.SetComConfig(115200)
            self.SetComTimeout( 1000)
            self.Purge()
            return True
        else:
            print("COM is NOT Opened")
            return False


    def Purge(self):
        _DLL.HidUart_FlushBuffers(self.handle, True, True)

    def Disconnect( self):
        self.Close()

    def SetComTimeout(self, timeout):
        # Add 200 ms to timeout for command overhead
        status = _DLL.HidUart_SetTimeouts(self.handle, timeout + 200, timeout + 200)
        return status

    # SetComConfig(DWORD baud = 115200, BYTE dataBits = 8, BYTE parity = NOPARITY, BYTE stopBits = ONESTOPBIT, BYTE flowControl = COM_NO_FLOW_CONTROL);
    def SetComConfig( self, baud):


        dataBits = HID_UART_EIGHT_DATA_BITS
        stopBits = HID_UART_SHORT_STOP_BIT

        
        parity = HID_UART_NO_PARITY
        flowControl = HID_UART_NO_FLOW_CONTROL

        status = self.SetUartConfig( baud, dataBits, parity, stopBits, flowControl)
        return status

    def query(self, command, suppress_output=True):
        """Send a command to the instrument and read the response"""
        # ReadBuf  = ct.create_string_buffer(100)
        # CbToRead = len( ReadBuf)
        #buf = command.encode()
        self.WriteString(command)
        val = self.ReadString()
        if not suppress_output:
            print(f"WRITE: {command} READ: {val}")
        return val


# def TestInvalDevIndex( NumDevices, vid, pid):
#     rc = 0
#     try:
#         hu = HidUartDevice()
#         hu.Open( NumDevices, vid, pid)
#         rc = -1
#     except HidSmbusError as e:
#         if e.status != HID_UART_DEVICE_NOT_FOUND :
#             print("TestInvalDevIndex: Unexpected error:", e, "-", hex(e.status))
#             rc = -1
#     finally:
#         return rc

# if __name__ == "__main__":
#     import sys
    
#     errorlevel = 1
#     opened = False
#     hu = HidUartDevice()

#     ndx = 0
#     if len(sys.argv) > 1:
#         ndx = int(sys.argv[1])

#     print('')
#     print("SLABHIDtoUART Library:", GetLibraryVersion())
#     print("SLABHIDDevice Library:", GetHidLibraryVersion())
#     print('')

#     # Note: this example will only work with a single Thorlabs device. Theoretically we could open multiple devices and keep track of them
#     # via the values returned by silabs_cp2110.Open().

#     print("Available MX Device:")
#     vid = 0x1313
#     pid_start = 0x5000
#     pid_end = 0x503f
#     for pid in range(pid_start, pid_end):
#         devices_for_pid = GetNumDevices(vid, pid)
#         if devices_for_pid > 0:
#             print(f"Found: VID = {vid:x} PID = {pid:x}")
#             break

#     if devices_for_pid != 1:
#         print( "This example will only work with one Thorlabs MX/TLX/MBX family device (found {} eligible devices).".format( str( devices_for_pid ) ) )
#         exit(0)
   

#     try:
#         NumDevices = GetNumDevices(vid, pid)

#         if TestInvalDevIndex( NumDevices, vid, pid) == 0:
#             if NumDevices :
#                 hu.Open(ndx, vid, pid)
#                 opened = True
#                 print('')
#                 print("    VID:", hu.GetString(HID_UART.VID_STR))
#                 print("    PID:", hu.GetString(HID_UART.PID_STR))
#                 print("Product:", hu.GetString(HID_UART.PRODUCT_STR))
#                 print("Company:", hu.GetString(HID_UART.MANUFACTURER_STR))
#                 print('')

#             errorlevel = 0

#     except HidUartError as e:
#         print("Device Error:", e, "-", hex(e.status))
#     finally:
#         if opened :
#             hu.Close()
#         if errorlevel:
#             print("FAIL\n")
#         else:
#             print("PASS\n")
#         sys.exit(errorlevel)
