from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, pyqtSignal

from Main_Window_ui import *

import cv2


class QLabelplusplus(QtWidgets.QLabel):

    segment_line_list = []
    painting_flg = 0
    painting_width = 1
    erasing_flg = 0
    painting_color = QColor()

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.drawing_flg = False
        self.ini_coord = QtCore.QPoint()
        self.fin_coord = QtCore.QPoint()
        self.exist_img_flg = 0

    def verifyPixmap(self):
        """verifyPixmap: verifies if pixmap exists in Work_Area qlabel"""

        if self.pixmap():
            self.exist_img_flg = 1
        else:
            self.exist_img_flg = 0

    def mousePressEvent(self, event):
        """mousePressEvent: defines actions triggers on mouse press event for free painting definition"""

        self.verifyPixmap()
        if event.button() == QtCore.Qt.LeftButton and self.exist_img_flg == 1:
            self.drawing_flg = True
            self.ini_coord = self.fin_coord = event.pos()
        elif self.exist_img_flg == 0:
            self.drawing_flg = False

    def mouseMoveEvent(self, event):
        """mouseMoveEvent: on each mouse move a line segment is created and appended to list"""

        if self.drawing_flg and QLabelplusplus.painting_flg == 1:
            # Update final coordinates
            self.fin_coord = event.pos()
            # Create line segment from initial coordinates to final coordinates
            segment = [
                QtCore.QLine(self.ini_coord, self.fin_coord),
                QLabelplusplus.painting_color,
                QLabelplusplus.painting_width,
            ]
            # QLabelplusplus.painting_color_list.append(QLabelplusplus.painting_color)
            QLabelplusplus.segment_line_list.append(segment)
            # Update the initial coordinates for next line segment
            self.ini_coord = self.fin_coord
            # call paintEvent method to update pixmap
            self.update()

    def paintEvent(self, event):
        """paintEvent:"""

        super().paintEvent(event)
        qpw = QtGui.QPainter(self)
        if QLabelplusplus.painting_flg == 1:
            # [line coordinates, line color, line width]
            for line_segments in QLabelplusplus.segment_line_list:
                qpw.setPen(
                    QtGui.QPen(
                        QColor(line_segments[1]),
                        line_segments[2],
                        QtCore.Qt.SolidLine,
                    )
                )
                qpw.drawLine(line_segments[0])

    def mouseReleaseEvent(self, event):
        """mouseReleaseEvent: resets all variables implied"""

        if self.drawing_flg:
            self.drawing_flg = False

    def delete_line_list(self):
        """snake_case refers to replace every space for _ and method name beguins with lowercase letter"""
        if len(QLabelplusplus.segment_line_list) > 0:
            QLabelplusplus.segment_line_list = []
            self.update()

    def activate_painting(self, color):
        """activate_painting:"""
        """CURSOR_NEW = QtGui.QCursor(QPixmap("icons/pen_b.png"))
        self.ui.Work_Area.setCursor(CURSOR_NEW)"""
        if QLabelplusplus.painting_flg == 0:
            QLabelplusplus.painting_flg = 1
            QLabelplusplus.painting_color = color
        elif (
            QLabelplusplus.painting_flg == 1 and QLabelplusplus.painting_color != color
        ):
            QLabelplusplus.painting_flg = 1
            QLabelplusplus.painting_color = color
        elif (
            QLabelplusplus.painting_flg == 1 and QLabelplusplus.painting_color == color
        ):
            QLabelplusplus.painting_flg = 0

    def paint_width(self, flg_w):
        if flg_w == 1:
            QLabelplusplus.painting_width += 1
        elif flg_w == 0 and QLabelplusplus.painting_width > 1:
            QLabelplusplus.painting_width -= 1
        QLabelplusplus.update(self)

    def undo_paint(self):
        QLabelplusplus.segment_line_list.pop(-1)
        QLabelplusplus.update(self)

    def painting_mask(self, roi):

        roi_size = roi.shape
        w_rate = roi_size[1] / QtCore.QRectF(self.contentsRect()).width()
        h_rate = roi_size[0] / QtCore.QRectF(self.contentsRect()).height()

        # [line coordinates, line color, line width]
        for seg_line in QLabelplusplus.segment_line_list:
            (r, g, b, alph) = QColor(seg_line[1]).getRgb()
            cv2.line(
                roi,
                (
                    int(seg_line[0].x1() * w_rate),
                    int(seg_line[0].y1() * h_rate),
                ),
                (
                    int(seg_line[0].x2() * w_rate),
                    int(seg_line[0].y2() * h_rate),
                ),
                (b, g, r),
                seg_line[2],
            )

        return roi
