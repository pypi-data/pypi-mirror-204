import time
from Uniform import Uniform
class Triangular:

    def generate(self, count=1):
        t = []

        for i in range(count):
            u = Uniform(time.perf_counter_ns()).generate(count=2)
            t.append(u[0] + u[1])
        
        return t