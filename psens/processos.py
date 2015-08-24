from multiprocessing import Process
import time
import random

dsensors=[{"name":"air","type":"DTH"},
          {"name":"water","type":"DS22"},
          {"name":"internal","type":"PSens"}]

def sensor(d, *o):
    try:
        print "process name: " + d["name"]
        print "\t Sensor type: "+d["type"]
        if o:
            for val in o:
                print "Others: "+ val

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
