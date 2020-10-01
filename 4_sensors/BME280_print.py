import BME280

BME280.setup()
BME280.get_calib_param()

temperature, humidity, pressure = BME280.read()
print ("temperature : {} ℃".format(temperature))
print ("humidity : {} ％".format(humidity))
print ("pressure : {} hPa".format(pressure/100))
