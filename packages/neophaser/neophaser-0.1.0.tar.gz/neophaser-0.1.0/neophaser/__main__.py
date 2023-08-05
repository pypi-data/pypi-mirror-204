import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from neophaser.gui import MainWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setApplicationDisplayName("neophaser")
	app.setWindowIcon(QIcon((os.path.join(os.path.dirname(os.path.realpath(__file__)), '../icon.png'))))
	w = MainWindow()
	app.exec()
