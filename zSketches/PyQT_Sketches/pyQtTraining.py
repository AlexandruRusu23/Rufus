import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def window():
    app = QApplication(sys.argv)
    wid = QDialog()
    wid.setStyleSheet("QDialog {background-color: yellow}")
    b1 = QPushButton(wid)
    b1.setText("Hello world!")
    b1.move(50, 50)
    b1.clicked.connect(showDialog2)

    wid.setWindowTitle("2 btns")
    wid.show()
    sys.exit(app.exec_())

def showDialog():
    d = QDialog()
    b1 = QPushButton("Ok",d)
    b1.move(50, 50)
    d.setWindowTitle("Dialog")
    d.setWindowModality(Qt.ApplicationModal)
    d.exec_()

def showDialog2():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("This is a message box")
    msg.setInformativeText("Additional informations")
    msg.setWindowTitle("Message Box")
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)

    retval = msg.exec_()
    print "value of pressed message box button:", retval

def msgbtn(i):
    print "Button presed is:", i.text()

def b1_clicked():
    print "Button 1 clicked"

if __name__ == '__main__':
    window()
