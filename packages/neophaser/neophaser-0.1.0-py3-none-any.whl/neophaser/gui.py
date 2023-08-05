import cv2
import imageio

import numpy as np

from PyQt6.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice, QUrl, QThread, QMutex, QMutexLocker, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QListWidget, QListWidgetItem, QComboBox, QHBoxLayout, QVBoxLayout, QFormLayout, QCheckBox, QSlider, QGroupBox, QSplitter, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QPixmap, QImage

from neophaser.board import ControllerBoard
from neophaser.controllers import controllers
from neophaser.options import OptionType
from neophaser.utils import DecimalSlider
from neophaser.visual import Visual, DataType

class VideoThread(QThread):
	frame_ready = pyqtSignal(np.ndarray)
	frame = 0

	def __init__(self, visual, parent=None):
		super().__init__(parent)
		self.visual = visual
		self.frames = visual.data.shape[0]
		self._running = True
		self.mutex = QMutex()

	def run(self):
		while self._running:
			self.frame = (self.frame + 1) % self.frames
			self.frame_ready.emit(self.visual.data[self.frame])
			QThread.msleep(30)
	
	def stop(self):
		with QMutexLocker(self.mutex):
			self._running = False


class MediaLoader(QWidget):
	loaded = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		# Media controls
		controls_layout = QHBoxLayout()
		layout.addLayout(controls_layout)

		open_file_button = QPushButton("Open")
		open_file_button.clicked.connect(self.open_file)
		controls_layout.addWidget(open_file_button)

		self.save_file_button = QPushButton("Save")
		self.save_file_button.clicked.connect(self.save_file)
		controls_layout.addWidget(self.save_file_button)
		self.save_file_button.hide()

		# Image and video display
		self.media_display = QLabel(self)
		# self.media_display.setScaledContents(True)
		# self.media_display.setMinimumSize(480, 270)
		layout.addWidget(self.media_display)

		self.setLayout(layout)

		# Media player
		self.media_player = QMediaPlayer(self)
		# self.video_widget = QVideoWidget(self)
		# self.media_player.setVideoOutput(self.video_widget)
		self.media_player.mediaStatusChanged.connect(self.media_status_changed)

		self.video_thread = None

	def open_file(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Open Media File", "", "Images (*.png *.jpg *.jpeg);;Videos (*.gif *.mp4 *.avi)")

		if file_path:
			self.media_player.setSource(QUrl.fromLocalFile(file_path))

			self.visual = Visual(file_path)
			self.data = self.visual.data

			self.loaded.emit()

			self.save_file_button.show()

			self.set_data(self.visual)
	
	def set_data(self, visual):
		self.visual = visual
		self.data = self.visual.data

		if visual.type == DataType.IMAGE:
			self.update_frame(self.data)
		elif self.visual.type == DataType.VIDEO:
			if self.video_thread:
				self.video_thread.stop()
				self.video_thread.wait()
			self.video_thread = VideoThread(self.visual)
			self.video_thread.frame_ready.connect(self.update_frame)
			self.video_thread.start()
	
	def update_frame(self, frame):
		self.media_display.setPixmap(QPixmap.fromImage(QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888).rgbSwapped()))
	
	def save_file(self):
		file_path, _ = QFileDialog.getSaveFileName(parent=self, caption='Save File', directory='', filter="Images (*.png *.jpg *.jpeg);;Animated (*.gif);;All files (*)")
		

		if file_path:
			if self.visual.type == DataType.IMAGE:
				cv2.imwrite(file_path, self.visual.data)
			elif self.visual.type == DataType.VIDEO:
				imageio.mimwrite(file_path, self.visual.data, fps=30)

	def media_status_changed(self, status):
		if status == QMediaPlayer.MediaStatus.EndOfMedia:
			self.video_widget.setHidden(True)
			self.media_display.setHidden(False)
			self.layout().removeWidget(self.video_widget)

class EffectOptionsWidget(QWidget):
	render = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		self.setLayout(QVBoxLayout())

		self.options_stack = QGroupBox()
		self.options_stack.setMinimumWidth(400)
		self.options_layout = QFormLayout()
		self.options_stack.setLayout(self.options_layout)

		self.layout().addWidget(self.options_stack)
	
	def set_options(self, effect):
		self.layout().removeWidget(self.options_stack)

		self.options_stack = QGroupBox()
		self.options_stack.setMinimumWidth(450)
		self.options_layout = QFormLayout()
		self.options_stack.setLayout(self.options_layout)

		for option in effect.options.values():
			option.callback = lambda v, opt=option: (
				setattr(opt, "value", v),
				self.render.emit(),
			)

			if option.type == OptionType.CHECKBOX:
				checkbox = QCheckBox()
				checkbox.setValue(option.value)
				checkbox.stateChanged.connect(option.callback)
				self.options_layout.addRow(option.name, checkbox)
			elif option.type == OptionType.DROPDOWN:
				dropdown = QComboBox()
				for drop in option.options:
					dropdown.addItem(drop)
				dropdown.setCurrentText(option.value)
				dropdown.currentTextChanged.connect(option.callback)
				self.options_layout.addRow(option.name, dropdown)
			elif option.type == OptionType.RANGE_SLIDER:
				if option.interval < 1:
					slider = DecimalSlider()
					# slider.setValue(option.value)
					slider.decimalValueChanged.connect(option.callback)
				else:
					slider = QSlider(orientation=Qt.Orientation.Horizontal)
					# slider.setValue(int(option.value))
					slider.valueChanged.connect(option.callback)
				slider.setMinimumWidth(250)
				slider.setRange(option.min, option.max)
				slider.setTickPosition(QSlider.TickPosition.TicksBelow)
				slider.setTickInterval(option.interval)
				self.options_layout.addRow(option.name, slider)

		self.options_stack.setLayout(self.options_layout)
		self.layout().addWidget(self.options_stack)
		
class DraggableListWidget(QListWidget):
	render = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setDragEnabled(True)
		self.viewport().setAcceptDrops(True)
		self.setDropIndicatorShown(True)
		self.setDragDropMode(QListWidget.DragDropMode.InternalMove)

	def mimeData(self, items):
		mime_data = QMimeData()
		encoded_data = QByteArray()
		stream = QDataStream(encoded_data, QIODevice.OpenModeFlag.WriteOnly)

		for item in items:
			stream.writeQString(item.text())

		mime_data.setData('application/x-qabstractitemmodeldatalist', encoded_data)
		return mime_data

	def dropMimeData(self, index, mime_data, action):
		if not mime_data.hasFormat('application/x-qabstractitemmodeldatalist'):
			return False

		encoded_data = mime_data.data('application/x-qabstractitemmodeldatalist')
		stream = QDataStream(encoded_data, QIODevice.OpenModeFlag.ReadOnly)

		while not stream.atEnd():
			text = stream.readQString()
			self.insertItem(index, QListWidgetItem(text))
			index += 1

		return True
	
	def mousePressEvent(self, event):
		item = self.itemAt(event.pos())
		if not item:
			self.clearSelection()
			self.setCurrentItem(None)
		super().mousePressEvent(event)

class BoardWidget(QWidget):
	render = pyqtSignal()

	def __init__(self, board, parent=None):
		super().__init__(parent)

		self.effects = list(controllers.keys())

		self.board = board

		self.init_ui()

	def init_ui(self):
		self.setLayout(QVBoxLayout())

		# Splitter for draggable list and options widget
		splitter = QSplitter(Qt.Orientation.Horizontal)
		self.layout().addWidget(splitter)

		# Draggable list widget
		self.list_widget = DraggableListWidget()
		splitter.addWidget(self.list_widget)
		self.list_widget.currentItemChanged.connect(self.show_effect_options)

		# Controls for adding and removing items
		controls_layout = QHBoxLayout()
		self.layout().addLayout(controls_layout)

		self.combo_box = QComboBox()
		controls_layout.addWidget(self.combo_box)

		add_button = QPushButton('+')
		add_button.clicked.connect(self.add_item)
		controls_layout.addWidget(add_button)

		remove_button = QPushButton('-')
		remove_button.clicked.connect(self.remove_item)
		controls_layout.addWidget(remove_button)

		# Dynamic options widget
		self.effect_options_widget = EffectOptionsWidget()
		splitter.addWidget(self.effect_options_widget)
		self.effect_options_widget.set_options(self.board)
		self.effect_options_widget.render.connect(self.render.emit)

		self.populate_dropdown()

	def populate_dropdown(self):
		self.combo_box.addItems(self.effects)

	def add_item(self):
		item_text = self.combo_box.currentText()
		self.list_widget.addItem(item_text)

		controller_item = controllers[item_text]()
		self.board.append(controller_item)

		self.render.emit()

	def remove_item(self):
		current_item = self.list_widget.currentItem()
		if current_item is not None:
			row = self.list_widget.row(current_item)
			self.list_widget.takeItem(row)
			self.board.remove(self.board[row])
		
		self.render.emit()

	def show_effect_options(self, current, previous):
		if current is not None:
			item_index = self.list_widget.row(current)
			effect_item = self.board[item_index]
			self.effect_options_widget.set_options(effect_item)  # Just an example to change options based on index
		else:
			self.effect_options_widget.set_options(self.board)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("neophaser")

		self.layout = QGridLayout()

		# button = QPushButton("Quit")
		# button.pressed.connect(self.close)
		# layout.addWidget(button, 0, 0)

		self.media_player = MediaLoader()
		self.media_player.loaded.connect(self.load_board)
		self.layout.addWidget(self.media_player, 0, 0)

		widget = QWidget()
		widget.setLayout(self.layout)
		self.setCentralWidget(widget)
		self.show()
	
	def load_board(self):
		self.visual = self.media_player.visual
		self.data = self.visual.data

		self.board = ControllerBoard(self.visual)
		board_manager = BoardWidget(self.board)

		board_manager.render.connect(self.process_visual)

		self.layout.addWidget(board_manager, 0, 1)
	
	def process_visual(self):
		self.visual.data = self.board.process()
		self.media_player.set_data(self.visual)