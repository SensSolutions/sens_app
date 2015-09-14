"""
This module sends data to broker and if it's not possible store-it in a
cache-file to send later.

created on Mon Sep 07 10:12:58 2015

@author: mcollado
"""

#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import logging
import csv
import os
import json
from pprint import pprint

logger = logging.getLogger('PSENSv0.1')

def sendData(d):
    """ This function send data recoverd by sensor to broker """

    """
    Check if remote broker is alive
    Check if exists a cache file
    Send cache data to broker then send last data
    If no broker, append data to cache file


    Must remove non required keys before send json:
    required_fields = ['name', 'last_name', 'phone_number', 'email']
    dict2 = {key:value for key, value in dict1.items() if key in required_fields}

        'results': [{'dname': 'temperature',
                  'dvalue': 25.5,
                  'time': '2015-09-09 16:22:28'},
                 {'dname': 'humidity',
                  'dvalue': 50.0,
                  'time': '2015-09-09 16:22:28'}],


    MySQL server and MQTTWARN are waiting this JSON:

    { "org" : "sens.solutions", "place" : "pool", "what" : "sensors", "sensor" : "air", "type" : "humidity", "value" : 48.7, "timestamp" : "2015-08-04 04:59:49" }

    """

    cachefile = os.path.join(d['path'], d['logpath'], (d['name'] + d['cache_suffix']))
    d['topic'] = d['org'] + "/" + d['location'] + "/" + d['type'] + "/" + d['name']
    logger.debug("Using cache file: %s", cachefile)
    logger.debug("Client ID: %s opening connection to: %s", d['clientID'], d['brokerRemoteIP'])
    try:
        
        mqttc = mqtt.Client(d['clientID'])
        mqttc.connect(d['brokerRemoteIP'], 1883)
        #
        if os.path.isfile(cachefile):
            sendFromCache(d['brokerRemoteIP'], d['clientID'], cachefile)
        # mqttc.connect(d['brokerRemoteIP'], 1883)

        for result in d['results']:

            """ This is ugly, fixit"""
            required_fields = ['org', 'place', 'type', 'name']
            result2 = {key:value for key, value in d.items() if key in required_fields}
            result.update(result2)
            d['message'] = json.dumps(result, sort_keys=True)

            mqttc.publish(d['topic'] + "/" + result['dname'], d['message'] )
            
        # mqttc.publish(d['topic'], d['message'])
        # implement clean disconnect from broker. Maybe
        logger.debug('Topic: %s : %s | Client ID: %s', d['topic'], d['message'], d['clientID'])
    except KeyboardInterrupt:
        pass
    except Exception, err:
        """Implement code to diferenciate connections error from others"""
        logger.warning('Error: %s, %s', str(err), d['brokerRemoteIP'])
        sendToCache(cachefile, d['topic'], d['message'])


def sendFromCache(brokerRemoteIP, clientID, cachefile):
    """This function send cache file contens to broker"""

    logger.debug('Reading cache file %s', cachefile)

    with open(cachefile, "r") as csvfile:
        f = csv.reader(csvfile, delimiter=';')
        count = 0
        try:
            mqttc = mqtt.Client(clientID)
            mqttc.connect(brokerRemoteIP, 1883)

            for row in f:
                mqttc.publish(row[0], row[1])
                # publish.single(row[0] , row[1], brokerRemoteIP, client_id= clientID, will=None, auth=None, tls=None)
                count += 1
                logger.debug('Send line: %i - topic: %s msg: %s',
                             f.line_num, row[0], str(row[1]))

            logger.warning("%i lines sent, removing cachefile: %s",
                           count, cachefile)
            os.remove(cachefile)

        except Exception, err:
            logger.warning('Error trying to send cache: %s', str(err))

def sendToCache(cachefile, topic, message):
    """Convert dictionary in CSV data before write-it to cache file?"""
    try:
        """
        save data not send in JSON format

        d = {'Topic': topic, 'Message': message, 'Date': hora}
        with open(cachefile + ".json", 'a') as jsonfile:
            jsontext = '{"Topic":' + topic + ', "Message":"' + message + '"}'
            print(d)
            json.dump(d,jsonfile, sort_keys = True, ensure_ascii=False)
        """
        with open(cachefile + ".csv", 'a') as csvfile:
            cachewriter = csv.writer(csvfile, delimiter=';')
            cachewriter.writerow([topic, message])
        logger.debug('Writing CSV line to cache file: %s', cachefile)

    except KeyboardInterrupt:
        pass

    except Exception, err:
        logger.warning("Error %s opening cachefile: %s", err, cachefile)

