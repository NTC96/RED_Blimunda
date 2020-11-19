#classe que define as funcoes que enviam e recebem dados terra-ar e ar-terra



print("hello LORA")

class LORA:
	"""docstring for LORA"""

	true_key=""
	msg_received =[]
	def __init__(self,COMMS_KEY):
		true_key="RED_ROCKS!!"
		#do lora inits here
	def lora_receive(self):
			#do stuff here
		msg_received = ["datatype","value","key"]
		return msg_received


	def lora_send(self,datatype,value):
			#do stuff here
		msg_sent = ["datatype","value","key"]
		return msg_sent
	

	def verify_key(self,key):

		if strcmp(key,true_key):
			return True 
		else:
			return False


		