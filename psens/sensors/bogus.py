import time
from random import randint
import logging
import sys

logger = logging.getLogger('PSENSv0.1')

def bogus(d,*o):
    try:
        if o:
            for val in o:
                print "Others: " + val

        logger.debug("process name: %s Sensor subtype: %s driver: %s", d['name'], d['subtype'], d['driver'])

        t = randint(1, 10)
        logger.debug("%s is going to sleep for %i s", d['name'], t)
        time.sleep(t)
        logger.warning("%s says bye bye.", d['name'])
    except Exception, err:
        logger.warning("Error: %s", str(err))
    except KeyboardInterrupt:
        sys.exit(0)

