"""
This module is the main loop

TODO: use NaN when no sensor value?
    import numpy as np
    a = arange(3,dtype=float)

    a[0] = np.nan
    a[1] = np.inf
    a[2] = -np.inf

TODO: Use URLparse:
    import urlparse
    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
    url = urlparse.urlparse(url_str)

    # Connect
    mqttc.username_pw_set(url.username, url.password)
    mqttc.connect(url.hostname, url.port)

TODO: merge  sensors & actuators folders.
    Both are drivers, without diference when calling it

created on Tue Jul 29 10:12:58 2014

@author: mcollado
"""

from multiprocessing import Process
import logging
import json
import sys
import os
import time
from random import randint
# Import custom modules
from pcontrol import pControl


def startup():
    """ Main function loop:
    - init logger
    - create childs & resucitate-it
    - read & check config files
    - check dependencies
    - Start dependecies
      |- local broker (mosquitto)
      |- Reverse SSH tunnel
    - ...
    """
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

    """Parse config variables (logs etc) to check accuracy"""

    deviceList = config['config']['device']

    logger.warning("Start Monitoring System UTC %s",
                   time.asctime(time.gmtime(time.time())))

    # print os.path.dirname(os.path.abspath(__file__))
    config['config']['global'][0]['path'] = os.path.dirname(os.path.abspath(__file__))
    config['config']['global'][0]['clientID'] = config['config']['global'][0]['clientID'] + "-"+ str(randint(1,99999))
    print config['config']['global'][0]['clientID']

    for device in deviceList:
        try:
            """
            Create new dict from deviceList + globalConfig and
            pass it to new process
            """
            device.update(config['config']['global'][0])
            """Merging device dict with config dict"""
            # logger.warning(device)
            p = Process(target=pControl, args=(device,))
            p.start()
            logger.warning("Starting Module: %s PID: %i", device["name"], p.pid)
            while True:
                if not p.is_alive():
                    logger.warning('%s is DEAD - Restarting-it', device['name'])
                    p.terminate()
                    p.run()
                    time.sleep(0.1)
                    logger.warning("New PID: %s", str(p.pid))

        except KeyboardInterrupt:
            # Not working, not hidding Traceback?
            logger.warning('Shutdown Monitoring system UTC %s',
                           time.asctime(time.gmtime(time.time())))
            p.join(timeout=2)
            sys.exit(0)
        except Exception, err:
            logger.warning("Error: %s", str(err))
    #    finally:
    #        p.join()

if __name__ == "__main__":
    startup()
