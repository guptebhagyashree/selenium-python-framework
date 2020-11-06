import logging
import inspect

def customLogger(logLevel=logging.DEBUG):
    # Gets the name of the class/method from where this method is called
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)

    # By default, log all messages
    logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(filename="automation.log", mode='a')
    fileHandler.setLevel(logLevel)

    formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s",
                                  datefmt="%d/%m/%Y %I:%M:%S %p: %a")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger
