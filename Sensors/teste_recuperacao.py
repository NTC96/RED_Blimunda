import time
import board
import digitalio # For use with SPI
import RPi.GPIO as GPIO
import adafruit_bmp280


#Cuidado com estes pinos ao inicio!!
out_drogue = 5 #por aqui o numero do pino usado para controlar o drogue
out_tender = 7 #por aqui o numero do pino usado para controlar o tender descender

flag_ejetou = 0

#temos de ver estes valores consoante o que der para 
altitude_drogue = 500 #por a altitude do apogeu para o drogue ejetar
altitude_tender = 200 #altitude do parachute main

# Create sensor object, communicating over the board's default I2C bus
#i2c = board.I2C()   # uses board.SCL and board.SDA
#bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# OR Create sensor object, communicating over the board's default SPI bus
spi = board.SPI()
bmp_cs = digitalio.DigitalInOut(board.D5)
bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)

# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25

GPIO.setup(out_drogue,GPIO.OUT)
GPIO.output(out_drogue,GPIO.LOW)

GPIO.setup(out_tender,GPIO.OUT)
GPIO.output(out_tender,GPIO.LOW)

t_ref = time.time()
print("tref = " + tref + "\n")

while True:
    print(time.time())
    print("\nTemperature: %0.1f C" % bmp280.temperature)
    print("Pressure: %0.1f hPa" % bmp280.pressure)
    print("Altitude = %0.2f meters" % bmp280.altitude)
    
    if(bmp280.altitude > altitude_drogue)
         GPIO.output(out_drogue,GPIO.HIGH)
         print("Ejetou o drogue crlh")
         flag_ejetou = 1

     
    if(bmp280.altitude < altitude_tender and flag_ejetou == 1)
         GPIO.output(out_drogue,GPIO.HIGH)
         print("Ejetou o drogue crlh")
         return 0
     
    time.sleep(0.25)
