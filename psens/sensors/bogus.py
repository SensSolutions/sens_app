'''
Module containig bogus module and sensor template

created on Tue Jul 29 10:12:58 2014

@author: mcollado
'''
import time
from random import randint
import logging
import sys

logger = logging.getLogger('PSENSv0.1')

def bogus(*o):
    """Bogus function does nothing and return a empty dict"""
    d = {}
    try:
        if o:
            for val in o:
                print "Others: " + val

        logger.debug("process name: %s Sensor subtype: %s driver: %s",
                     d['name'], d['subtype'], d['driver'])

# Specific code starts here

        t = randint(1, 10)
        logger.debug("%s is going to sleep for %i s", d['name'], t)
        time.sleep(t)
        logger.warning("%s says bye bye.", d['name'])

# Specific code ends here

    except Exception, err:
        logger.warning("Error: %s", str(err))
    except KeyboardInterrupt:
        sys.exit(0)

    return d

