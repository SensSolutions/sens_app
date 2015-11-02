#!/usr/bin/python
# -*- coding: utf-8 -*-
#import paho.mqtt.client as paho
import paho.mqtt.client as paho

host="84.88.95.122"
port=1883

def on_connect(pahoClient, obj, rc):
# Once connected, publish message
    try:
        client.publish("sens.solutions/pool/internal/status/ErrorCode", "Hello World", 0)
        print "Connected Code = %d"%(rc)
    except:
        print "Connected Code = %d"%(rc)

def on_log(pahoClient, obj, level, string):
        print string

def on_publish(pahoClient, packet, mid):
# Once published, disconnect
        print "Published"
        pahoClient.disconnect()

def on_disconnect(pahoClient, obj, rc):
        print "Disconnected"

# Create a client instance
client=paho.Client()

# Register callbacks
client.on_connect = on_connect
client.on_log = on_log
client.on_publish = on_publish
client.on_disconnnect = on_disconnect

#Set userid and password
#client.username_pw_set(userID, password)

#connect
x = client.connect(host, port, 60)

client.loop_forever()
