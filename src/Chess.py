import sys
import controllers
from PySide import QtGui, QtCore

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)  
    win  = controllers.MainWindowController() 

    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
                app, QtCore.SLOT("quit()"))
    app.exec_()
