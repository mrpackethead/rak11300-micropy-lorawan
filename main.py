from micropySX126X.lib.sx1262 import SX1262
import time
from src.setup import setup
from src.lorawan import Lorawan
import cfg.config as config
from src.callback import Callback

#setup the radio hardware
sx, hardware = setup()

#intialise the Lorawan layer
lorawan = Lorawan(
    lorawan_cfg=config.lorawan_cfg,
    sx=sx,
    hardware=hardware
)

#Intialise the Call back Function for receiving data and intialise it
callback = Callback(sx)
sx.setBlockingCallback(  
    blocking = False,
    callback = callback.receive_callback_function
)

frame_counter = 0

while True:
    data = b'SomeData'
    Lorawan.send_data(data, frame_counter, timeout=5, sx=sx)
    time.sleep(10)
