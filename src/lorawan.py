from src.encryption_aes import AES
import gc
import random
import cfg.frequency_plans

class Lorawan:
	def __init__(self, lorawan_cfg, sx, hardware ):
		
		self.hardware = hardware
		self.sx = sx
		self.lorawan_cfg = lorawan_cfg
		self.freq_plan = cfg.frequency_plans[self.lorawan_cfg.freq_plan]
		

	def send_data(self, data, frame_counter, timeout=5):
		data_length = len(data)
		enc_data = bytearray(data_length)
		lora_pkt = bytearray(64)

		# Copy bytearray into bytearray for encryption
		enc_data[0:data_length] = data[0:data_length]

		# Encrypt data 
		aes = AES(
			self.lorawan_cfg.device_address,
			self.lorawan_cfg.app_key,
			self.lorawan_cfg.network_key,
			frame_counter = frame_counter
		)
		enc_data = aes.encrypt(enc_data)
		
		# Construct MAC Layer packet (PHYPayload)
		# MHDR (MAC Header) - 1 byte
		lora_pkt[0] = REG_DIO_MAPPING_1 # MType: unconfirmed data up, RFU / Major zeroed #TODO
		
		# MACPayload
		# FHDR (Frame Header): DevAddr (4 bytes) - short device address
		lora_pkt[1] = self._ttn_config.device_address[3]
		lora_pkt[2] = self._ttn_config.device_address[2]
		lora_pkt[3] = self._ttn_config.device_address[1]
		lora_pkt[4] = self._ttn_config.device_address[0]
		# FHDR (Frame Header): FCtrl (1 byte) - frame control
		lora_pkt[5] = 0x00
		# FHDR (Frame Header): FCnt (2 bytes) - frame counter
		lora_pkt[6] = self.frame_counter & 0x00FF
		lora_pkt[7] = (self.frame_counter >> 8) & 0x00FF
		# FPort - port field
		lora_pkt[8] = self._fport
		# Set length of LoRa packet
		lora_pkt_len = 9

		# load encrypted data into lora_pkt
		lora_pkt[lora_pkt_len : lora_pkt_len + data_length] = enc_data[0:data_length]

		# lora packet length now has header bytes
		lora_pkt_len += data_length

		# Calculate Message Integrity Code (MIC)
		# MIC is calculated over: MHDR | FHDR | FPort | FRMPayload
		mic = bytearray(4)
		mic = aes.calculate_mic(lora_pkt, lora_pkt_len, mic)

		# Load MIC in package
		lora_pkt[lora_pkt_len : lora_pkt_len + 4] = mic[0:4]
		# Recalculate packet length (add MIC length)
		lora_pkt_len += 4
		
		 
		# select a channel to operate on
		self.sx.setFrequency(self.freq_plan[random.getrandbits(3)])
		self.sx.send(lora_pkt)
		
		# blink led1
		self.hardware.blink_led1()

		#collect any garbage
		gc.collect()
		


		#send_packet
		   #set_lock(True)  # wait until RX_Done, lock and begin writing. Don't think we need this.
		   #begin_packet - writes some registers, and sets frequency
		   #write - writes out the data to the buffer
		   #end_packet - puts it in tx mode, and waits
		   #set_lock(False)
		   #blink_led
		   #collect_garbage
