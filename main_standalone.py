import configparser
import argparse
import time
import os
from datetime import datetime

import send2serial
import tasmota

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main(file, port, baudrate = '9600', device = '7475a', poweroff = 'off'):

    if not port or port == '?':
        print('Avaliable Serial Ports: \n')
        send2serial.listComPorts()
    else:
        if file:
            if os.path.exists(file):

                # Tasmota - check for on
                if poweroff == 'on':
                    print(tasmota.tasmota_setStatus('on'))
                    time.sleep(5) # Just to be sure, wait 5 seconds

                # Start printing
                send2serial.sendToPlotter(str(file), str(port), int(baudrate), str(device) )

                # Tasmota - turn off plotter
                if poweroff == 'on':
                    print(tasmota.tasmota_setStatus('off'))
                    time.sleep(5) # Just to be sure, wait 5 seconds

            else:
                print('Please select a valid .hpgl file')
        else:
            print('Please select a valid file')

if __name__ == '__main__':

    # Initialize
    parser = argparse.ArgumentParser(description='Remote printing service for Pen Plotter.')
    parser.add_argument('-f', '--file', help='HPGL Input file')
    parser.add_argument('-p', '--port', help='COM Plotter Port, use ? to list available ports')
    parser.add_argument('-b', '--baudrate', help='Plotter Baudrate, default 9600', default='9600')
    parser.add_argument('-t', '--tasmota', help='Enable auto-poweroff when print is finished using tasmota device', default='on', choices=['on', 'off'])
    parser.add_argument('-d', '--device', help='Selected printing device', default='7475a', choices=['7475a', 'mp4200'])

    args = parser.parse_args()

    try:
        main(args.file, args.port, args.baudrate, args.device, args.tasmota)
    except KeyboardInterrupt:
        print('Ended!')
