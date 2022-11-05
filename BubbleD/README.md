# BubbleD - Bubble chamber Display 

The Bubble chamber Display (BubbleD) is a software made to display and control digitised images of the bubble chamber experiment. The projected image can be controlled using a graphical user interface and/or an external controller. The details of connecting the external controller are in the [controller](controller/README.md) folder and the description of the setup and digitised images of the bubble chamber can be found in sceibo https://uni-bonn.sciebo.de/index.php/apps/files?dir=/212-E/private/experiment-upgrade.


## Dependencies 
BubbleD requires Python 3 (written in Python 3.8) and PyQt5. 
Other dependencies include the python modules and packages:
* argparse
* configparser
* numpy
* pyfirmata

Additional dependencies are needed to connect the software to the external controller (see [controller](controller/README.md)).

## Folder structure
The images to be projected should be stored in the following folder structure and naming scheme:

```
BubbleD
│   README.md
│   ...
└──images
│  └──Film xxxx_yyyy (where xxxx_yyyy are the range of slides numbers)
│     └──Film Type (Default, Original, Transparent with other threshold values, etc.)  
│        └──view_1
│           │    │ xxxx.png
│           │    │ ...  
│           └──view_2
│           └──view_3
│  └──Film aaaa_bbbb

```

## Usage
The software can be used with or without the external controller board. 
1. Ensure the `StandardFrimata.ino` is uploaded to the Teensy 4.1 microcontroller board for operation with the external controller (see [controller](controller/README.md)).    
2. To run the software execute the [main.py](main.py) file in python3. If no argument is provided, by default the software connects to the external controller and imports the port mentioned in the configuration file of table 1. If configuration file path is not provided, a default config_table1.ini is written in the current folder.

```bash
usage: main.py [-h] [-c {True,False}] [-p PORT] [-t {1,2}] [-cfg CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -c {True,False}, --controller {True,False}
                        Start GUI with/without external controller
  -p PORT, --port PORT  Port connected to the external controller
  -t {1,2}, --table {1,2}
                        Choose table to load config file
  -cfg CONFIG, --config CONFIG
                        Insert directory to read/write config_table1.ini or
                        config_table2.ini
```


## Testing external controller
Ensure the `StandardFrimata.ino` is uploaded to the Teensy 4.1 microcontroller board for operation with the external board (see [controller](controller/README.md)). The connections can be then tested using the [test_io.py](test_io.py).

```bash
usage: test_io.py [-h] [-p PORT] [-di {2,3,4,5,6,7,8,9,10,11,12}]
                  [-do {2,3,4,5,6,7,8,9,10,11,12}] [-ai {1,2,3,4}]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port connected to the external controller
  -di {2,3,4,5,6,7,8,9,10,11,12}, --digitalin {2,3,4,5,6,7,8,9,10,11,12}
                        Digital input pin to test
  -do {2,3,4,5,6,7,8,9,10,11,12}, --digitalout {2,3,4,5,6,7,8,9,10,11,12}
                        Digital output pin to test
  -ai {1,2,3,4}, --analogin {1,2,3,4}
                        Analog input pin to test

```
