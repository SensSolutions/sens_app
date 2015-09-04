'''
created on Tue Jul 29 10:12:58 2014

@author: mcollado
'''


from multiprocessing import Process
import logging
from sensors import bogus
import importlib
import json
import sys
import os
import time

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




def readSensor(SensorDict, ConfigData):
    '''
    This funtion loads correct driver for every sensor
    and returns the read values
    '''
    try:
        """
        http://stackoverflow.com/a/5391245
        try:
            func = getattr(modulename, funcname)
        except AttributeError:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else:
            func(arg)


        http://stackoverflow.com/a/15004155
        The gettattr function has an optional third argument for a default
        value to return if the attribute does not exist, so you could use that:

        fun = getattr(modulename, funcname, None)

        if fun is None:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else
            fun(arg)
        """

        s_module = "sensors." + SensorDict['type']
        logger.debug('Loading Sensor module %s with driver "%s"',
                     s_module, SensorDict['driver'])
        my_module = importlib.import_module(s_module, package=None)
        try:
            # print s_module
            # print my_module
            my_function = getattr(my_module, SensorDict['driver'])
            logger.debug("%s", my_module)
            # except AttributeError:
            # logger.warning("Function not found %s (%s)", SensorDict['driver'], SensorDict)
        except Exception, err:
            logger.warning("Error: %s", err)
        my_function(SensorDict)

    except Exception, err:
        logger.warning("Error importing custom module: %s No driver for: %s",
                       str(err), my_module)
        logger.debug("Using Bogus function")
        bogus.bogus(SensorDict)


def sendData(data):
    pass
    ''' This function send data recoverd by sensor to broker '''
    '''
    Must remove non required keys before send json:
    required_fields = ['name', 'last_name', 'phone_number', 'email']
    dict2 = {key:value for key, value in dict1.items() if key in required_fields}
    '''

sensorsList = config['config']['sensors']
configData = config['config']['app']

logger.warning("Start Monitoring System UTC %s",
               time.asctime(time.gmtime(time.time())))

for s in sensorsList:
    try:
        # print s
        p = Process(target=readSensor, args=(s, configData,))
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
