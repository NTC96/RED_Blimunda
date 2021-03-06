from sense_hat import SenseHat
import time
import busio
import board
import os
import datetime
import adafruit_mpl3115a2

print("Initialization\nI am in GET_DATA")

sense = SenseHat()

# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the MPL3115A2.
#sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
# Alternatively you can specify a different I2C address for the device:
# sensor = adafruit_mpl3115a2.MPL3115A2(i2c, address=0x10)

# You can configure the pressure at sealevel to get better altitude estimates.
# This value has to be looked up from your local weather forecast or meteorlogical
# reports.  It will change day by day and even hour by hour with weather
# changes.  Remember altitude estimation from barometric pressure is not exact!
# Set this to a value in pascals:
#sensor.sealevel_pressure = 102250


class GET_DATA:

    def __init__(self):
        self.press=0
        self.press_0 = 1017.70  # em milibars, mexer aqui


    def temperature_raw_sense(self):
        temp = sense.get_temperature()  # diretamente do sensor
        # temp = sense.get_temperature_from_humidity() # do sensor de humidade
        # temp = sense.get_temperature_from_pressure() # do sensor de presso
        # temp = round(temp,2 ) # para arredondar
        return temp  # em celsius

    def angles_raw(self):
        # sense.set_imu_config(True,True,True)
        o = sense.get_orientation_degrees()
        pitch = o["pitch"]
        roll = o["roll"]
        yaw = o["yaw"]
        # print("pitch {0} roll {1} yaw {2}".format(pitch, roll, yaw))
        return [round(pitch,3), round(roll,3), round(yaw,3)]  # em radianos


    def pressure_raw_sense(self):
        self.press = sense.get_pressure()  # em milibars
        #self.press = self.press * 100  # convert para Pa
        return self.press  # em Pa

    def humidity_raw(self):
        hum = sense.get_humidity()
        return hum

    def magneto_raw(self):
        magnet = sense.get_compass_raw()  # em microteslas
        mx = magnet['x']
        my = magnet['y']
        mz = magnet['z']
        return [mx, my, mz]


    def acceleration_raw(self):
        accel = sense.get_accelerometer_raw()
        ax = accel['x']
        ay = accel['y']
        az = accel['z']
        # print("pitch {0} roll {1} yaw {2}".format(ax, ay, az))
        return [round(ax,3),round(ay,3), round(az,3)]  # em Gs


    def gps_raw(self):
        position = "por definir"
        return position

    def altitude_raw_sense(self):
        # alt = 44331.5 - 4946.62 * press ** (0.190263)
        # esta da valores decentes mas nao encontrei esta referencia em mais lado nenhum

        # pressao em milibars, dai estar a dividir por 100
        # saquei da wikipedia, formula standard para a pressure altitude
        # alt = (1-(press/(100*1013.25))**0.190284)*145366.45 #em pes

        # converter para metros
        # alt = alt * 0.3048

        # importante!! sea level pressure standard
        self. pressure_raw_sense()
        alt = (1 - (self.press / (self.press_0)) ** 0.190284) * 145366.45 * 0.3048
        return alt

    def altitude_raw_mpl(self):
        return sensor.altitude

    def pressure_raw_mpl(self):
        return sensor.altitude

    def temperature_raw_mpl(self):
        return sensor.temperature
