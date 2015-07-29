import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import time
import logging
import csv
import os

#import sendcache

logger = logging.getLogger('PSENSv0.1')
port=1883

def pControl(org, place, brokerIP, clientId, cachefile):
    logger.debug(pControl)
    topic = org + "/" + place + "/" + "internal/status/ErrorCode"
    message = "0"

    while True:
        try:
            # logger.debug('Topic: %s : %s | Client ID: %s', (topic, message, clientId))
            print 'Topic: ' + topic + ': '+ message + ' | Client ID: ' + clientId
            login = publish.single(topic, message, hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)
            print 'Error: '+login
            #if (login):
            logger.debug(login)
            if os.path.exists(cachefile):
                sendCache(brokerIP, clientId, cfgfile)
                logger.debug("Cache sent")
            else: 
                logger.debug('No cache file exists')
        except:
            logger.warning('Connecting Error to %s', (brokerIP))
            with open(cachefile, 'w') as csvfile:
                cachewriter = csv.writer(csvfile, delimiter = ';')
                cachewriter.writerow([topic, message])
            logger.debug('Writing line to cache file: %s',(cachefile))
        else:
            logger.debug('Message sent')

        time.sleep(1)


