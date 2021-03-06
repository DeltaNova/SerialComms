#!/usr/bin/env python
# sercom_send.py - Serial Send Script
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
