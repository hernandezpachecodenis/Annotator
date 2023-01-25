from Main_Window_ui import *


class Edge_Detection_Buttons(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Create personalize layout widget
        # Ui_MainWindow.layoutWidget_4 = QtWidgets.QWidget(self.frame_right_dynamic) -> in Main_Window_ui.py
        Ui_MainWindow.layoutWidget_4.setGeometry(QtCore.QRect(0, 0, 382, 32))
        Ui_MainWindow.layoutWidget_4.setObjectName("layoutWidget_4")

        # Create horizontal layout that containts the buttons
        Edge_Detection_Buttons.hLayout_dynamic_right = QtWidgets.QHBoxLayout(
            self.layoutWidget_4
        )
        self.hLayout_dynamic_right.setContentsMargins(0, 0, 0, 0)
        self.hLayout_dynamic_right.setObjectName("hLayout_dynamic_right")

        self.Sobel_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Sobel_btn.sizePolicy().hasHeightForWidth())
        self.Sobel_btn.setSizePolicy(sizePolicy)
        self.Sobel_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap("icons/sobel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Sobel_btn.setIcon(icon4)
        self.Sobel_btn.setIconSize(QtCore.QSize(30, 30))
        self.Sobel_btn.setObjectName("Sobel_btn")
        self.hLayout_dynamic_right.addWidget(self.Sobel_btn)
        self.Laplacian_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Laplacian_btn.sizePolicy().hasHeightForWidth()
        )
        self.Laplacian_btn.setSizePolicy(sizePolicy)
        self.Laplacian_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap("icons/laplacian.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Laplacian_btn.setIcon(icon5)
        self.Laplacian_btn.setIconSize(QtCore.QSize(30, 30))
        self.Laplacian_btn.setObjectName("Laplacian_btn")
        self.hLayout_dynamic_right.addWidget(self.Laplacian_btn)
        self.Canny_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canny_btn.sizePolicy().hasHeightForWidth())
        self.Canny_btn.setSizePolicy(sizePolicy)
        self.Canny_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap("icons/canny.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Canny_btn.setIcon(icon6)
        self.Canny_btn.setIconSize(QtCore.QSize(30, 30))
        self.Canny_btn.setObjectName("Canny_btn")
        self.hLayout_dynamic_right.addWidget(self.Canny_btn)
        self.Prewitt_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Prewitt_btn.sizePolicy().hasHeightForWidth())
        self.Prewitt_btn.setSizePolicy(sizePolicy)
        self.Prewitt_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap("icons/prewitt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Prewitt_btn.setIcon(icon7)
        self.Prewitt_btn.setIconSize(QtCore.QSize(30, 30))
        self.Prewitt_btn.setObjectName("Prewitt_btn")
        self.hLayout_dynamic_right.addWidget(self.Prewitt_btn)
        self.Robert_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Robert_btn.sizePolicy().hasHeightForWidth())
        self.Robert_btn.setSizePolicy(sizePolicy)
        self.Robert_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap("icons/robert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Robert_btn.setIcon(icon8)
        self.Robert_btn.setIconSize(QtCore.QSize(30, 30))
        self.Robert_btn.setObjectName("Robert_btn")
        self.hLayout_dynamic_right.addWidget(self.Robert_btn)
        Edge_Detection_Buttons.Thresh_bw_slider = QtWidgets.QSlider(self.layoutWidget_3)
        Edge_Detection_Buttons.Thresh_bw_slider.setMinimumSize(QtCore.QSize(200, 30))
        Edge_Detection_Buttons.Thresh_bw_slider.setSliderPosition(127)
        Edge_Detection_Buttons.Thresh_bw_slider.setMaximum(255)
        Edge_Detection_Buttons.Thresh_bw_slider.setOrientation(QtCore.Qt.Horizontal)
        Edge_Detection_Buttons.Thresh_bw_slider.setEnabled(False)
        Edge_Detection_Buttons.Thresh_bw_slider.setObjectName("Thresh_bw_slider")
        Edge_Detection_Buttons.hLayout_dynamic_right.addWidget(self.Thresh_bw_slider)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Sobel_btn.setText(_translate("MainWindow", "..."))
        self.Laplacian_btn.setText(_translate("MainWindow", "..."))
        self.Canny_btn.setText(_translate("MainWindow", "..."))
        self.Prewitt_btn.setText(_translate("MainWindow", "..."))
        self.Robert_btn.setText(_translate("MainWindow", "..."))
