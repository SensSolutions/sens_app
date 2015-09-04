    and returns the read values
    '''
    try:
        """
        http://stackoverflow.com/a/5391245
        try:
            func = getattr(modulename, funcname)
        except AttributeError:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else:
            func(arg)


        http://stackoverflow.com/a/15004155
        The gettattr function has an optional third argument for a default
        value to return if the attribute does not exist, so you could use that:

        fun = getattr(modulename, funcname, None)

        if fun is None:
            print 'function not found "%s" (%s)' % (funcname, arg)
        else
            fun(arg)
        """

        s_module = "sensors." + SensorDict['type']
        logger.debug('Loading Sensor module %s with driver "%s"',
                     s_module, SensorDict['driver'])
        my_module = importlib.import_module(s_module, package=None)
        try:
            # print s_module
            # print my_module
            my_function = getattr(my_module, SensorDict['driver'])
            logger.debug("%s", my_module)
            # except AttributeError:
            # logger.warning("Function not found %s (%s)", SensorDict['driver'], SensorDict)
        except Exception, err:
            logger.warning("Error: %s", err)
        my_function(SensorDict)
