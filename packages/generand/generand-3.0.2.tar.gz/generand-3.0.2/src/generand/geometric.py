from .uniform import Uniform
import time
import math

class Geometric:

    def __init__(self,p=0.1):
        self.p = p
    
    def generate(self, n = 1):
        geometric = []
        u = Uniform(time.perf_counter_ns()).generate(n)
        for i in range(n):
            geometric.append(1+math.ceil(math.log(u[i])/math.log(1-self.p)))
        return geometric
