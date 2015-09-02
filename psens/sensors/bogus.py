import time
from random import randint


def bogus(d,*o):
    try:
        if o:
            for val in o:
                print "Others: " + val

        print "process name: " + d['name'] + " Sensor subtype: "+d['subtype'] + " Driver: "+ d['driver']

        t = randint(1, 10)
        print "\t" + str(d['name']) + " is going to sleep for " + str(t) + "s"
        time.sleep(t)
        print "\t" + d['name'] + " say by by"
    except Exception, e:
        print "Error: " + str(e)
