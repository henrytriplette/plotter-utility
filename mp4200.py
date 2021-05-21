#!/usr/bin/env python
import sys
import time
import serial
import serial.tools.list_ports

speed = 2

tty = serial.Serial(port = "COM3", baudrate = 9600, timeout=0.5, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, xonxoff = True)

tty.flush()
tty.write(b'\033.@;0:')  # Plotter Configuration [Manual 10-27]
tty.write(b'\033.Y')  # Plotter On [Manual 10-26]
tty.write(b'\033.K')  # abort graphics
tty.write(b'IN;')  # HPGL initialize
tty.write(b'SP1;')
tty.write(b'PA2000,2000;')
tty.write(b'CI500;')
