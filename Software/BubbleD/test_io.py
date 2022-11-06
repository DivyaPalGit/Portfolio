"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Feb 2022
"""

from pyfirmata import Arduino, util, INPUT
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port",
                    default='/dev/ttyACM0',
                    help="Port connected to the external controller"
                    )

parser.add_argument("-di", "--digitalin", type=int, choices=range(2, 13),
                    default=2,
                    help="Digital input pin to test"
                    )

parser.add_argument("-do", "--digitalout", type=int, choices=range(2, 13),
                    default=10,
                    help="Digital output pin to test"
                    )

parser.add_argument("-ai", "--analogin", type=int, choices=range(1, 5),
                    default=1,
                    help="Analog input pin to test"
                    )

args = parser.parse_args()

print('Connecting microcontroller')
board = Arduino(args.port)
print('Microcontroller connected')

button = board.digital[args.digitalin]
button.mode = INPUT
poti = board.analog[args.analogin]
poti.enable_reporting()
board.digital[args.digitalout].write(1)   # Starting LED
print(f'LED at pin {args.digitalout} stopped.')

it = util.Iterator(board)
it.start()
time.sleep(1)

for counter in range(0, 10):
    print(f'Button {args.digitalin} value:', button.read(),
          f', Potentiometer {args.analogin} value:', poti.read())

board.digital[args.digitalout].write(0)  # Stopping led
print(f'LED at pin {args.digitalout} stopped.')

board.exit()
print('Microcontroller exited')
