#####################################
############## Controlador Blimunda
##### Equipa de Controlo - RED
##### Versão 4.0
#####################################


import time
from scipy import interpolate
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

class CONTROL_BLOCK:
    def __init__(self):

        #Initializing some variables
        
        self.lastErr = 0

        self.kp = 0.001
        self.ki = -0.0055
        self.kd = -0.1

        self.minimum_cd = 0.4 #Minimum CD value for the rocket with airbrakes closed
        self.maximum_cd = 1.2 #Maximum CD value for the rocket with airbrakes fully opened
        self.nominal_cd = 0.4 #Nominal CD value for the rocket
        self.max_change_rate = 0.5

        self.current_cd = self.nominal_cd

        self.flag = 0
        self.real_trajectory = list()
        self.errSum = 0
        self.angle = 0

        ###TESTING###
        self.plottlist = list()
        self.plotcdlist = list()
        
        self.altitudeTest = list()
        self.errorlist = list()
        self.plottchange = list()

        return

    def PID(self, error):
        #### PID Controller####
        self.errorlist.append(error)

        #How long since we last calculated
        timeChange = self.real_trajectory[len(self.real_trajectory)-1][0] - self.real_trajectory[len(self.real_trajectory)-2][0]  #Mudar isto dependendo dos sensores
        
        if self.flag > 1:
            #intregration and derivatives          
            self.errSum += error * timeChange
            dErr = (error - self.lastErr) / timeChange

            #computes PID Output
            Output = self.kp * error + self.ki * self.errSum + self.kd * dErr

            self.lastErr = error

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
                
        if self.flag > 1:

            cd_change = self.PID(error) #Vou só pôr da altitude mas se se quiser depois mais genérico é fazer lista, mudar o 0 para i-1 e pôr dentro do loop

            #CD change rate check
            
            timeChange = self.real_trajectory[len(self.real_trajectory)-1][0] - self.real_trajectory[len(self.real_trajectory)-2][0]
            
            lastCd = self.current_cd
            
            self.current_cd = cd_change+self.nominal_cd
        
            if self.current_cd < 0.4:
                self.current_cd = 0.4
        
            if self.current_cd > 1.2:
                self.current_cd = 1.2
                
            if (self.current_cd - lastCd)/timeChange > self.max_change_rate:
                self.current_cd = timeChange*self.max_change_rate + lastCd
            if (self.current_cd - lastCd)/timeChange < -1*self.max_change_rate:
                self.current_cd = -timeChange*self.max_change_rate + lastCd
    
            self.plottchange.append(timeChange)
        
        self.plotcdlist.append(self.current_cd)                             
        self.plottlist.append(t)

        return self.current_cd

    def setup(self):

        ###Reads nominal trajectory data
        self.nominal_trajectory = self.read_nominal_trajectory()
        ####TESTING#####
        self.test_trajectory = self.read_real_trajectory()
        return

    def iteration(self, elapsed_time, h):
    
        #Creates list of variables that impact trajectory control
        self.altitude = h
        self.altitudeTest.append(h) 
        self.real_trajectory.append([elapsed_time, self.altitude]) #Colocar aqui a altitude!!!!

        #Calculate next target cd value
        target_cd = self.calculate_next_cd() #Pus target_cd em vez de current_cd porque não sei se depois conseguimos pôr exatamente o current_cd igual ao target_cd

        #Steppler 
        self.angle = target_cd * 10/1.2 
        self.stepper(self.angle)

        ###Marks the first change in cd (and useful for testing [sorry for the spam = its working fine], remove after testing the print and += must be only =)
        self.flag += 1

        return self.flag

    def steppler(self, x):
        #Definimos cada um dos pins do Raspberry Pi que vamos utilizar como entradas e saídas do stepper
        out1 = 13 #IN1
        out2 = 11 #IN2
        out3 = 15 #IN3
        out4 = 12 #IN4

        i=0
        positive=0
        negative=0
        y=0

        GPIO.setmode(GPIO.BOARD) #Usamos isto para usarmos o modo que utiliza os número de cada Pin do Raspberry Pi
        GPIO.setup(out1,GPIO.OUT)
        GPIO.setup(out2,GPIO.OUT)
        GPIO.setup(out3,GPIO.OUT)
        GPIO.setup(out4,GPIO.OUT)

        GPIO.output(out1,GPIO.LOW) #GPIO.LOW = 0  e GPIO.HIGH = 1
        GPIO.output(out2,GPIO.LOW)
        GPIO.output(out3,GPIO.LOW)
        GPIO.output(out4,GPIO.LOW)
        if x>0 and x<=400:
            for y in range(x,0,-1):
                if negative==1:
                    if i==7:
                        i=0
                    else:
                        i=i+1
                    y=y+2
                    negative=0
                positive=1
                if i==0:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==1:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==2:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==3:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==4:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==5:
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(timeSleep)
                elif i==6:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(timeSleep)
                elif i==7:    
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(timeSleep)
                if i==7:
                    i=0
                    continue
                i=i+1
        
        
        elif x<0 and x>=-400:
            x=x*-1
            for y in range(x,0,-1):
                if positive==1:
                    if i==0:
                        i=7
                    else:
                        i=i-1
                    y=y+3
                    positive=0
                negative=1
                if i==0:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==1:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==2:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==3:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==4:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(timeSleep)
                elif i==5:
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(timeSleep)
                elif i==6:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(timeSleep)
                elif i==7:    
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(timeSleep)
                if i==0:
                    i=7
                    continue
                i=i-1 
                
        GPIO.cleanup()
        return

###############Testing##########################
    def read_real_trajectory(self):

        data = list()
        altitudes = list()

        with open("Controler_h.txt") as f:
             read = [list(line.split()) for line in f]

        new_format = self.interpolator_format(read)
        data.append(new_format[0])

        data = interpolate.splrep(new_format[0], new_format[1])
            
        return data

    def get_real_trajectory(self, value):

        result =  interpolate.splev(value, self.test_trajectory)
        
        return result

    def plot(self):

        plt.plot(self.plottlist, self.plotcdlist)
        plt.figure()
        
        #f = open("erros.txt", "a")
        #for i in range(2, len(self.errorlist)):
        #    f.write(str(self.errorlist[i]) + '\n')  
        #f.close()
        
        #f = open("tempos.txt", "a")
        #for i in range(len(self.plottchange)-1):
        #    f.write(str(self.plottchange[i]) + '\n')  
        #f.close()

        return
################################################

# if __name__ == "__main__":
#
#     classe = CONTROL_BLOCK()
#     classe.setup()
#
#     i = 0
#     t0 = time.time()
#
#     while(i < 2500):
#         current_time = time.time()
#         elapsed_time = current_time - t0
# 
#         if elapsed_time > 5:
#             classe.iteration(elapsed_time, classe.get_real_trajectory(elapsed_time))
#
#         i+=1
#         time.sleep(0.01)
#
#     classe.plot()



