"""Main ArduimoLink object
"""
import serial.tools.list_ports
from serial import Serial
import time


class ArduinoLink(object):

    """Summary
    
    Attributes:
        baudrate (TYPE): Description
        link (TYPE): Description
        port (TYPE): Description
        timeout (TYPE): Description
    """
    
    def __init__(self, baudrate=9600, port=None, timeout=1):
        """Summary
        
        Args:
            baudrate (int, optional): Description
            port (None, optional): Description
            timeout (int, optional): Description
        """
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.link = Serial()

    def handshake(self, ser_conn):
        """Summary
        
        Args:
            ser_conn (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        print('Trying Handshake')
        # We try 3 times, the first byte might restart the aruduino
        for _ in range(3):
            ser_conn.write(b'Q')
            time.sleep(.5)
            response = ser_conn.readline()
            if response == b'R':
                print(f'Handshake succesfull on {ser_conn.port}')
                return True
        else:
            return False


    def test_ports(self):
        """Summary
        """
        # go over available ports and try a handshake on them,
        # if succesfull we open the connection
        ports = self.list_ports()
        for port in ports:
            try:
                print(port)
                ard = Serial(port, self.baudrate, timeout=self.timeout)
                if self.handshake(ard):
                    self.link.port = port
                    self.link.baudrate = self.baudrate
                    self.link.timeout = self.timeout
                    self.open()
                    print(f'Open connection on {port}')
            except Exception as e:
                print(e)

    def open(self):
        """Summary
        """
        if not self.link.is_open:
            self.link.open()

    def write(self, message, verbose=False):
        """Summary
        
        Args:
            message (TYPE): Description
            verbose (bool, optional): Description
        """
        self.open()
        if isinstance(message, bytes):
            pass
        else:
            message = chr(message).encode()
        self.link.write(message)
        if verbose:
            print(f'wrote {message} to {self.link.port}')

    def readline(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        # Read bytes from the connection untill a \n is reached
        self.open()
        return self.link.readline()

    def read(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        # Read the first available byte from the connection
        self.open()
        return self.link.read()

    def list_ports(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        # we build a list of all available ports on this machine
        comports = serial.tools.list_ports.comports()
        ports = [port.device for port in comports if port.device]
        # ports = check_output(['ls /dev/cu.*'],
        #                          shell=True,
        #                          universal_newlines=True).splitlines()
        return ports



