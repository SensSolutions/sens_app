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
    act_module = None
    act_result = None
    try:

        module_name = str("actuators." + ActDict['subtype'])
        logger.debug('Loading "%s" with driver "%s"',
                     module_name, ActDict['driver'])
        act_module = importlib.import_module(module_name, package=None)
        # Loading Actuator module actuators.callhome with driver "call_home"
        #print act_module

        try:
            # print s_module
            # print my_module
            logger.debug("Loading Actuator Module: %s", act_module)
            act_function = getattr(act_module, ActDict['driver'])
            # except AttributeError:
            # logger.warning("Function not found %s (%s)", ActDict['driver'], ActDict)
        except Exception, err:
            logger.warning("Error Loading Actuator Module: %s", err)
        act_result = act_function(ActDict)

    except Exception, err:
        logger.warning("Error importing custom module: %s No driver for: %s",
                       str(err), act_module)
        logger.debug('Using Bogus Actuator function instead "%s"', act_module)
        act_result = bogus_act.bogus(ActDict)

    return act_result


