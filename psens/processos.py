"""
created on Tue Jul 29 10:12:58 2014

@author: mcollado
"""


from multiprocessing import Process
import logging
from sensors import bogus
import importlib
import json
import sys
import time

"""
sensorsList=[{"name":"air", "type" : "th", "subtype" : "DHT", "driver":"dht"},
        {"name":"water", "type":"th", "subtype":"ds18b20", "driver":"ds18b20"},
        {"name":"internal", "type":"bogus", "subtype":"PSens", "driver":"bogus", "sleep_time":60},
        {"name":"joke", "type":"th", "subtype":"Joke", "driver":"joke"}]
"""

if len(sys.argv) > 2:
    print "Too much arguments"
    print "Usage " + str(sys.argv[0]) + "config.file"
    print 'default configfile = "config.json"'
# elif len(sys.argv) == 1:
#    conf_file = str(sys.argv[1])
else:
    conf_file = "config.json"

with open(conf_file) as jsonfile:
    config = json.load(jsonfile)

json.dumps(config, sort_keys=True, ensure_ascii=False)


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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


def sensor(SensorDict):
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
        logger.debug("Loading Sensor module %s with driver %s", s_module, SensorDict['driver'])
        my_module = importlib.import_module(s_module, package=None)
        try:
            my_function = getattr(my_module, SensorDict['driver'])
        except AttributeError:
            logger.warning("Function not found %s (%s)", SensorDict['driver'], SensorDict)
        result = my_function(SensorDict)

    except Exception, err:
        logger.warning("Error importing custom module: %s No driver for: %s", str(err), s_module)
        # logger.warning("No driver for: ", s_module)
        logger.debug("Using Bogus function")
        bogus.bogus(SensorDict)

sensorsList = config['config']['sensors']

logger.warning("Start Monitoring System")
for s in sensorsList:
    try:
        # print s
        p = Process(target=sensor, args=(s,))
        p.start()
        logger.warning("Starting Module: %s PID: %i", s["name"], p.pid)
        while True:
            if not p.is_alive():
                logger.warning('%s is DEAD - Restarting-it', s['name'])
                p.terminate()
                p.run()
                time.sleep(0.1)
                logger.warning("New PID: %s", str(p.pid))

    except Exception, err:
        logger.warning("Error: %s", str(err))
    except KeyboardInterrupt:
        # Not working, not hidding Traceback
        logger.warning('Shutdown Monitoring system')
        p.join(timeout=2)
        sys.exit(0)
    finally:
        p.join()
