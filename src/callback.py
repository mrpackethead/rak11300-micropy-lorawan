from micropySX126X.lib.sx1262 import SX1262
from src.encryption_aes import AES
import cfg.config as config
import gc


class Callback:
	def __init__(self, sx):
		self.sx = sx

		self.device_address = config.lorawan_cfg.device_address,
		self.app_key = config.lorawan_cfg.app_cfg,
		self.network_key = config.lorawan_cfg.network_key,

	def receive_callback_function(self, events):
		
		if events & SX1262.RX_DONE:
			msg, err = self.sx.recv()
			error = SX1262.STATUS[err]

			aes = AES(
				self.device_address,
				self.app_key,
				self.network_key,
				self.frame_counter
			)
			
			decoded_msg = aes.decrypt_payload(msg)

			print('Receive: {}, {}'.format(decoded_msg, error))

			#TODO. need to decode the content of the mesage more throughly.. 
			

		
		elif events & SX1262.TX_DONE:
			print('TX done.')

		gc.collect()
