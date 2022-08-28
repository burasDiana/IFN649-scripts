import paho.mqtt.client as mqtt
import serial
import time
import string

# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different
ser = serial.Serial("/dev/rfcomm0", 9600)
ser.write(str.encode('Start\r\n'))
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ifn649") #ifn649 #teensy_data

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #text = msg.payload.decode('utf-8').strip('\r\n')
    #print("Received data:")
    #print(text)
    print(msg.topic+" "+str(msg.payload))
    ser.write(str.encode(str(msg.payload)))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("3.110.142.220", 1883, 60)

client.loop_forever()

