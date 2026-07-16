# Title: ULN_serial.py
# Created Date: 2025-09-22
# Last modified date: 2026-03-23
#
# Notes:
# Example for the ULN lasers using serial commands. Sets TEC mode to auto
# and briefly turns laser on.
#

import serial
import time

PORT = 'COM3'
BAUD = 115200
TIMEOUT = 5

# Send command parse return code E.G 000: OK:response, etc.
def send_cmd(ser, cmd):
    ser.write((cmd + '\r\n').encode())
    raw = ser.readline().decode().strip()

    code, text = raw.split(':', 1)

    if code.strip() == '000':
        print(f'[OK]  {cmd:<20} - {text.strip()}')
    else:
        print(f'[ERR] {cmd:<20} - {code.strip()}: {text.strip()}')

ser = serial.Serial(PORT, BAUD, bytesize=8, parity='N', stopbits=1, timeout=TIMEOUT)

send_cmd(ser, 'nop')
time.sleep(0.5)

send_cmd(ser, 'laser_tec_ctrl_mode auto')
time.sleep(0.5)

send_cmd(ser, 'laser on')
time.sleep(3)

send_cmd(ser, 'laser off')
time.sleep(0.5)

ser.close()
print('Done - port closed.')
