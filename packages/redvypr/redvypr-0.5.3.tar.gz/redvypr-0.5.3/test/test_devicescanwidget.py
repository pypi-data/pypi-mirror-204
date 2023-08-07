from PyQt5 import QtWidgets, QtCore, QtGui
import redvypr.gui
import sys
import redvypr


def main():
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    #print('Screen: %s' % screen.name())
    size = screen.size()
    #print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    width = int(rect.width()*4/5)
    height = int(rect.height()*2/3)

    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    devwidget = redvypr.gui.redvyprDeviceWidget()
    # Set the size

    layout.addWidget(devwidget)
    widget.resize(1000, 800)
    widget.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
