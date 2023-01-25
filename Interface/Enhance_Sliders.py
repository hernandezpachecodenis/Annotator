from Main_Window_ui import *


class Enhance_Sliders(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Create personalize layout widget
        # Ui_MainWindow.layoutWidget_3 = QtWidgets.QWidget(self.frame_left_dynamic) -> in Main_Window_ui.py
        Ui_MainWindow.layoutWidget_3.setGeometry(QtCore.QRect(0, 0, 392, 32))
        Ui_MainWindow.layoutWidget_3.setObjectName("layoutWidget_3")

        # Create horizontal layout that containts the sliders
        Enhance_Sliders.hLayout_dynamic_left = QtWidgets.QHBoxLayout(
            self.layoutWidget_3
        )
        self.hLayout_dynamic_left.setContentsMargins(0, 0, 0, 0)
        self.hLayout_dynamic_left.setObjectName("hLayout_dynamic_left")

        Enhance_Sliders.brightnessSlider = QtWidgets.QSlider(self.layoutWidget_3)
        Enhance_Sliders.brightnessSlider.setMinimumSize(QtCore.QSize(192, 30))
        Enhance_Sliders.brightnessSlider.setSliderPosition(50)
        Enhance_Sliders.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        Enhance_Sliders.brightnessSlider.setInvertedControls(False)
        Enhance_Sliders.brightnessSlider.setObjectName("brightnessSlider")
        self.hLayout_dynamic_left.addWidget(self.brightnessSlider)
        Enhance_Sliders.contrastSlider = QtWidgets.QSlider(self.layoutWidget_3)
        Enhance_Sliders.contrastSlider.setMinimumSize(QtCore.QSize(192, 30))
        Enhance_Sliders.contrastSlider.setSliderPosition(50)
        Enhance_Sliders.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        Enhance_Sliders.contrastSlider.setObjectName("contrastSlider")
        self.hLayout_dynamic_left.addWidget(self.contrastSlider)
