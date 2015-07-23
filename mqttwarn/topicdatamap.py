import time

try:
    import json
except ImportError:
    import simplejson as json

def Topic2Data(topic):
    if type(topic) == str:
        try:
	    #sens.solutions/pool/sensors/air/humidity
            parts = topic.split('/')
            org = parts[0]
            place = parts[1]
	    what = parts[2]
	    sensor = parts[3]
        except:
            org = 'unknown'
            place = 'unknown'
	    what = 'unknow'
            sensor = 'unknown'
        return dict(org=org, place=place, what=what, sensor=sensor)
    return None


# custom function to filter out any temperature notifications which 
# is less than 30C

def TempFilter(topic, message):
    data = dict(json.loads(message).items())

    if 'temperature' in data:
        if data['value'] is not None: 
            return float(data['value']) >= 27.0

    return True     # Suppress message because no high temp
