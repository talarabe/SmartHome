from Modes import HVAC_Mode
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


