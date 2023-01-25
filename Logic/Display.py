from PyQt5 import QtGui
import cv2


class Display:
    """class Display implements functions for displaying image(s) in the viewer Sorce_File"""

    def convert_to_pixmap(self, path_img):
        """convert_to_pixmap: returns pixmap object for Qlabel component through directory qimage object or path"""

        pixmap_image = QtGui.QPixmap(path_img)

        return pixmap_image

    def convert_to_qimage(self, path_img):
        """convert_to_qimage: returns pixmap object for Qlabel component through directory qimage object or path"""

        qimage_image = QtGui.QImage(path_img)

        return qimage_image

    def convert_cv_qt(self, cv_img):
        """convert_cv_qt: converts from an opencv image to QPixmap"""

        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )

        return QtGui.QPixmap.fromImage(Qt_format)

    def brightness_contrast(self, alpha_value, beta_value, path_img):
        """brightness_contrast: Implements brightness (alpha) and contrast (beta) operation g(i,j) = alpha * f(i,j) + beta"""

        opencv_img = cv2.imread(path_img, cv2.IMREAD_UNCHANGED)
        img_output = cv2.convertScaleAbs(opencv_img, alpha=alpha_value, beta=beta_value)
        # converts from an opencv image to QPixmap
        pixmap_img = self.convert_cv_qt(img_output)

        return pixmap_img

    def convert_to_gray_scale(self, path_img):
        """convert_to_gray_scale: converts image in path_img to gray scale"""

        # Read image using qimage
        qimage_img = self.convert_to_qimage(path_img)
        if qimage_img.isGrayscale():
            pixmap_img = self.convert_to_pixmap(qimage_img)
            grayscale_flg = 0
        else:
            grayscale = qimage_img.convertToFormat(QtGui.QImage.Format_Grayscale8)
            pixmap_img = QtGui.QPixmap.fromImage(grayscale)
            grayscale_flg = 1

        return pixmap_img, grayscale_flg

    def convert_to_black_white(self, path_img):
        """convert_to_black_white: converts image in path_img to binary"""

        # Read image using opencv
        opencv_img = cv2.imread(path_img, cv2.IMREAD_GRAYSCALE)
        # Noise reduction
        opencv_img = cv2.medianBlur(opencv_img, 5)
        b_w_img = cv2.adaptiveThreshold(
            opencv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        bw_pixmap = self.convert_cv_qt(b_w_img)
        bw_flg = 1

        return bw_pixmap, bw_flg

    def convert_to_black_white_inv(self, path_img):
        """convert_to_black_white_inv: converts image in path_img to binary inverted"""

        # Read image using opencv
        opencv_img = cv2.imread(path_img, cv2.IMREAD_GRAYSCALE)
        # Noise reduction
        opencv_img = cv2.medianBlur(opencv_img, 5)
        b_w_img = cv2.adaptiveThreshold(
            opencv_img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )
        bw_pixmap = self.convert_cv_qt(b_w_img)
        wb_flg = 1

        return bw_pixmap, wb_flg

    def rectangle_edge_detection(
        self, img_format, roi_img, contour_color, contour_width
    ):
        """rectangle_edge_detection: detects contours in roi_img and return contoured image"""

        (r, g, b, alph) = QtGui.QColor(contour_color).getRgb()
        if img_format == 3:
            ref_gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        else:
            # falta caso en que la imagen es binaria, message trabajr en el Work_Area
            ref_gray = roi_img
        ret, thresh = cv2.threshold(ref_gray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cv2.drawContours(roi_img, contours, -1, (b, g, r), contour_width)

        return roi_img
