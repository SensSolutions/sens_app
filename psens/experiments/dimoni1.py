#!/usr/bin/python
# -*- coding: utf-8 -*-

# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

# standard python libs
import logging
import time

# third party libs
from daemon import runner

print "Before class load"

class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/Users/mcollado/Coding/rasp-tempsensor/psens/experiments/run/testdaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            # Main code goes here ...
            # Note that logger level needs to be set to logging.DEBUG
            # before this shows up in the logs
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warn("Warning message")
            logger.error("Error message")
            time.sleep(10)

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("./log/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

print "Starting app"
app = App()

daemon_runner = runner.DaemonRunner(app)
print "Daemonizing app"
# This ensures that the logger file handle does not get closed
# during daemonization
daemon_runner.daemon_context.files_preserve = [handler.stream]
daemon_runner.do_action()
