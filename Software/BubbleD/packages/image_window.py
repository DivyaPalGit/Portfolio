"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Feb 2022
Purpose: Loads, scales, translates and rotates the image for projection.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPainter, QIcon
from PyQt5.QtWidgets import QWidget
import numpy as np


class ImageWindow(QWidget):
    """
    Selected image(s) will be displayed on the projection screen.
    """

    def __init__(self, icon_path):
        super().__init__()
        self.setWindowIcon(QIcon(icon_path))

    def selectImage(self, img_folder=("./images/Film 2411_2510"),
                    n_view=3, View=np.empty(3),
                    FilmType='Default',
                    ImageNo=2500,
                    ImgFormat='png',
                    dx=np.empty(3),
                    dy=np.empty(3),
                    tx=0,
                    ty=600,
                    tw=2160,
                    th=3840,
                    scale=1):
        """Loads and scales the selected image(s)"""
        self.sc_img = [None]*n_view
        self.Nv = len(View[View > 0])
        for v, v_value in enumerate(View):
            if v_value > 0:
                img = (img_folder + '/' + FilmType + '/view_' +
                       str(v+1) + '/' + str(ImageNo) + '.' + ImgFormat)
                self.img = QImage(img)
                self.sc_img[v] = self.img.scaled(int(th*scale), int(tw*scale),
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation)
        self.dx, self.dy = dx, dy
        self.tx, self.ty = tx, ty
        self.tw, self.th = tw, th
        self.repaint()

    def setDisplacement(self, dx=np.empty(3), dy=np.empty(3)):
        """Repaints the event with modified displpacement"""
        self.dx = dx
        self.dy = dy
        self.repaint()

    def setTable(self, tx=0, ty=600, tw=3840, th=2160):
        """Repaints the images with modified size of
        the table(white) background"""
        self.tx, self.ty = tx, ty
        self.tw, self.th = tw, th
        self.repaint()

    def paintEvent(self, event):
        """Shows the image(s) in the projection screen"""
        qp = QPainter()
        qp.begin(self)
        qp.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0))
        qp.fillRect(self.tx, self.ty, self.tw, self.th, QColor(255, 255, 255))
        rotate_counter = 0
        for i_im, p_im in enumerate(self.sc_img):
            if isinstance(p_im, QImage):
                if rotate_counter < 1:
                    qp.translate(p_im.height(), 0)
                    qp.rotate(90)
                    rotate_counter += 1
                qp.drawImage(self.dy[i_im], self.dx[i_im], p_im)
        qp.end()
