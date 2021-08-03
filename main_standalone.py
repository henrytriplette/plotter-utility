import configparser
import argparse
import os
from datetime import datetime

import send2serial

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main(file, port, baudrate = '9600', device = '7475a'):

    if not port:
        print('Avaliable Serial Ports: \n')
        send2serial.listComPorts()
    else:
        if file:
            if os.path.exists(file):
                send2serial.sendToPlotter(str(file), str(port), int(baudrate), str(device) )
            else:
                print('Please select a valid .hpgl file')
        else:
            print('Please select a valid file')

if __name__ == '__main__':

    # Initialize
    parser = argparse.ArgumentParser(description='Remote printing service for Pen Plotter.')
    parser.add_argument('-f', '--file', help='HPGL Input file')
    parser.add_argument('-p', '--port', help='COM Plotter Port')
    parser.add_argument('-b', '--baudrate', help='Baudrate', default='9600')
    parser.add_argument('-d', '--device', help='Selected printing device', default='7475a', choices=['7475a', 'mp4200'])

    args = parser.parse_args()

    try:
        main(args.file, args.port, args.baudrate, args.device)
    except KeyboardInterrupt:
        print('Ended!')
