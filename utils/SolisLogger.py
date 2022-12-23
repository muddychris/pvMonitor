from pysolarmanv5 import PySolarmanV5

class SolisLogger :
    # define base of solis input registers
    solisInputRegBase = 30000
    
    #define interesting registers, https://www.aggsoft.com/serial-data-logger/tutorials/modbus-data-logging/ginlong-solis-pv.htm
    # using register numbers recorded in https://www.scss.tcd.ie/Brian.Coghlan/Elios4you/RS485_MODBUS-Hybrid-BACoghlan-201811228-1854.pdf
    regDateTime = solisInputRegBase + 3022
    regGenPwrTdy = solisInputRegBase + 3035
    regPhaseAcurrent = solisInputRegBase + 3076
    regInverterTemp = solisInputRegBase + 3093
    regInverterState = solisInputRegBase + 3095
    regBattVoltage = solisInputRegBase + 3133
    regBattCurrent = solisInputRegBase + 3134
    regBattCurrDirn = solisInputRegBase + 3135
    regBattPercent = solisInputRegBase + 3139
    regHousePwrTdy = solisInputRegBase + 3179
    
    def __init__ (self, solisIpAddr, solisSerialNumber, solisPort, logger) :
        self.solisIpAddr = solisIpAddr
        self.solisSerialNumber = solisSerialNumber
        self.solisPort = solisPort
        self.logger = logger
        
        self.modbus = None
        
        self.reconnect()
        
    def disconnect (self) :
        # need to actually disconnect to prevent resource leaks
        self.modbus.disconnect()
        self.modbus = None
    
    def reconnect (self) :
        # todo investigate testing for connectivity first
        if (self.modbus == None) :
            self.logger.warning (f"Connecting to solis inverter {self.solisSerialNumber} at {self.solisIpAddr}:{self.solisPort}")
            self.modbus = PySolarmanV5 (self.solisIpAddr, self.solisSerialNumber, port=self.solisPort, mb_slave_id=1, verbose=False, logger = self.logger)

    def readDate (self) :
        self.reconnect()
        dateData = self.modbus.read_input_registers(register_addr=self.regDateTime, quantity=6)
        dateStr = f"20{dateData[0]}{dateData[1]:02}{dateData[2]:02}{dateData[3]:02}{dateData[4]:02}{dateData[5]:02}"

        return dateStr
    
    def readBattPercent(self) :
        self.reconnect()
        return self.modbus.read_input_register_formatted(register_addr=self.regBattPercent, quantity=1)
    
    def readBattVoltage(self) :
        self.reconnect()
        return self.modbus.read_input_register_formatted(register_addr=self.regBattVoltage, quantity=1, scale=0.1)
    
    def readBattCurrent(self) :
        self.reconnect()
        current = self.modbus.read_input_register_formatted(register_addr=self.regBattCurrent, quantity=1, scale=0.1)
        dirn = self.modbus.read_input_register_formatted(register_addr=self.regBattCurrDirn, quantity=1)
        if (dirn == 0) : #charging
            current = -current
        return current

    def readImportCurrent(self) :
        self.reconnect()
        current = self.modbus.read_input_register_formatted(register_addr=self.regPhaseAcurrent, quantity=1, scale=0.1)
        return current

    def readGenPwrTdy(self) :
        self.reconnect()
        power = self.modbus.read_input_register_formatted(register_addr=self.regGenPwrTdy, quantity=1, scale=0.1)
        return power
    
    def readHsePwrTdy(self) :
        self.reconnect()
        power = self.modbus.read_input_register_formatted(register_addr=self.regHousePwrTdy, quantity=1, scale=0.1)
        return power

    def readInverterState(self) :
        self.reconnect()
        dirn = self.modbus.read_input_register_formatted(register_addr=self.regInverterState, quantity=1)
        return dirn
 
    def readInverterTemp(self) :
        self.reconnect()
        return self.modbus.read_input_register_formatted(register_addr=self.regInverterTemp, quantity=1, scale=0.1)
    
    def getLoggingHeadings(self) :
        return "datetime, percent, dcVolts, dcCurrent, acCurrent, genPwrTdy, hsePwrTdy, invTemp"
    
    def getLoggingData(self) :
        dateStr = self.readDate()
        battPercent = self.readBattPercent()
        battVoltage = self.readBattVoltage()
        battCurrent = self.readBattCurrent()
        importCurrent = self.readImportCurrent()
        genPwrToday = self.readGenPwrTdy()
        hsePwrToday = self.readHsePwrTdy()
        inverterTemp = self.readInverterTemp()
        dataStr = f"{dateStr}, {battPercent:02}, {battVoltage:#.2f}, {battCurrent:#.2f}, {importCurrent:#.2f}, {genPwrToday:#.2f}, {hsePwrToday:#.2f}, {inverterTemp:#.2f}"

        return dataStr