import time
from machine import Pin
import cfg.config as config

class Hardware:
	def __init__(self):
		
		self.led1 = Pin(0, Pin.OUT)
		
	def blink_led1(self, times = 1, on_ms = 100, off_ms = 100):
		for i in range(times):
			self.led1.On()
			time.sleep_ms(on_ms)
			self.led1.Off()
			time.sleep_ms(off_ms)