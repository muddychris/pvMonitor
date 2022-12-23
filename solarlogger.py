from utils.SolisLogger import SolisLogger

from utils.Logger import Logger
from utils.Configurator import Configurator

import platform
from time import sleep

program = "Solis Logger"
version = "v0.01"

def main():

    log_directory = "/home/chris/solis/log"
    G_logger = Logger ('solis', log_directory)
    logger = G_logger.getLogger()

    logger.warning ("Starting " + program + " " + version + " on Python " + platform.python_version())

    G_configurator = Configurator (logger)
    G_configurator.readConfig ("config/solis.ini")

    solisIpAddr = G_configurator.getString('INVERTER', "url")
    solisPort = G_configurator.getInt('INVERTER', "port")
    solisSerialNumber = G_configurator.getInt('INVERTER', "serialNumber")
    
    solis = SolisLogger (solisIpAddr, solisSerialNumber, solisPort, logger)
 
    headerStr = solis.getLoggingHeadings()
    logger.info (headerStr)
    
    while (True) :
        try :
            dataStr = solis.getLoggingData()           
            logger.info (dataStr)
        except Exception:
            solis.disconnect()
            logger.warning ("Exception reading inverter, trying again")
            dataStr = solis.getLoggingData()            
            logger.info (dataStr)
            
            pass
        
        # check for high current demand
        battCurrent = solis.readBattCurrent()
        if (battCurrent > 20) :
            dataStr = solis.getLoggingData()            
            logger.info (dataStr + " ***")
               
        solis.disconnect()
        
        
        sleep(5 * 60)
    

if __name__ == "__main__":
    main()
