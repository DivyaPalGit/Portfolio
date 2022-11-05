# BubbleD - Bubble chamber Display 
The Bubble chamber Display (BubbleD) is a software to display and control digitised images of the bubble chamber experiment. For conducting the experiment, multiple images have to be overlapped and projected on a table to be manually analysed by students, mimicking the experimental setup from the 1970s.  

The software opens two windows, one for control and the other for projecting the images in a second display or projector. The control window can be used either for changing the settings of the projection, like the display selection, background, etc. or for movement of the images displayed in the second window.  The projected image can also be controlled using a specialised input device (referred to hereafter as an external controller board) constructed for the experiment. It consists of switches, potentiometers and a joystick connected to a microcontroller board and the functionalities are predefined in the software. The hardware specifics like the pins used in the microcontroller, the display size, etc., can be defined in [configuration](packages/config_table1.py) specific to the table or display to be used for projection. 

![Figure 1: Settings](docs/Settings.png}{width=100}
![Figure 2: Controller](docs/Controller.png){width=100}      

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
