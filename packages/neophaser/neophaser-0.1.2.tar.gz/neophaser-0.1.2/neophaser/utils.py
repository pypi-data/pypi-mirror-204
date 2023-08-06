from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QSlider

class DecimalSlider(QSlider):
    decimalValueChanged = pyqtSignal(float)

    def __init__(self, orientation=Qt.Orientation.Horizontal, decimals=2, parent=None):
        super().__init__(orientation, parent)
        self._multiplier = 10 ** decimals

        # Connect the original valueChanged signal to a custom slot
        super().valueChanged.connect(self._on_value_changed)

    def setRange(self, minimum, maximum):
        super().setRange(int(minimum * self._multiplier), int(maximum * self._multiplier))
    
    def setTickInterval(self, interval):
        super().setTickInterval(int(interval * self._multiplier))

    def setValue(self, value):
        super().setValue(int(value * self._multiplier))

    def value(self):
        return super().value() / self._multiplier

    def setSingleStep(self, value):
        super().setSingleStep(int(value * self._multiplier))

    def singleStep(self):
        return super().singleStep() / self._multiplier

    def _on_value_changed(self, value):
        decimal_value = value / self._multiplier
        self.decimalValueChanged.emit(decimal_value)
