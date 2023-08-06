from .uniform import Uniform
import time
import math
class Poisson:

    """Generates pseudo poisson random numbers using A-R method"""

    def __init__(self,alpha=0.1):
        self.alpha = alpha

    def generate(self, n= 1):
        poisson = []
        for _ in range(n):
            p = math.exp(-self.alpha)
            F = p
            i= 0
            u = Uniform(time.perf_counter_ns()).generate()[0]
            while u>F:     
                p = self.alpha*p/(i+1)
                F=F+p
                i=i+1
            poisson.append(i)
        return poisson