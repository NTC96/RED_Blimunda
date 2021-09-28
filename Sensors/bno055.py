# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bno055
import adafruit_tca9548a
import i2c_mux_select


print("hii")
i2c = board.I2C()
time.sleep(0.3)
i2c_mux_select.I2C_setup(0x70,0)
# Create the TCA9548A object and give it the I2C bus
#tca = adafruit_tca9548a.TCA9548A(i2c)
time.sleep(0.3)
sensor = adafruit_bno055.BNO055_I2C(i2c)
time.sleep(0.3)
i2c_mux_select.I2C_setup(0x70,4)
sensor1 = adafruit_bno055.BNO055_I2C(i2c)
# If you are going to use UART uncomment these lines
# uart = board.UART()
# sensor = adafruit_bno055.BNO055_UART(uart)

last_val = 0xFFFF


def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


while True:
   # print("Temperature: {} degrees C".format(sensor.temperature))
    """
    print(
        "Temperature: {} degrees C".format(temperature())
    )  # Uncomment if using a Raspberry Pi
    """
   # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
   # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
   # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    i2c_mux_select.I2C_setup(0x70,0)
    print("Euler angle: {}".format(sensor.euler))
    i2c_mux_select.I2C_setup(0x70,4)
    #print("Euler angle: {}".format(sensor.euler))
    print("Accelerometer (m/s^2): {}".format(sensor1.acceleration))
   # print("Quaternion: {}".format(sensor.quaternion))
   # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
   # print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    time.sleep(1)
