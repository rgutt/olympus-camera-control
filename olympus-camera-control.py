import sys
#from PySide2.QtUiTools import QUiLoader
#from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QSlider, QTreeWidget, QTreeWidgetItem,QDialog
#from PySide2.QtCore import QFile, QObject, Signal, Slot, QTimer, QThread, Qt
#from PySide2.QtGui import QImage, QPixmap

#from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QSlider, QTreeWidget,QDialog
#from PyQt5.QtCore import QFile, QObject, pyqtSignal, pyqtSlot, QTimer, QThread, Qt
#from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import QDialog,QApplication, QTreeWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QBrush, QPen

#from PyQt5 import QtCore, QtGui, QtWidgets

import omddialog as omdDialog
import time
import omd as omd
import numpy as np
import olylivede as olive
import liveViewFeatures as lvf
import cv2
import binascii
import io
from PIL import Image
from requests_retry_session import requests_retry_session, requests
import socket

def get_qimage(image: np.ndarray):
    assert (np.max(image) <= 255)
    image8 = image.astype(np.uint8, order='C', casting='unsafe')
    image_rgb = cv2.cvtColor(image8, cv2.COLOR_BGR2RGB)
    height, width, colors = image_rgb.shape
    bytesPerLine = 3 * width
    image = QImage(image_rgb.data, width, height, bytesPerLine,
                       QImage.Format_RGB888)
    image = image.rgbSwapped()
    return image

class liveStreamThread(QThread):
    changePixmap = pyqtSignal(QImage)
    cameraCurrentValues = pyqtSignal(object)
    def run(self):
        self.init_run = True
        self.UDP_IP = ''
        self.UDP_PORT = 1234
        self.omd = omd.OMD()
        self.omd.stop_liveview()

        self.cameraCurrentValuesDict = {}
        with socket.socket(socket.AF_INET, socket.SocketKind.SOCK_DGRAM) as s:
            s.bind((self.UDP_IP, self.UDP_PORT))
            self.omd.start_liveview(self.UDP_PORT)
            while True:
                try:
                    s.settimeout(1)
                    data = s.recvfrom(2048)[0]
                    frame = olive.Frame(data)
                    sub_frame_id = 0
                    frame_broken = False
                    while not frame.has_finished() and frame.has_started():
                        s.settimeout(1)
                        try:
                            data = s.recvfrom(2048)[0]
                            frame_broken = frame.add_subframe(data)
                        except socket.timeout:
                            frame_broken = True
                            print("Timeout exception raised (inner)")

                        sub_frame_id = sub_frame_id + 1
                        if sub_frame_id == 100 or frame_broken:
                            print("Ill frame", frame_broken,frame.has_finished(),frame.has_started())
                            frame_broken = True
                            print(sub_frame_id)
                            break
                    if not frame_broken:
                        if frame.has_finished() and frame.has_started():
                            try:
                                picture_stream = io.BytesIO(frame.frame)
                                picture = Image.open(picture_stream)
                                convertToQtFormat = get_qimage(np.array(picture))
                                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                                self.changePixmap.emit(p)
                                self.cameraCurrentValues.emit(frame.cameraCurrenValues)
                                if self.init_run:
                                    self.init_run = False

                            except Exception as err:
                                print(format(err))
                except socket.timeout:
                    print("Timeout exception raised (outer)")
                    self.omd.start_liveview(self.UDP_PORT)
        self.omd.stop_liveview()


class omdForm(QDialog):
    def __init__(self, parent=None):

        super(omdForm, self).__init__(parent)
        self.window = omdDialog.Ui_mainDialog()
        self.window.setupUi(self)
        self.isinit = False
        self.rangeset = False

        self.lvf =lvf.liveViewFeatures()



        self.omd = omd.OMD()
        self.window.connectedSlider.sliderReleased.connect(self.init_ComboBox)
        self.window.setAsCurrentPushButton.clicked.connect(self.set_camera_values)


        self.dictComboBox = {"takemode" : self.window.takeModeComboBox,\
                            "isospeedvalue" : self.window.isoComboBox,\
                            "focalvalue" : self.window.focalComboBox,\
                            "shutspeedvalue" : self.window.shutComboBox,\
                            "expcomp" : self.window.expCompComboBox}

        self.dictLiveLabel = {"isospeedvalue" : self.window.liveIsoLabel,\
                            "focalvalue" : self.window.liveFocalLabel,\
                            "shutspeedvalue" : self.window.liveShutLabel,\
                            "expcomp" : self.window.liveExpLabel}

        self.window.liveResComboBox.activated.connect(self.changeLiveViewResolution)
        self.window.selectedTreeWidget.setHeaderLabels(['check','takemode','iso','fstop','shut','exp'])
        self.dictHeaderMap = {"takemode" : "takemode",\
                            "iso" : "isospeedvalue",\
                            "fstop" : "focalvalue",\
                            "shut" : "shutspeedvalue",\
                            "exp" : "expcomp"}

        self.init_ComboBox()


        self.window.takeModeComboBox.activated.connect(self.enable_Combox)

        self.window.addCapturePushButton.clicked.connect(self.addCapture)

        self.window.deleteCapturePushButton.clicked.connect(self.deleteCapture)

        self.window.takePicturePushButton.clicked.connect(self.takePicture)

        self.lsth = liveStreamThread(self)
        self.lsth.changePixmap.connect(self.setImage)
        self.lsth.cameraCurrentValues.connect(self.setCameraCurrentValues)
        self.lsth.start()


        self.window.liveStreamLabel.mousePressEvent = self.setFocusPoint


        self.show()


    @pyqtSlot()
    def setFocusPoint(self, event):
        self.lvf.frameCount = 90
        self.lvf.xPos = event.x()
        self.lvf.yPos = event.y()
        self.lvf.xLen = 60
        self.lvf.yLen = 60
        self.omd.assignafframe(self.lvf.xPos,self.lvf.yPos)



    @pyqtSlot()
    def changeLiveViewResolution(self):
        self.omd.change_live_stream_resolution(self.window.liveResComboBox.currentText())

    @pyqtSlot(object)
    def setCameraCurrentValues(self,cameraCurrentValues):
        for setting in cameraCurrentValues:
            self.dictLiveLabel[setting].setText(cameraCurrentValues[setting][0])
            self.omd.cam_properties.set_current_value(setting,cameraCurrentValues[setting][0])


        if not self.rangeset:
            max_focalvalue = cameraCurrentValues["focalvalue"][2]
            self.omd.cam_properties.change_allowed_values_range("focalvalue",\
                cameraCurrentValues["focalvalue"][1],cameraCurrentValues["focalvalue"][2])
            self.window.focalComboBox.clear()
            self.window.focalComboBox.addItems(self.omd.cam_properties.get_allowed_values("focalvalue"))
            self.rangeset = True

    @pyqtSlot(QImage)
    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        if self.lvf.frameCount > 0:
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.green,self.lvf.tLine, Qt.SolidLine))
            painter.drawRect(self.lvf.xPos-self.lvf.xLen//2, self.lvf.yPos-self.lvf.yLen//2, self.lvf.xLen, self.lvf.yLen)
            self.lvf.frameCount -= 1
            painter.end()



        self.window.liveStreamLabel.setPixmap(pixmap)



    @pyqtSlot()
    def takePicture(self):
        self.lsth.Pause = True
        self.omd.assignafframe(self.lvf.xPos,self.lvf.yPos)
        for i in range(self.window.selectedTreeWidget.topLevelItemCount()):
            for j in range(1,self.window.selectedTreeWidget.columnCount()):
                header = self.window.selectedTreeWidget.headerItem().text(j)
                value = self.window.selectedTreeWidget.topLevelItem(i).text(j)
                setting = self.dictHeaderMap[header]
                self.omd.set_setting(setting, value)
                self.omd.cam_properties.set_current_value(setting,value)
            self.omd.take_picture()
            print(i)
        time.sleep(self.window.selectedTreeWidget.topLevelItemCount())
        self.lsth.Pause = False
        self.omd.change_live_stream_resolution(self.window.liveResComboBox.currentText())
        self.omd.assignafframe(self.lvf.xPos,self.lvf.yPos)




    @pyqtSlot()
    def addCapture(self):
        item = QTreeWidgetItem()
        item.setCheckState(0,Qt.Unchecked)
        i = 1
        for setting in self.dictComboBox:
            item.setText(i, self.dictComboBox[setting].currentText())
            i += 1
        self.window.selectedTreeWidget.addTopLevelItem(item)
        self.window.deleteCapturePushButton.setEnabled(True)
        self.window.takePicturePushButton.setEnabled(True)

    @pyqtSlot()
    def deleteCapture(self):
        i = 0
        while self.window.selectedTreeWidget.topLevelItemCount() > 0 and i < self.window.selectedTreeWidget.topLevelItemCount():
            if self.window.selectedTreeWidget.topLevelItem(i).checkState(0) == 2:
                self.window.selectedTreeWidget.takeTopLevelItem(i)
            else:
                i += 1
        if self.window.selectedTreeWidget.topLevelItemCount() == 0:
            self.window.deleteCapturePushButton.setEnabled(False)
            self.window.takePicturePushButton.setEnabled(False)


    @pyqtSlot()
    def init_ComboBox(self):
        if (self.check_connection() and not self.isinit):
            self.isinit = True
            self.omd.reinit()
            self.window.takeModeComboBox.addItem("No takemode selected")
            for setting in self.dictComboBox:
                self.dictComboBox[setting].addItems(self.omd.cam_properties.get_allowed_values(setting))
                self.dictComboBox[setting].setCurrentText(self.omd.cam_properties.get_current_value(setting))
            self.dictComboBox["takemode"].removeItem(self.window.takeModeComboBox.findText("ART"))
            self.dictComboBox["takemode"].removeItem(self.window.takeModeComboBox.findText("movie"))
            for res in self.omd.cam_properties.get_allowed_live_view_res():
                self.window.liveResComboBox.addItem(res)
            self.window.liveResComboBox.setCurrentText(self.omd.cam_properties.get_live_view_res()[1])
            self.enable_Combox()



    @pyqtSlot()
    def enable_Combox(self):
        if (self.window.takeModeComboBox.currentText() == "A"):
            self.window.isoComboBox.setEnabled(True)
            self.window.focalComboBox.setEnabled(True)
            self.window.shutComboBox.setEnabled(False)
            self.window.expCompComboBox.setEnabled(True)
            self.window.addCapturePushButton.setEnabled(True)
            self.window.setAsCurrentPushButton.setEnabled(True)
        elif (self.window.takeModeComboBox.currentText() == "S"):
            self.window.isoComboBox.setEnabled(True)
            self.window.focalComboBox.setEnabled(False)
            self.window.shutComboBox.setEnabled(True)
            self.window.expCompComboBox.setEnabled(True)
            self.window.addCapturePushButton.setEnabled(True)
            self.window.setAsCurrentPushButton.setEnabled(True)
        elif (self.window.takeModeComboBox.currentText() == "P"):
            self.window.isoComboBox.setEnabled(True)
            self.window.focalComboBox.setEnabled(False)
            self.window.shutComboBox.setEnabled(False)
            self.window.expCompComboBox.setEnabled(True)
            self.window.addCapturePushButton.setEnabled(True)
            self.window.setAsCurrentPushButton.setEnabled(True)
        elif (self.window.takeModeComboBox.currentText() == "M"):
            self.window.isoComboBox.setEnabled(True)
            self.window.focalComboBox.setEnabled(True)
            self.window.shutComboBox.setEnabled(True)
            self.window.expCompComboBox.setEnabled(False)
            self.window.addCapturePushButton.setEnabled(True)
            self.window.setAsCurrentPushButton.setEnabled(True)
        elif (self.window.takeModeComboBox.currentText() == "iAuto"):
            self.window.isoComboBox.setEnabled(False)
            self.window.focalComboBox.setEnabled(False)
            self.window.shutComboBox.setEnabled(False)
            self.window.expCompComboBox.setEnabled(False)
            self.window.addCapturePushButton.setEnabled(True)
            self.window.setAsCurrentPushButton.setEnabled(True)
        else:
            self.window.isoComboBox.setEnabled(False)
            self.window.focalComboBox.setEnabled(False)
            self.window.shutComboBox.setEnabled(False)
            self.window.expCompComboBox.setEnabled(False)
            self.window.addCapturePushButton.setEnabled(False)
            self.window.setAsCurrentPushButton.setEnabled(False)


    @pyqtSlot()
    def check_connection(self):
        if self.omd.islive():
            self.window.connectedLabel.setStyleSheet('color: green')
            self.window.connectedLabel.setText('connected')
            self.window.connectedSlider.setStyleSheet('color: green')
            self.window.connectedSlider.setSliderPosition(1)
            return True
        else:
            self.window.connectedLabel.setStyleSheet('color: red')
            self.window.connectedLabel.setText('not connected')
            self.window.connectedSlider.setStyleSheet('color: red')
            self.window.connectedSlider.setSliderPosition(0)
            return False
    def set_camera_values(self):
        for setting in self.dictComboBox:
            self.omd.cam_properties.set_current_value(setting,self.dictComboBox[setting].currentText())
            self.omd.set_setting(setting,self.omd.cam_properties.get_current_value(setting))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = omdForm()
    sys.exit(app.exec_())
