"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Feb 2022

Purpose: Loads the gui and defines the function of objects in the gui.

Common abbreviations used in the ui:
    cbx QComboBox
    btn QPushButton/QToolButton
    lcd QLCDNumber
    lbl QLabel
    txt QLineEdit
    box QGroupBox
    hsp/vsp (Horizontal/Vertical) Spacer
    sbx QSpinBox
    hsl (Horizontal) QSlidder
    hbl/vbl QHBoxLayout/QVBoxLayout
"""

import os
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QMessageBox)
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QImageReader, QGuiApplication, QScreen
from packages.image_window import ImageWindow
import platform

''' To set the icon correctly in a windows uncomment the lines below'''
if platform.system().lower() == 'windows':
    print('OS: Windows')
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class GUIcontrol(QMainWindow):
    '''
    Connects all the buttons and defines there functioning.
    '''

    def __init__(self, config):
        super(GUIcontrol, self).__init__()
        self.config = config
        self.set_path()
        uic.loadUi(self.gui_path, self)
        self.set_icon()
        self.initialise_gui()
        self.set_defaults()
        self.connect_buttons()
        self.im_win = ImageWindow(self.icon_path)
        self.folder_selection()
        self.show_display()

    def set_path(self):
        """Defines the relative paths"""
        self.path = self.config['Paths']
        self.gui_path = self.path['gui']
        self.icon_path = self.path['icon']
        self.img_path = self.path['images']
        self.ctrl = self.config['GUIParamters']

    def set_icon(self):
        """Sets software icon"""
        self.setWindowIcon(QIcon(self.icon_path))

    def get_screen(self):
        """
        Checks for available displays and sets the default projection display.
        """
        screen_list = QGuiApplication.screens()
        self.NScreens = len(screen_list)
        self.screen_geo = [0]*self.NScreens
        self.resolution = [0]*self.NScreens
        self.cbx_ProjScrn.clear()
        self.gui_display = None
        self.projector = None
        self.unused_display = []

        for i, screen in enumerate(screen_list):
            self.screen_geo[i] = QScreen.geometry(screen)
            screen_size = [self.screen_geo[i].width(),
                           self.screen_geo[i].height()]
            self.resolution[i] = ('{}[{}x{}]'.
                                  format(i, screen_size[0], screen_size[1]))

            # Required resolution:
            self.gui_dim = list(map(int, self.ctrl['gui_display'].split('x')))
            self.proj_dim = list(map(int, self.ctrl['proj_display'].split('x')))

            # Verifying if display have desired resolution
            if (self.gui_display is None) and (screen_size == self.gui_dim):
                self.gui_display = self.screen_geo[i]
                self.cbx_TouchScrn.addItem(self.resolution[i])
            elif (self.projector is None) and (screen_size == self.proj_dim):
                self.projector = self.screen_geo[i]
                self.cbx_ProjScrn.addItem(self.resolution[i])
            else:
                '''If there are more than two displays,
                adding them to the choice list.
                '''
                self.cbx_TouchScrn.addItem(self.resolution[i])
                self.cbx_ProjScrn.addItem(self.resolution[i])

    def select_ProjScrn(self):
        """ Selects the projection screen"""
        self.projector = self.screen_geo[
            int(self.cbx_ProjScrn.currentText()[0])]

    def show_display(self):
        """ Shows gui/projector based on which screen is available"""
        self.get_screen()
        if self.gui_display is None:
            self.hide()
        else:
            self.setGeometry(self.gui_display)
            self.show()
        if self.projector is None:
            self.show()
            self.stop_projection()
        else:
            self.start_projection()

    def initialise_gui(self):
        '''Initiating required functions'''
        self.Nv = int(self.ctrl['num_views'])
        self.projViews = np.zeros(self.Nv)
        self.sbx_x = np.array([self.sbx_xv1, self.sbx_xv2, self.sbx_xv3])
        self.sbx_y = np.array([self.sbx_yv1, self.sbx_yv2, self.sbx_yv3])
        self.hsl_x = np.array([self.hsl_xv1, self.hsl_xv2, self.hsl_xv3])
        self.hsl_y = np.array([self.hsl_yv1, self.hsl_yv2, self.hsl_yv3])
        self.btn_xn = np.array([self.btn_xv1n, self.btn_xv2n, self.btn_xv3n])
        self.btn_xp = np.array([self.btn_xv1p, self.btn_xv2p, self.btn_xv3p])
        self.btn_yn = np.array([self.btn_yv1n, self.btn_yv2n, self.btn_yv3n])
        self.btn_yp = np.array([self.btn_yv1p, self.btn_yv2p, self.btn_xv3p])

        for x in self.sbx_x:
            x.setRange(int(self.ctrl['x_min']), int(self.ctrl['x_max']))
        for y in self.sbx_y:
            y.setRange(int(self.ctrl['y_min']), int(self.ctrl['y_max']))
        [x.setMaximum(int(self.ctrl['x_max'])) for x in self.hsl_x]
        [x.setMinimum(int(self.ctrl['x_min'])) for x in self.hsl_x]
        [x.setSingleStep(5) for x in self.hsl_x]
        [y.setMaximum(int(self.ctrl['y_max'])) for y in self.hsl_y]
        [y.setMinimum(int(self.ctrl['y_min'])) for y in self.hsl_y]
        [y.setSingleStep(10) for y in self.hsl_y]

        self.proj_dim = list(map(int, self.ctrl['proj_display'].split('x')))
        self.sbx_xtable.setRange(0, int(self.proj_dim[0]))
        self.sbx_ytable.setRange(0, int(self.proj_dim[1]))
        self.sbx_wtable.setRange(0, int(self.proj_dim[0]))
        self.sbx_htable.setRange(0, int(self.proj_dim[1]))

        self.box_ProjectView.setEnabled(True)
        self.box_SlideNumber.setEnabled(True)
        self.box_ImgProp.setEnabled(True)
        self.box_table.setEnabled(False)
        self.reset_flag = 0

    def set_defaults(self):
        ''' Sets the default values'''
        self.txt_FolderName.setText(self.img_path)
        self.set_default_displacement()
        self.sbx_SlideNumber.setValue(
            np.random.randint(0, int(self.ctrl['num_images'])-1))
        self.xTable = 0
        self.yTable = int(self.ctrl['table_start'])
        self.wTable = int(self.proj_dim[0])
        self.hTable = int(self.ctrl['table_stop'])
        self.imgScale = float(self.ctrl['image_scale'])
        self.sbx_xtable.setValue(self.xTable)
        self.sbx_ytable.setValue(self.yTable)
        self.sbx_wtable.setValue(self.wTable)
        self.sbx_htable.setValue(self.hTable)

    def set_default_displacement(self):
        """ Sets the default displacement"""
        self.dy = [int(self.ctrl['dy_v1']),
                   int(self.ctrl['dy_v2']),
                   int(self.ctrl['dy_v3'])]
        self.dx = [int(self.ctrl['dx_v1']),
                   int(self.ctrl['dx_v2']),
                   int(self.ctrl['dx_v3'])]
        for i in range(0, self.Nv):
            self.sbx_x[i].setValue(self.dx[i])
            self.sbx_y[i].setValue(self.dy[i])
            self.hsl_x[i].setValue(self.dx[i])
            self.hsl_y[i].setValue(self.dy[i])

        self.reset_flag = 0

    def connect_buttons(self):
        """
        Connects buttons to appropriate functions
        """
        # Screen
        self.cbx_ProjScrn.activated.connect(self.select_ProjScrn)
        self.btn_ScrnUpdate.clicked.connect(self.show_display)

        # Folder selection
        self.btn_FolderCnf.clicked.connect(self.folder_selection)
        self.btn_FolderBrowse.clicked.connect(self.browse_folder)

        self.btn_PV = [self.btn_PV1, self.btn_PV2, self.btn_PV3]
        [v.clicked.connect(self.enable_projection) for v in self.btn_PV]

        # Slide number
        self.cbx_SlideNumber.activated.connect(self.get_slide_num)
        self.btn_SlideNumber_low.clicked.connect(self.sbx_SlideNumber.stepDown)
        self.btn_SlideNumber_high.clicked.connect(self.sbx_SlideNumber.stepUp)
        self.sbx_SlideNumber.valueChanged.connect(self.set_slide_num)

        # Film type selection -Chosing editted/original image
        self.cbx_FilmType.activated.connect(self.set_img_type)

        # Image format
        self.cbx_ImgFormat.activated.connect(self.set_img_format)

        # Table settings
        self.btn_en_table.clicked.connect(self.enable_table)
        self.sbx_xtable.valueChanged.connect(self.set_table)
        self.sbx_ytable.valueChanged.connect(self.set_table)
        self.btn_xtableN.clicked.connect(self.sbx_xtable.stepDown)
        self.btn_xtableP.clicked.connect(self.sbx_xtable.stepUp)
        self.btn_ytableN.clicked.connect(self.sbx_ytable.stepDown)
        self.btn_ytableP.clicked.connect(self.sbx_ytable.stepUp)
        self.sbx_wtable.valueChanged.connect(self.set_table)
        self.sbx_htable.valueChanged.connect(self.set_table)
        self.btn_wtableN.clicked.connect(self.sbx_wtable.stepDown)
        self.btn_wtableP.clicked.connect(self.sbx_wtable.stepUp)
        self.btn_htableN.clicked.connect(self.sbx_htable.stepDown)
        self.btn_htableP.clicked.connect(self.sbx_htable.stepUp)

        # --- Displacement---
        self.btn_adj_rst.clicked.connect(self.reset_displacement)

        # Spin box entry
        [x.valueChanged.connect(self.set_sbx_displacement) for x in self.sbx_x]
        [y.valueChanged.connect(self.set_sbx_displacement) for y in self.sbx_y]

        # Slidder entry
        [x.valueChanged.connect(self.set_hsl_displacement) for x in self.hsl_x]
        [y.valueChanged.connect(self.set_hsl_displacement) for y in self.hsl_y]

        # Select view
        [self.btn_xn[i].clicked.connect(
            self.sbx_x[i].stepDown) for i in range(0, self.Nv)]
        [self.btn_yn[i].clicked.connect(
            self.sbx_y[i].stepDown) for i in range(0, self.Nv)]
        [self.btn_xp[i].clicked.connect(
            self.sbx_x[i].stepUp) for i in range(0, self.Nv)]
        [self.btn_yp[i].clicked.connect(
            self.sbx_y[i].stepUp) for i in range(0, self.Nv)]

        # Reset all
        self.btn_resetAll.clicked.connect(self.reset_all)
        QGuiApplication.instance().screenRemoved.connect(self.show_display)
        QGuiApplication.instance().screenRemoved.connect(self.show_display)

    def folder_selection(self):
        """ Selects & displays the image folder in the line edit"""
        if self.txt_FolderName.text() is None:
            self.errorhandling('Error: Please select a folder!')
        else:
            self.film_folder = self.txt_FolderName.text()
        self.box_ImgProp.setEnabled(True)
        self.get_img_type()

    def get_img_type(self, view=1):
        """
        Gets all the subfolder.
        This is added to easily switch between original and editted images.
        """
        self.img_type_list = sorted(folder for folder in sorted(
                                      os.listdir(self.film_folder)))
        self.cbx_FilmType.clear()
        self.cbx_FilmType.addItems(self.img_type_list)
        if not self.img_type_list:
            self.errorhandling('Error: Empty folder', ' Chose a valid folder.')
        else:
            self.cbx_FilmType.setCurrentText(self.img_type_list[0])

        self.set_img_type()

    def set_img_type(self):
        """
        Changes the image type (i.e. subfolder) to selected value.
        """
        self.img_type = self.cbx_FilmType.currentText()
        self.get_img_format()

    def get_img_format(self, view=1):
        """ Gets the selected image format"""
        self.img_dir = self.film_folder+'/'+self.img_type+'/view_'+str(view)
        self.img_format_list = sorted(set([img[-3:] for img in
                                           sorted(os.listdir(self.img_dir))]))
        self.cbx_ImgFormat.clear()
        self.cbx_ImgFormat.addItems(self.img_format_list)

        if not self.img_format_list:
            self.errorhandling('Error: Empty folder',
                               ' Chose a valid folder.')
        else:
            self.cbx_ImgFormat.setCurrentText(self.img_format_list[0])
        self.set_img_format()

    def set_img_format(self):
        """ Set the image"""
        self.img_format = self.cbx_ImgFormat.currentText()
        if self.img_format.lower() in QImageReader().supportedImageFormats():
            self.get_film_list()
        else:
            self.errorhandling('Error: Unaccepted image format',
                               'Please ensure the image is'
                               'supported by QImage.')

    def enable_table(self):
        """Enables adjustment of Table parameters"""
        if self.btn_en_table.isChecked():
            self.box_table.setEnabled(True)
        else:
            self.box_table.setEnabled(False)

    def set_table(self):
        """Adjustment of Table parameters"""
        self.xTable = self.sbx_xtable.value()
        self.yTable = self.sbx_ytable.value()
        self.wTable = self.sbx_wtable.value()
        self.hTable = self.sbx_htable.value()
        self.update_projection()

    def get_film_list(self):
        """Creates a list of all slides in the film"""
        self.film_list = [img[:-4] for img in sorted(os.listdir(self.img_dir))
                          if img.endswith(self.img_format)]
        self.cbx_SlideNumber.clear()
        self.cbx_SlideNumber.addItems(self.film_list)
        self.NFilms = len(self.film_list)
        self.sbx_SlideNumber.setRange(0, self.NFilms-1)
        self.set_slide_num()

    def get_slide_num(self):
        """Gets the current slide number"""
        self.slide_num = int(self.cbx_SlideNumber.currentText())
        self.update_projection()
        self.sbx_SlideNumber.setValue(
            self.film_list.index(str(self.slide_num)))

    def set_slide_num(self):
        """Selects a particular slide"""
        self.cbx_SlideNumber.setCurrentText(self.film_list
                                            [self.sbx_SlideNumber.value()])
        self.get_slide_num()

    def browse_folder(self):
        """ Browses for the folder and writes it in the line edit """
        self.txt_FolderName.setText(QFileDialog.getExistingDirectory())

    def enable_projection(self):
        """ Enables the projection and the controller tab
            for the selected view"""
        if (v.isChecked() for v in self.btn_PV):
            self.projViews = np.array([v.isChecked()*1 for v in self.btn_PV])
            self.update_projection()

    def update_projection(self):
        """Updates the projected image"""
        self.im_win.selectImage(img_folder=self.film_folder,
                                View=self.projViews,
                                FilmType=self.img_type,
                                ImageNo=self.slide_num,
                                ImgFormat=self.img_format,
                                dx=self.dx,
                                dy=self.dy,
                                tx=self.xTable,
                                ty=self.yTable,
                                tw=self.wTable,
                                th=self.hTable,
                                scale=self.imgScale)

    def start_projection(self):
        """ Starts the projection screen"""
        self.update_projection()
        self.im_win.move(self.projector.left(), self.projector.top())
        self.im_win.showFullScreen()
        self.box_PositionAdjustment.setEnabled(True)

    def stop_projection(self):
        """ Stops the projection screen"""
        self.im_win.close()
        self.box_PositionAdjustment.setEnabled(False)

    def set_sbx_displacement(self):
        """Sets the value of image displacement through the QSpinBox"""
        if self.reset_flag == 0:
            self.dx = [x.value() for x in self.sbx_x]
            self.dy = [y.value() for y in self.sbx_y]
            [self.hsl_x[i].setValue(self.dx[i]) for i in range(0, self.Nv)]
            [self.hsl_y[i].setValue(self.dy[i]) for i in range(0, self.Nv)]
            self.im_win.setDisplacement(dx=self.dx, dy=self.dy)

    def set_hsl_displacement(self):
        """Sets the value of image displacement through the Qslidder"""
        if self.reset_flag == 0:
            self.dx = [x.value() for x in self.hsl_x]
            self.dy = [y.value() for y in self.hsl_y]
            [self.sbx_x[i].setValue(self.dx[i]) for i in range(0, self.Nv)]
            [self.sbx_y[i].setValue(self.dy[i]) for i in range(0, self.Nv)]
            self.im_win.setDisplacement(dx=self.dx, dy=self.dy)

    def reset_displacement(self):
        """ Resets the displacement to default value"""
        self.reset_flag = 1  # Ensures simultaneous reset of all displacements
        self.set_default_displacement()
        self.set_sbx_displacement()

    def reset_all(self):
        """
        Resets the selected folder, format, table settings,
        displacement, and starts projection.
        Doesn't reset the default display.
        """
        self.reset_flag = 1  # Ensures simultaneous reset of all displacements
        self.set_defaults()
        self.folder_selection()

    def errorhandling(self, err_txt, err_info):
        """ Opens an error window"""
        err = QMessageBox()
        err.setIcon(QMessageBox.Critical)
        err.setText(err_txt)
        err.setInformativeText(err_info)
        err.setWindowTitle("Error")
        err.exec_()

    def closeEvent(self, event):
        self.im_win.close()
