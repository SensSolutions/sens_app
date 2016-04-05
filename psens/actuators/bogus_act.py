'''
Module containig bogus module and actuator template

created on Tue Jul 29 10:12:58 2014

@author: mcollado
'''
import time
import datetime
from random import randint
import logging
import sys

logger = logging.getLogger('PSENSv0.1')

def bogus(d, *o):
    """Bogus Function"""
    l = list()
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
        d['message']= "Bogus actuator, nothing to do"
        now = datetime.datetime.now()
        hora = now.strftime("%Y-%m-%d %H:%M:%S")
        l.insert(0, {'dname': 'message', 'dvalue': 'Bogus actuator, nothing to do', 'timestamp': hora})

# Specific code ends here

    except Exception, err:
        logger.warning("Error: %s", str(err))
    except KeyboardInterrupt:
        sys.exit(0)

    return l

