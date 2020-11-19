#Classe que define as funcoes que obtem os dados diretamente dos varios sensores

print("Initialization\nIm in GET_DATA")

class GET_DATA:

	def __init__(self):
		#funcao que corre quando a class e declarada
		#do get data inits here
		cenas=""


	def altitude_raw(self):
		a="altitude"#isto deve ser um numero e nao uma string 

		#do stuff here
		return a



	def temperature_raw(self):

		t=21
		#do stuff here
		return t

	def angles_raw(self):

		angles= ["roll","pitch","yaw"] #lista coom 3 elementos que contem os 3 angulos de euler 
							#angles = [roll,pitch,yaw]
		#do stuff here					
		return angles 
	def magneto_raw(self):

		magneto = ["mx","my","mz"] #lista coom 3 elementos que contem as 3 componentes do campo magnetico medido 
					#do stuff here		#magneto = [mx,my,mz]
		return magneto
	def accelaration_raw(self):

		accelaration = ["ax","ay","az"] #lista coom 3 elementos que contem as 3 componentes da acelaracao medida
							#acelaration = [ax,ay,az]
							#do stuff here
		return accelaration


	def gps_raw(self):

		position = ["x","y","z"] #lista coom 3 elementos que contem as 3 componentes da acelaracao medida
							#position= [ax,ay,az]
							#do stuff here
		return position



