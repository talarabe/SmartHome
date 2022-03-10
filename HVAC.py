from Modes import HVAC_Mode
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


