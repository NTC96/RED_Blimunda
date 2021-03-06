#classe que define as funcoes que enviam e recebem dados terra-ar e ar-terra
import time
print("hello LORA")

class LORA:
	"""docstring for LORA"""

	def __init__(self,COMMS_KEY,Serial):
		self.true_key="RED_ROCKS!!"
		self.serial=Serial
		self.msg_id_sent=0000
		#do lora inits here
	def lora_receive(self):

		#do stuff here
		'''datatype = { COMMAND, FLIGHTMODE,cenas}
		Value = {test_airbrakes,"test_gps","test_altimetro", " ",outros_testes,StandBye,Flight]
		Key=
		'''

		if self.serial.inWaiting() > 0 :
			time.sleep(0.1)
			r_buff = self.serial.read(self.serial.inWaiting())
			if r_buff != "" :
				return r_buff.decode("ascii","ignore")
		#msg_received = ["COMMAND","Flight","RED_ROCKS!!","msg_sent"] #[Datatype, Value, Key]
		else :
			return 0

	def lora_send(self,datatype,value):
		#do stuff here
		#msg_sent = ["datatype","value","key","msg_sent"]  #datatype = { "altitude","gps_data", "angles"}# value = valor
		msg_sent = []
		msg_sent.append(datatype)
		msg_sent.append(value)

		msg_sent.append(self.true_key)
		msg_sent.append(self.msg_id_sent)
		#print("LORA MSG SENT", msg_sent)
		msg_sent=str(msg_sent)+"\r\n"
		self.serial.write(msg_sent.encode("ascii"))

		return msg_sent


	def verify_key(self,key):

		if key==self.true_key:
			return True
		else:
			return False

