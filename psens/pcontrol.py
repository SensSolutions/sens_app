#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import logging
import csv
import os
import datetime
import json

import sendcache

logger = logging.getLogger('PSENSv0.1')
port=1883

def pControl(org, place, brokerIP, clientId, cachefile):
    logger.warning(pControl)
    topic = org + "/" + place + "/" + "internal/status/ErrorCode"
    message = "0"

#
    mqttc=mqtt.Client(clientId)
    mqttc.loop_start()

    logger.critical("Start sending data")
    while True:
        try:

# Check for cache file and send contens
#
            if os.path.isfile(cachefile):
                sendcache.sendCache(brokerIP, clientId, cachefile)
#
            mqttc.connect(brokerIP, port)
            mqttc.publish(topic, message)
# implement clean disconnect from broker. Maybe
            logger.debug('Topic: %s : %s | Client ID: %s', topic, message, clientId)
        except Exception, e:
            logger.warning('Error: %s, %s',str(e), brokerIP)
# for debug pourposes, no need

            now = datetime.datetime.now()
            hora = now.strftime("%Y-%m-%d %H:%M:%S")
# Move to a cache file to maintain code organized.
#
            with open(cachefile, 'a') as csvfile:
                cachewriter = csv.writer(csvfile, delimiter = ';')
                cachewriter.writerow([topic, message, hora])
            logger.debug('Writing CSV line to cache file: %s',cachefile)

# save data not send in JSON format
#
#            d = {'Topic': topic, 'Message': message, 'Date': hora}
#            with open(cachefile + ".json", 'a') as jsonfile:
#                # jsontext = "{'Topic':"+topic+", 'Message':"+message+", Date:"+hora+"}"
#                # print(d)
#                json.dump(d,jsonfile, sort_keys = True, ensure_ascii=False)

        time.sleep(1)


