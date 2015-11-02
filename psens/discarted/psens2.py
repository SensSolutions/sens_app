#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
created on Tue Jul 29 10:12:58 2014

@author: mcollado
"""


import random
from ConfigParser import SafeConfigParser
import sys
from multiprocessing import Process
import time
import os
import logging
from daemon import runner
# import paho.mqtt.publish as publish
# import ConfigParser
# import Adafruit_DHT
# import datetime

# Importing my modules
import pcontrol
#import airsensor

# create logger
logger = logging.getLogger('PSENSv0.1')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

Config = SafeConfigParser()
'''
if len(sys.argv) > 2:
    print "Too much arguments"
    print "Usage " + str(sys.argv[0]) + "psens.cfg"
else:
    cfgfile = str(sys.argv[1])

if len(sys.argv) == 1:
    cfgfile = "psens.cfg"

Config.read(cfgfile)
'''
Config.read("psens.cfg")

brokerIP   = Config.get('Broker', 'broker_ip')
clientId   = Config.get('Broker', 'client_id') + "/" +  str(random.randint(1000,9999))
topic      = Config.get('Broker', 'topic')
sleepTime  = Config.getfloat('Broker', 'sleep_time')
writeLog   = Config.getboolean('Log','write_log')
logName    = Config.get('Log', 'logname')

try:
    # sens.solutions/pool/sensors/air/humidity
    parts = topic.split('/')
    org = parts[0]
    place = parts[1]
    what = parts[2]
except:
    org = 'unknown'
    place = 'unknown'
    what = 'unknow'


# IMplementing connexion debugging
def info(title):
    logger.debug(title)
    logger.debug('debug message')

    if hasattr(os, 'getppid'):  # only available on Unix
        logger.debug('parent process : %i', os.getppid())
    logger.debug('process id: %i', os.getpid())


class App():

    def __init__(self):
        # On linux use /dev/tty
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        # self.stdout_path = '/dev/tty'
        # self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/Users/mcollado/Coding/rasp-tempsensor/psens/psens2.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            # Main code goes here ...
            # Note that logger level needs to be set to logging.DEBUG before
            # this shows up in the logs
            logger.debug("Starting main loop")

            if __name__ == '__main__':
                logger.debug('Starting Main')
                info('main line')
                p = Process(target=pcontrol.pControl, args=(org, place, brokerIP, clientId))
                p.start()
#                o = Process(target=airsensor.airSensor, args=(org, place, brokerIP, clientId, cfgfile))
#                o.start()
                while True:
                    if not p.is_alive():
                       logger.warning('pControl is DEAD - Restarting-it')
                       p.terminate()
                       p.run()
                       time.sleep(0.1)
                       logger.warning("New PID: " + str(p.pid))
                p.join()
'''                    if not o.is_alive():
                       logger.warning('airSensor is DEAD - Restarting-it')
                       o.terminate()
                       o.run()
                       time.sleep(0.1)
                       logger.warning("New PID: " + str(o.pid))'''


#                   o.join()

app = App()

daemon_runner = runner.DaemonRunner(app)
# This ensures that the logger file handle does not
# get closed during daemonization
daemon_runner.daemon_context.files_preserve = [fh.stream]
daemon_runner.do_action()
