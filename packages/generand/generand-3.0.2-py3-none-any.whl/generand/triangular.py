import time
from .uniform import Uniform
import math

class Triangular:

    def __init__(self,a=1,b=2,c=3):
        self.a = a
        self.b = b
        self.c = c

    def generate(self, n=1):
        t = []

        for _ in range(n):
            u = Uniform(time.perf_counter_ns()).generate()
            if u[0] < (self.b - self.a)/(self.c-self.a):
                t.append(self.a + math.sqrt((self.b-self.a)*(self.c-self.a)*u[0]))
            else:
                t.append(self.c - math.sqrt((self.c-self.a)*(self.c-self.b)*(1-u[0])))
            #t.append(u[0] + u[1])
        
        return t