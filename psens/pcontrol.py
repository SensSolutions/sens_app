"""
This module  control the main loop of every sensor and/or actuator.

created on Mon Sep 07 10:12:58 2015

@author: mcollado
"""
import importlib
import time
import logging
# import custom modules
from senddata import sendData
from sensor import readSensor
from actuator import loadActuators


logger = logging.getLogger('PSENSv0.1')


def pControl(device):
    """
    This functions control the main loop of every  device
    A device can be a sensor, an actuator, an hibrid, etc.
    Every devide type must have his own function to define
    how it works

    Code must get actuators definition from config dict and import functions,
    execute and send data
    """

    if device['type'] == "sensor":
        pSensor(device)
    elif device['type'] == "actuator":
        pActuator(device)
    elif device['type'] == "hibrid":
        pHibrid(device)
    else:
        logger.warning("Error No controler found for %s device type", device['type'])


def pSensor(device):
    """
    Here we define the bussines logic for sensors.
    Specific functions for sensors are defined in sensor.py
    
    readSensor() returns a list whith sensor data, usualy a row for every
    value:
    [{"name": "air", "temperature": 25.5, "type": "sensor", "what": "sensors"},
     {"name": "air", "humidity": 50.5, "type": "sensor", "what": "sensors"}]

    device mut look like this:

    {'brokerLocalIP': '127.0.0.1',
     'brokerRemoteIP': '84.88.95.122',
     'cache_suffix': '.cache',
     'clientID': 'PSens',
     'driver': 'dht',
     'location': 'pool',
     'logpath': 'log',
     'model': 22,
     'name': 'air',
     'org': 'sens.solutions',
     'path': '/Users/mcollado/Coding/rasp-tempsensor/psens',
     'pin': 4,
     'place': 'pool',
     'results': [{'dname': 'temperature',
                  'dvalue': 25.5,
                  'time': '2015-09-09 16:22:28'},
                 {'dname': 'humidity',
                  'dvalue': 50.0,
                  'time': '2015-09-09 16:22:28'}],
     'sleep_time': 10,
     'subtype': 'th',
     'type': 'sensor',
     'what': 'sensors'}
    """
    while True:
        # from pprint import pprint

        sResultList = readSensor(device)
        logger.debug("Results: %s", sResultList)
        device['results'] = sResultList
        # pprint(device)
        """Append result list to device dictionary"""
        sendData(device)
        time.sleep(device['sleep_time'])


def pActuator(device):
    """
    Here we define the bussines logic for actuators.
    Specific functions for sensors are defined in actuators.py
    """
    while True:
        actData = loadActuators(device)
        sendData(actData)
        time.sleep(device['sleep_time'])


def pHibrid(device):
    """
    Here we define the bussines logic for a sensor plus an actuator.
    """
    while True:
        """To think and define this Block"""
        sResultList = readSensor(device)
        sendData(sResultList)
        if "actuators" in device:
            for actuator in device['actuators']:
                try:
                    act_module = importlib.import_module(actuator, package=None)
                    act_function = getattr(act_module, device['act_function'])
                except Exception, err:
                    logger.warning("Error: %s", err)
                act_result = act_function(sResultList)
                sendData(act_result)

        """ Until here """
        time.sleep(device['sleep_time'])

