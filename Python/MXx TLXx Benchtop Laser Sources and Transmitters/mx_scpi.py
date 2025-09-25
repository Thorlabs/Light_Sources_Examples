"""
Exposes interface to control Thorlabs MX instruments
Some of the commands are listed below - see the Remote Control User Guide for a full list of available SCPI commands

"""


import SLABHIDtoUART_drv as instr


class mx_usb(instr.HidUartDevice):
    """Class to provide control of MX instrument via usb"""

    def __init__(self, vid, pid, baudrate=115200, timeout=1, **kwargs):
        """Initialize parent class and local vars"""

        # Initialize parent class
        self.hu = instr.HidUartDevice.__init__(self)

    # Set commands are answered with a simply accept = '1' or an Error code - see the Remote Control User Guide for information.           
    def set_(self, command):
        success = self.query(command)
        if not success:
            raise WriteFailedError(f"Error. Write failed. Sent {command}, received {success}")
        success = success.strip('\r')
        return success

    # All responses will be returned as a string 
    # It is the responsibility of the calling program to convert from a string to the expected type
    def get(self, command, **kwargs):
        output = self.query(command, **kwargs)
        if len(output) == 0:
            raise ReadFailedError(f"Error. Read failed. Sent {command}.")            
        output = output.strip('\r') # strip the included \r from the received message
        return output

    def restart(self):
        """Restart the instrument"""
        self.query("SYS:RESTART")
    
    def sys_wake(self):
        self.query("SYS:WAKE")

    def sys_sleep(self):
        self.query("SYS:SLEEP")

#region SystemCommand
    def get_sys_boot_ver(self):
        command = f"SYS:BOOT{'?'}\n"
        output = self.get(command).strip()
        return output

    def get_sys_app_ver(self):
        command = f"SYS:FIRM{'?'}\n"
        output = self.get(command).strip()
        return output

    def get_sys_hw(self):
        command = f"SYS:HARD{'?'}\n"
        output = self.get(command).strip()
        return output

    def get_sys_model(self):
        command = f"SYS:MODEL{'?'}\n"
        output = self.get(command).strip()
        return output

    def get_sys_product(self):
        command = f"SYS:PRODUCT{'?'}\n"
        output = self.get(command).strip()
        return output

    def get_sys_sn(self):
        command = f"SYS:SER{'?'}\n"
        output = self.get(command).strip()
        return output
    
    def get_sys_wavelength(self):
        command = f"SYS:WAVE{'?'}\n"
        output = self.get(command).strip()
        return output
#endregion

    # Get the Laser Power On= 1 or Off = 0
    def get_laser_power(self):
        command = f"LAS:POW{'?'}\n"
        output = self.get(command).strip()
        return output


    def get_rgb_mode(self):
        command = f"RGB:POW{'?'}\n"
        output = self.get(command).strip()
        return output

    def set_rgb_mode(self, val):
        command = f"RGB:POW: {val}\n"
        success = self.set_(command)
        return success

    def get_rgb_red(self):
        command = f"RGB:RED{'?'}\n"
        output = self.get(command).strip()
        return output

    def set_rgb_red(self,val):
        command = f"RGB:RED: {val}\n"
        success = self.set_(command)
        return success

    def get_rgb_green(self):
        command = f"RGB:GREEN{'?'}\n"
        output = self.get(command).strip()
        return output

    def set_rgb_green(self,val):
        command = f"RGB:GREEN: {val}\n"
        success = self.set_(command)
        return success

    def get_rgb_blue(self):
        command = f"RGB:BLUE{'?'}\n"
        output = self.get(command).strip()
        return output

    def set_rgb_blue(self,val):
        command = f"RGB:BLUE: {val}\n"
        success = self.set_(command)
        return success

    def get_rgb_white(self):
        command = f"RGB:WHITE{'?'}\n"
        output = self.get(command).strip()
        return output

    def set_rgb_white(self,val):
        command = f"RGB:WHITE: {val}\n"
        success = self.set_(command)
        return success

        
class WriteFailedError(Exception):
    pass

class ReadFailedError(Exception):
    pass
