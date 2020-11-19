#programa pincipal esboco







print("Initialization\nIm in....")
clock=11212

class GET_DATA:

	def __init__(self):
		#funcao que corre quando a class e declarada
		#do get data inits here
		cenas=""
		

	def altitude_raw(self):
		a=2
		#do stuff here
		return a



	def temperature_raw(self):

		t=21
		#do stuff here
		return t

	def angles_raw(self):

		angles= ["roll","pitch","yaw"] #lista coom 3 elementos que contem os 3 angulos de euler 
							#angles = [roll,pitch,yaw]
		return angles 
	def magneto_raw(self):

		magneto = ["mx","my","mz"] #lista coom 3 elementos que contem as 3 componentes do campo magnetico medido 
							#magneto = [mx,my,mz]
		return magneto
	def accelaration_raw(self):

		accelaration = ["ax","ay","az"] #lista coom 3 elementos que contem as 3 componentes da acelaracao medida
							#magneto = [ax,ay,az]
		return accelaration


p1=GET_DATA()
print(clock)
print(p1.altitude_raw())