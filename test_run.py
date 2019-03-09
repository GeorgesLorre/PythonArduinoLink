from main import ArduinoLink
import time

delay=0.2

if __name__ == '__main__':
    a = ArduinoLink()
    a.test_ports()
    while True:
        a.write(b'R')
        time.sleep(2)
        for y in [b'P', b'S']:
            a.write(y)
            time.sleep(delay)
