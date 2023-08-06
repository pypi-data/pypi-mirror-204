from .uniform import Uniform
import time
import math

class Weibull:

    def __init__(self,lamda=0.1,beta=1):
        self.lamda = lamda
        self.beta = beta

    def generate(self, n = 1):
        weibull = []
        u = Uniform(time.perf_counter_ns()).generate(n)
        for i in range(n):
            weibull.append((-math.log(u[i])**(1/self.beta))/self.lamda)
        return weibull