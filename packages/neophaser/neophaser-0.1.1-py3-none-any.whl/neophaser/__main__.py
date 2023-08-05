import sys
import pkg_resources

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from neophaser.gui import MainWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setApplicationDisplayName("neophaser")
	app.setWindowIcon(QIcon(pkg_resources.resource_filename('neophaser', 'assets/icon.png')))
	w = MainWindow()
	app.exec()
