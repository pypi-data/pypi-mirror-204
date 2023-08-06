from .uniform import Uniform
import time

class Bernoulli:

    def __init__(self,p=0.1):
        self.p = p

    def generate(self, n=1):
        u = Uniform().generate(n=n)
        bernouli= []
        for i in range(n):
            if u[i] <= self.p:
                bernouli.append(1)
            else: 
                bernouli.append(0)
        return bernouli