import paho.mqtt.client as mqtt # mosquitto.py is deprecated
import time

mqttc=mqtt.Client("ioana")
mqttc.connect("127.0.0.1", 1883)
#mqttc.subscribe("test/", 2) # <- pointless unless you include a subscribe callback
mqttc.loop_start()
while True:
    try:
        mqttc.publish("test","Hello")
        time.sleep(10)# sleep for 10 seconds before next call
        print("Hello")
    except:
        print("Error")
