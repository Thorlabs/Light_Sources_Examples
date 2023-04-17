import time
import serial

def send_command(port, command):
    response = b''
    port.write(command)
    start_time = round(time.time() * 1000)
    end_time = round(time.time() * 1000)

    while not response.__contains__(b'\r'):
        response += port.read_all()
        time.sleep(.1)
        end_time = round(time.time() * 1000)
        if end_time - start_time > 2000:
            response = b'timeout'
            break
    return response;

def main():
    com = serial.Serial(port = 'COM3',
                        baudrate = 115200, 
                        bytesize=8, 
                        parity=serial.PARITY_NONE, 
                        stopbits=1, xonxoff=False, 
                        rtscts=0, 
                        timeout=1
    )

    com.flushInput()
    com.flushOutput()

    print('Return from the ID Command: ')
    print(send_command(com, b'SYS:MODEL?\n'))

    com.close()

main()