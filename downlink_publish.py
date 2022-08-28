import paho.mqtt.publish as publish
publish.single("ifn649", "ON", hostname="3.110.142.220")
print("Done")