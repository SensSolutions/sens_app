from multiprocessing import Process
from sensors import bogus
import importlib

dsensors=[{"name":"air", "type" : "th", "subtype" : "DHT", "driver":"dht"},
        {"name":"water", "type":"th", "subtype":"ds18b20", "driver":"ds18b20"},
        {"name":"internal", "type":"bogus", "subtype":"PSens", "driver":"bogus", "sleep_time":60},
        {"name":"joke", "type":"th", "subtype":"Joke", "driver":"joke"}]


def sensor(d, *o):
    try:
        '''
        http://stackoverflow.com/a/5391245
        try:
            func = getattr(modulename, funcname)
        except AttributeError:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else:
            func(arg)
        '''

        '''
        http://stackoverflow.com/a/15004155
        The gettattr function has an optional third argument for a default
        value to return if the attribute does not exist, so you could use that:

        fun = getattr(modulename, funcname, None)

        if fun is None:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else
            fun(arg)
        '''
        s_module = "sensors." + d['type']
        print "\t\t[+] Loading Sensor Driver: " + s_module + "." + d['driver']
        my_module = importlib.import_module(s_module, package=None)
        try:
            my_function = getattr(my_module, d['driver'])
        except AttributeError:
            print '\t\t[+] Function not found "%s" (%s)' % (d['driver'], d)
        result = my_function(d)

    except Exception, e:
        print "Error importing custom module: " + str(e)
        print "No driver for: " + s_module
        print "Using Bogus function"
        bogus.bogus(d)


print "- Starting"
for s in dsensors:
    try:
        print "Starting Module: " + s["name"]
        # print s
        p = Process(target=sensor, args=(s,))
        p.start()
        # print "Starting " + s["name"] + " PID: " + str(p.pid())
    except Exception, e:
        print "Error: " + str(e)
