from multiprocessing import Process
import importlib
import time
import random

dsensors=[{"name":"air","type":"th","subtype":"DHT","app":"dht"},
        {"name":"water","type":"th","subtype":"ds18b20", "app":"ds18b20"},
        {"name":"internal","type":"bogus","subtype":"PSens","app":"PSens","sleep_time":60},
        {"name":"joke","type":"th","subtype":"Joke","app":"joke"}]

def sensor(d, *o):
    try:
        '''
        try:
            func = getattr(modulename, funcname)
        except AttributeError:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else:
            func(arg)       
        '''

        '''
        The gettattr function has an optional third argument for a default value to return if the attribute does not exist, so you could use that:

        fun = getattr(modulename, funcname, None)

        if fun is None:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else
            fun(arg)
        '''
        s_module = "sensors." + d['type'] 
        print "\t\t[+] Loading Sensor Driver: " + s_module + "." + d['app']
        my_module = importlib.import_module(s_module,package=None)
        try:
            my_function = getattr(my_module, d['app'])
        except AttributeError:
            print '\t\t[+] Function not found "%s" (%s)' % (d['app'], d)
        result = my_function(d)
        #my_module.joke()

    except Exception, e:
        print "Error importing custom module: " + str(e)
        print "No driver for: " + s_module
        print "Using Bogus function"
        bogus_sensor(d)

def bogus_sensor(d,*o):
    try:
        if o:
            for val in o:
                print "Others: "+ val

        print "process name: " + d["name"] + " Sensor subtype: "+d["subtype"] + " Driver: "+ d["app"]

        t = random.randint(1,10)
        print "\t" +  str(d["name"]) + " is going to sleep for " + str(t) + "s"
        time.sleep(t)
        print "\t" + d["name"] + " say by by"
    except Exception, e:
        print "Error: " + str(e)

print "- Starting"
for s in dsensors:
    try:
        print "Starting Module: " + s["name"]
        #print s
        p = Process(target=sensor, args=(s,))
        p.start()
        #print "Starting " + s["name"] + " PID: " + str(p.pid())
    except Exception, e:
        print "Error: " + str(e)
