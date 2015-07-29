import paho.mqtt.publish as publish
import time
import logging
import csv
import os

logger = logging.getLogger('PSENSv0.1')


def sendCache(brokerIP, clientId, cfgfile):
    logger.debug(sendCache)

    Config = SafeConfigParser()
    Config.read(cfgfile)
    
    cachefile  = Config.get('DEFAULT', 'cachefile') 
    logger.debug ('Opening cache file %s', (cachefile))


    with open (cachefile, "r") as csvfile:
        f = csv.reader(csvfile, delimiter =';')
        try:
            for row in f:
              login = publish.single(topic , msg, hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)
              logging.warning('Send line: %i - topic: %s msg: %s',(f.line_num, topic, msg))
        except:
            csv.Error as e:
            logger.warning('Error reading %s, line %d %d: %s' % (cachefile, f.line_num, e))

    os.remove(cachefile)

