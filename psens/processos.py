'''
This module is the main loop:
    - init logger
    - create childs & resucitate-it
    - read & check config files
    - check dependencies
    - Start dependecies
      |- mosquitto
      |- SSH 
    
created on Tue Jul 29 10:12:58 2014

@author: mcollado
'''


from multiprocessing import Process
import logging
import importlib
import json
import sys
import os
import time
# Import custom modules
from sensors import bogus
from pcontrol import pControl

# create logger
logger = logging.getLogger('PSENSv0.1')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('log/debug.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -
                               %(funcName)s - %(lineno)d - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

if len(sys.argv) > 2:
    logger.warning('Too much arguments\nUsage: %s config.file\nDefault configfile = "config.json"', str(sys.argv[0]))
elif len(sys.argv) == 2:
    conf_file = str(sys.argv[1])
else:
    conf_file = "config.json"

try:
    os.access(conf_file, os.R_OK)
    with open(conf_file) as jsonfile:
        config = json.load(jsonfile)
except IOError, err:
    logger.warning("Error: %s not found. %s", conf_file, err)
    sys.exit(0)

json.dumps(config, sort_keys=True, ensure_ascii=False)


sensorsList = config['config']['sensors']
configData = config['config']['app']

logger.warning("Start Monitoring System UTC %s",
               time.asctime(time.gmtime(time.time())))

for s in sensorsList:
    try:
        # print s
        """
        Create new dict from sensorList + configData and 
        pass it to new process 

        Control process can't be readSersor() must be another function:
        pcontrol.py
        """
        p = Process(target=pControl, args=(s, configData,))
        p.start()
        logger.warning("Starting Module: %s PID: %i", s["name"], p.pid)
        while True:
            if not p.is_alive():
                logger.warning('%s is DEAD - Restarting-it', s['name'])
                p.terminate()
                p.run()
                time.sleep(0.1)
                logger.warning("New PID: %s", str(p.pid))

    except KeyboardInterrupt:
        # Not working, not hidding Traceback
        logger.warning('Shutdown Monitoring system UTC %s', 
                       time.asctime(time.gmtime(time.time())))
        p.join(timeout=2)
        sys.exit(0)
    except Exception, err:
        logger.warning("Error: %s", str(err))
    finally:
        p.join()
