"""
The following code will subscribe on topic f and republish on topic f2

created on Fry Sep 18 11:55:39 2015

@author: mcollado
"""

import paho.mqtt.client as mqtt
import subprocess

logger = logging.getLogger('PSENSv0.1')

def callHome(d):
     d['topic'] = d['org'] + "/" + d['location'] + "/callhome"
    message = 'ON'
    def on_connect(mosq, obj, rc):
        mqttc.subscribe(d['topic'] , 0)
        logger.debug("Connected with Result Code: %s", str(rc))
    
    def on_message(mosq, obj, msg):
        global message
        missatge = msg.topic + " " + str(msg.qos) + " " + str(msg.payload)
        logger.warning("Received: %s", missatge)
        (ip,port) = msg.payload.split(":")
        #message = msg.payload
        #mqttc.publish("f2",msg.payload);
        logger.warning("Calling home: %s:%s", ip, port)
        startSSH(ip, port)
        logger.debug("Hanging callhome")
    
    def on_publish(mosq, obj, mid):
        logger.debug("mid: %s", str(mid))
    
    def on_subscribe(mosq, obj, mid, granted_qos):
        logger.debug("Subscribed: %s QOS: %s", str(mid), str(granted_qos))
    
    def on_log(mosq, obj, level, string):
        logger.debug(string)
    
    mqttc = mqtt.Client(d['clientID'])
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log # comment on production
    # Connect
    mqttc.connect(d['brokerRemoteIP'], 1883,60)
    
    
    # Continue the network loop
    mqttc.loop_forever()

def startSSH(ip, port):
    p = subprocess.Popen(["ssh", "-N", "-R", port + ":localhost:22", "pi@" + ip], stdout=subprocess.PIPE)
    output, err = p.communicate()
    logger.debug(output)

"""
TODO: use diferent users to log when callhome
"""


"""
The value of rc indicates success or not:

0: Connection successful 1: Connection refused - incorrect protocol version 2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 4: Connection refused - bad username or password 5: Connection refused - not authorised 6-255: Currently unused.
"""



"""
Let's assume that Destination's IP is 192.168.20.55 (box that you want to access).
You want to access from Linux client with IP 138.47.99.99.
Destination (192.168.20.55) <- |NAT| <- Source (138.47.99.99)
1. SSH from the destination to the source (with public ip) using command below:

ssh -N -R 19999:localhost:22 sourceuser@138.47.99.99

* port 19999 can be any unused port.

Remote port forwarding for anyone at work !

If you want everybody at source to be able to SSH into your destination 
machine, there’s no -g option for remote forward, so you need to change the 
SSH configuration of source, add to sshd_config :

GatewayPorts yes

2. Now you can SSH from source to destination through SSH tuneling:

ssh localhost -p 19999

3. 3rd party servers can also access 192.168.20.55 through Destination (138.47.99.99).
Destination (192.168.20.55) <- |NAT| <- Source (138.47.99.99) <- Bob's server
3.1 From Bob's server:

ssh sourceuser@138.47.99.99

3.2 After the sucessful login to Source:

ssh localhost -p 19999

* the connection between destination and source must be alive at all time.
"""
