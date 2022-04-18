from micropySX126X.lib.sx1262 import SX1262
from src.callback import Callback

def setup():
	sx = SX1262(cs='P5',irq='P6',rst='P7',gpio='P8')

	# LoRa
	sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
		power=-5, currentLimit=60.0, preambleLength=8,
		implicit=False, implicitLen=0xFF,
		crcOn=True, txIq=False, rxIq=False,
		tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True
	)

	sx.setBlockingCallback(False, Callback.receive_callback_function)

	return sx