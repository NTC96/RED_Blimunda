import math
# formato: aaa.aa aaa.aa aaa.aa gg.gggggg gg.gggggg hhhh.hh vvvv.v rrrr.r rrrr.r rrrr.r ttttt
# Como interpretar? a= aceleracao (em cada eixo), g= gps (lat e long), h= altitude, v= velocidade
#                   r = rotacao (em cada eixo) t=tempo
# Os dados podem ter o numero de casas decimais que se quiser, mas a partir das casas decimais acima representadas
# serao ignoradas
# Os dados não podem exceder o numero de algarismos inteiros (à esquerda da virgula). O sinal - conta como um algarismo
# Por exemplo -34.4542 123.1 são dados validos para aceleracoes. 231230 é um dado inválido para o tempo.

def comprime_dados(acc, gps, alt, v, rot, t, f, msg):
    s = ""
    if f==1:
        s += chr(126) + msg
        return s

    # comprime acc
    i = 0
    while i < len(acc):
        if acc[i]<-99:
            acc[i]=-99
        if acc[i]>999:
            acc[i]=999
        acc[i] = '{:06.2f}'.format(acc[i])
        s += str(acc[i])
        i += 1

    # comprime gps
    i = 0
    while i < len(gps):
        if gps[i]<-9.9:
            gps[i]=-9.9
        if gps[i]>99:
            gps[i]=99
        gps[i] = '{:09.6f}'.format(gps[i])
        s += str(gps[i])
        i += 1

    # comprime h
    if alt < -999:
        alt = -999
    if alt > 9999:
        alt = 9999
    alt = '{:07.2f}'.format(alt)
    s += str(alt)

    # comprime v
    if v < -999:
        v = -999
    if v > 9999:
        v = 9999
    v = '{:06.1f}'.format(v)
    s += str(v)

    # comprime rot
    i = 0
    while i < len(rot):
        if rot[i] < -999:
            rot[i] = -999
        if rot[i] > 9999:
            rot[i] = 9999
        rot[i] = '{:06.1f}'.format(rot[i])
        s += str(rot[i])
        i += 1

    # comprime t
    if t < 0:
        alt = 0
    if t > 99999:
        alt = 99999
    t = '{:05.0f}'.format(t)
    s += str(t)

    s = s.replace(".", "")

    # s tem agora 62 caracteres

    s2 = ""
    i = 0
    while i < len(s):
        soma = 0
        char1 = s[i]
        char2 = s[i + 1]
        if char1 == '-':
            soma += 10 * 11
        else:
            soma += int(char1) * 11
        if char2 == '-':
            soma += 10
        else:
            soma += int(char2)

        s2 += chr(soma)
        i += 2

    # s2 tem agora 31 caracteres

    return s2


def descomprime_dados(s):
    s2 = ""
    s3 = ""
    i = 0
    if ord(s[0])==126:
        return s[1:len(s)]

    while i < len(s):
        aux = math.floor(ord(s[i]) / 11)
        if (aux == 10):
            s2 += "-"
        else:
            s2 += str(aux)

        aux2 = round((ord(s[i])/11 - aux) * 11)
        if (aux2 == 10):
            s2 += "-"
        else:
            s2 += str(aux2)
        i += 1

    #acc
    s3 += s2[0:3] + "." + s2[3:5] + " " + s2[5:8] + "." + s2[8:10] + " " + s2[10:13] + "." + s2[13:15] + " "
    #gps
    s3 += s2[15:17] + "." + s2[17:23] + " " + s2[23:25] + "." + s2[25:31] + " "
    #alt
    s3 += s2[31:35] + "." + s2[35:37] + " "
    #v
    s3 += s2[37:41] + "." + s2[41:42] + " "
    #rot
    s3 += s2[42:46] + "." + s2[46:47] + " " + s2[47:51] + "." + s2[51:52] + " " + s2[52:56] + "." + s2[56:57] + " "
    #t
    s3 += s2[57:62] + "\n"

    return s3
