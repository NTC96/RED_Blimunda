#classe que define as funcoes que enviam e recebem dados terra-ar e ar-terra



print("hello LORA")

class LORA:
	"""docstring for LORA"""

	def __init__(self,COMMS_KEY):

		
		self.true_key="RED_ROCKS!!"

		self.msg_id_sent=0000
		self.msg_received =[]
		#do lora inits here
	def lora_receive(self):

		#do stuff here
		'''datatype = { COMMAND, FLIGHTMODE,cenas}
		Value = {test_airbrakes,"test_gps","test_altimetro", " ",outros_testes,StandBye,Flight]
		Key=
		'''
		msg_received = ["datatype","value","RED_ROCKS!!","msg_sent"] #[Datatype, Value, Key]
		return msg_received


	def lora_send(self,datatype,value):
			#do stuff here
		#msg_sent = ["datatype","value","key","msg_sent"]  #datatype = { "altitude","gps_data", "angles"}# value = valor
		msg_sent = []
		msg_sent.append(datatype)
		msg_sent.append(value)
		self.msg_id_sent+=1
		msg_sent.append(self.true_key)
		msg_sent.append(self.msg_id_sent)
		print("LORA MSG SENT", msg_sent)
		return msg_sent
	

	def verify_key(self,key):
		
		if key==self.true_key:
			
			return True 
		else:
			return False


		