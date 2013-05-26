#!/usr/bin/env python
# sercom_send.py - Serial Send Script
import serial
ser = serial.Serial('/dev/ttyUSB0',9600)

def main():
    while True:
        try:
            x = int(raw_input("Send ASCII Character: "))
            ser.write(chr(x))
        except ValueError, TypeError:
            print("Oops! That was not a valid value. Try again...")

if __name__ == "__main__":
    # Someone is launching this directly
    main()
