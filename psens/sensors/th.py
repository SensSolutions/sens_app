"""
Module containig temperature and humidity drivers for diferent sensors

created on Tue Jul 29 10:12:58 2014

@author: mcollado
"""

import random
import time
import datetime
import logging
import json

logger = logging.getLogger('PSENSv0.1')

""" All functions must return a list with a dictionary on every row:
    l=[{"type":"sensor","name":"XXXXX"},
       {"type":"sensor","name":"YYYYY"}]
"""


def dht(d):
    """  Function to recover data from DHT type sensor with Adafruit Library """ 
    l = list()
    try:
        import Adafruit_DHT
        """
        Try to grab a sensor reading.  Use the read_retry
        method which will retry up to 15 times to get a sensor reading
        (waiting 2 seconds between each retry).
        """
        #(humidity, temperature) = Adafruit_DHT.read_retry(round(d['model'],2), round(d['pin'],2))
        (humidity, temperature) = Adafruit_DHT.read_retry(d['model'], d['pin'])
        #(humidity, temperature) = (50.0, 25.5)
        
        """
        Note that sometimes you won't get a reading and
        the results will be null (because Linux can't
        guarantee the timing of calls to read the sensor).
        If this happens try again!
        """

        if humidity is not None and temperature is not None:
            now = datetime.datetime.now()
            hora = now.strftime("%Y-%m-%d %H:%M:%S")
            # logger.debug("Data read: %s", json.dumps(d, sort_keys=True))
            l.insert(0,{'dname':'temperature', 'dvalue':round(temperature,2), 'timestamp':hora})
            l.insert(1,{'dname':'humidity', 'dvalue':round(humidity,2), 'timestamp':hora})

            time.sleep(d['sleep_time'])
        else:
            logger.warning("Failed to get reading. Try again!")
            time.sleep(d['sleep_time'])

    except KeyboardInterrupt:
        pass
        # Just to capture the Traceback
    except Exception, err:
        logger.warning("Critical Error: %s", err)

    return l

def dht_false(d):
    """  Function to recover data from false DHT type sensor with Adafruit Library
         Same output with random imput. Used to test send function """ 
    l = list()
    try:
        humidity = random.uniform(40, 60)
        temperature = random.uniform(20, 30)
        
        now = datetime.datetime.now()
        hour = now.strftime("%Y-%m-%d %H:%M:%S")
        # logger.debug("Data read: %s", json.dumps(d, sort_keys=True))
        l.insert(0,{'dname':'temperature', 'dvalue':round(temperature,2), 'timestamp':hour})
        l.insert(1,{'dname':'humidity', 'dvalue':round(humidity,2), 'timestamp':hour})

        time.sleep(d['sleep_time'])

    except KeyboardInterrupt:
        pass
        # Just to capture the Traceback
    except Exception, err:
        logger.warning("Critical Error: %s", err)

    return l


def ds18b20(d, *o):
    """ Function to recover data from DS18B20 type sensor """
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

def oweather(d):
    """ Function recovering forecast or actual temp and hum from http://openweathermap.org/
    or http://www.wunderground.com """
    # API key: ce5cdd60706b23fec352881e70ae2b8d
    try:
        import pyowm
    except Exception, err:
        logger.warning("Critical Error: %s", err)

    l = list()
    obs = dict()
    try:
        owm = pyowm.OWM(d['api_key'])
        observation = owm.weather_at_place(d['place'])
        w = observation.get_weather()
        
        now = datetime.datetime.now()
        hora = now.strftime("%Y-%m-%d %H:%M:%S")
        # logger.debug("Data read: o%s", json.dumps(d, sort_keys=True))
        obs = w.get_temperature('celsius')
        l.append({'dname':'temperature', 'dvalue':obs['temp'], 'timestamp':hora})
        l.append({'dname':'humidity', 'dvalue':w.get_humidity(), 'timestamp':hora})
        obs = w.get_pressure()
        l.append({'dname':'pressure', 'dvalue':obs['press'], 'timestamp':hora})

        time.sleep(d['sleep_time'])

    except KeyboardInterrupt:
        pass
        # Just to capture the Traceback

    except Exception, err:
        logger.warning("Error: %s", err)

    return l
