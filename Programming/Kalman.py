
print("Estou no filtro")
#Mass : Fora da funcao, no main, mass = mass - mfr*delta
#mfr = 1.08 if mass>m0, else mfr=0
#m0 = 17 (kg)
#Onde delta = time.time() - t0
#t0 vai se registando com time.time() apos cada iteracao do filtro
#o primeiro valor de mass e' 17+7 = 24 (kg)
#v = equacao do movimento = v + a*delta -> v0 = 0 (m/s)
#Podemos determinar a altitude apos o voo para nao sobrecarregar o pi

class KALMAN:

    def __init__(self):
        self.g = 9.81
        self.A = 0
        self.C = 1
        self.P = 1000
        self.Q = 1
        self.R = 2500 #mudar quando tivermos mais info sobre o ruido apos o teste com o drone -> R = (desvio_padrao)^2
        self.P_h = 1000
        self.Q_h = 1
        self.R_h = 2500
        self.Ve=1709
        self.L = 0.0065
        self.M = 0.0289654
        self.p0 = 101325
        self.R0 = 8.31447
        self.temperatura = 25 + 373.15
        self.densidade = 1.22
        self.v = 0


    def densidade(self, alt):

        aux1 = (self.p0 * self.M) / (self.R0 * (self.temperatura))
        aux2 = 1 - ((self.L * alt) / (self.temperatura))
        aux3 = ((self.g * self.M) / (self.R0 * self.L)) - 1
        densidade = aux1 * (aux2**aux3)

        return densidade

    def filtro(self, dataa, datah, mfr, mass, delta, h_hat,pitch):

        Fm = mfr * self.Ve # *cos(pitch) ou assim
        Fa = 0.43*densidade(self,h_hat)*self.v*self.v* 0.017671*0.5
        if self.v<0:
            Fa=-Fa

        #Aceleracao:

        a_prediction = Fm/mass - Fa/mass - self.g
        P_prediction = self.A * self.P * self.A + self.Q
        residual = dataa - self.C*a_prediction
        K = (P_prediction * self.C)/(self.C * P_prediction * self.C + self.R)
        acel_corrigida = a_prediction + K*residual
        self.P = (1 - K*self.C)*P_prediction

        #-------------------------------------------------------#

        #Altitude:
        self.v = self.v + ac*delta

        h_prediction = h_hat + self.v*delta + 0.5*delta*delta*acel_corrigida
        P_prediction_h = self.P_h + self.Q_h
        residual_h = datah - h_prediction
        K_h = (P_prediction_h)/(P_prediction_h + self.R_h)
        h = h_prediction + K_h*residual_h
        self.P_h = (1 - K)*P_prediction_h


        return h


"""
#Main: 

m=24
m0=17

t=time.time()
v=0
h=0

#No ciclo while:

#Espera pelos sensores

delta = time.time() - t

if m>m0:    #Se ainda houver combustivel (m > m0), a massa do rocket vai diminuindo
            #'a medida em que se vai queimando o combustivel 
            
    mfr=1.08
    m=m-mfr*delta
else:       #Se ja nao houver combustivel nao ha mass flow rate e a forca do motor sera' 0
    mfr=0

h = filtro(self, a[2], alt, mfr, v, m, delta, h) #e pitch

t=time.time()
#v = v + ac*delta


controlador
"""