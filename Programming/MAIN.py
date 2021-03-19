#esboco do Main
#lets build from here
import RPi.GPIO as GPIO
import serial
import threading
import time
from Get_data import GET_DATA
from Kalman import KALMAN
from Lora_comms import LORA
from Control import CONTROL_BLOCK
ser = serial.Serial("/dev/ttyS0",115200)
ser.flushInput()
ser.flushOutput()
COMMS_KEY="RED_ROCKS!!"
GET=GET_DATA()
Lora=LORA(COMMS_KEY,ser)
FILTRO = KALMAN()
CONTROL = CONTROL_BLOCK()

#####################Variaveis globais########################################
#MODOS
#Mode = "Teste"
#Mode = "Standby" - prelancamento
#Mode = "Flight"
rocket_mode_global = "Idle"

############################Flight Data########################################

altitude_global = 0
temp_global = 0
gps_global = ["gps_x","gps_y","gps_z"]
euler_angles_global = ["pitch","roll","yaw"]
accelaration_global = ["a_x","a_y","a_z"]
magneto_global=["m_x","m_y","m_z"]
#FLAGS
launch_lora_ok = 0
control_ready=1
text_flag=0
#Constantes
accelaration_noise_factor = 2 # se aceelaracao > 2g durante 1s ja descolou
previous_time = 0 
msg_rate=40
#lista da threading conditions
t_condition=[]  #0              1             2       3           4         5         6               7             8            9                  10
#t_condition=[mode_check,altitude_check,temp_check,euler_check,ace_check,gps_check,l_lora_ok_check,lora_flag_check,control_ready,tempo_zero_check, elapsed_fligh_time_check ]




print("hello MAIN")



def Lora_thread_function_receive(t_condition): #funcao que vai estar sempre a receber e sempre a enviar dados para terra

	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global
	global lora_flag
	global launch_lora_ok
	msg_received=Lora.lora_receive() #msg_received = ["datatype","value","key"]
	#trata da informacao recebida
	if msg_received != 0 :
		print("recebeu")
		print(msg_received)
		if Lora.verify_key(msg_received[-13:-2]):
			print("KEY TRUE_Loras\n")
			if  "COMMAND" in msg_received :
				print("Command")
				teste = 0
				if "test_airbrakes" in msg_received :
					print("test_airbrakes")
					t_condition[0].acquire()
					rocket_mode_global = "Teste"
					t_condition[0].release()
					teste="airbrakes"

				if "test_acelaration" in msg_received :
					t_condition[0].acquire()
					rocket_mode_global = "Teste"
					t_condition[0].release()
					teste = "accelaration"

				if "test_altimetro" in msg_received:
					print("testedo altimetro")

					t_condition[0].acquire()
					rocket_mode_global= "Teste"
					t_condition[0].release()
					teste = "altimetro"

				if "test_gps" in msg_received :

					t_condition[0].acquire()	
					rocket_mode_global= "Teste"
					t_condition[0].release()
					teste = "gps"
				if "test_euler" in msg_received:
					t_condition[0].acquire()	
					rocket_mode_global= "Teste"
					t_condition[0].release()
					teste = "euler"
				t_sensor_test = threading.Thread(target=Get_sensors_thread_function_test, args=(t_condition,teste))
				t_sensor_test.start()

			elif "FLIGHTMODE" in  msg_received:
				print("flight mode")
				if "standby" in msg_received :
					print("standby")
					t_condition[0].acquire()
					rocket_mode_global = "Standby"
					t_condition[0].release()
				if "launch" in msg_received:
					t_condition[6].acquire()
					launch_lora_ok = 1
					t_condition[6].release()
			else :
				t_condition[0].acquire()
				rocket_mode_global = "Idle"
				t_condition[0].release()
	t_condition[7].acquire()
	lora_flag=0
	t_condition[7].release()

def Lora_thread_function_send(t_condition,datatype,value):
	global lora_flag
	Lora.lora_send(datatype,value)
	t_condition[7].acquire()
	lora_flag=0
	t_condition[7].release()

def Get_sensors_thread_function_test(t_condition,teste):

	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global

	print("sensors")
	if teste == "airbrakes" :
		print("airbrake teste")
		#step motor sweep
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"step motor","MOTOR",)) #send to station
		t_lora_send.start()

	if teste == "altimetro":
		print("altitude raw")
		altitude_global = GET.altitude_raw_sense()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"altitude_test",altitude_global,)) #send to station
		t_lora_send.start()


	if teste == "gps":

		gps_global = GET.gps_raw()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"gps_test",gps_global,)) #send to station
		t_lora_send.start()

	if teste == "euler":

		euler_angles_global = GET.angles_raw()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"euler_test",euler_angles_global,)) #send to station
		t_lora_send.start()

	if teste == "accelaration":
		accelaration_global = GET.acceleration_raw()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"ace_test",accelaration_global,)) #send to station
		t_lora_send.start()



def Get_sensors_thread_function_standby(t_condition,accelaration):

	global previous_time
	global gps_global
	global euler_angles_global
	global accelaration_global
	global tempo_zero
	global sensor_flag
	global launch_lora_ok

	if launch_lora_ok == 1 :     #OK_LANCAR
		if previous_time == 0:
			previous_time = time.time()
		if accelaration > accelaration_noise_factor: # verificar se ja descolou #colocar o modulo #FAZER O MODULO
			if time.time() - previous_time > 1 :
				#ja descolou
				t_condition[0].acquire()
				rocket_mode_global = "Flight"
				t_condition[0].release()
				t_condition[9].acquire()
				tempo_zero = time.time()
				t_condition[9].release()
		else :
			previous_time = time.time()

def Get_sensors_thread_function_flight(t_condition):
#read from sensors
	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global
	global sensor_flag
	global elapsed_flight_time
	global tempo_zero
	global lora_flag

	t_condition[0].acquire()
	altitude_global = GET.altitude_raw_sense()
	t_condition[0].release()
	t_condition[3].acquire()
	euler_angles_global = GET.angles_raw()
	t_condition[3].release()
	t_condition[10].acquire()
	elapsed_flight_time = time.time() - tempo_zero
	t_condition[10].release()
	t_condition[4].acquire()
	accelaration_global = GET.acceleration_raw()
	t_condition[4].release()
	t_condition[5].acquire()
	gps_global = GET.gps_raw()
	t_condition[5].release()

	if rocket_mode_global == "Standby":
		t_sensors_standby = threading.Thread(target=Get_sensors_thread_function_standby, args=(t_condition,accelaration_global,))
		t_sensors_standby.start()
	data = str(round(altitude_global,4)) + ";" + str(gps_global) + ";" + str(accelaration_global) + ";" + str(euler_angles_global) + ";" +str(round(elapsed_flight_time,5))
	if lora_flag == 0 and Lora.msg_id_sent % msg_rate  ==0:
		print("Lora-----------",Lora.msg_id_sent)
		lora_flag = 1
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"Data",data,)) #send to station
		t_lora_send.start()
	Lora.msg_id_sent+=1
	t_file = threading.Thread(target=save_data, args=(t_condition,data,))
	t_file.start()

	#send to station
	#enable controller
	#enable filter

def t_control_thread(t_condition,h):
	global control_ready
	global elapsed_flight_time

	t_condition[8].acquire()
	control_ready=0
	t_condition[8].release()
	CONTROL.iteration(elapsed_flight_time, h)
	t_condition[8].acquire()
	control_ready=1
	t_condition[8].release()

def save_data(t_condition,data):
	global text_flag
	t_condition[11].acquire()
	# define beginning time
	# open write file
	#filename = "data_" + str(ctime) + ".txt"
	filename = "data.txt"
	#filename = filename.replace(" ", "_")
	#filename = filename.replace(":", "_")

	# file.write("Format: rel.time(s) press(Pa) altitude(m) temp(oC) [pitch roll yaw](rad) [mx my mz](microteslas) [
	# ax ay az](Gs)\n\n")
	if text_flag==0:
		file = open(filename,"w")
		ctime = time.ctime()
		file.write("Start time = %s\n\n" % ctime)
		file.write("Format: rel.time(s) press(Pa) altitude(m) temp(oC) [pitch roll yaw](rad) [ax ay az](Gs)\n\n") 
		text_flag=1
	else :
		#print(data)
		file = open(filename,"a")
		file.write(data+"\n")

	file.close()
	t_condition[11].release()

for i in range(12):
	t_condition.append(threading.Lock())


start = time.time()

def MAIN():

	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global
	global test_airbrakes
	global test_altimetro
	global test_gps_check
	global altitude
	global lora_flag
	global tempo_zero
	global launch_lora_ok
	lora_flag=0
	tempo_zero=0
	m=24  #massa inicial
	m0=17 #mass final

	t=time.time()
	v=0   #velocity
	h=0	  #altitude

	#No ciclo while:

	#Espera pelos sensores

	#CONTROL.setup()
	while (True):


		if rocket_mode_global == "Idle" or rocket_mode_global=="Teste":

			if lora_flag == 0 :
				t_condition[7].acquire()
				lora_flag=1
				t_condition[7].release()
				t_lora_receive = threading.Thread(target=Lora_thread_function_receive, args=(t_condition,))
				#t_thread.append(t_lora_receive)
				#t_thread[-1].start() #lora receivex
				t_lora_receive.start()
				t_lora_receive.join()



		if rocket_mode_global == "Standby": #prelancamento

			if lora_flag == 0:
				if launch_lora_ok == 0:
					t_lora_receive = threading.Thread(target=Lora_thread_function_receive, args=(t_condition,))
					t_lora_receive.start()
					t_lora_receive.join()
				t_sensor_flight = threading.Thread(target=Get_sensors_thread_function_flight, args=(t_condition,))
				t_sensor_flight.start()

		if rocket_mode_global == "Flight":

			t_sensor_flight.start()
			if altitude_global != altitude:
				#wait altitude
				altitude = altitude_global

				##################Filtro
				a_z = accelaration_global[2]    #tem de ser accelaration dos zzzzzzzzzzzzzzzzz
				delta = time.time() - t
				if m>m0:    #Se ainda houver combustivel (m > m0), a massa do rocket vai diminuindo
				            #'a medida em que se vai queimando o combustivel
				    mfr=1.08
				    m=m-mfr*delta
				else:       #Se ja nao houver combustivel nao ha mass flow rate e a forca do motor sera' 0
				    mfr=0
				h = FILTRO.filtro(self, a_z, altitude , mfr, m, delta, h) #e pitch
				t=time.time()
				#v = v + ac*delta
				if control_ready == 1:
					t_control = threading.Thread(target=t_control_thread, args=(t_condition,h,))
					t_control.start()
				#controller
				#h  a ser usado



MAIN()
if time.time() - start > 5 :
	sys.exit()

