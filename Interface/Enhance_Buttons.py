from Main_Window_ui import *


class Enhance_Buttons(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Create personalize layout widget
        # Ui_MainWindow.layoutWidget_3 = QtWidgets.QWidget(self.frame_left_dynamic) -> in Main_Window_ui.py
        Ui_MainWindow.layoutWidget_3.setGeometry(QtCore.QRect(0, 0, 140, 32))
        Ui_MainWindow.layoutWidget_3.setObjectName("layoutWidget_3")

        # Create horizontal layout that containts the buttons
        Enhance_Buttons.hLayout_dynamic_left = QtWidgets.QHBoxLayout(
            self.layoutWidget_3
        )
        self.hLayout_dynamic_left.setContentsMargins(0, 0, 0, 0)
        self.hLayout_dynamic_left.setObjectName("hLayout_dynamic_left")

        self.Brightness_btn_plus = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Brightness_btn_plus.sizePolicy().hasHeightForWidth()
        )
        self.Brightness_btn_plus.setSizePolicy(sizePolicy)
        self.Brightness_btn_plus.setMinimumSize(QtCore.QSize(30, 30))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap("icons/brightness.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Brightness_btn_plus.setIcon(icon6)
        self.Brightness_btn_plus.setIconSize(QtCore.QSize(30, 30))
        self.Brightness_btn_plus.setObjectName("Brightness_btn_plus")
        self.hLayout_dynamic_left.addWidget(self.Brightness_btn_plus)
        self.Brightness_btn_minus = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Brightness_btn_minus.sizePolicy().hasHeightForWidth()
        )
        self.Brightness_btn_minus.setSizePolicy(sizePolicy)
        self.Brightness_btn_minus.setMinimumSize(QtCore.QSize(30, 30))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap("icons/brightness_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Brightness_btn_minus.setIcon(icon7)
        self.Brightness_btn_minus.setIconSize(QtCore.QSize(30, 30))
        self.Brightness_btn_minus.setObjectName("Brightness_btn_minus")
        self.hLayout_dynamic_left.addWidget(self.Brightness_btn_minus)
        self.Contrast_btn_plus = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Contrast_btn_plus.sizePolicy().hasHeightForWidth()
        )
        self.Contrast_btn_plus.setSizePolicy(sizePolicy)
        self.Contrast_btn_plus.setMinimumSize(QtCore.QSize(30, 30))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap("icons/contrast.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Contrast_btn_plus.setIcon(icon8)
        self.Contrast_btn_plus.setIconSize(QtCore.QSize(30, 30))
        self.Contrast_btn_plus.setObjectName("Contrast_btn_plus")
        self.hLayout_dynamic_left.addWidget(self.Contrast_btn_plus)
        self.Contrast_btn_minus = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Contrast_btn_minus.sizePolicy().hasHeightForWidth()
        )
        self.Contrast_btn_minus.setSizePolicy(sizePolicy)
        self.Contrast_btn_minus.setMinimumSize(QtCore.QSize(30, 30))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap("icons/contrast1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Contrast_btn_minus.setIcon(icon9)
        self.Contrast_btn_minus.setIconSize(QtCore.QSize(30, 30))
        self.Contrast_btn_minus.setObjectName("Contrast_btn_minus")
        self.hLayout_dynamic_left.addWidget(self.Contrast_btn_minus)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Brightness_btn_plus.setText(_translate("MainWindow", "..."))
        self.Brightness_btn_minus.setText(_translate("MainWindow", "..."))
        self.Contrast_btn_plus.setText(_translate("MainWindow", "..."))
        self.Contrast_btn_minus.setText(_translate("MainWindow", "..."))
