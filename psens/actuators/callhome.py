"""
The following code will subscribe on topic f and republish on topic f2

created on Fry Sep 18 11:55:39 2015

@author: mcollado
"""
import datetime
import logging
import paho.mqtt.client as mqttc
import subprocess
import urllib


logger = logging.getLogger('PSENSv0.1')


def call_home(d):
    """
    This functions publish the public ip address.
    to retreive results in DB:
    SELECT timestamp, type, dname, dvalue FROM data WHERE type='actuator' ORDER BY timestamp DESC LIMIT 20;
    """
    l = list()
    d['topic'] = d['org'] + "/" + d['location'] + "/callhome"
    try:
        messagech = get_public_ip(d['get_public_ip'])
        logger.debug("Got message to send: %s to %s", messagech, d['get_public_ip'])
        now = datetime.datetime.now()
        hora = now.strftime("%Y-%m-%d %H:%M:%S")
        l.insert(0, {'dname': 'public_ip', 'dvalue': messagech, 'timestamp': hora})

        """
        def on_connect(mosq, obj, rc):
           mqttc.subscribe(d['topic'] , 0)
           logger.debug("Connected with Result Code: %s", str(rc))

        def on_message(mosq, obj, msg):
            global message
            message = msg.topic + " " + str(msg.qos) + " " + str(msg.payload)
            logger.warning("Received: %s", message)
            (ip,port) = msg.payload.split(":")
            #message = msg.payload
            #mqttc.publish("f2",msg.payload);
            logger.warning("Calling home: %s:%s", ip, port)
            #startSSH(ip, port)
            logger.debug("Hanging callhome")

        def on_publish(mosq, obj, mid):
            logger.debug("mid: %s", str(mid))

        def on_subscribe(mosq, obj, mid, granted_qos):
            logger.debug("Subscribed: %s QOS: %s", str(mid), str(granted_qos))

        def on_log(mosq, obj, level, string):
            logger.debug(string)

        mqttc = mqtt.Client(d['clientID'])
        # Assign event callbacks
        #mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_publish = on_publish
        #mqttc.on_subscribe = on_subscribe
        mqttc.on_log = on_log # comment on production
        # Connect
        mqttc.connect(d['brokerRemoteIP'], 1883,60)


        # Continue the network loop
            mqttc.loop_forever()
        """
    except KeyboardInterrupt:
        pass
        # Just to capture the Traceback
    except Exception, err:
        logger.warning("Critical Error: %s", err)

    return l


def get_stunnel(d):
    """
    This functions subscribes to a broker's topic waiting for ip, port and user
    to stablish a reverse tunnel
    """
    d['topic'] = d['org'] + "/" + d['location'] + "/actuator/callhome/remote_ip"
    mqtt_con = None

    def on_connect(mosq, obj, rc):
        #mqtt_con.subscribe(d['topic'], 0)
        logger.debug("Connected with Result Code: %s", str(rc))


    def on_message(mosq, obj, msg):
        global message
        message = msg.topic + " " + str(msg.qos) + " " + str(msg.payload)
        logger.warning("Received: %s", message)
        (ip, port, uid) = msg.payload.split(":")
        # message = msg.payload
        # mqttc.publish("f2",msg.payload);
        logger.warning("Got message from broker: %s", message)
        logger.warning("Calling home: IP: %s Port:%s User: %s", ip, port, uid)
        startSSH(ip, port, uid)
        logger.debug("Hanging callhome")


    def on_publish(mosq, obj, mid):
        logger.debug("mid: %s", str(mid))


    def on_subscribe(mosq, obj, mid, granted_qos):
        logger.warning("Subscribed: %s QOS: %s", str(mid), str(granted_qos))
        print("Subscribed: " + str(mid) + " " + str(granted_qos))


    def on_log(mosq, obj, level, string):
        logger.debug(string)

    try:
        mqtt_con = mqttc.Client(d['clientID'])
        logger.debug("Creating object: %s", mqtt_con)
        # Assign event callbacks
        mqtt_con.on_message = on_message
        mqtt_con.on_connect = on_connect
        mqttc.on_publish = on_publish
        mqtt_con.on_subscribe = on_subscribe
        mqtt_con.on_log = on_log  # comment on production
        # Connect
        mqtt_con.connect(d['brokerRemoteIP'], 1883, 60)
        #mqtt_con.subscribe("$SYS/#", 0)
        logger.warning("Going to subscribe to: %s", str(d['topic']))
        mqtt_con.subscribe(str(d['topic']))

        # Continue the network loop
        mqtt_con.loop_forever()
    except KeyboardInterrupt:
        pass
        # Just to capture the Traceback
    except Exception, err:
        logger.warning("Critical Error: %s", err)

    return None


def startSSH(ip, port, uid):
    """
    This function establish a reverse tunnel from PSens to tunnel server
    """
    #ip = "84.88.95.122"
    #port = "22"
    #uid = "pi"
    p = None
    try:
        p = subprocess.Popen(["ssh", "-N", "-R", port + ":localhost:22", uid + "@" + ip], stdout=subprocess.PIPE)
        output, err = p.communicate()
        logger.debug(output)
    except Exception, err:
        logger.warning("Can't create tunnel: %s", err)

def get_public_ip(ip):
    """ This functions return the public IP
    put this PHP script somewhere and call it remoteip.php:
    <?php echo $_SERVER['REMOTE_ADDR']; ?>
    """
    p = None
    try:
        p = urllib.urlopen('http://' + ip + '/remoteip.php').read()
    except Exception, err:
        logger.warning("Can't get public IP: %s", err)

    return p



"""
The value of rc indicates success or not:

0: Connection successful
1: Connection refused - incorrect protocol version
2: Connection refused - invalid client identifier
3: Connection refused - server unavailable
4: Connection refused - bad username or password
5: Connection refused - not authorised
6-255: Currently unused.
"""

"""
Let's assume that Destination's IP is 192.168.20.55 (box that you want to access).
You want to access from Linux client with IP 138.47.99.99.
Destination (192.168.20.55) <- |NAT| <- Source (138.47.99.99)
1. SSH from the destination to the source (with public ip) using command below:

ssh -N -R 19999:localhost:22 sourceuser@138.47.99.99

* port 19999 can be any unused port.

Remote port forwarding for anyone at work !
"""
"""
If you want everybody at source to be able to SSH into your destination 
machine, there's no -g option for remote forward, so you need to change the
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
