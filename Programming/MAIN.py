#esboco do Main 
#lets build from here

from Get_data import GET_DATA
from Lora_comms import LORA
COMMS_KEY="RED ROCKS!!"
GET=GET_DATA() 
Lora=LORA(COMMS_KEY)




print("hello MAIN")




def Get_sensors():

	a = GET.altitude_raw()
	b = GET.temperature_raw()
	c = GET.angles_raw()
	d = GET.magneto_raw()
	e = GET.accelaration_raw()
	f = GET.gps_raw()
	
	print(a)
	print(b)
	print(c)
	print(d)
	print(e)


def MAIN():

	Get_sensors()








MAIN()