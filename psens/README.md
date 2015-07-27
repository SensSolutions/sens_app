# Platform Sens.Solutions

Temperature Sensor Monitoring

##Installation Steps
###Step 1:Clone the project to your application folder.

    git clone https://github.com/SensSolutions/sens_platform.git

###Step 2: Activate the virtual environment and install the requirements.
 
     cd sens_platform
     virtualenv env
     source env/bin/activate
     pip install -r requirements.txt 

##TODO

 * Automaticaly create output name from sensor version and pin used, or by user choice.
 * Verify that multiple sensors and applications instances works correctly.
 * Correct reading errors (sensor return incorrect values).
 * Do a sensor analyse function to calibrate sensor.
 * Daemonize code (and create startup scripts).

##Copyright

* Parts of code are from [Adafruit's Raspberry-Pi Python Code Library](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code) by Tony DiCola.
* Parts from [Cacti documentation](http://docs.cacti.net/manual:088:3a_advanced_topics.1_data_input_methods#making_your_scripts_work_with_cacti)
* https://www.eclipse.org/paho/clients/python/docs/

##TODO
* Add protection from sensor error readings (Â X % last value)
* Move settings to a external file
** http://pymotw.com/2/ConfigParser/index.html
* Capture signal handling (^C and friends)
* Write logs somewhere?
* Daemonize?
** http://code.activestate.com/recipes/278731/
** http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/