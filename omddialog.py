from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainDialog(object):
    def setupUi(self, mainDialog):
        mainDialog.setObjectName("mainDialog")
        mainDialog.resize(1339, 745)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        mainDialog.setFont(font)
        mainDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.isoComboBox = QtWidgets.QComboBox(mainDialog)
        self.isoComboBox.setEnabled(False)
        self.isoComboBox.setGeometry(QtCore.QRect(1080, 160, 221, 32))
        self.isoComboBox.setObjectName("isoComboBox")
        self.isoLabel = QtWidgets.QLabel(mainDialog)
        self.isoLabel.setEnabled(False)
        self.isoLabel.setGeometry(QtCore.QRect(1120, 130, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.isoLabel.setFont(font)
        self.isoLabel.setObjectName("isoLabel")
        self.focalComboBox = QtWidgets.QComboBox(mainDialog)
        self.focalComboBox.setEnabled(False)
        self.focalComboBox.setGeometry(QtCore.QRect(1080, 250, 221, 32))
        self.focalComboBox.setObjectName("focalComboBox")
        self.focalLabel = QtWidgets.QLabel(mainDialog)
        self.focalLabel.setEnabled(False)
        self.focalLabel.setGeometry(QtCore.QRect(1120, 220, 151, 18))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.focalLabel.setFont(font)
        self.focalLabel.setObjectName("focalLabel")
        self.shutComboBox = QtWidgets.QComboBox(mainDialog)
        self.shutComboBox.setEnabled(False)
        self.shutComboBox.setGeometry(QtCore.QRect(1080, 340, 221, 32))
        self.shutComboBox.setObjectName("shutComboBox")
        self.shutLabel = QtWidgets.QLabel(mainDialog)
        self.shutLabel.setEnabled(False)
        self.shutLabel.setGeometry(QtCore.QRect(1120, 310, 151, 18))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.shutLabel.setFont(font)
        self.shutLabel.setObjectName("shutLabel")
        self.expCompComboBox = QtWidgets.QComboBox(mainDialog)
        self.expCompComboBox.setEnabled(False)
        self.expCompComboBox.setGeometry(QtCore.QRect(1080, 430, 221, 32))
        self.expCompComboBox.setObjectName("expCompComboBox")
        self.expCompLabel = QtWidgets.QLabel(mainDialog)
        self.expCompLabel.setEnabled(False)
        self.expCompLabel.setGeometry(QtCore.QRect(1110, 400, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.expCompLabel.setFont(font)
        self.expCompLabel.setObjectName("expCompLabel")
        self.takeModeComboBox = QtWidgets.QComboBox(mainDialog)
        self.takeModeComboBox.setGeometry(QtCore.QRect(1080, 70, 221, 32))
        self.takeModeComboBox.setObjectName("takeModeComboBox")
        self.takeModeLabel = QtWidgets.QLabel(mainDialog)
        self.takeModeLabel.setGeometry(QtCore.QRect(1140, 40, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.takeModeLabel.setFont(font)
        self.takeModeLabel.setObjectName("takeModeLabel")
        self.addCapturePushButton = QtWidgets.QPushButton(mainDialog)
        self.addCapturePushButton.setEnabled(False)
        self.addCapturePushButton.setGeometry(QtCore.QRect(920, 580, 141, 34))
        self.addCapturePushButton.setObjectName("addCapturePushButton")
        self.connectedLabel = QtWidgets.QLabel(mainDialog)
        self.connectedLabel.setEnabled(True)
        self.connectedLabel.setGeometry(QtCore.QRect(1110, 620, 101, 18))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.connectedLabel.setFont(font)
        self.connectedLabel.setAutoFillBackground(False)
        self.connectedLabel.setStyleSheet("color:red")
        self.connectedLabel.setObjectName("connectedLabel")
        self.connectedSlider = QtWidgets.QSlider(mainDialog)
        self.connectedSlider.setGeometry(QtCore.QRect(1140, 650, 31, 20))
        self.connectedSlider.setStyleSheet("color:red")
        self.connectedSlider.setMaximum(1)
        self.connectedSlider.setSliderPosition(0)
        self.connectedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.connectedSlider.setObjectName("connectedSlider")
        self.liveStreamLabel = QtWidgets.QLabel(mainDialog)
        self.liveStreamLabel.setGeometry(QtCore.QRect(10, 80, 640, 480))
        self.liveStreamLabel.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.liveStreamLabel.setMouseTracking(True)
        self.liveStreamLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.liveStreamLabel.setAutoFillBackground(False)
        self.liveStreamLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0)\n"
"")
        self.liveStreamLabel.setObjectName("liveStreamLabel")
        self.setAsCurrentPushButton = QtWidgets.QPushButton(mainDialog)
        self.setAsCurrentPushButton.setEnabled(False)
        self.setAsCurrentPushButton.setGeometry(QtCore.QRect(1150, 510, 81, 34))
        self.setAsCurrentPushButton.setObjectName("setAsCurrentPushButton")
        self.liveIsoLabel = QtWidgets.QLabel(mainDialog)
        self.liveIsoLabel.setGeometry(QtCore.QRect(70, 570, 81, 18))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.liveIsoLabel.setFont(font)
        self.liveIsoLabel.setStyleSheet("color:green")
        self.liveIsoLabel.setObjectName("liveIsoLabel")
        self.liveFocalLabel = QtWidgets.QLabel(mainDialog)
        self.liveFocalLabel.setGeometry(QtCore.QRect(190, 570, 91, 18))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.liveFocalLabel.setFont(font)
        self.liveFocalLabel.setStyleSheet("color:green")
        self.liveFocalLabel.setObjectName("liveFocalLabel")
        self.liveShutLabel = QtWidgets.QLabel(mainDialog)
        self.liveShutLabel.setEnabled(True)
        self.liveShutLabel.setGeometry(QtCore.QRect(320, 570, 101, 18))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.liveShutLabel.setFont(font)
        self.liveShutLabel.setStyleSheet("color:green")
        self.liveShutLabel.setObjectName("liveShutLabel")
        self.liveExpLabel = QtWidgets.QLabel(mainDialog)
        self.liveExpLabel.setEnabled(True)
        self.liveExpLabel.setGeometry(QtCore.QRect(450, 570, 91, 18))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.liveExpLabel.setFont(font)
        self.liveExpLabel.setStyleSheet("color:green")
        self.liveExpLabel.setObjectName("liveExpLabel")
        self.selectedTreeWidget = QtWidgets.QTreeWidget(mainDialog)
        self.selectedTreeWidget.setGeometry(QtCore.QRect(670, 80, 401, 481))
        self.selectedTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.selectedTreeWidget.setColumnCount(6)
        self.selectedTreeWidget.setObjectName("selectedTreeWidget")
        self.selectedTreeWidget.headerItem().setText(0, "1")
        self.selectedTreeWidget.headerItem().setText(1, "2")
        self.selectedTreeWidget.headerItem().setText(2, "3")
        self.selectedTreeWidget.headerItem().setText(3, "4")
        self.selectedTreeWidget.headerItem().setText(4, "5")
        self.selectedTreeWidget.headerItem().setText(5, "6")
        self.selectedTreeWidget.header().setCascadingSectionResizes(True)
        self.selectedTreeWidget.header().setDefaultSectionSize(80)
        self.selectedTreeWidget.header().setHighlightSections(True)
        self.selectedTreeWidget.header().setMinimumSectionSize(30)
        self.selectedTreeWidget.header().setSortIndicatorShown(False)
        self.selectedTreeWidget.header().setStretchLastSection(False)
        self.liveResComboBox = QtWidgets.QComboBox(mainDialog)
        self.liveResComboBox.setGeometry(QtCore.QRect(600, 60, 51, 20))
        self.liveResComboBox.setObjectName("liveResComboBox")
        self.deleteCapturePushButton = QtWidgets.QPushButton(mainDialog)
        self.deleteCapturePushButton.setEnabled(False)
        self.deleteCapturePushButton.setGeometry(QtCore.QRect(680, 580, 161, 34))
        self.deleteCapturePushButton.setObjectName("deleteCapturePushButton")
        self.takePicturePushButton = QtWidgets.QPushButton(mainDialog)
        self.takePicturePushButton.setEnabled(False)
        self.takePicturePushButton.setGeometry(QtCore.QRect(820, 640, 88, 34))
        self.takePicturePushButton.setObjectName("takePicturePushButton")

        self.retranslateUi(mainDialog)
        QtCore.QMetaObject.connectSlotsByName(mainDialog)

    def retranslateUi(self, mainDialog):
        _translate = QtCore.QCoreApplication.translate
        mainDialog.setWindowTitle(_translate("mainDialog", "OMD Camera Control"))
        self.isoComboBox.setAccessibleName(_translate("mainDialog", "isospeedvalue"))
        self.isoLabel.setText(_translate("mainDialog", "Iso speed value"))
        self.focalComboBox.setAccessibleName(_translate("mainDialog", "focalvalue"))
        self.focalLabel.setText(_translate("mainDialog", "focal length value"))
        self.shutComboBox.setAccessibleName(_translate("mainDialog", "shutspeedvalue"))
        self.shutLabel.setText(_translate("mainDialog", "shut speed value"))
        self.expCompComboBox.setAccessibleName(_translate("mainDialog", "expcomp"))
        self.expCompLabel.setText(_translate("mainDialog", "expose compensation"))
        self.takeModeLabel.setText(_translate("mainDialog", "take mode"))
        self.addCapturePushButton.setText(_translate("mainDialog", "Add to capture list"))
        self.connectedLabel.setText(_translate("mainDialog", "not connected"))
        self.liveStreamLabel.setText(_translate("mainDialog", "Live Stream"))
        self.setAsCurrentPushButton.setText(_translate("mainDialog", "Set values"))
        self.liveIsoLabel.setText(_translate("mainDialog", "Iso"))
        self.liveFocalLabel.setText(_translate("mainDialog", "focal"))
        self.liveShutLabel.setText(_translate("mainDialog", "shut"))
        self.liveExpLabel.setText(_translate("mainDialog", "exp"))
        self.deleteCapturePushButton.setText(_translate("mainDialog", "Delete from capture list"))
        self.takePicturePushButton.setText(_translate("mainDialog", "Take picture"))
