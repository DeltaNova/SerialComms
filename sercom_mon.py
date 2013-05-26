#!/usr/bin/env python
# sercom_mon.py - Serial Monitor Script
import serial
ser = serial.Serial('/dev/ttyUSB0',9600)

def main():
    while True:
        while(ser.inWaiting() > 0):
            print(ser.readline().rstrip())

if __name__ == "__main__":
    # Someone is launching this directly
    main()
