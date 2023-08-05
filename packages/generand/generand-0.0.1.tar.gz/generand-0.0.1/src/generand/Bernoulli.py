from Uniform import Uniform

class Bernoulli:

    def __init__(self, seed:int = 1):
        self.U = Uniform(seed)

    def generate(self, p = 0.5):
        u = self.U.generate(1)
        if u > p:
            return 1
        else: 
            return 0