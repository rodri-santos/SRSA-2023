import BMP085 as BMP085
import PCF8591 as ADC
import time
import paho.mqtt.publish as publish

MQTT_SERVER = "10.6.1.4"
MQTT_PATH1 = "19_temperature"  # this is the name of topic, like temp
MQTT_PATH2 = "19_luminosity"
MQTT_PATH3 = "19_pressure"
ADC_VALUE = 0.0048828125

def setup():
    ADC.setup(0x48)
    print ('\n Barometer begins...')

def loop():
    while True:

        sensor = BMP085.BMP085()
        temp = sensor.read_temperature()	# Read temperature to veriable temp
        pressure = sensor.read_pressure()	# Read pressure to veriable pressure

        print ('')
        print ('      Temperature = {0:0.2f} C'.format(temp))	# Print temperature
        print ('      Pressure = {0:0.2f} Pa'.format(pressure))	# Print pressure
        time.sleep(1)
        print ('')

        print('Raw value: ', ADC.read(1))
        print('In lux: ', (250.0 / (ADC_VALUE * ADC.read(1))) - 50)

        publish.single(MQTT_PATH1, temp, hostname=MQTT_SERVER)
        publish.single(MQTT_PATH3, pressure, hostname=MQTT_SERVER)
        publish.single(MQTT_PATH2, (250.0 / (ADC_VALUE * ADC.read(1)) - 50), hostname=MQTT_SERVER)# send data continuously every 3 seconds
        time.sleep(3)

def destroy():
    pass

if __name__ == '__main__':		# Program start from here
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()


