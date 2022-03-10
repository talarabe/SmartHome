from enum import Enum
#class HVAC_Mode(Enum):
#    COOL_ON = 1
#    COOL_OFF = 2
#    HEAT_PUMP = 3
#    HEAT_STRIPS = 4


from Power import PowerSupply   
from components import *

            
class House(object):
    def __init__(self, env, init_temp, logging):
        self.env = env
        self.temp = init_temp
        self.action = env.process(self.run())
        self.deltaT_HVAC = 0.0
        self.deltaT = 0.01
        self.power_supply = PowerSupply(env)
        self.hvac = HVAC(env, self.power_supply, self)
        self.thermostat = Thermostat(env,self,self.hvac,72.0)
        self.logging = logging

    def getTemp(self):
        return self.temp

    def setDeltaT_HVAC(self, deltaT):
        self.deltaT_HVAC = deltaT

    def run(self):
        i=1
        while True:
            yield self.env.timeout(1)
            self.temp = self.temp + self.deltaT + self.deltaT_HVAC
            print('Current temp %f' % self.temp)
            timeValue = self.deltaT * i
            tempValue = self.temp
            sql = "INSERT INTO TempData (Id, time, temp) VALUES (1, 0.1, 72.0)"
            vals = (i, timeValue, tempValue)
            self.logging.execute(sql)

            ++i


import simpy
import pyodbc

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'DESKTOP-MHACNH9\SQLEXPRESS'
database = 'SmartHome' 
username = 'test2' 
password = 'test2' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


env = simpy.Environment()
myHome = House(env, 72, cursor)
env.run(until=160)

cnxn.commit();

