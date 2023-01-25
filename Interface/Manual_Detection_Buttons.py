from Main_Window_ui import *


class Manual_Detection_Buttons(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Create personalize layout widget
        # Ui_MainWindow.layoutWidget_4 = QtWidgets.QWidget(self.frame_right_dynamic) -> in Main_Window_ui.py
        Ui_MainWindow.layoutWidget_4.setGeometry(QtCore.QRect(0, 0, 176, 32))
        Ui_MainWindow.layoutWidget_4.setObjectName("layoutWidget_4")

        # Create horizontal layout that containts the buttons
        Manual_Detection_Buttons.hLayout_dynamic_right = QtWidgets.QHBoxLayout(
            self.layoutWidget_4
        )
        self.hLayout_dynamic_right.setContentsMargins(0, 0, 0, 0)
        self.hLayout_dynamic_right.setObjectName("hLayout_dynamic_right")
        self.Pen_b_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Pen_b_btn.sizePolicy().hasHeightForWidth())
        self.Pen_b_btn.setSizePolicy(sizePolicy)
        self.Pen_b_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon17 = QtGui.QIcon()
        icon17.addPixmap(
            QtGui.QPixmap("icons/pen_b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Pen_b_btn.setIcon(icon17)
        self.Pen_b_btn.setIconSize(QtCore.QSize(30, 30))
        self.Pen_b_btn.setObjectName("Pen_b_btn")
        self.hLayout_dynamic_right.addWidget(self.Pen_b_btn)
        self.Pen_w_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Pen_w_btn.sizePolicy().hasHeightForWidth())
        self.Pen_w_btn.setSizePolicy(sizePolicy)
        self.Pen_w_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon18 = QtGui.QIcon()
        icon18.addPixmap(
            QtGui.QPixmap("icons/pen_w.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Pen_w_btn.setIcon(icon18)
        self.Pen_w_btn.setIconSize(QtCore.QSize(30, 30))
        self.Pen_w_btn.setObjectName("Pen_w_btn")
        self.hLayout_dynamic_right.addWidget(self.Pen_w_btn)
        self.Paint_width_up = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Paint_width_up.sizePolicy().hasHeightForWidth()
        )
        self.Paint_width_up.setSizePolicy(sizePolicy)
        self.Paint_width_up.setMinimumSize(QtCore.QSize(30, 30))
        icon15 = QtGui.QIcon()
        icon15.addPixmap(
            QtGui.QPixmap("icons/ROI_w+.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Paint_width_up.setIcon(icon15)
        self.Paint_width_up.setIconSize(QtCore.QSize(30, 30))
        self.Paint_width_up.setObjectName("Paint_width_up")
        self.hLayout_dynamic_right.addWidget(self.Paint_width_up)
        self.Paint_width_down = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Paint_width_down.sizePolicy().hasHeightForWidth()
        )
        self.Paint_width_down.setSizePolicy(sizePolicy)
        self.Paint_width_down.setMinimumSize(QtCore.QSize(30, 30))
        icon16 = QtGui.QIcon()
        icon16.addPixmap(
            QtGui.QPixmap("icons/ROI_w-.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Paint_width_down.setIcon(icon16)
        self.Paint_width_down.setIconSize(QtCore.QSize(30, 30))
        self.Paint_width_down.setObjectName("Paint_width_down")
        self.hLayout_dynamic_right.addWidget(self.Paint_width_down)
        self.Undo_paint_btn = QtWidgets.QToolButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Undo_paint_btn.sizePolicy().hasHeightForWidth()
        )
        self.Undo_paint_btn.setSizePolicy(sizePolicy)
        self.Undo_paint_btn.setMinimumSize(QtCore.QSize(30, 30))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap("icons/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.Undo_paint_btn.setIcon(icon6)
        self.Undo_paint_btn.setIconSize(QtCore.QSize(30, 30))
        self.Undo_paint_btn.setObjectName("Undo_paint_btn")
        self.hLayout_dynamic_right.addWidget(self.Undo_paint_btn)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Pen_b_btn.setText(_translate("MainWindow", "..."))
        self.Pen_w_btn.setText(_translate("MainWindow", "..."))
        self.Paint_width_up.setText(_translate("MainWindow", "..."))
        self.Paint_width_down.setText(_translate("MainWindow", "..."))
        self.Undo_paint_btn.setText(_translate("MainWindow", "..."))
