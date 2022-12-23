import configparser
from datetime import datetime, time, timedelta

class Configurator :
    def __init__ (self, logger) :
        self.config = configparser.ConfigParser()
        self.logger = logger
        
    def readConfig (self, configFile) :
        self.configFile = configFile
        self.config.read(configFile)
        #print ("read config : sections " + str (self.config.sections()))
    
    def getString (self, section, alias) :
        return self.config[section][alias]
    
    def getInt (self, section, alias) :
        return int(self.config[section][alias])
    
    def readBoolean (self, section, alias) :
        return (self.config[section][alias].lower() == "true")
