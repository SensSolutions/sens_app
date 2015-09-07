"""
This module  control the main loop of every sensor & actuator.

created on Mon Sep 07 10:12:58 2015

@author: mcollado
"""
# import paho.mqtt.publish as publish
# import paho.mqtt.client as mqtt
import importlib
import time
import logging
# import csv
# import os
# import datetime

# import custom modules
from senddata import sendData
from readsensor import readSensor


logger = logging.getLogger('PSENSv0.1')
port = 1883
module = "PControl"

""" OLD MODULE CODE


def pControl(org, place, brokerIP, clientId, cachefile):

    topic = org + "/" + place + "/" + "internal/status/ErrorCode"
    message = "0"
    cachefile = cachefile + module
#
    mqttc = mqtt.Client(clientId)
    mqttc.loop_start()

    logger.warning("Starting module: %s-%s", __name__, module)
    while True:
        try:

            # Check for cache file and send contens
            #
            if os.path.isfile(cachefile):
                sendcache.sendCache(brokerIP, clientId, cachefile)

            mqttc.connect(brokerIP, port)
            mqttc.publish(topic, message)
            # implement clean disconnect from broker. Maybe
            logger.debug('Topic: %s : %s | Client ID: %s', topic, message, clientId)
        except Exception, e:
            logger.warning('Error: %s, %s', str(e), brokerIP)

# for debug pourposes, no real need
            now = datetime.datetime.now()
            hora = now.strftime("%Y-%m-%d %H:%M:%S")

# Move to a cache file to maintain code organized.
            with open(cachefile + ".csv", 'a') as csvfile:
                cachewriter = csv.writer(csvfile, delimiter=';')
                cachewriter.writerow([topic, message, hora])
            logger.debug('Writing CSV line to cache file: %s', cachefile)



        time.sleep(1)
"""


def pControl(d):
    """This functions control the main loop of every sensor & actuator"""
    """
    Code must get actuators definition from config dict and import functions,
    execute and send data
    """

    while True:
        sdata = readSensor(d)
        sendData(sdata)

        """To think and define this Block"""
        if "actuators" in d:
            for actuator in d['actuators']:
                act_module = importlib.import_module(actuator, package=None)
                try:
                    act_function = getattr(act_module, d['act_function'])
                except Exception, err:
                    logger.warning("Error: %s", err)
                act_result = act_function(sdata)
                sendData(act_result)

        """ Until here """

        time.sleep(d['sleep_time'])

