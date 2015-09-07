"""
This module read data from sensors loading specific driver for every sensor

created on Mon Sep 07 10:12:58 2015

@author: mcollado
"""

import importlib
import logging
# import custom modules
from actuators import bogus_act

logger = logging.getLogger('PSENSv0.1')


def loadActuators(ActDict):
    '''
    This funtion loads correct driver for every actuator
    and returns the result values
    '''
    try:

        module_name = "actuators." + ActDict['type']
        logger.debug('Loading Sensor module %s with driver "%s"',
                     module_name, ActDict['driver'])
        act_module = importlib.import_module(module_name, package=None)
        try:
            # print s_module
            # print my_module
            act_function = getattr(act_module, ActDict['driver'])
            logger.debug("%s", act_module)
            # except AttributeError:
            # logger.warning("Function not found %s (%s)", ActDict['driver'], ActDict)
        except Exception, err:
            logger.warning("Error: %s", err)
        act_result = act_function(ActDict)

    except Exception, err:
        logger.warning("Error importing custom module: %s No driver for: %s",
                       str(err), act_module)
        logger.debug("Using Bogus function")
        act_result = bogus.bogus(ActDict)

    return act_result


