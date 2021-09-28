import time
import busio
import board
import os
import datetime
import adafruit_bmp280
import adafruit_bno055
import adafruit_gps
import digitalio
from picamera import PiCamera
import adafruit_bno055
import adafruit_tca9548a
import i2c_mux_select


print("Initialization\nI am in GET_DATA")

class GET_DATA:

    def __init__(self):
        self.press=0
        self.press_0 = 1017.70  # em milibars, mexer aqui


        # Initialize the I2C bus.
        self.spi = board.SPI()
        self.bmp_cs = digitalio.DigitalInOut(board.D5)
        self.bmp280_spi = adafruit_bmp280.Adafruit_BMP280_SPI(self.spi, self.bmp_cs)

        self.bmp280_spi.sea_level_pressure = self.press_0
        i2c = board.I2C()
        self.gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface
# Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Turn on just minimum info (RMC only, location):
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
# gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
        self.gps.send_command(b"PMTK220,1000")
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
# gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
# gps.send_command(b'PMTK220,500')
        self.last_print = time.monotonic()
        self.gps_fix_var = 0


        time.sleep(0.3)
        i2c_mux_select.I2C_setup(0x70,0)
        time.sleep(0.3)
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        time.sleep(0.3)
        i2c_mux_select.I2C_setup(0x70,4)
        time.sleep(0.3)
        self.sensor1 = adafruit_bno055.BNO055_I2C(i2c)


    def gps_fix(self):
        self.gps.update()
        # Every second print out current location details if there's a fix.
        self.current = time.monotonic()
        if self.current - self.last_print >= 1.0:
            self.last_print = self.current
            if not self.gps.has_fix:
            # Try again if we don't have a fix yet.
                print("Waiting for fix...")
                return False
            else :
               return True

    def gps_get_p(self):
        self.gps.update()

        self.current = time.monotonic()
        if self.current - self.last_print >= 1.0:
            self.last_print = self.current
            if not self.gps.has_fix:
                print("gps_fixing problem")



        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
            print("=" * 40)  # Print a separator line.
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                   self.gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                   self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
                   self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                   self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                   self.gps.timestamp_utc.tm_min,  # month!
                   self.gps.timestamp_utc.tm_sec,
                )
            )
            print("Latitude: {0:.6f} degrees".format(self.gps.latitude))
            print("Longitude: {0:.6f} degrees".format(self.gps.longitude))
            print("Fix quality: {}".format(self.gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
            if self.gps.satellites is not None:
                print("# satellites: {}".format(self.gps.satellites))
            if self.gps.altitude_m is not None:
                print("Altitude: {} meters".format(self.gps.altitude_m))
            if self.gps.speed_knots is not None:
                print("Speed: {} knots".format(self.gps.speed_knots))
            if self.gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(self.gps.track_angle_deg))
            if self.gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(self.gps.horizontal_dilution))
            if self.gps.height_geoid is not None:
                print("Height geoid: {} meters".format(self.gps.height_geoid))

    def temperature_raw_bmp_spi(self):
        #temp = sense.get_temperature()  # diretamente do sensor
        # temp = sense.get_temperature_from_humidity() # do sensor de humidade
        # temp = sense.get_temperature_from_pressure() # do sensor de presso
        # temp = round(temp,2 ) # para arredondar
        return self.bmp280_spi.temperature  # em celsius

    def angles_raw(self):
        i2c_mux_select.I2C_setup(0x70,0)
        #print("Euler angle: {}".format(sensor.euler))

        return self.sensor.euler  # em radianos


    def pressure_raw_bmp_spi(self):
        self.press = self.bmp280_spi.pressure  # em milibars
        return self.press  # em Pa


    def acceleration_raw(self):
        #accel = sense.get_accelerometer_raw()
        #ax = accel['x']
        #ay = accel['y']
        #az = accel['z']
 # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
   # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
   # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    #print("Euler angle: {}".format(sensor.euler))
   # print("Accelerometer (m/s^2): {}".format(sensor1.acceleration))
   # print("Quaternion: {}".format(sensor.quaternion))
   # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
   # print("Gravity (m/s^2): {}".format(sensor.gravity))

        i2c_mux_select.I2C_setup(0x70,4)
        #print("Euler angle: {}".format(sensor.euler))
        return self.sensor1.acceleration # em m/s2


    def altitude_bmp_spi(self):
        return self.bmp280_spi.altitude

    def still_pic_camera(self):
        timestamp_pic = time.time()
        camera.start_preview()
        time.sleep(2)
        camera.capture("/home/pi/Desktop/image" + str(timestamp_pic) + "jpg")
        camera.stop_preview()
        return
    def video_camera(self, duration):
        #isto convem ser feito em thread separado para nao afetar as outras cenas que tem de acontecer ao mm tempo
        timestamp_vid = time.time()
        camera.start_preview()
        camera.start_recording("/home/pi/Desktop/video" + str(timestamp_vid) + "jpg")
        time.sleep(duration)
        camera.stop_recording()
        camera.stop_preview()
        return



data = GET_DATA()
print("INIT")
while True :
    
    #if not data.gps_fix() :
    #    continue
    #data.gps_get_p()
    print("\nTemperature: %0.1f C" % data.temperature_raw_bmp_spi())
    print("Pressure: %0.1f hPa" % data.pressure_raw_bmp_spi())
    print("Altitude = %0.2f meters" % data.altitude_bmp_spi())
    print("Acceleration :{}".format(data.acceleration_raw()))
    print("Euler angle: {}".format(data.angles_raw()))
    print("timestamp = %f" %time.time())
#     #print("video is being recorded for 4 seconds")
#     #data.video_camera(4)

#     #print("photo is being taken")
#     #data.still_pic_camera()
    time.sleep(1)


