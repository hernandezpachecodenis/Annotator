import os.path
import cv2

# from Main_Window_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets


class QLabelplus(QtWidgets.QLabel):
    """class QLabelplus: promotes QLabel widget Source_File redefining mouse click events"""

    # FLAGS
    activate_ROI_flg = 0  # single ROI selection is being used
    activate_ROI_edge_flg = 0  # into rectangle roi detection is being used
    activate_ROI_multiple_flg = 0  # multiple ROI selection is being used
    activate_ROI_all_image_flg = 0  # all image ROI selection is being used
    exist_img_flg = 0  # pixmap exists in QLabel Source_File
    undo_flg = 0  # undo action is being used
    # DATA MEMBERS
    mouse_released_sig = QtCore.pyqtSignal()  # emited signal on mouse release
    rect_roi_multiple = []  # [rectangle coordinates, rectangle color, rectangle width]
    rect_roi = QtCore.QRect()  # QRect(self.ini_coord, self.fin_coord)
    selected_color = "#E00C0C"  # default rectangle border color
    pen_width = 1  # default rectangle border width

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.drawing_flg = False
        self.ini_coord = QtCore.QPoint()  # mouse click initial coordinates
        self.fin_coord = QtCore.QPoint()  # mouse click final coordinates

    def verify_pixmap(self):
        """verify_pixmap: verifies if pixmap exists in Source_File qlabel"""

        if self.pixmap():
            QLabelplus.exist_img_flg = 1
        else:
            QLabelplus.exist_img_flg = 0

    def mousePressEvent(self, event):
        """mousePressEvent: defines actions triggers on mouse press event for ROI definition"""

        if (
            QLabelplus.activate_ROI_flg == 1
            or QLabelplus.activate_ROI_edge_flg == 1
            or QLabelplus.activate_ROI_multiple_flg == 1
        ):
            self.verify_pixmap()
            if event.button() == QtCore.Qt.LeftButton and QLabelplus.exist_img_flg == 1:
                self.drawing_flg = True
                self.ini_coord = self.fin_coord = event.pos()
                QLabelplus.undo_flg = 0
            elif QLabelplus.exist_img_flg == 0:
                self.drawing_flg = False
        elif QLabelplus.activate_ROI_all_image_flg == 1:
            self.verify_pixmap()
            if event.button() == QtCore.Qt.LeftButton and QLabelplus.exist_img_flg == 1:
                self.drawing_flg = False
                QLabelplus.rect_roi = self.contentsRect()
                # On signal emited
                self.mouse_released_sig.emit()

    def mouseMoveEvent(self, event):
        """mouseMoveEvent: update final coordinates on mouse move for rectangle continuity painting"""

        if self.drawing_flg:
            self.fin_coord = event.pos()
            self.update()

    def paintEvent(self, event):
        """paintEvent: method triggered on update() and used for form painting"""

        super().paintEvent(event)
        qp = QtGui.QPainter(self)
        # ROI border color (pen color) and border width definition
        qp.setPen(
            QtGui.QPen(
                QtGui.QColor(QLabelplus.selected_color),
                QLabelplus.pen_width,
                QtCore.Qt.SolidLine,
            )
        )
        # Single/multiple ROI drawing
        if (
            QLabelplus.activate_ROI_flg == 1
            and QLabelplus.activate_ROI_edge_flg == 0
            and QLabelplus.activate_ROI_multiple_flg == 0
            and QLabelplus.activate_ROI_all_image_flg == 0
        ):
            QLabelplus.rect_roi = QtCore.QRect(self.ini_coord, self.fin_coord)
            qp.drawRect(QLabelplus.rect_roi)
        elif QLabelplus.activate_ROI_flg == 0 and (
            QLabelplus.activate_ROI_edge_flg == 1
            or QLabelplus.activate_ROI_multiple_flg == 1
        ):
            # Continuouslly repaint actual rectangle if not undo_ROI_multiple_roi is activated
            if QLabelplus.undo_flg == 0:
                QLabelplus.rect_roi = QtCore.QRect(self.ini_coord, self.fin_coord)
                qp.drawRect(QLabelplus.rect_roi)
            # Add previous painted rectangles to pixmap
            for rectangles in QLabelplus.rect_roi_multiple:
                qp.setPen(
                    QtGui.QPen(
                        QtGui.QColor(rectangles[1]),
                        rectangles[2],
                        QtCore.Qt.SolidLine,
                    )
                )
                qp.drawRect(rectangles[0])

    def deleteRect(self):
        """snake_case refers to replace every space for _ and method name beguins with lowercase letter"""
        if QLabelplus.rect_roi:
            self.ini_coord = self.fin_coord = QtCore.QPoint()
            self.update()
        if QLabelplus.rect_roi_multiple:
            self.ini_coord = self.fin_coord = QtCore.QPoint()
            QLabelplus.rect_roi_multiple = []
            self.update()

    def mouseReleaseEvent(self, event):
        """snake_case refers to replace every space for _ and method name begins with lowercase letter"""

        self.fin_coord = event.pos()
        if self.drawing_flg and (self.ini_coord - self.fin_coord).manhattanLength() > 6:
            if (
                QLabelplus.activate_ROI_multiple_flg == 1
                or QLabelplus.activate_ROI_edge_flg == 1
            ):
                # [rectangle coordinates, rectangle color, rectangle width]
                r = [
                    QtCore.QRect(self.ini_coord, self.fin_coord),
                    QLabelplus.selected_color,
                    QLabelplus.pen_width,
                ]
                QLabelplus.rect_roi_multiple.append(r)
            # On signal emited
            self.mouse_released_sig.emit()
            self.drawing_flg = False
            self.update()

    def activate_ROI(self):
        """snake_case refers to replace every space for _ and method name beguins with lowercase letter"""

        QLabelplus.activate_ROI_edge_flg = 0
        QLabelplus.activate_ROI_multiple_flg = 0
        QLabelplus.activate_ROI_all_image_flg = 0
        if QLabelplus.activate_ROI_flg == 0:
            QLabelplus.activate_ROI_flg = 1
        elif QLabelplus.activate_ROI_flg == 1:
            QLabelplus.activate_ROI_flg = 0

    def activate_ROI_edge(self):
        """snake_case refers to replace every space for _ and method name beguins with lowercase letter"""

        QLabelplus.activate_ROI_flg = 0
        QLabelplus.activate_ROI_multiple_flg = 0
        QLabelplus.activate_ROI_all_image_flg = 0
        if QLabelplus.activate_ROI_edge_flg == 0:
            QLabelplus.activate_ROI_edge_flg = 1
        elif QLabelplus.activate_ROI_edge_flg == 1:
            QLabelplus.activate_ROI_edge_flg = 0

    def activate_ROI_multiple(self):
        """snake_case refers to replace every space for _ and method name beguins with lowercase letter"""

        QLabelplus.activate_ROI_flg = 0
        QLabelplus.activate_ROI_edge_flg = 0
        QLabelplus.activate_ROI_all_image_flg = 0
        if QLabelplus.activate_ROI_multiple_flg == 0:
            QLabelplus.activate_ROI_multiple_flg = 1
        elif QLabelplus.activate_ROI_multiple_flg == 1:
            QLabelplus.activate_ROI_multiple_flg = 0

    def activate_ROI_all_image(self):
        """sdbf"""

        QLabelplus.activate_ROI_flg = 0
        QLabelplus.activate_ROI_edge_flg = 0
        QLabelplus.activate_ROI_multiple_flg = 0
        if QLabelplus.activate_ROI_all_image_flg == 0:
            QLabelplus.activate_ROI_all_image_flg = 1
        elif QLabelplus.activate_ROI_all_image_flg == 1:
            QLabelplus.activate_ROI_all_image_flg = 0

    def ROI_color(sel_color):
        if sel_color != "#E00C0C":
            # format “#RRGGBB”
            QLabelplus.selected_color = sel_color

    def ROI_width(self, flg):
        if flg == 1:
            QLabelplus.pen_width += 1
        elif flg == 0 and QLabelplus.pen_width > 1:
            QLabelplus.pen_width -= 1
        # Repaint ROIs with pen width modified only if single ROI selection
        if (
            QLabelplus.activate_ROI_flg == 1
            and QLabelplus.activate_ROI_multiple_flg == 0
            and QLabelplus.activate_ROI_edge_flg == 0
        ):
            QLabelplus.update(self)

    def single_label_img(self, im_opencv, path_q, roi):

        # Converts roi selected color from format “#RRGGBB” to (RGB) format
        (r, g, b, alph) = QtGui.QColor(QLabelplus.selected_color).getRgb()

        cv2.rectangle(
            im_opencv,
            (roi.x(), roi.y()),
            (roi.x() + roi.width(), roi.y() + roi.height()),
            (b, g, r),
            QLabelplus.pen_width,
        )
        img_name = os.path.basename(path_q)
        img_directory = os.path.dirname(path_q)

        cv2.imwrite(img_directory + "/" + "labeled_" + img_name, im_opencv)

    def multiple_label_img(self, im_opencv, path_q, roi_list):

        # [rectangle coordinates, rectangle color, rectangle width]
        for ROIs in roi_list:
            (r, g, b, alph) = QtGui.QColor(ROIs[1]).getRgb()
            cv2.rectangle(
                im_opencv,
                (ROIs[0].x(), ROIs[0].y()),
                (ROIs[0].x() + ROIs[0].width(), ROIs[0].y() + ROIs[0].height()),
                (b, g, r),
                ROIs[2],
            )  # Revisar los 2 ciclos for an anotador y aqui. hacer como en QLabelplusplus

        img_name = os.path.basename(path_q)
        img_directory = os.path.dirname(path_q)

        cv2.imwrite(img_directory + "/" + "labeled_" + img_name, im_opencv)

    def undo_ROI_multiple_roi(self):
        """undo_ROI_multiple_roi: update rect_roi_multiple by poping last ROI and repaint"""
        if QLabelplus.activate_ROI_edge_flg == 1:
            QLabelplus.undo_flg = 1
            # On signal emited
            self.handle_released()
        elif QLabelplus.activate_ROI_multiple_flg == 1:
            QLabelplus.undo_flg = 1
            QLabelplus.rect_roi_multiple.pop(-1)
            QLabelplus.update(self)
