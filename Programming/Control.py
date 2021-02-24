#####################################
############## Controlador Blimunda
##### Equipa de Controlo - RED
##### Versao 2.0
#####################################


import time
from scipy import interpolate



class CONTROL_BLOCK:
    def __init__(self):
    
        self.lastErr = 0

        self.kp = 0.001
        self.ki = -0.0055
        self.kd = -0.1

        self.minimum_cd = 0.4 #Minimum CD value for the rocket with airbrakes closed
        self.maximum_cd = 1.2 #Maximum CD value for the rocket with airbrakes fully opened
        self.nominal_cd = 0.4 #Nominal CD value for the rocket
        self.max_change_rate = 0.5

        self.current_cd = self.nominal_cd

     ###Initializing some variables
        self.flag = 0
        self.real_trajectory = list()
        self.errSum = 0
        return






    def PID(self, error):
     #### PID Controller####

        #How long since we last calculated
        #now = time.time()
        #timeChange = now - lastTime

        if self.flag > 1:
        #value from matlab
            timeChange = self.real_trajectory[len(self.real_trajectory)-1][0] - self.real_trajectory[len(self.real_trajectory)-2][0]  #Mudar isto dependendo dos sensores

            #intregration and derivatives
            
            self.errSum += error * timeChange
            dErr = (error - self.lastErr) / timeChange

            #computes PID Output
            Output = self.kp * error + self.ki * self.errSum + self.kd * dErr

            self.lastErr = error
            #lastTime = now
        else:
            Output = self.nominal_cd
        return Output



    def interpolator_format(self, data):

        new_format = list()
        
        for i in range(len(data)):
            for j in range(len(data[0])):
                if i == 0:
                    new_format.append(list())

                new_format[j].append(data[i][j])

        return new_format



    def read_nominal_trajectory(self):

        data = list()
        altitudes = list()
        with open("Nominal_trajectory.txt") as f:
             read = [list(line.split()) for line in f]

        new_format = self.interpolator_format(read)
        data.append(new_format[0])

        data = interpolate.splrep(new_format[0], new_format[1])
            
        return data




    def get_nominal_trajectory(self, value, tck):

        result =  interpolate.splev(value, tck)
        
        return result


    def calculate_next_cd(self):
        t = self.real_trajectory[len(self.real_trajectory) - 1][0]
        error = self.get_nominal_trajectory(t, self.nominal_trajectory) - self.real_trajectory[len(self.real_trajectory) - 1][1]

        cd_change = self.PID(error) #Vou sso por da altitude mas se se quiser depois mais generico e fazer lista, mudar o 0 para i-1 e por dentro do loop

        #CD change rate check

        if abs(cd_change) > self.max_change_rate:
            cd_change = (cd_change/abs(cd_change)) * self.max_change_rate 


        #CD Range check
        if cd_change + self.current_cd < self.minimum_cd:
            self.current_cd = self.minimum_cd

        elif cd_change + self.current_cd > self.maximum_cd:
            self.current_cd = self.maximum_cd
            
        return











    def setup(self):

     ###Reads nominal trajectory data
        self.nominal_trajectory = self.read_nominal_trajectory()
        return





    def iteration(self, elapsed_time, h):

    ###Starts flight clock
    #t0 = time.time()   <------------------------------------------


    ###Initial cd value

        ###Reads sensor data (this list will have more variables in the future) and current elapsed time
        #current_time = time.time()
        #elapsed_time = current_time - t0
        
        ###Creates list of variables that impact trajectory control
        self.altitude = h
        self.real_trajectory.append([elapsed_time, self.altitude]) #Colocar aqui a altitude!!!!

        ###Calculate next target cd value
        target_cd = self.calculate_next_cd() #Pus target_cd em vez de current_cd porque nao sei se depois conseguimos por exatamente o current_cd igual ao target_cd


        ###Changes current_cd value to target_cd
        #Funcao que envovlve motor dos airbrakes para que current_cd = target_cd <----------------------------------------------


        ###Marks the first change in cd (and useful for testing [sorry for the spam = its working fine], remove after testing the print and += must be only =)
        self.flag += 1


        return self.flag


'''
if __name__ == "__main__":

    classe = CONTROL_BLOCK()
    classe.setup()
    
    t0 = time.time()
    while(1):
        current_time = time.time()
        elapsed_time = current_time - t0
        print(classe.iteration(elapsed_time, 3.14))




'''