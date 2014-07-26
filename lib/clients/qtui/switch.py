import sys
from PyQt4 import QtGui, QtCore

class TextChangingButton(QtGui.QPushButton):
    """Button that changes its text to ON or OFF and colors when it's pressed""" 
    def __init__(self, parent = None):
        super(TextChangingButton, self).__init__(parent)
        self.setCheckable(True)
        self.setFont(QtGui.QFont('MS Shell Dlg 2',pointSize=10))
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        #connect signal for appearance changing
        self.toggled.connect(self.setAppearance)
        self.setAppearance(self.isDown())
    
    def setAppearance(self, down):
        if down:
            self.setText('Closed')
            self.setPalette(QtGui.QPalette(QtCore.Qt.darkGreen))
        else:
            self.setText('Opened')
            self.setPalette(QtGui.QPalette(QtCore.Qt.black))
    
    def sizeHint(self):
        return QtCore.QSize(37, 26)

class QCustomSwitchChannel(QtGui.QFrame):
    def __init__(self, title, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFrameStyle(0x0001 | 0x0030)
        self.makeLayout(title)
    
    def makeLayout(self, title):
        layout = QtGui.QGridLayout()
        title = QtGui.QLabel(title)
        title.setFont(QtGui.QFont('MS Shell Dlg 2',pointSize=16))
        layout.addWidget(title, 0,0,1,3)
        
        #editable fields

        self.TTLswitch = TextChangingButton()
        layout.addWidget(self.TTLswitch, 1,0, 2,1)          
        self.setLayout(layout)
    

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    icon = QCustomSwitchChannel('369')
    icon.show()
    app.exec_()