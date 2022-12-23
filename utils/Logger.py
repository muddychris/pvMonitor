import logging
import logging.handlers

class Logger () :
    def __init__ (self, logName, logDirectory) :
        self.logger = logging.getLogger(logName)
        self.logger.setLevel(logging.DEBUG)

        try:
            os.mkdir(logDirectory)
            self.logger.info("Created log directory")
        except:
            self.logger.info("Log directory already exists")
    
        # create file handler which logs even debug messages
        self.fh = logging.handlers.RotatingFileHandler(logDirectory + "/" + logName + ".log",maxBytes=1000000,backupCount=10)
        self.fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.WARNING)
        # create formatter and add it to the handlers
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)
        # add the handlers to the logger
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)
        
    def getLogger (self) :
        return self.logger

