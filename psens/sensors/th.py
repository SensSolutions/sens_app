'''
Module containig temperature and humidity modules

created on Tue Jul 29 10:12:58 2014

@author: mcollado
'''

from random import randint
import time
import datetime
import logging
import json

logger = logging.getLogger('PSENSv0.1')


def dht(d):
    ''' Function to recover data from DHT type sensor with Adafruit Library '''
    try:
        # import Adafruit_DHT
        while True:
            """
            Try to grab a sensor reading.  Use the read_retry
            method which will retry up to 15 times to get a sensor reading
            (waiting 2 seconds between each retry).
            """
            #d['humidity'], d['temperature'] = Adafruit_DHT.read_retry(round(d['model'],2), round(d['pin'],2)
            d['humidity'], d['temperature'] = (50.0, 25.5)

            """
            Note that sometimes you won't get a reading and
            the results will be null (because Linux can't
            guarantee the timing of calls to read the sensor).
            If this happens try again!
            """
            if d['humidity'] is not None and d['temperature'] is not None:
                now = datetime.datetime.now()
                d['hora'] = now.strftime("%Y-%m-%d %H:%M:%S")
                logger.debug("Data read: %s", json.dumps(d, sort_keys=True))
                time.sleep(d['sleep_time'])
            else:
                logger.warning("Failed to get reading. Try again!")
                time.sleep(d['sleep_time'])

    except KeyboardInterrupt:
        pass
        # Just to capture the Traceback
    except Exception, err:
        logger.warning("Critical Error: %s", err)

    return d

def ds18b20(d, *o):
    ''' Function to recover data from DS18B20 type sensor '''
    try:
        if o:
            for val in o:
                print "Others: " + val

        print "\t\t[+]Process name: " + d['name'] + " | " + __name__
        print "\t\t[+]Sensor subtype: " + d['subtype']

        t = randint(1, 10)
        print "\t\t[+]Going to sleep for " + str(t) + "s"
        time.sleep(t)
        print "\t\t[+]" + d['name'] + " say by by"
    except Exception, e:
        print "\t\t[+]Error: " + str(e) + " on module: " + __name__


def joke(d):
    """Bogus function"""
    print d
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')
