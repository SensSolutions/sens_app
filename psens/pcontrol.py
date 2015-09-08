"""
This module  control the main loop of every sensor & actuator.

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

    while True:
        sdata = readSensor(device)
        sendData(sdata)


        time.sleep(device['sleep_time'])


def pSensor(device):
    """
    Here we define the bussines logic for sensors.
    Specific functions for sensors are defined in sensor.py
    """
    while True:
        sdata = readSensor(device)
        sendData(sdata)
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
        sdata = readSensor(device)
        sendData(sdata)
        if "actuators" in device:
            for actuator in device['actuators']:
                act_module = importlib.import_module(actuator, package=None)
                try:
                    act_function = getattr(act_module, device['act_function'])
                except Exception, err:
                    logger.warning("Error: %s", err)
                act_result = act_function(sdata)
                sendData(act_result)

        """ Until here """
        time.sleep(device['sleep_time'])

