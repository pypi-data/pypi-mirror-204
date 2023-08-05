import enum
import mimetypes

import cv2
import numpy as np

# image and video file types enum
class DataType(enum.Enum):
	IMAGE = enum.auto()
	VIDEO = enum.auto()

class Visual:
	def __init__(self, path):
		self.path = path

		mime_type, _ = mimetypes.guess_type(self.path)

		if mime_type.startswith("video") or mime_type == "image/gif":
			self.type = DataType.VIDEO
			self.data = self._read_video()
		elif mime_type.startswith("image"):
			self.type = DataType.IMAGE
			self.data = self._read_image()
		else:
			raise ValueError("The file is neither an image nor a video.")

		self.original = self.data

		self.effects = []

	def _read_image(self):
		return cv2.imread(self.path)

	def _read_video(self):
		cap = cv2.VideoCapture(self.path)

		num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

		height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

		video_array = np.empty((num_frames, height, width, 3), dtype=np.uint8)

		# Read the video frames and store them in the numpy array
		frame_index = 0
		while cap.isOpened():
			ret, frame = cap.read()
			if not ret:
				break

			# Store the frame in the numpy array
			video_array[frame_index] = frame
			frame_index += 1

		# Release the video capture object
		cap.release()

		return video_array
