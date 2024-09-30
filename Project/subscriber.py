import paho.mqtt.client as mqtt  # import library
import socket
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import configparser
import statistics

MQTT_SERVER = "10.6.1.4"   # specify the broker address, it can be IP of raspberry pi or simply localhost
MQTT_PORT = 1883
MQTT_PATH1 = "19_temperature"  # this is the name of topic, like temp
MQTT_PATH2 = "19_luminosity"
MQTT_PATH3 = "19_pressure"
MQTT_PATH4 = "sensor_data_hum_1"
MQTT_PATH5 = "sensor_data_hum_2"
MQTT_PATH6 = "sensor_data_energy"

config = configparser.ConfigParser()
config.read('healthy_intervals.cfg')

temperature_min = float(config['Intervals']['temperature_min'])
temperature_max = float(config['Intervals']['temperature_max'])
luminosity_min = float(config['Intervals']['luminosity_min'])
luminosity_max = float(config['Intervals']['luminosity_max'])
pressure_min = float(config['Intervals']['pressure_min'])
pressure_max = float(config['Intervals']['pressure_max'])

last_alarms = {}


def generate_timestamp():
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    return timestamp


def generate_message(sensor, value, status, start_timestamp):
    timestamp = generate_timestamp()
    message = None
    if status == "NEW":
        message = f"{timestamp} {sensor} - Rasp 10 - Value: {value} (NEW ALARM)"
    elif status == "STARTED":
        message = f"{timestamp} {sensor} - Rasp 10 - Value: {value} (started {start_timestamp})"
    elif status == "CANCELLED":
        message = f"{timestamp} {sensor} - Rasp 10 - Value: {value} (ALARM CANCELLED)"
    return message


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(MQTT_PATH1 + "Connected with result code " + str(rc))
    print(MQTT_PATH2 + "Connected with result code " + str(rc))
    print(MQTT_PATH3 + "Connected with result code " + str(rc))
    print(MQTT_PATH4 + "Connected with result code " + str(rc))
    print(MQTT_PATH5 + "Connected with result code " + str(rc))
    print(MQTT_PATH6 + "Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH1)
    client.subscribe(MQTT_PATH2)
    client.subscribe(MQTT_PATH3)
    client.subscribe(MQTT_PATH4)
    client.subscribe(MQTT_PATH5)
    client.subscribe(MQTT_PATH6)


token = "Jyrg8gT879LyBjyZCYaDMNb_cIkN67NcNC_EFY_EkYdK_RoRDLmG5OA9ilZttJbBsP-HpYJ1KeSDBrRf3TS3ug=="
org = "SRSA"  # CHANGE TO YOUR INFLUXDB CLOUD ORGANIZATION
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"  # CHANGE CHANGE TO YOUR INFLUXDB CLOUD HOST URL
bucket = "project_bucket"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# The callback for when a PUBLISH message is received from the server.
temperaturas = []

def on_message(client, userdata, msg):
    if str(msg.topic) == "19_temperature":
        top = str(msg.topic)
        temperatura = float(msg.payload)
        temperaturas.append(temperatura)
        print(f"O valor da temperatura em {top}: {temperatura}")
        p = influxdb_client.Point("[Temperature]").field("temperature", temperatura).time(datetime.now())  # CHANGE TO YOUR MEASUREMENT NAME
        write_api.write(bucket=bucket, org=org, record=p)
        med_cel = statistics.mean(temperaturas)
        med_far = (med_cel * 9/5) + 32
        print(f"Media das temperaturas registadas: Celsius --> {med_cel} | Fahrenheit --> {med_far} ")
        message = None
        if top in last_alarms:
            if not (temperature_min <= temperatura <= temperature_max):
                elapsed_time = time.time() - last_alarms[top]["timestamp"]
                if elapsed_time < 20:
                    return
                else:
                    start_time = datetime.fromtimestamp(last_alarms[top]["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
                    message = generate_message("19_temperature", temperatura, "STARTED", start_time)

            if temperature_min <= temperatura <= temperature_max:
                message = generate_message("19_temperature", temperatura, "CANCELLED", generate_timestamp())
                del last_alarms[top]
        else:
            last_alarms[top] = {"value": temperatura, "timestamp": time.time()}
            message = generate_message("19_temperature", temperatura, "NEW", generate_timestamp())

        if message is not None:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ClientSocket.sendto(str.encode(message), ("10.9.0.2", 5001))

    elif str(msg.topic) == "19_luminosity":
        top = str(msg.topic)
        luminosidade = float(msg.payload)
        print(f"O valor da luminosidade em {top}: {luminosidade}")
        p = influxdb_client.Point("[Luminosity]").field("luminosity", luminosidade).time(datetime.now())  # CHANGE TO YOUR MEASUREMENT NAME
        write_api.write(bucket=bucket, org=org, record=p)
        message = None
        if top in last_alarms:
            if not (luminosity_min <= luminosidade <= luminosity_max):
                elapsed_time = time.time() - last_alarms[top]["timestamp"]
                if elapsed_time < 20:
                    return
                else:
                    start_time = datetime.fromtimestamp(last_alarms[top]["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
                    message = generate_message("19_luminosity", luminosidade, "STARTED", start_time)

            if luminosity_min <= luminosidade <= luminosity_max:
                message = generate_message("19_luminosity", luminosidade, "CANCELLED", generate_timestamp())
                del last_alarms[top]
        else:
            last_alarms[top] = {"value": luminosidade, "timestamp": time.time()}
            message = generate_message("19_luminosity", luminosidade, "NEW", generate_timestamp())

        if message is not None:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ClientSocket.sendto(str.encode(message), ("10.9.0.2", 5001))

    elif str(msg.topic) == "19_pressure":
        top = str(msg.topic)
        pressao = float(msg.payload)
        print(f"O valor da pressao em {top}: {pressao}")
        p = influxdb_client.Point("[Pressure]").field("pressure", pressao).time(datetime.now())  # CHANGE TO YOUR MEASUREMENT NAME
        write_api.write(bucket=bucket, org=org, record=p)
        message = None
        if top in last_alarms:
            if not (pressure_min <= pressao <= pressure_max):
                    elapsed_time = time.time() - last_alarms[top]["timestamp"]
                    if elapsed_time < 20:
                        return
                    else:
                        start_time = datetime.fromtimestamp(last_alarms[top]["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
                        message = generate_message("19_pressure", pressao, "STARTED",start_time)

            if pressure_min <= pressao <= pressure_max :
                message = generate_message("19_pressure", pressao, "CANCELLED", generate_timestamp())
                del last_alarms[top]
        else:
            last_alarms[top] = {"value": pressao, "timestamp": time.time()}
            message = generate_message("19_pressure", pressao, "NEW", generate_timestamp())

        if message is not None:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ClientSocket.sendto(str.encode(message), ("10.9.0.2", 5001))

    elif str(msg.topic) == "sensor_data_hum_1":
        top = str(msg.topic)
        hum1 = float(msg.payload)
        p = influxdb_client.Point("[Humidity]").field("humidity1", hum1).time(datetime.now())  # CHANGE TO YOUR MEASUREMENT NAME
        write_api.write(bucket=bucket, org=org, record=p)
        print(f"O valor da humidade em {top}: {hum1}")

    elif str(msg.topic) == "sensor_data_hum_2":
        top = str(msg.topic)
        hum2 = float(msg.payload)
        p = influxdb_client.Point("[Humidity]").field("humidity2", hum2).time(datetime.now())  # CHANGE TO YOUR MEASUREMENT NAME
        write_api.write(bucket=bucket, org=org, record=p)
        print(f"O valor da humidade em {top}: {hum2}")

    elif str(msg.topic) == "sensor_data_energy":
        top = str(msg.topic)
        energia = str(msg.payload)
        p = influxdb_client.Point("[Energy]").field("energy", energia).time(datetime.now())  # CHANGE TO YOUR MEASUREMENT NAME
        write_api.write(bucket=bucket, org=org, record=p)
        print(f"O valor da energia consumida no {top}: {energia}")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT)
client.loop_forever()  # use this line if you don't want to write any further code. It blocks the code forever to check for data
# client.loop_start() #use this line if you want to write any more code here