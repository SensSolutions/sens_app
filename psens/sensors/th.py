from random import randint
import time

def dht(d, *o):
    try:
        if o:
            for val in o:
                print "Others: "+ val

        print "\t\t[+]Process name: " + d['name']+ " | "+ __name__
        print "\t\t[+]Sensor subtype: "+d['subtype']

        t= randint(1,10)
        print "\t\t[+]"+ d['name'] +" is going to sleep for " + str(t) + "s"
        time.sleep(t)
        print "\t\t[+]" + d['name'] + " say by by"
    except Exception, e:
        print "\t\t[+]Error: " + str(e) + " on module: " + __name__

def ds18b20(d, *o):
    try:
        if o:
            for val in o:
                print "Others: "+ val

        print "\t\t[+]Process name: " + d['name']+ " | "+ __name__
        print "\t\t[+]Sensor subtype: "+d['subtype']

        t= randint(1,10)
        print "\t\t[+]Going to sleep for " + str(t) + "s"
        time.sleep(t)
        print "\t\t[+]" + d['name'] + " say by by"
    except Exception, e:
        print "\t\t[+]Error: " + str(e) + " on module: " + __name__

def joke(d):
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')
