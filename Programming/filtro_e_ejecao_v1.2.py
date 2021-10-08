from numpy import *
import statistics

# FILTRO V1.2

class FILTRO:

    def __init__(self):

        # Inicializacoes:

        self.tempo_seg = 10  # Tempo minimo para haver ejecao e 10 segundos
        self.delta_esperado = 0.35
        self.delta = [0.35, 0.35, 0.35, 0.35, 0.35]
        self.declive = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.acc_m = [0.0, 0.0]  # primeira casa = medicao mais recente, segunda casa = medicao anterior
        self.acc_f = [0.0, 0.0]  # igual mas para filtro em vez de medicao
        self.alt_m = [0.0, 0.0]  # igual para altitude
        self.alt_f = [0.0, 0.0]
        self.tempo = [0.0, 0.0]  # tempo atual e tempo anterior tal que delta = self.tempo[0] - self.tempo[1]
        self.motor_off = 0  # Quando o motor se desligar (acel<0) a flag fica a 1
        self.tempo_verif_acc = 0
        self.tempo_verif_alt = 0
        self.tempo_segunda_ejecao = 0
        self.ejecao_acc = 0
        self.ejecao_alt = 0
        self.ejecao_dois = 0
        self.contador_abortar_acel = 0
        self.contador_abortar_alt = 0
        self.abort_main=0

        # Parametros:

        # Para aceleracao:
        self.peso_it_acel = 0.3
        self.coef_er_acel = 2
        self.input_ab_acel = 1
        self.ajuste_acel = 1
        self.desvio_acel = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.erro_acel = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.mediana_acel = statistics.median(self.desvio_acel)
        self.erro_toleravel_acel = self.coef_er_acel * max(self.erro_acel)

        # Para altitude:
        self.peso_it_alt = 0.5
        self.coef_er_alt = 2
        self.input_ab_alt = 1
        self.ajuste_alt = 1
        self.desvio_alt = [50.0, 50.0, 50.0, 50.0, 50.0]
        self.erro_alt = [50.0, 50.0, 50.0, 50.0, 50.0]
        self.mediana_alt = statistics.median(self.desvio_alt)
        self.erro_toleravel_alt = self.coef_er_alt * max(self.erro_alt)

    # Filtro
    def filtro(self, acel, alt, relogio, input_airbrakes):  # (tempo total desde o inicio EM SEGUNDOS)

        if self.contador_abortar_acel>4 or self.contador_abortar_alt>4:
            self.abort_main=1

        i = 3
        self.tempo[1] = self.tempo[0]
        self.tempo[0] = relogio  # EM SEGUNDOS
        while i >= 0:
            self.delta[i + 1] = self.delta[i]
            i = i - 1

        self.delta[0] = self.tempo[0] - self.tempo[1]
        if(self.delta[0] == 0):
            self.delta[0]=self.delta[1]

        self.delta_esperado = statistics.median(self.delta)

        self.acc_m[1] = self.acc_m[0]
        self.acc_m[0] = acel

        self.alt_m[1] = self.alt_m[0]
        self.alt_m[0] = alt

        fator = self.delta[0] / self.delta_esperado
        if fator > 1:
            fator = fator * (-0.4 * arctan(fator - 1) + 1)  # Se correr mal, confirmar melhor este arctan()
            if fator > 3 and self.motor_off>0: #ou seja faltaram 4 dados de seguida
                self.abort_main=1
        else:
            fator = fator * (-0.4 * arctan(-fator + 1) + 1)

        # FILTRO ACEL

        filtro_aux = self.ajuste_acel * (self.peso_it_acel * (self.acc_m[0] - self.acc_f[0]) * fator + self.acc_f[0])

        diff = abs(filtro_aux - self.acc_m[0])

        if self.acc_m[0] < filtro_aux:
            erro_temp = diff + self.mediana_acel
        else:
            erro_temp = abs(diff - self.mediana_acel)

        if ((self.acc_f[0] < 0 and self.acc_f[1] < 0 and relogio > 3) or (
                relogio > 8)):  # Confirmar valores de tempo mas na altura fez sentido
            self.motor_off = 1

        if (erro_temp > self.erro_toleravel_acel and self.motor_off > 0):  # matar dados
            filtro_atual = self.acc_f[0] + 0.8 * (self.acc_f[0] - self.acc_f[1]) * self.delta[0] / self.delta_esperado
            self.acc_f[1] = self.acc_f[0]
            self.acc_f[0] = filtro_atual

            self.contador_abortar_acel = self.contador_abortar_acel +1

            self.erro_toleravel_acel = self.erro_toleravel_acel + 1 / cosh(5 * (self.erro_toleravel_acel))
        else:
            self.contador_abortar_acel=0
            if self.motor_off > 0:
                i = 3
                while i >= 0:
                    self.desvio_acel[i + 1] = self.desvio_acel[i]
                    i = i - 1
                self.desvio_acel[0] = diff

                i = 3
                while i >= 0:
                    self.erro_acel[i + 1] = self.erro_acel[i]
                    i = i - 1
                self.erro_acel[0] = erro_temp

            self.mediana_acel = statistics.median(self.desvio_acel)
            self.erro_toleravel_acel = self.coef_er_acel * max(self.erro_acel) + input_airbrakes

            self.acc_f[1] = self.acc_f[0]
            self.acc_f[0] = filtro_aux

        # FILTRO ALT

        filtro_aux = self.ajuste_alt * (self.peso_it_alt * (self.alt_m[0] - self.alt_f[0]) * fator + self.alt_f[0])

        diff = abs(filtro_aux - self.alt_m[0])

        if self.alt_m[0] < filtro_aux:
            erro_temp = diff + self.mediana_alt
        else:
            erro_temp = abs(diff - self.mediana_alt)

        if (erro_temp > self.erro_toleravel_alt and self.motor_off > 0):
            filtro_atual = self.alt_f[0] + 0.8 * (self.alt_f[0] - self.alt_f[1]) * self.delta[0] / self.delta_esperado
            self.alt_f[1] = self.alt_f[0]
            self.alt_f[0] = filtro_atual

            self.contador_abortar_alt = self.contador_abortar_alt + 1

            self.erro_toleravel_alt = self.erro_toleravel_alt + 25 / cosh(0.1 * (self.erro_toleravel_alt))
        else:
            self.contador_abortar_alt = 0
            if self.motor_off > 0:
                i = 3
                while i >= 0:
                    self.desvio_alt[i + 1] = self.desvio_alt[i]
                    i = i - 1
                self.desvio_alt[0] = diff

                i = 3
                while i >= 0:
                    self.erro_alt[i + 1] = self.erro_alt[i]
                    i = i - 1
                self.erro_alt[0] = erro_temp

            self.mediana_alt = statistics.median(self.desvio_alt)
            self.erro_toleravel_alt = self.coef_er_alt * max(self.erro_alt) + input_airbrakes

            self.alt_f[1] = self.alt_f[0]
            self.alt_f[0] = filtro_aux

        return [self.acc_f[0], self.alt_f[0], self.motor_off, self.abort_main]

    def condicoes_ejecao_main(self, relogio, flag_abortar_main):  #tempo EM SEGUNDOS

        if flag_abortar_main == 0:
            if relogio <= self.tempo_seg:
                self.tempo_verif_acc = relogio
                self.tempo_verif_alt = relogio

            i = 3
            while i >= 0:
                self.declive[i + 1] = self.declive[i]
                i = i - 1
            self.declive[0] = (self.alt_m[0] - self.alt_f[1]) / self.delta[0]
            print(statistics.median(self.declive))

            if (relogio > self.tempo_seg and flag_abortar_main == 0):  # deixar passar o periodo de maior ruido por causa do motor

                if (self.acc_f[0] < -10.5):  # verificar este valor mas da ultima vez que foi visto fazia sentido
                    self.tempo_verif_acc = relogio

                if (relogio - self.tempo_verif_acc > 2 and self.ejecao_acc == 0):  # verificar este valor mas fez sentido
                    # EJECAO ACEL
                    self.ejecao_acc = 1

                if (statistics.median(self.declive) > 45):  # verificar este valor mas fez sentido aquando da ultima verificacao
                    self.tempo_verif_alt = relogio

                if (relogio - self.tempo_verif_alt > 2 and self.ejecao_alt == 0):  # verificar este valor mas fez sentido
                    self.ejecao_alt = 1

            if ((self.ejecao_alt > 0 or self.ejecao_acc > 0) and relogio > self.tempo_seg and self.ejecao_dois == 0 and flag_abortar_main == 0):
                if (self.alt_f[0] > 480): #com uma v terminal de 20 m/s, demora 1s a descer 20m, ou seja ejeta aos 460m, se houver paraquedas claro
                    self.tempo_segunda_ejecao = relogio

                if (relogio - self.tempo_segunda_ejecao > 1):
                    self.ejecao_dois = 1
            else:
                self.tempo_segunda_ejecao = relogio

        return [self.ejecao_alt, self.ejecao_acc, self.ejecao_dois]