import time
import serial

def send_command(port, command):
    response = b''
    port.write(command)
    while not response.__contains__(b'CMD>'):
        response += port.read_all()
        time.sleep(.1)
    return response;

def main():
    com = serial.Serial(port = 'COM3',
                        baudrate = 115200, 
                        bytesize=8, 
                        parity=serial.PARITY_NONE, 
                        stopbits=1, xonxoff=True, 
                        rtscts=0, 
                        timeout=1
    )
    
    com.flushInput()
    com.flushOutput()

    print('Return from the ID Command: ')
    print(send_command(com, b'id\r'))

    print('Return from the Limits Command: ')
    print(send_command(com, b'sh limit\r'))

    print('Setting the pump power to 100mW')
    send_command(com, b'ch 1 pow 100\r')

    if(input('Type "on" to enable the laser\n').__eq__('on')):
        print('Turning the laser on')
        send_command(com, b'la on\r')

    time.sleep(5)

    print('Turning the laser off')
    send_command(com, b'la off\r')

    com.close()

main()



    
