#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import logging
import csv
import os

logger = logging.getLogger('PSENSv0.1')

def sendCache(brokerIP, clientId, cachefile):
#    logger.warning(sendCache)
    logger.debug(sendCache)

    # Config = SafeConfigParser()
    # Config.read(cfgfile)

    # cachefile  = Config.get('DEFAULT', 'cachefile')
    logger.warning ('Reading cache file %s', cachefile)


    with open (cachefile, "r") as csvfile:
        f = csv.reader(csvfile, delimiter =';')
        try:
            mqttc=mqtt.Client(clientId)
            mqttc.connect(brokerIP, 1883)

            for row in f:
                logger.warning('Read line: %i - topic: %s msg: %s',f.line_num, row[0], str(row[1]))
                mqttc.publish(row[0], row[1])
                #publish.single(row[0] , row[1], brokerIP, client_id= clientId, will=None, auth=None, tls=None)
                logger.warning('Send line: %i - topic: %s msg: %s',f.line_num, row[0], str(row[1]))

            logger.debug("Cache sent, removing cachefile: %s",cachefile)
            os.remove(cachefile)

        except Exception, e:
            logger.warning('Error trying to send cache: %s', str(e))
            # csv.Error as e:
            # logger.warning('Error reading %s, line %d: %s' % (cachefile, f.line_num, csv.Error))








