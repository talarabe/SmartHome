import simpy
class MyContainer(simpy.Container):
    def __init__(self,env,init,capacity):
        print('My Container')
#        simpy.Container(env, init, capacity)
        super().__init__(env, init, capacity)

    def get(self, amount):
        print('My Container Get')
        if (amount <= super().level):
            print('Get Amount')
            return super().get(amount)
        else:
            print('Requested Power Exceeds Supply - Shutdown Supply')
            raise ValueError

class PowerSupply:
    def __init__(self, env):
 #       self.kW = simpy.Container(env, init=6000, capacity=6000)
        self.kW = MyContainer(env, init=6000, capacity=6000)
        self.mon_proc = env.process(self.monitor_supply(env))
        print('Power Supply Created with MyContainer')

    def monitor_supply(self, env):
        while True:
            if self.kW.level <= 500:
                print('PowerSupply Danger Low at {env.now}')

            yield env.timeout(1)

