"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Feb 2022
Purpose: Communicates with the microcontroller (loaded with Standard Firmata
code) and connects it to the gui.
"""

import time
from pyfirmata import Arduino, util, INPUT
from PyQt5.QtCore import QTimer
from packages.gui_control import GUIcontrol


class IOcontrol():
    def __init__(self, port, config):
        self.port = port
        self.config = config
        self.Initiate_Microcontroller()
        print('Connection established. Starting UI.')
        self.control = GUIcontrol(self.config)

        ''' Updates and synchronises external input/output with gui'''
        self.timerFast = QTimer()
        self.timerFast.timeout.connect(self.updateInput)
        self.timerFast.start(1)  # Update rate: 1 ms

    def updateInput(self):
        self.read_input()
        self.connect_input()

    def Initiate_Microcontroller(self):
        """Initiates required variables and connects to the microcontroller"""

        # Initiating variables
        self.InputPanel = self.config['InputPanel']
        self.last_start_state = False
        self.last_Film_state = []
        self.last_Project_state = []
        self.last_Move_state = False
        self.last_test_state = False
        self.MoveView = 0
        self.last_Poti = [0, 0]
        self.last_Joy = [0.5, 0.5]
        self.centre_Joy = [float(self.InputPanel['joy_midx']),
                           float(self.InputPanel['joy_midy'])]
        self.Joy_xtol = float(self.InputPanel['joy_tolx'])
        self.Joy_ytol = float(self.InputPanel['joy_tolx'])
        self.Joy_stepX = float(self.InputPanel['joy_stepx'])
        self.Joy_stepY = float(self.InputPanel['joy_stepy'])
        self.Poti_xtol = float(self.InputPanel['poti_tolx'])
        self.Poti_ytol = float(self.InputPanel['poti_toly'])
        self.Poti_stepX = float(self.InputPanel['poti_stepx'])
        self.Poti_stepY = float(self.InputPanel['poti_stepy'])
        self.Joy_xpolarity = self.InputPanel['joy_polx']
        self.Joy_ypolarity = self.InputPanel['joy_poly']
        self.Poti_xpolarity = self.InputPanel['poti_polx']
        self.Poti_ypolarity = self.InputPanel['poti_poly']
        self.last_buttonclicked = time.time()

        # Connecting the microcontroller
        print('Connecting to microcontroller')
        teensy = self.config['TeensyPins']
        if self.port is None:
            print("Importing port value from config")
            self.board = Arduino(teensy['port'])
        else:
            self.board = Arduino(self.port)

        # Control Slide Number
        self.mcu_btn_SlideNumber = [
            self.board.digital[int(teensy['next_slide'])],
            self.board.digital[int(teensy['previous_slide'])]
            ]

        # Select view to be projected and moved
        self.mcu_btn_PV = [
            self.board.digital[int(teensy['view1'])],
            self.board.digital[int(teensy['view2'])],
            self.board.digital[int(teensy['view3'])]
            ]
        self.mcu_btn_MoveView = self.board.digital[int(teensy['select_view'])]

        # Set displacement
        self.mcu_pot_xy = [self.board.analog[int(teensy['poti_x'])],
                           self.board.analog[int(teensy['poti_y'])]]
        self.mcu_joy_xy = [self.board.analog[int(teensy['joy_x'])],
                           self.board.analog[int(teensy['joy_y'])]]

        # Leds
        self.led = [int(teensy['led1']),
                    int(teensy['led2']),
                    int(teensy['led3'])]

        # Switch off all LEDs
        for led in self.led:
            self.board.digital[led].write(0)

        # Set the input buttons
        for btn_fn in self.mcu_btn_SlideNumber:
            btn_fn.mode = INPUT
        for btn_pv in self.mcu_btn_PV:
            btn_pv.mode = INPUT
        [pot.enable_reporting() for pot in self.mcu_pot_xy]
        [joy.enable_reporting() for joy in self.mcu_joy_xy]
        self.mcu_btn_MoveView.mode = INPUT

        ''' Assigning an iterator that will be used to read the status
        of the inputs of the circuit.'''
        it = util.Iterator(self.board)
        it.start()
        time.sleep(1)
        # Switch off all LEDs at the start
        self.board.digital[self.led[0]].write(1)

    def read_input(self):
        "Inputs to read"
        self.FilmNo = [btn.read() for btn in self.mcu_btn_SlideNumber]
        self.Project = [btn.read() for btn in self.mcu_btn_PV]
        self.Move = self.mcu_btn_MoveView.read()
        self.Poti = [pot.read() for pot in self.mcu_pot_xy]
        self.Joy = [joy.read() for joy in self.mcu_joy_xy]
        if None in (self.FilmNo or self.Project or
                    self.Move or self.Poti or self.Joy):
            self.control.errorhandling('Error: Micontroller input None',
                                       'Check the input connections.')
            self.board.exit()

    def connect_input(self):
        # Change the Film Number
        if self.FilmNo != self.last_Film_state:
            if self.FilmNo[0]:
                self.control.sbx_SlideNumber.stepDown()
            elif self.FilmNo[1]:
                self.control.sbx_SlideNumber.stepUp()
        self.last_Film_state = self.FilmNo

        # Start/stop a film|view in the projection window
        if self.Project != self.last_Project_state:
            for i, p in enumerate(self.Project):
                if p:
                    if not self.control.btn_PV[i].isChecked():
                        self.control.btn_PV[i].click()
                elif not p:
                    if self.control.btn_PV[i].isChecked():
                        self.control.btn_PV[i].click()
            if not any(self.Project):
                for led in self.led:
                    self.board.digital[led].write(0)
        self.last_Project_state = self.Project

        # Select the view to be moved
        if self.Move != self.last_Move_state:
            if self.Move and (time.time() - self.last_buttonclicked) > 0.2:
                # Time bound to avoid errors due to fast button clicking
                self.last_buttonclicked = time.time()
                self.MoveView = (self.MoveView+1) % 3
                for led in self.led:
                    self.board.digital[led].write(0)
                self.board.digital[self.led[self.MoveView]].write(1)
        self.last_Move_state = self.Move

        # Joystick functionality
        # x-movement
        self.Joy_dx = self.Joy[0]-self.last_Joy[0]
        if ((self.Joy_dx > 0) and (
                 self.Joy[0] > (self.centre_Joy[0] + self.Joy_xtol))) or (
                 (self.Joy_dx < 0) and (
                  self.Joy[0] < (self.centre_Joy[0] - self.Joy_xtol))):
            if self.Joy_xpolarity == '+':
                self.control.sbx_x[self.MoveView].setValue(
                    self.control.dx[self.MoveView]
                    - int(self.Joy_stepX*self.Joy_dx))
            elif self.Joy_xpolarity == '-':
                self.control.sbx_x[self.MoveView].setValue(
                    self.control.dx[self.MoveView]
                    + int(self.Joy_stepX*self.Joy_dx))
            self.control.set_sbx_displacement()

        # y-movement
        self.Joy_dy = self.Joy[1]-self.last_Joy[1]
        if ((self.Joy_dy > 0) and (
                self.Joy[1] > (self.centre_Joy[1] + self.Joy_ytol))) or (
                (self.Joy_dy < 0) and (
                 self.Joy[1] < (self.centre_Joy[1] - self.Joy_ytol))):
            if self.Joy_ypolarity == '+':
                self.control.sbx_y[self.MoveView].setValue(
                    self.control.dy[self.MoveView]
                    - int(self.Joy_dy*self.Joy_stepY))
            elif self.Joy_ypolarity == '-':
                self.control.sbx_y[self.MoveView].setValue(
                    self.control.dy[self.MoveView]
                    + int(self.Joy_dy*self.Joy_stepY))
            self.control.set_sbx_displacement()

        self.last_Joy[0] = self.Joy[0]
        self.last_Joy[1] = self.Joy[1]

        # Potentiometer
        self.Poti_dx = self.Poti[0]-self.last_Poti[0]
        self.Poti_dy = self.Poti[1]-self.last_Poti[1]
        if (abs(self.Poti_dx) > self.Poti_xtol) or (
                abs(self.Poti_dy) > self.Poti_ytol):
            # x-movement
            if self.Poti_xpolarity == '+':
                self.control.sbx_x[self.MoveView].setValue(
                    self.control.dx[self.MoveView]
                    + int(self.Poti_dx*self.Poti_stepX/self.Poti_xtol))
            elif self.Poti_xpolarity == '-':
                self.control.sbx_x[self.MoveView].setValue(
                    self.control.dx[self.MoveView]
                    - int(self.Poti_dx*self.Poti_stepX/self.Poti_xtol))
            # y-movement
            if self.Poti_ypolarity == '+':
                self.control.sbx_y[self.MoveView].setValue(
                    self.control.dy[self.MoveView]
                    + int(self.Poti_dy*self.Poti_stepY/self.Poti_xtol))
            elif self.Poti_ypolarity == '-':
                self.control.sbx_y[self.MoveView].setValue(
                    self.control.dy[self.MoveView]
                    - int(self.Poti_dy*self.Poti_stepY/self.Poti_xtol))

            self.control.set_sbx_displacement()
            self.last_Poti[0] = self.Poti[0]
            self.last_Poti[1] = self.Poti[1]

    def close(self):
        for led in self.led:
            self.board.digital[led].write(0)
        self.board.exit()
