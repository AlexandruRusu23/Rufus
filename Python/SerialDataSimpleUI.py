# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SerialDataSimpleUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import DataManager
import threading

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self._dataManager = DataManager.DataManager('/dev/ttyUSB0', 9600, 'test_create_DB')
        self._starter = 0
        self._stoper = 0

    def __del__(self):
        print 'End'

    def Start(self):
        if (self._starter < 1):
            self._dataManager.start()
            self._starter = self._starter + 1

    def Stop(self):
        if (self._stoper < 1):
            self._dataManager.Stop()
            self._stoper = self._stoper + 1

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(384, 417)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelTemperature = QtGui.QLabel(Form)
        self.labelTemperature.setObjectName(_fromUtf8("labelTemperature"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelTemperature)
        self.lineEditTemperature = QtGui.QLineEdit(Form)
        self.lineEditTemperature.setEnabled(True)
        self.lineEditTemperature.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditTemperature.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditTemperature.setReadOnly(True)
        self.lineEditTemperature.setObjectName(_fromUtf8("lineEditTemperature"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditTemperature)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtGui.QFormLayout.FieldRole, spacerItem)
        self.labelHumidity = QtGui.QLabel(Form)
        self.labelHumidity.setObjectName(_fromUtf8("labelHumidity"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelHumidity)
        self.lineEditHumidity = QtGui.QLineEdit(Form)
        self.lineEditHumidity.setEnabled(True)
        self.lineEditHumidity.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditHumidity.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditHumidity.setReadOnly(True)
        self.lineEditHumidity.setObjectName(_fromUtf8("lineEditHumidity"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditHumidity)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtGui.QFormLayout.FieldRole, spacerItem1)
        self.labelLighting1 = QtGui.QLabel(Form)
        self.labelLighting1.setObjectName(_fromUtf8("labelLighting1"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelLighting1)
        self.lineEditLighting1 = QtGui.QLineEdit(Form)
        self.lineEditLighting1.setEnabled(True)
        self.lineEditLighting1.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditLighting1.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditLighting1.setReadOnly(True)
        self.lineEditLighting1.setObjectName(_fromUtf8("lineEditLighting1"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEditLighting1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtGui.QFormLayout.FieldRole, spacerItem2)
        self.labelLighting2 = QtGui.QLabel(Form)
        self.labelLighting2.setObjectName(_fromUtf8("labelLighting2"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.labelLighting2)
        self.lineEditLighting2 = QtGui.QLineEdit(Form)
        self.lineEditLighting2.setEnabled(True)
        self.lineEditLighting2.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditLighting2.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditLighting2.setReadOnly(True)
        self.lineEditLighting2.setObjectName(_fromUtf8("lineEditLighting2"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEditLighting2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(7, QtGui.QFormLayout.FieldRole, spacerItem3)
        self.labelGas1 = QtGui.QLabel(Form)
        self.labelGas1.setObjectName(_fromUtf8("labelGas1"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.labelGas1)
        self.lineEditGas1 = QtGui.QLineEdit(Form)
        self.lineEditGas1.setEnabled(True)
        self.lineEditGas1.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditGas1.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditGas1.setReadOnly(True)
        self.lineEditGas1.setObjectName(_fromUtf8("lineEditGas1"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.lineEditGas1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(9, QtGui.QFormLayout.FieldRole, spacerItem4)
        self.labelGas2 = QtGui.QLabel(Form)
        self.labelGas2.setObjectName(_fromUtf8("labelGas2"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.labelGas2)
        self.lineEditGas2 = QtGui.QLineEdit(Form)
        self.lineEditGas2.setEnabled(True)
        self.lineEditGas2.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditGas2.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditGas2.setReadOnly(True)
        self.lineEditGas2.setObjectName(_fromUtf8("lineEditGas2"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.lineEditGas2)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(11, QtGui.QFormLayout.FieldRole, spacerItem5)
        self.labelMovement = QtGui.QLabel(Form)
        self.labelMovement.setObjectName(_fromUtf8("labelMovement"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.LabelRole, self.labelMovement)
        self.lineEditMovement = QtGui.QLineEdit(Form)
        self.lineEditMovement.setEnabled(True)
        self.lineEditMovement.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditMovement.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditMovement.setReadOnly(True)
        self.lineEditMovement.setObjectName(_fromUtf8("lineEditMovement"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.lineEditMovement)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(13, QtGui.QFormLayout.FieldRole, spacerItem6)
        self.labelDistance = QtGui.QLabel(Form)
        self.labelDistance.setObjectName(_fromUtf8("labelDistance"))
        self.formLayout.setWidget(14, QtGui.QFormLayout.LabelRole, self.labelDistance)
        self.lineEditDistance = QtGui.QLineEdit(Form)
        self.lineEditDistance.setEnabled(True)
        self.lineEditDistance.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEditDistance.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEditDistance.setText(_fromUtf8(""))
        self.lineEditDistance.setReadOnly(True)
        self.lineEditDistance.setObjectName(_fromUtf8("lineEditDistance"))
        self.formLayout.setWidget(14, QtGui.QFormLayout.FieldRole, self.lineEditDistance)
        self.horizontalLayout_2.addLayout(self.formLayout)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.startButton = QtGui.QPushButton(Form)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.verticalLayout_8.addWidget(self.startButton)
        self.startButton.clicked.connect(self.Start)
        self.stopButton = QtGui.QPushButton(Form)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.verticalLayout_8.addWidget(self.stopButton)
        self.stopButton.clicked.connect(self.Stop)

        self.showButton = QtGui.QPushButton(Form)
        self.showButton.setObjectName(_fromUtf8("showButton"))
        self.verticalLayout_8.addWidget(self.showButton)
        self.showButton.clicked.connect(self.PopulateData)

        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem8)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEditTemperature, self.lineEditHumidity)
        Form.setTabOrder(self.lineEditHumidity, self.lineEditLighting1)
        Form.setTabOrder(self.lineEditLighting1, self.lineEditLighting2)
        Form.setTabOrder(self.lineEditLighting2, self.lineEditGas1)
        Form.setTabOrder(self.lineEditGas1, self.lineEditGas2)
        Form.setTabOrder(self.lineEditGas2, self.lineEditMovement)
        Form.setTabOrder(self.lineEditMovement, self.lineEditDistance)
        Form.setTabOrder(self.lineEditDistance, self.startButton)
        Form.setTabOrder(self.startButton, self.stopButton)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.labelTemperature.setText(_translate("Form", "Temperature", None))
        self.labelHumidity.setText(_translate("Form", "Humidity", None))
        self.labelLighting1.setText(_translate("Form", "Lighting (1)", None))
        self.labelLighting2.setText(_translate("Form", "Lighting (2)", None))
        self.labelGas1.setText(_translate("Form", "Gas Concentration (1)", None))
        self.labelGas2.setText(_translate("Form", "Gas Concentration (2)", None))
        self.labelMovement.setText(_translate("Form", "Movement", None))
        self.labelDistance.setText(_translate("Form", "Distance (cm)", None))
        self.startButton.setText(_translate("Form", "Start", None))
        self.stopButton.setText(_translate("Form", "Stop", None))
        self.showButton.setText(_translate("Form", "Show", None))

    def PopulateData(self):
        if(self._starter > 0):
            myDict = self._dataManager.GetData()
            self.lineEditTemperature.setText(myDict['temperature'])
            self.lineEditLighting1.setText(myDict['light_1'])
            self.lineEditLighting2.setText(myDict['light_2'])
            self.lineEditGas1.setText(myDict['mq2_1'])
            self.lineEditGas2.setText(myDict['mq2_2'])
            self.lineEditHumidity.setText(myDict['humidity'])
            self.lineEditDistance.setText(myDict['distance'])
            self.lineEditMovement.setText(myDict['motion'])

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    app.exec_()
