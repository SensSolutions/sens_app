from multiprocessing import Process
import importlib
import time
import random
import sensors

dsensors=[{"name":"air","type":"th","subtype":"DTH","app":"sensors.th.th"},
          {"name":"water","type":"temp","subtype":"DS22"},
          {"name":"internal","type":"bogus","subtype":"PSens","sleep_time":60}]

def sensor(d, *o):
    try:
        ''' To avoid load in memory all sensors capture apps,
            we load only que specific one
            https://docs.python.org/2/library/importlib.html#importlib.import_module
            This code isn't working yet, maybe it can be left
            for a n+1 version
        '''
        my_module = importlib.import_module('sensors',package=None)
        #my_module.run()
        print "\t\t[+] Loading Sensors"
        sensors.th.th(d)

    except Exception, e:
        print "Error importing custom module: " + str(e)
        print "No sensor control application: " + d["type"]
        print "Using Bogus function"
        bogus_sensor(d)

def bogus_sensor(d,*o):
    try:
        if o:
            for val in o:
                print "Others: "+ val

        print "process name: " + d["name"] + " Sensor subtype: "+d["subtype"] + "Control App: "+ d["app"]

        t= random.randint(1,10)
        print "\tGoing to sleep for " + str(t) + "s"
        time.sleep(t)
        print "\t" + d["name"] + " say by by"
    except Exception, e:
        print "Error: " + str(e)

print "- Starting"
for s in dsensors:
    try:
        print "Starting Module: " + s["name"]
        print s
        p = Process(target=sensor, args=(s,))
        p.start()
        #print "Starting " + s["name"] + " PID: " + str(p.pid())
    except Exception, e:
        print "Error: " + str(e)
