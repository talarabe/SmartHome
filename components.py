from enum import Enum
class HVAC_Mode(Enum):
    COOL_ON = 1
    COOL_OFF = 2
    HEAT_PUMP = 3
    HEAT_STRIPS = 4

class Relay_Mode(Enum):
    ON = 1
    OFF = 0

class HVAC(object):
    def __init__(self, env, power_supply, home):
        self.env = env
        self.power_supply = power_supply
        self.home = home

    def command(self, mode):
        if mode == HVAC_Mode.COOL_ON:
            try:
                self.power_supply.kW.get(5500)
                print('HVAC Cooling')
                self.home.setDeltaT_HVAC(-0.02)
            except ValueError:
                print('Oops!')
                raise ValueError
        elif mode == HVAC_Mode.COOL_OFF:
            self.power_supply.kW.put(5500)
            print('HVAC Off')
            self.home.setDeltaT_HVAC(0.0)


class Thermostat(object):
    def __init__(self, env, home, HVAC, initTemp):
        self.env = env
        self.home = home
        self.HVAC = HVAC
        self.setTemp = initTemp
        self.deltaTemp = 0.5
        self.monitorTemp = env.process(self.monitorTemp())
        self.mode = HVAC_Mode.COOL_OFF


    def monitorTemp(self):
        sample_time = 1
        temp = self.home.getTemp()
        while True:
            yield self.env.timeout(1)
            if (self.home.getTemp() - self.setTemp) > self.deltaTemp and self.mode == HVAC_Mode.COOL_OFF:
                print('Turn on HVAC')
                self.mode = HVAC_Mode.COOL_ON
                self.HVAC.command(HVAC_Mode.COOL_ON)
#                yield self.env.timeout(HVAC_duration)
            elif (self.home.getTemp() - self.setTemp) < -self.deltaTemp and self.mode == HVAC_Mode.COOL_ON:
                print('Turn off HVAC')
                self.mode = HVAC_Mode.COOL_OFF
                self.HVAC.command(HVAC_Mode.COOL_OFF)
#            yield self.env.timeout(idle_duration)


