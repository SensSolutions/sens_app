"""
This module sends data to broker and if it's not possible store-it in a
cache-file to send later.

created on Mon Sep 07 10:12:58 2015

@author: mcollado
"""

#import paho.mqtt.publish as publish
import paho.mqtt.publish as mqtt
import logging
import csv
import os
import json

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
    logger.debug("Client ID: %s opening connection to: %s", d['clientID'], d['brokerRemoteIP'])

    """ TODO: rewrite in more pythonish way:
        try mqtt.connect:
            send = mqtt.publish
        except:
            send = senToCache

        We have to take care of diferents argument. Use someting linke:
        We can use the **kwargs argument to accept an arbitrary number of named options:
            def render(context, **kwargs):
                ... template = kwargs['template'] if 'template' in kwargs else 'my_default_template'
                ... # do something with your template
                ... print template
                ...
            render() 'my_default_template'
            render(template='custom_template') 'custom_template'
        - See more at: http://www.abidibo.net/blog/2015/04/09/pythons-excess-arguments/#sthash.PbG99nyx.dpuf
        """
    """
    try:
        mqttc = mqtt.Client(d['clientID'])
        mqttc.connect(d['brokerRemoteIP'], 1883)
        conn_ok = True
    except KeyboardInterrupt:
        pass
    except Exception, err:
        conn_ok = False
        logger.warning('Error: %s, %s', str(err), d['brokerRemoteIP'])
    """

    conn_ok = True
        #
    #print "Cachefile: " + cachefile

    if os.path.isfile(cachefile + ".csv") and conn_ok:
        logger.warning("There's a cache file loading it")
        sendFromCache(d['brokerRemoteIP'], d['clientID'], cachefile)
    # mqttc.connect(d['brokerRemoteIP'], 1883)

    l = list()
    for result in d['results']:
        required_fields = ['org', 'place', 'type', 'name']
        result2 = {key:value for key, value in d.items() if key in required_fields}
        result.update(result2)
        d['message'] = json.dumps(result, sort_keys=True)
        d['newtopic'] = d['topic'] + "/" + result['dname']
        l.append((d['newtopic'],d['message'],0, False))
        
    if conn_ok:
        mqtt.multiple(l, hostname=d['brokerRemoteIP'])
        # rewrite this part using code from experiments/mypaho.py
        #mqttc.publish(d['topic'] + "/" + result['dname'], d['message'])
        #logger.debug('Topic: %s/%s : %s | Client ID: %s', d['topic'], result['dname'], d['message'], d['clientID'])
    else:
        sendToCache(cachefile, d['newtopic'], d['message'])


def sendData2(d):
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

    """ TODO: rewrite in more pythonish way:
        try mqtt.connect:
            send = mqtt.publish
        except:
            send = senToCache

        We have to take care of diferents argument. Use someting linke:
        We can use the **kwargs argument to accept an arbitrary number of named options:
            def render(context, **kwargs):
                ... template = kwargs['template'] if 'template' in kwargs else 'my_default_template'
                ... # do something with your template
                ... print template
                ...
            render() 'my_default_template'
            render(template='custom_template') 'custom_template'
        - See more at: http://www.abidibo.net/blog/2015/04/09/pythons-excess-arguments/#sthash.PbG99nyx.dpuf
        """
    try:
        mqttc = mqtt.Client(d['clientID'])
        mqttc.connect(d['brokerRemoteIP'], 1883)
        conn_ok = True
    except KeyboardInterrupt:
        pass
    except Exception, err:
        """Implement code to diferenciate connections error from others"""
        conn_ok = False
        logger.warning('Error: %s, %s', str(err), d['brokerRemoteIP'])

        #
    #print "Cachefile: " + cachefile

    if os.path.isfile(cachefile + ".csv") and conn_ok:
        logger.warning("There's a cache file loading it")
        sendFromCache(d['brokerRemoteIP'], d['clientID'], cachefile)
    # mqttc.connect(d['brokerRemoteIP'], 1883)

    mqttc.loop_start()
    for result in d['results']:
	print result
        """ This is ugly, fix-it"""
        required_fields = ['org', 'place', 'type', 'name']
        result2 = {key:value for key, value in d.items() if key in required_fields}
        result.update(result2)
        d['message'] = json.dumps(result, sort_keys=True)

        if conn_ok:
            # rewrite this part using code from experiments/mypaho.py
            mqttc.publish(d['topic'] + "/" + result['dname'], d['message'])
            logger.debug('Topic: %s/%s : %s | Client ID: %s', d['topic'], result['dname'], d['message'], d['clientID'])
        else:
            sendToCache(cachefile, d['topic']+ "/" + result['dname'], d['message'])


def sendFromCache(brokerRemoteIP, clientID, cachefile):
    """This function send cache file contens to broker"""

    logger.debug('Reading cache file %s', cachefile)

    with open(cachefile + ".csv", "r") as csvfile:
        f = csv.reader(csvfile, delimiter=';')
        count = 0
        try:
            msgs = list()
            for row in f:
                msgs.append((row[0], row[1], 0, False))
                count += 1

            mqtt.multiple(msgs, hostname=brokerRemoteIP, client_id= clientID, will=None, auth=None, tls=None)
            logger.warning("%i lines sent, removing cachefile: %s",
                           count, cachefile)
            os.remove(cachefile + ".csv")

        except Exception, err:
            logger.warning('Error trying to send cache: %s', str(err))

def sendToCache(cachefile, topic, message):
    """Convert dictionary in CSV data before write-it to cache file?"""
    try:
        """
        save data not send in JSON format
        #d = {'Topic': topic, 'Message': message }

        with open(cachefile + ".json", 'a') as jsonfile:
            #jsontext = '{"Topic":' + topic + ', "Message":"' + message + '"}'
            print(json.dumps(d))
            json.dump(d,jsonfile, sort_keys = True, ensure_ascii=False)
        """

        with open(cachefile + ".csv", 'a') as csvfile:
            cachewriter = csv.writer(csvfile, delimiter=';')
            cachewriter.writerow([topic, message])
        logger.warning('Writing CSV line to cache file: %s', cachefile)

    except KeyboardInterrupt:
        pass

    except Exception, err:
        logger.warning("Error %s opening cachefile: %s", err, cachefile)

