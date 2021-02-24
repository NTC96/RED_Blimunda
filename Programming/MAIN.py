#esboco do Main 
#lets build from here
import threading
import time
from Get_data import GET_DATA
from Kalman import KALMAN
from Lora_comms import LORA
from Control import CONTROL_BLOCK


COMMS_KEY="RED_ROCKS!!"
GET=GET_DATA() 
Lora=LORA(COMMS_KEY)
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
#Flags de testes
test_airbrakes = 0
test_altimetro = 0
test_gps = 0 
test_euler_angles = 0
lora_flag = 0
test_acelaration = 0

control_ready=1
#Constantes
accelaration_noise_factor = 2 # se aceelaracao > 2g durante 1s ja descolou
previous_time = 0 

#lista da threading conditions
t_condition=[]  #0              1             2       3           4         5         6               7                  8                     9               10                     11                    12             13                 14              15
# t_condition=[mode_check,altitude_check,temp_check,euler_check,ace_check,gps_check,ace_test_check,test_airbrakes_check,test_altimetro_check ,test_gps_check ,test_euler_angles_check,launch_lora_ok_check,lora_flag_check,control_ready,tempo_zero_check, elapsed_fligh_time_check ]




print("hello MAIN")



def Lora_thread_function_receive(t_condition): #funcao que vai estar sempre a receber e sempre a enviar dados para terra

	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global
	global magneto_global
	global test_airbrakes
	global test_altimetro
	global test_gps_check
	global lora_flag

	

	var1=0
	
	var1+=1
	
	msg_received=Lora.lora_receive() #msg_received = ["datatype","value","key"]
	#trata da informacao recebida

	
	if Lora.verify_key(COMMS_KEY):
		print("KEY TRUE_Loras\n")
		if msg_received[0]== "COMMAND":

			if msg_received[1]== "test_airbrakes" :
				t_condition[0].acquire()
				rocket_mode_global = "Teste"
				t_condition[0].release()
				t_condition[7].acquire()
				test_airbrakes = 1
				t_condition[7].release()

			if msg_received[1]== "test_acelaration" :
				t_condition[0].acquire()
				rocket_mode_global = "Teste"
				t_condition[0].release()
				t_condition[6].acquire()
				test_acelaration = 1
				t_condition[6].release()	

			if msg_received[1] == "test_altimetro":

				t_condition[0].acquire()
				rocket_mode_global= "Teste"
				t_condition[0].release()
				t_condition[8].acquire()
				test_altimetro=1
				t_condition[8].release()

			if msg_received[1] == "test_gps":

				t_condition[0].acquire()	
				rocket_mode_global= "Teste"
				t_condition[0].release()
				t_condition[9].acquire()
				test_gps = 1
				t_condition[9].release()

		elif msg_received[0] == "FlightMode":
		
			if msg_received[1] == "Standby":


				t_condition[0].acquire()
				rocket_mode_global = "Standby"
				t_condition[0].release()

			if msg_received[1] == "Launch":
				t_condition[11].acquire()
				launch_lora_ok = 1 
				t_condition[11].release()

		else :
			t_condition[0].acquire()
			rocket_mode_global = "Idle"
			t_condition[0].release()

		t_sensor_test.start()	


def Lora_thread_function_send(t_condition,datatype,value):
	global lora_flag
	
	#ter em atencao pode haver conflito de thread, se sim por acquire and release
	'''
		if rocket_mode_global == "Flight":
			
			#altitude_wait
			#send altitude
			Lora.lora_send("altitude",altitude_global)
			#gps_wait
			#send_gps
			Lora.lora_send("gps_data",gps_global)
			#gps_wait
			#send_gps
			Lora.lora_send("angles",euler_angles_global)
		else if 
	'''

	t_condition[12].acquire()
	lora_flag=0
	t_condition[12].release()





def Get_sensors_thread_function_test(t_condition):
	
	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global
	global magneto_global
	global test_airbrakes
	global test_altimetro
	global test_gps_check

	print("sensors")
	


	t_condition[0].acquire()
	t_condition[8].acquire()
	if rocket_mode_global == "Teste" and test_altimetro==1:

		t_condition[1].acquire()
		altitude_global = GET.altitude_raw()
		
		
		test_altimetro = 0
		
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"altitude_test",altitude_global,)) #send to station
		t_condition[1].release()
		t_lora_send.start()
		

	t_condition[8].release()
	t_condition[9].acquire()

	if rocket_mode_global == "Teste" and test_gps==1:

		t_condition[5].acquire()
		gps_global = GET.gps_raw()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"gps_test",gps_global,)) #send to station
		t_condition[5].release()
		test_gps = 0
		t_lora_send.start()
		
	t_condition[9].release()
	t_condition[10].acquire()

	if rocket_mode_global == "Teste" and test_euler_angles==1:

		t_condition[3].acquire()
		euler_angles_global = GET.angles_raw()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"euler_test",euler_angles_global,)) #send to station
		t_condition[3].release()
		test_euler_angles = 0
		t_lora_send.start()
	if rocket_mode_global == "Teste" and test_acelaration ==1:
		t_condition[4].acquire()
		euler_angles_global = GET.angles_raw()
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"ace_test",accelaration_global,)) #send to station
		t_condition[4].release()
		test_acelaration = 0
		t_lora_send.start()
	

	t_condition[10].release()
	
def Get_sensors_thread_function_standby(t_condition,accelaration):

	global previous_time
	global gps_global
	global euler_angles_global
	global accelaration_global
	global tempo_zero 
	global sensor_flag


	if launch_lora_ok == 1 :     #OK_LANCAR

		if previous_time == 0:

			previous_time = time.time()

		if accelaration > accelaration_noise_factor:# verificar se ja descolou #colocar o modulo #FAZER O MODULO

			if time.time() - previous_time > 1 :

				#ja descolou
				t_condition[0].acquire()
				rocket_mode_global = "Flight"
				t_condition[0].release()
				t_condition[13].acquire()
				tempo_zero = time.time()
				t_condition[13].release()


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
	global magneto_global
	global test_airbrakes
	global test_altimetro
	global test_gps_check
	global sensor_flag
	global elapsed_flight_time
	global tempo_zero

	t_condition[0].acquire()
	altitude_global = GET.altitude_raw()
	t_condition[0].release()
	t_condition[3].acquire()
	euler_angles_global = GET.angles_raw()
	t_condition[3].release()
	t_condition[15].acquire()
	elapsed_flight_time = time.time() - tempo_zero
	t_condition[15].release()
	accelaration_global = GET.accelaration_raw()
	
	#magneto_global = GET.magneto_raw()
	
	gps_global = GET.gps_raw()

	if rocket_mode_global == "Standby":

		t_sensors_standby = threading.Thread(target=Get_sensors_thread_function_standby, args=(t_condition,accelaration_global,))
		t_sensors_standby.start()

	data = str(altitude_global) + ";" + str(gps_global) + ";" + str(accelaration_global) + ";" + str(euler_angles_global)

	if lora_flag == 0 :
		lora_flag = 1
		t_lora_send = threading.Thread(target=Lora_thread_function_send, args=(t_condition,"Data",data,)) #send to station
		t_lora_send.start()
	#send to station 
	#enable controller
	#enable filter





def t_control_thread(t_condition,h):
	global control_ready
	global elapsed_flight_time

	t_condition[13].acquire()
	control_ready=0
	t_condition[13].release()
	CONTROL.iteration(elapsed_flight_time, h)
	t_condition[13].acquire()
	control_ready=1
	t_condition[13].release()




def save_data(data):

	# define beginning time
    ctime = time.ctime()
    print("start time: %s \n" % ctime)
    time.sleep(2)
    start = time.time()

    # open write file
    filename = "data_" + str(datetime.datetime.now()) + ".txt"
    filename = filename.replace(" ", "_")
    file = open(filename, "w")
    file.write("Start time = %s\n\n" % ctime)
    # file.write("Format: rel.time(s) press(Pa) altitude(m) temp(oC) [pitch roll yaw](rad) [mx my mz](microteslas) [
    
    # ax ay az](Gs)\n\n")
    if file_flag==1:

    	file.write("Format: rel.time(s) press(Pa) altitude(m) temp(oC) [pitch roll yaw](rad) [ax ay az](Gs)\n\n")

    file.write("%f %f %f %f [%f %f %f] [%f %f %f]\n" % (t, press, a, b, c[0], c[1], c[2], e[0], e[1], e[2]))



for i in range(13):
	t_condition.append(threading.Lock())



t_lora_receive = threading.Thread(target=Lora_thread_function_receive, args=(t_condition,))

t_sensor_test = threading.Thread(target=Get_sensors_thread_function_test, args=(t_condition,))
t_sensor_flight = threading.Thread(target=Get_sensors_thread_function_flight, args=(t_condition,))

start = time.time()

def MAIN():

	global rocket_mode_global
	global altitude_global
	global temp_global
	global gps_global
	global euler_angles_global
	global accelaration_global
	global magneto_global
	global test_airbrakes
	global test_altimetro
	global test_gps_check
	global altitude
	global lora_flag

	m=24  #massa inicial
	m0=17 #mass final

	t=time.time()
	v=0   #velocity
	h=0	  #altitude

	#No ciclo while:

	#Espera pelos sensores

	var=0
	CONTROL.setup()

	while (var<100):
		var+=1
		print("main")

		if rocket_mode_global == "Idle" or rocket_mode_global=="Teste":

			if lora_flag==0:

				t_condition[12].acquire()
				lora_flag=1
				t_condition[12].release()
				t_lora_receive.start() #lora receive
				#x.join()


		if rocket_mode_global == "Standby": #prelancamento

			if lora_flag == 0:

				t_lora_receive.start()
				t_lora_receive.join()
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