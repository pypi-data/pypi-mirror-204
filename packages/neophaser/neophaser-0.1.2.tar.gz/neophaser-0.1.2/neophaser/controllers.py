from pedalboard import (
	Chorus,
	Delay,
	HighShelfFilter,
	LowShelfFilter,
	Phaser,
	Reverb,
	Resample,
)

from neophaser.options import EffectController, EffectOption, OptionType

class ChorusController(EffectController):
	def __init__(self):
		self.effect = Chorus()

		self.options = {
			"rate_hz": EffectOption("Rate (Hz)", OptionType.RANGE_SLIDER, min=0, max=100, interval=1),
			"depth": EffectOption("Depth", OptionType.RANGE_SLIDER, min=0, max=50, interval=2),
			"centre_delay_ms": EffectOption("Center Delay (ms)", OptionType.RANGE_SLIDER, min=0, max=20, interval=1),
			"feedback": EffectOption("Feedback", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1)
		}

class DelayController(EffectController):
	def __init__(self):
		self.effect = Delay()

		self.options = {
			"delay_seconds": EffectOption("Delay (s)", OptionType.RANGE_SLIDER, min=0, max=2, interval=0.1),
			"feedback": EffectOption("Feedback", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"mix": EffectOption("Mix", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1)
		}

class HighShelfFilterController(EffectController):
	def __init__(self):
		self.effect = HighShelfFilter()

		self.options = {
			"cutoff_frequency_hz": EffectOption("Cutoff Frequency (Hz)", OptionType.RANGE_SLIDER, min=1, max=1000, interval=10),
			"gain_db": EffectOption("Resonance", OptionType.RANGE_SLIDER, min=-20, max=20, interval=2),
			"q": EffectOption("Q", OptionType.RANGE_SLIDER, min=1, max=3, interval=0.2)
		}	

class LowShelfFilterController(EffectController):
	def __init__(self):
		self.effect = LowShelfFilter()

		self.options = {
			"cutoff_frequency_hz": EffectOption("Cutoff Frequency (Hz)", OptionType.RANGE_SLIDER, min=1, max=1000, interval=10),
			"gain_db": EffectOption("Resonance", OptionType.RANGE_SLIDER, min=-20, max=20, interval=2),
			"q": EffectOption("Q", OptionType.RANGE_SLIDER, min=1, max=3, interval=0.2)
		}

class PhaserController(EffectController):
	def __init__(self):
		self.effect = Phaser()

		self.options = {
			"rate_hz": EffectOption("Rate (hz)", OptionType.RANGE_SLIDER, min=0, max=2, interval=0.1),
			"depth": EffectOption("Depth", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"centre_frequency_hz": EffectOption("Center Frequency (Hz)", OptionType.RANGE_SLIDER, min=500, max=2000, interval=500),
			"feedback": EffectOption("Feedback", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"mix": EffectOption("Mix", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
		}

class ReverbController(EffectController):
	def __init__(self):
		self.effect = Reverb()

		self.options = {
			"room_size": EffectOption("Room Size", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"damping": EffectOption("Damping", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"wet_level": EffectOption("Wet Level", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"dry_level": EffectOption("Dry Level", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"width": EffectOption("Width", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
			"freeze_mode": EffectOption("Freeze Mode", OptionType.RANGE_SLIDER, min=0, max=1, interval=0.1),
		}

class ResampleController(EffectController):
	def __init__(self):
		self.effect = Resample()

		self.options = {
			"target_sample_rate": EffectOption("Target Sample Rate", OptionType.RANGE_SLIDER, min=0, max=20000, interval=1000),
		}

controllers = {
	"Chorus": ChorusController,
	"Delay": DelayController,
	"HighShelf": HighShelfFilterController,
	"LowShelf": LowShelfFilterController,
	"Phaser": PhaserController,
	"Reverb": ReverbController,
	"Resample": ResampleController,
}