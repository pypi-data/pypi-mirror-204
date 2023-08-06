from .uniform import Uniform
import time
import math

class Normal:

    def __init__(self,mu=0,sigma=1):
        self.mu = mu
        self.sigma = sigma
    
    """Using Box Muller Method"""
    def generate(self, n = 1):
        normal = []
        for i in range(n):
            u = Uniform(time.perf_counter_ns()).generate(n=2)
            normal.append(self.mu + self.sigma * math.sqrt(-2*math.log(u[0]))*math.cos(2*math.pi*u[1]))
        return normal
