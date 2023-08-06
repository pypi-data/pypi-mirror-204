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
            
            x = 0
            p = 1
            i= 0
            u = Uniform(time.perf_counter_ns()).generate(n=5*self.alpha)
            while p >= math.exp(-self.alpha):
                
                x+=1
                p = u[i]*p
                i+=1
            poisson.append(x)
        return poisson