from PyQt5 import QtCore

import cv2
import numpy as np


class Process:
    """class Process implements functionalities related with processing Work_Area"""

    # 0: black and white 0-255, 1: binary 0-1, 2: gray scale, 3: color, 10: unknown format
    format_roi_indicator = 10

    def mapped_coordinates(self, coord_rect, pixmap_size_Rect, contents_label_Rect):
        """mapped_coordinates: maps coordinates obtain in pixmap widget respect to coordinates in original image"""

        width_rate = pixmap_size_Rect.width() / contents_label_Rect.width()
        height_rate = pixmap_size_Rect.height() / contents_label_Rect.height()
        # Define scaled rectangle QRect(x, y, x width, y height)
        mapped_coord = QtCore.QRect(
            int(coord_rect.x() * width_rate),
            int(coord_rect.y() * height_rate),
            int(coord_rect.width() * width_rate),
            int(coord_rect.height() * height_rate),
        )

        return mapped_coord

    def define_roi(self, filename_p, mapped_roi):
        """define_roi: conform ROI image using original image and mouse click defined rectangle"""

        # Read image using opencv in it's original format
        Process.im_opencv = cv2.imread(filename_p, cv2.IMREAD_UNCHANGED)
        # Inverts coordinates axis (opencv shape respect pyqt rect)
        Process.im_opencv_roi = Process.im_opencv[
            mapped_roi.y() : (mapped_roi.y() + mapped_roi.height()),
            mapped_roi.x() : (mapped_roi.x() + mapped_roi.width()),
        ]
        # 0: black and white [0,255]; 1: binary [0,1]; 2: gray scale [0-255]; 3: color; 10: unknown format
        if len(Process.im_opencv_roi.shape) == 3:
            Process.format_roi_indicator = 3
        elif len(Process.im_opencv_roi.shape) == 2:
            if np.isin(Process.im_opencv_roi, [0, 1]).all():
                Process.coloformat_roi_indicatorr_roi_flg = 1
            elif np.isin(Process.im_opencv_roi, [0, 255]).all():
                Process.format_roi_indicator = 0
            else:
                Process.format_roi_indicator = 2

        return Process.im_opencv_roi, Process.format_roi_indicator

    def sobel_detection(self, var_thresh):
        """sobel_detection: implements sobel edge detection method"""

        # 0: black and white 0-255, 1: binary 0-1, 2: gray scale, 3: color, 10: unknown format
        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_roi_blur = cv2.GaussianBlur(im_roi, (3, 3), 0)
        # Apply Sobel filter in the horizontal and vertical direction
        sobel_x = cv2.Sobel(im_roi_blur, cv2.CV_8U, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(im_roi_blur, cv2.CV_8U, 0, 1, ksize=3)
        # Combine both gradient results
        sobel_img = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        # Convert to black and white image
        var_thresh, b_w_sobel = cv2.threshold(
            sobel_img, var_thresh, 255, cv2.THRESH_BINARY
        )
        return b_w_sobel

    def laplacian_detection(self, var_thresh):
        """laplacian_detection: implements laplacian edge detection method"""

        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_roi_blur = cv2.GaussianBlur(im_roi, (3, 3), 0)
        # Apply laplacian filter
        laplacian_img = cv2.Laplacian(im_roi_blur, cv2.CV_8U)
        # Convert to black and white image
        var_thresh, b_w_laplacian = cv2.threshold(
            laplacian_img, var_thresh, 255, cv2.THRESH_BINARY
        )

        return b_w_laplacian

    def canny_detection(self, var_thresh):
        """canny_detection: implements Canny edge detection method"""

        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_roi_blur = cv2.GaussianBlur(im_roi, (3, 3), 0)
        # Apply Canny filter VERRRRR threshold
        canny_img = cv2.Canny(im_roi_blur, var_thresh, threshold2=240)

        return canny_img

    def prewitt_detection(self, var_thresh):
        """prewitt_detection: implements Prewitt edge detection method"""

        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_roi_blur = cv2.GaussianBlur(im_roi, (3, 3), 0)
        # Define Prewitt mask in the horizontal and vertical direction
        Prewitt_op_x = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        Prewitt_op_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        # Apply Prewitt filter in the horizontal and vertical direction
        img_prewittx = cv2.filter2D(im_roi_blur, -1, Prewitt_op_x)
        img_prewitty = cv2.filter2D(im_roi_blur, -1, Prewitt_op_y)
        # Combine both gradient results
        prewitt_img = cv2.addWeighted(img_prewittx, 0.5, img_prewitty, 0.5, 0)
        # Convert to black and white image
        var_thresh, b_w_prewitt = cv2.threshold(
            prewitt_img, var_thresh, 255, cv2.THRESH_BINARY
        )

        return b_w_prewitt

    def robert_detection(self, var_thresh):
        """robert_detection: implements Robert edge detection method"""

        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_roi_blur = cv2.GaussianBlur(im_roi, (3, 3), 0)
        # Define Robert mask in the horizontal and vertical direction
        Robert_op_x = np.array([[1, 0], [0, -1]])
        Robert_op_y = np.array([[0, 1], [-1, 0]])
        # Apply Robert filter in the horizontal and vertical direction
        img_robertx = cv2.filter2D(im_roi_blur, -1, Robert_op_x)
        img_roberty = cv2.filter2D(im_roi_blur, -1, Robert_op_y)
        # Combine both gradient results
        robert_img = cv2.addWeighted(img_robertx, 0.5, img_roberty, 0.5, 0)
        # Convert to black and white image
        var_thresh, b_w_robert = cv2.threshold(
            robert_img, var_thresh, 255, cv2.THRESH_BINARY
        )

        return b_w_robert

    def convert_to_gray(self):
        """convert_to_gray: converts ROI image to gray scale"""
        # FALTAN VALIDACIONES DE FORMATO DE IMAGEN
        if Process.format_roi_indicator == 3:
            gray_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            gray_roi = Process.im_opencv_roi

        # Define flag indicator of ROI changes
        gray_roi_flg = 1

        return gray_roi, gray_roi_flg

    def convert_to_black_white(self):
        """convert_to_black_white: converts ROI image to black and white"""

        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_opencv_roi = cv2.medianBlur(im_roi, 5)

        b_w_roi = cv2.adaptiveThreshold(
            im_opencv_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Define flag indicator of ROI changes
        bw_roi_flg = 1

        return b_w_roi, bw_roi_flg

    def convert_to_white_black(self):
        """convert_to_white_black: converts ROI image to black and white inverted"""

        if Process.format_roi_indicator == 3:
            im_roi = cv2.cvtColor(Process.im_opencv_roi, cv2.COLOR_BGR2GRAY)
        else:
            im_roi = Process.im_opencv_roi
        # Noise reduction
        im_opencv_roi = cv2.medianBlur(im_roi, 5)

        w_b_roi = cv2.adaptiveThreshold(
            im_opencv_roi,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )

        # Define flag indicator of ROI changes
        wb_roi_flg = 1

        return w_b_roi, wb_roi_flg
